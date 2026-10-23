# cria uma função que recebe um csv e 3 valores, percentagem de treino, de validação e de teste, tem de dar 100% no final.
# Deves ter em consideração que uma linha do csv equivale a um instante, logo todos os instantes relativos a um id devem estar juntos; percebeste?
import csv, json

ALL_TRAJS = True
if not ALL_TRAJS:
    INPUT_CSV_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/partial/small_fishing_trajs.csv"
    INPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/partial/small_fishing_trajs.json"
    OUTPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/partial/small_fishing_trajs_ordered_by_id.json"
else:
    INPUT_CSV_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/full/128_fishing_trajs.csv"
    INPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/full/128_fishing_trajs.json"
    OUTPUT_JSON_FILE_PATH = "/home/dinisrosa22/Documentos/UNI/UC/MIACD/IA CENTRADA NO HUMANO/TRABALHO PROJETO/CODE/database/full/128_fishing_trajs_ordered_by_id.json"


def csv_to_json_file(csv_file_path, json_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        leitor = csv.DictReader(csv_file)
        dados = list(leitor)

    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)


def dados_por_id(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        dados = json.load(json_file)

    ordered_dataset = {}
    for dado in dados:
        if dado["id"] not in ordered_dataset.keys():
            ordered_dataset[dado["id"]] = {
                "total_rows": 1,
                "t": [dado["t"]],
                "longitude": [dado["longitude"]],
                "latitude": [dado["latitude"]],
                "x": [dado["x"]],
                "y": [dado["y"]],
                "signed_turn": [dado["signed_turn"]],
                "bearing": [dado["bearing"]],
                "time_gap": [dado["time_gap"]],
                "distance_gap": [dado["distance_gap"]],
                "euc_speed": [dado["euc_speed"]],
                "distanceToShore": [dado["distanceToShore"]],
                "label": [dado["label"]]
                }
        else:
            ordered_dataset[dado["id"]]["total_rows"] += 1
            ordered_dataset[dado["id"]]["t"].append(dado["t"])
            ordered_dataset[dado["id"]]["longitude"].append(dado["longitude"])
            ordered_dataset[dado["id"]]["latitude"].append(dado["latitude"])
            ordered_dataset[dado["id"]]["x"].append(dado["x"])
            ordered_dataset[dado["id"]]["y"].append(dado["y"])
            ordered_dataset[dado["id"]]["signed_turn"].append(dado["signed_turn"])
            ordered_dataset[dado["id"]]["bearing"].append(dado["bearing"])
            ordered_dataset[dado["id"]]["time_gap"].append(dado["time_gap"])
            ordered_dataset[dado["id"]]["distance_gap"].append(dado["distance_gap"])
            ordered_dataset[dado["id"]]["euc_speed"].append(dado["euc_speed"])
            ordered_dataset[dado["id"]]["distanceToShore"].append(dado["distanceToShore"])
            ordered_dataset[dado["id"]]["label"].append(dado["label"])

    with open(OUTPUT_JSON_FILE_PATH, mode='w', encoding='utf-8') as json_file:
        json.dump(ordered_dataset, json_file, indent=4, ensure_ascii=False)
    return ordered_dataset


def load_ordered_dataset(json_file_path):
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        ordered_dataset = json.load(json_file)
    return ordered_dataset









if __name__ == "__main__":
    csv_to_json_file(INPUT_CSV_FILE_PATH, INPUT_JSON_FILE_PATH)
    dados_por_id(INPUT_JSON_FILE_PATH)