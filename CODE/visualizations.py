from matplotlib import pyplot as plt
from partition_dataset import *


def plot_rows_by_id(dataset):
    ids = list(dataset.keys())
    rows = [dataset[id_]["total_rows"] for id_ in ids]

    plt.figure(figsize=(20, 6))
    plt.bar(ids, rows)
    plt.xlabel("ID")
    plt.ylabel("Número de rows")
    plt.title("Número de rows por ID")
    plt.xticks(rotation=90)
    plt.tight_layout()
    try:
        plt.savefig("figures/rows_by_id.png")
    except FileNotFoundError:
        import os
        os.makedirs("figures")
        plt.savefig("figures/rows_by_id.png")






if __name__ == "__main__":
    ALL_TRAJS = True
    dataset = load_ordered_dataset(OUTPUT_JSON_FILE_PATH)
    plot_rows_by_id(dataset)