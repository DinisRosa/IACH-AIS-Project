# Constantes partilhadas por todo o projecto (caminhos, flags e parâmetros de plot).

# ---------------------------------------------------------------- pipeline
ALL_TRAJS = True

if not ALL_TRAJS:
    INPUT_CSV_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/partial/small_fishing_trajs.csv"
    INPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/partial/small_fishing_trajs.json"
    OUTPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/partial/small_fishing_trajs_ordered_by_id.json"
else:
    INPUT_CSV_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/full/128_fishing_trajs.csv"
    INPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/full/128_fishing_trajs.json"
    OUTPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/full/128_fishing_trajs_ordered_by_id.json"

# ---------------------------------------------------------------- figuras
FIGURES_DIR = "figures"

# ---------------------------------------------------------------- dados
FEATURES = ["euc_speed", "signed_turn", "bearing", "time_gap", "distance_gap", "distanceToShore"]
LOG_FEATURES = ("time_gap", "distance_gap")

# ---------------------------------------------------------------- classes
FISHING_LABELS = ("02", "04")
BINARY_CLASSES = ["Navegação", "Pesca"]

# ---------------------------------------------------------------- cores
NAV_COLOR = "#4C72B0"
FISH_COLOR = "#DD8452"
OUTLIER_COLOR = "#C44E52"
CLASS_COLORS = {"Navegação": NAV_COLOR, "Pesca": FISH_COLOR}
ORIG_CLASS_COLORS = {"01-sailing": NAV_COLOR, "02-fishing": FISH_COLOR,
                     "03-sailing": NAV_COLOR, "04-fishing": FISH_COLOR,
                     "05-sailing": NAV_COLOR}

# ---------------------------------------------------------------- amostragem
SAMPLE_SIZE = 20000          # pontos usados no scatter euc_speed vs signed_turn
RANDOM_SEED = 0

# ---------------------------------------------------------------- gaps temporais
TIME_GAP_THRESHOLD = 60      # segundos: gap acima do qual o intervalo é anómalo

# ---------------------------------------------------------------- janelas sobrepostas
WINDOW_LENGTH = 50           # comprimento da janela (número de pontos)
WINDOW_OVERLAP = 0.5         # 50% de sobreposição entre janelas consecutivas
WINDOW_PLOT_POINTS = 200     # pontos da trajetória mostrados na figura
WINDOW_PLOT_COUNT = 4        # nº de janelas consecutivas desenhadas
WINDOW_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
