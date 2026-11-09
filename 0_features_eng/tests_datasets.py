import csv, json
import os
import sys

# Torna importável o `constants.py` de CODE/ quando o script corre diretamente.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (INPUT_CSV_FILE_PATH, INPUT_JSON_FILE_PATH,
                       OUTPUT_JSON_FILE_PATH, REDUCED_OUTPUT_JSON_FILE_PATH)


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


def remove_redundant_features(input_json_file_path, output_json_file_path):
    with open(input_json_file_path, mode='r', encoding='utf-8') as json_file:
        dataset = json.load(json_file)

    # Lista completa de colunas redundantes ou desnecessárias a remover:
    # - longitude, latitude: substituídas por x, y
    # - t: substituída pelo time_gap
    # - bearing: redundante face ao signed_turn
    # - distance_gap: redundante face a euc_speed e time_gap (opcional, mas recomendado)
    columns_to_remove = {"longitude", "latitude", "t", "bearing", "distance_gap"}

    reduced_dataset = {}
    for trajectory_id, entry in dataset.items():
        reduced_dataset[trajectory_id] = {
            key: value for key, value in entry.items()
            if key not in columns_to_remove
        }

    with open(output_json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(reduced_dataset, json_file, indent=4, ensure_ascii=False)

    return reduced_dataset




if __name__ == "__main__":
    csv_to_json_file(INPUT_CSV_FILE_PATH, INPUT_JSON_FILE_PATH)
    dados_por_id(INPUT_JSON_FILE_PATH)
    remove_redundant_features(OUTPUT_JSON_FILE_PATH, REDUCED_OUTPUT_JSON_FILE_PATH)