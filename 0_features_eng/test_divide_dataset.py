import json

from csv_to_dataset import convert_csv_to_json
from divide_dataset import divide_dataset


HEADER = (
    "id,t,longitude,latitude,x,y,signed_turn,bearing,time_gap,distance_gap,"
    "euc_speed,distanceToShore,label"
)


def write_csv(path):
    rows = [HEADER]
    for trajectory_number in range(6):
        identifier = f"boat-{trajectory_number}"
        for point_number in range(2):
            rows.append(
                f"{identifier},{point_number},1,2,3,4,"
                f"{trajectory_number + 0.1},{90 + point_number},"
                f"{10 + point_number},{20 + point_number},"
                f"{3.5 + trajectory_number},{7.2 + point_number},"
                f"{'01-sailing' if point_number == 0 else '02-fishing'}"
            )
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def read_split(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_csv_conversion_and_split_keep_trajectories_intact(tmp_path, monkeypatch):
    source = tmp_path / "input.csv"
    dataset_path = tmp_path / "dataset.json"
    write_csv(source)

    convert_csv_to_json(source, dataset_path)

    output_paths = tuple(tmp_path / f"{name}.json"
                         for name in ("train", "test", "validation"))
    monkeypatch.setattr("divide_dataset.TRAIN_JSON_FILE_PATH", str(output_paths[0]))
    monkeypatch.setattr("divide_dataset.TEST_JSON_FILE_PATH", str(output_paths[1]))
    monkeypatch.setattr("divide_dataset.VALIDATION_JSON_FILE_PATH", str(output_paths[2]))

    generated_paths = divide_dataset(dataset_path, 50, 33, 17, seed=123)

    assert tuple(generated_paths) == tuple(str(path) for path in output_paths)
    splits = [read_split(path) for path in output_paths]
    split_ids = [set(split) for split in splits]
    assert all(split_ids[index].isdisjoint(split_ids[other])
               for index in range(len(split_ids))
               for other in range(index + 1, len(split_ids)))
    assert set().union(*split_ids) == {f"boat-{number}" for number in range(6)}

    for split in splits:
        for identifier, trajectory in split.items():
            trajectory_number = int(identifier.rsplit("-", 1)[1])
            assert trajectory == {
                "label": [0, 1],
                "x": [3.0, 3.0],
                "y": [4.0, 4.0],
                "signed_turn": [trajectory_number + 0.1] * 2,
                "euc_speed": [3.5 + trajectory_number] * 2,
                "time_gap": [10.0, 11.0],
                "distanceToShore": [7.2, 8.2],
            }


def test_csv_conversion_and_split_are_deterministic(tmp_path, monkeypatch):
    source = tmp_path / "input.csv"
    dataset_path = tmp_path / "dataset.json"
    write_csv(source)
    convert_csv_to_json(source, dataset_path)

    first_paths = tuple(tmp_path / f"first-{name}.json"
                        for name in ("train", "test", "validation"))
    second_paths = tuple(tmp_path / f"second-{name}.json"
                         for name in ("train", "test", "validation"))

    for paths in (first_paths, second_paths):
        monkeypatch.setattr("divide_dataset.TRAIN_JSON_FILE_PATH", str(paths[0]))
        monkeypatch.setattr("divide_dataset.TEST_JSON_FILE_PATH", str(paths[1]))
        monkeypatch.setattr("divide_dataset.VALIDATION_JSON_FILE_PATH", str(paths[2]))
        divide_dataset(dataset_path, 50, 33, 17, seed=123)

    assert [read_split(path) for path in first_paths] == [
        read_split(path) for path in second_paths
    ]
