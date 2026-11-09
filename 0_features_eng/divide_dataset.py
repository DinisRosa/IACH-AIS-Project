import json
import os
import sys

import numpy as np

# Torna importável o `constants.py` de CODE/ quando o script corre diretamente.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (OUTPUT_JSON_FILE_PATH, RANDOM_SEED, TEST_JSON_FILE_PATH,
                       TRAIN_JSON_FILE_PATH, VALIDATION_JSON_FILE_PATH)

SPLIT_NAMES = ("train", "test", "validation")


def _validate_percentages(percentages):
    """Garante três inteiros positivos que somam exatamente 100."""
    for name, value in zip(SPLIT_NAMES, percentages):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
            raise TypeError(f"a percentagem de {name} tem de ser um inteiro, recebido {value!r}")
        if value < 1:
            raise ValueError(f"a percentagem de {name} tem de ser pelo menos 1, recebido {value}")
    if sum(percentages) != 100:
        raise ValueError(f"as percentagens têm de somar 100, recebido {sum(percentages)}")


def _split_counts(n_ids, percentages):
    """Distribui `n_ids` pelos splits pelo método do maior resto."""
    exact = [n_ids * percentage / 100 for percentage in percentages]
    counts = [int(np.floor(value)) for value in exact]
    remainder = n_ids - sum(counts)
    order = sorted(range(len(percentages)),
                   key=lambda index: (-(exact[index] - counts[index]), index))
    for index in order[:remainder]:
        counts[index] += 1
    if min(counts) < 1:
        raise ValueError(
            f"{n_ids} IDs não chegam para as percentagens {percentages}: "
            f"o split ficaria vazio (contagens {counts})"
        )
    return counts


def _write_split(dataset, ids, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    split = {trajectory_id: dataset[trajectory_id] for trajectory_id in sorted(ids)}
    with open(output_path, mode="w", encoding="utf-8") as json_file:
        json.dump(split, json_file, indent=4, ensure_ascii=False)
    return output_path


def divide_dataset(dataset_path, train_percentage, test_percentage,
                   validation_percentage, seed=RANDOM_SEED):
    """Divide o dataset por ID em train/test/validation e grava um JSON por split.

    A divisão é feita por trajetória (ID), nunca por número de pontos, pelo que
    cada ID aparece inteiro num único split. Devolve os três caminhos gerados,
    por ordem (train, test, validation).
    """
    percentages = (train_percentage, test_percentage, validation_percentage)
    _validate_percentages(percentages)

    with open(dataset_path, mode="r", encoding="utf-8") as json_file:
        dataset = json.load(json_file)
    if not isinstance(dataset, dict) or not dataset:
        raise ValueError(f"{dataset_path} não contém um dataset indexado por ID")

    ids = sorted(dataset)
    rng = np.random.default_rng(seed)
    shuffled = [ids[index] for index in rng.permutation(len(ids))]

    counts = _split_counts(len(ids), percentages)
    train_end = counts[0]
    test_end = train_end + counts[1]
    splits = (shuffled[:train_end], shuffled[train_end:test_end], shuffled[test_end:])

    output_paths = (TRAIN_JSON_FILE_PATH, TEST_JSON_FILE_PATH, VALIDATION_JSON_FILE_PATH)
    return tuple(_write_split(dataset, split_ids, path)
                 for split_ids, path in zip(splits, output_paths))


if __name__ == "__main__":
    divide_dataset(OUTPUT_JSON_FILE_PATH, 70, 20, 10)
