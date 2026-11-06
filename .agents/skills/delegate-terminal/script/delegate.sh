#!/usr/bin/env bash
# delegate.sh — delega uma tarefa pesada para o terminal (abacusai, com opencode
# como fallback/refinação), para poupar a quota do modelo orquestrador.
#
# Só usa modelos remotos. Não usa Ollama nem qualquer modelo local.
#
# Uso:
#   delegate.sh [opções] "<tarefa>"
#
# Opções:
#   -f FICHEIRO   Ficheiro a incluir como contexto (repetível).
#   -P FICHEIRO   Ler a tarefa de um ficheiro (útil para prompts longos).
#   -m MODELO     Modelo da Abacus (por omissão: $ABACUS_MODEL ou ROUTE_LLM).
#   -r "INSTR."   Depois da Abacus, refinar o resultado com o opencode.
#   -M MODELO     Modelo do opencode, no formato provider/modelo
#                 (por omissão: $OPENCODE_MODEL). Obrigatório para -r e para o fallback.
#   -o FICHEIRO   Guardar o resultado neste ficheiro (stdout só mostra um resumo).
#   -t SEGUNDOS   Timeout por chamada (por omissão: 300).
#   -h            Esta ajuda.
#
# Códigos de saída: 0 = sucesso, 1 = erro de uso, 2 = todas as ferramentas falharam.

MODEL="${ABACUS_MODEL:-ROUTE_LLM}"
OC_MODEL="${OPENCODE_MODEL:-}"
TIMEOUT=300
MAX_ARG=60000   # acima disto, o prompt vai por stdin (limite de um único argumento no Linux ~128 KB)

files=()
task=""
task_file=""
refine=""
out=""

log() { printf '[delegate] %s\n' "$*" >&2; }

usage() {
  sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'
}

while getopts ":m:M:f:P:r:o:t:h" opt; do
  case "$opt" in
    m) MODEL="$OPTARG" ;;
    M) OC_MODEL="$OPTARG" ;;
    f) files+=("$OPTARG") ;;
    P) task_file="$OPTARG" ;;
    r) refine="$OPTARG" ;;
    o) out="$OPTARG" ;;
    t) TIMEOUT="$OPTARG" ;;
    h) usage; exit 0 ;;
    :) log "a opção -$OPTARG precisa de um valor"; exit 1 ;;
    *) log "opção desconhecida: -$OPTARG"; usage >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

# --- Tarefa ---------------------------------------------------------------
if [ -n "$task_file" ]; then
  [ -r "$task_file" ] || { log "não consigo ler o ficheiro da tarefa: $task_file"; exit 1; }
  task="$(cat "$task_file")"
else
  task="$*"
fi
[ -n "$task" ] || { log "falta a tarefa"; usage >&2; exit 1; }

# --- Prompt = tarefa + ficheiros de contexto --------------------------------
prompt="$task"
for f in "${files[@]}"; do
  [ -r "$f" ] || { log "não consigo ler o ficheiro de contexto: $f"; exit 1; }
  prompt+=$'\n\n'"=== FICHEIRO: $f ==="$'\n'"$(cat "$f")"
done

# --- Timeout (se existir) -----------------------------------------------------
TO=()
if command -v timeout >/dev/null 2>&1; then
  TO=(timeout "$TIMEOUT")
fi

# --- Chamadas às ferramentas ----------------------------------------------------
run_abacus() {
  local p="$1"
  command -v abacusai >/dev/null 2>&1 || { log "abacusai não encontrado no PATH"; return 127; }
  if [ "${#p}" -le "$MAX_ARG" ]; then
    "${TO[@]}" abacusai -p --model "$MODEL" "$p"
  else
    printf '%s' "$p" | "${TO[@]}" abacusai -p --model "$MODEL" \
      "Executa a tarefa descrita no conteúdo recebido por stdin."
  fi
}

run_opencode() {
  local p="$1"
  command -v opencode >/dev/null 2>&1 || { log "opencode não encontrado no PATH"; return 127; }
  [ -n "$OC_MODEL" ] || { log "modelo do opencode não definido (usa -M provider/modelo ou \$OPENCODE_MODEL)"; return 126; }
  if [ "${#p}" -le "$MAX_ARG" ]; then
    "${TO[@]}" opencode run --model "$OC_MODEL" "$p"
  else
    printf '%s' "$p" | "${TO[@]}" opencode run --model "$OC_MODEL" \
      "Executa a tarefa descrita no conteúdo recebido por stdin."
  fi
}

# --- Passo 1: abacusai (com fallback para opencode) ---------------------------------
used="abacusai"
result="$(run_abacus "$prompt")"
rc=$?

if [ "$rc" -ne 0 ] || [ -z "${result//[[:space:]]/}" ]; then
  log "abacusai falhou ou devolveu vazio (código $rc); a tentar o opencode"
  result="$(run_opencode "$prompt")"
  rc=$?
  used="opencode"
  if [ "$rc" -ne 0 ] || [ -z "${result//[[:space:]]/}" ]; then
    log "o opencode também falhou (código $rc). Responde tu diretamente ao utilizador."
    exit 2
  fi
fi

# --- Passo 2 (opcional): refinação com o opencode ----------------------------------
if [ -n "$refine" ] && [ "$used" = "abacusai" ]; then
  refined="$(run_opencode "$refine"$'\n\n'"--- CONTEÚDO A REFINAR ---"$'\n'"$result")"
  rrc=$?
  if [ "$rrc" -eq 0 ] && [ -n "${refined//[[:space:]]/}" ]; then
    result="$refined"
    used="abacusai+opencode"
  else
    log "a refinação falhou (código $rrc); a devolver o resultado da abacusai sem refinar"
  fi
fi

# --- Saída ------------------------------------------------------------------------------
if [ -n "$out" ]; then
  mkdir -p "$(dirname "$out")" 2>/dev/null
  printf '%s\n' "$result" > "$out" || { log "não consegui escrever em $out"; exit 2; }
  lines="$(printf '%s\n' "$result" | wc -l | tr -d ' ')"
  log "ok via $used; $lines linhas guardadas em $out"
  printf 'Resultado guardado em %s (%s linhas, via %s).\n' "$out" "$lines" "$used"
else
  log "ok via $used"
  printf '%s\n' "$result"
fi