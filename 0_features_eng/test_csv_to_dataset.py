import json
from concurrent.futures import ThreadPoolExecutor

import pytest

from csv_to_dataset import (
    FEATURE_COLUMNS,
    OUTPUT_COLUMNS,
    DatasetValidationError,
    convert_csv_to_json,
)


HEADER = (
    "id,t,longitude,latitude,x,y,signed_turn,bearing,time_gap,distance_gap,"
    "euc_speed,distanceToShore,label"
)


def write_csv(tmp_path, rows):
    source = tmp_path / "input.csv"
    source.write_text("\n".join((HEADER, *rows)) + "\n", encoding="utf-8")
    return source


def valid_row(identifier="boat-1", label="02-fishing"):
    return f"{identifier},0,1,2,3,4,0.1,90,10,20,3.5,7.2,{label}"


def test_conversion_groups_rows_and_keeps_only_final_columns(tmp_path):
    source = write_csv(tmp_path, [valid_row(), valid_row(label="01-sailing"), valid_row("boat-2")])
    output = tmp_path / "dataset.json"

    result = convert_csv_to_json(source, output)

    assert result == output
    dataset = json.loads(output.read_text(encoding="utf-8"))
    assert list(dataset) == ["boat-1", "boat-2"]
    assert set(dataset["boat-1"]) == set(OUTPUT_COLUMNS)
    assert dataset["boat-1"]["label"] == [1, 0]
    assert dataset["boat-1"]["euc_speed"] == [3.5, 3.5]
    assert dataset["boat-1"]["x"] == [3.0, 3.0]
    assert dataset["boat-1"]["time_gap"] == [10.0, 10.0]
    assert all(
        column not in dataset["boat-1"]
        for column in ("t", "longitude", "latitude", "bearing", "distance_gap")
    )


def test_missing_required_column_fails_without_output(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text(HEADER.replace("x,", ""), encoding="utf-8")
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError, match="missing required column.*x"):
        convert_csv_to_json(source, output)

    assert not output.exists()


def test_non_numeric_feature_reports_csv_line_column_and_value(tmp_path):
    source = write_csv(tmp_path, [valid_row(), valid_row().replace("3.5", "oops")])
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError) as error:
        convert_csv_to_json(source, output)

    message = str(error.value)
    assert "line 3" in message
    assert "id='boat-1'" in message
    assert "column='euc_speed'" in message
    assert "value='oops'" in message
    assert not output.exists()


def test_non_numeric_feature_after_blank_line_reports_physical_line(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text(
        HEADER + "\n" + valid_row() + "\n\n" + valid_row().replace("3.5", "oops") + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError) as error:
        convert_csv_to_json(source, output)

    assert "line 4" in str(error.value)


def test_non_numeric_feature_after_multiline_record_reports_start_line(tmp_path):
    source = tmp_path / "input.csv"
    multiline_row = valid_row(identifier='"boat\ncontinued"')
    source.write_text(
        HEADER + "\n" + multiline_row + "\n" + valid_row().replace("3.5", "oops") + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError) as error:
        convert_csv_to_json(source, output)

    assert "line 4" in str(error.value)


def test_non_finite_value_reports_line_id_column_and_value(tmp_path):
    source = write_csv(tmp_path, [valid_row().replace("3.5", "inf")])
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError) as error:
        convert_csv_to_json(source, output)

    message = str(error.value)
    assert "line 2" in message
    assert "id='boat-1'" in message
    assert "column='euc_speed'" in message
    assert "value='inf'" in message
    assert not output.exists()


def test_nan_value_reports_as_non_finite(tmp_path):
    source = write_csv(tmp_path, [valid_row().replace("3.5", "NaN")])
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError, match=r"line 2.*not finite"):
        convert_csv_to_json(source, output)

    assert not output.exists()


@pytest.mark.parametrize(
    ("raw_label", "expected"),
    [
        ("01-sailing", 0),
        ("02-fishing", 1),
        ("03-sailing", 0),
        ("04-fishing", 1),
        ("05-sailing", 0),
    ],
)
def test_label_mapping(raw_label, expected, tmp_path):
    source = write_csv(tmp_path, [valid_row(label=raw_label)])
    output = tmp_path / "dataset.json"

    convert_csv_to_json(source, output)

    assert json.loads(output.read_text(encoding="utf-8"))["boat-1"]["label"] == [expected]


@pytest.mark.parametrize("raw_label", ["unknown", ""])
def test_unknown_label_reports_csv_line_and_original_value(tmp_path, raw_label):
    source = write_csv(tmp_path, [valid_row(label=raw_label)])
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError) as error:
        convert_csv_to_json(source, output)

    message = str(error.value)
    assert "line 2" in message
    assert "column='label'" in message
    assert f"value={raw_label!r}" in message
    assert not output.exists()


def test_empty_id_reports_csv_line(tmp_path):
    source = write_csv(tmp_path, [valid_row(identifier="")])
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError, match=r"line 2.*column='id'"):
        convert_csv_to_json(source, output)

    assert not output.exists()


def test_empty_dataset_fails_without_output(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text(HEADER + "\n", encoding="utf-8")
    output = tmp_path / "dataset.json"

    with pytest.raises(DatasetValidationError, match="no data rows"):
        convert_csv_to_json(source, output)

    assert not output.exists()


def test_concurrent_conversions_use_independent_temporary_files(tmp_path):
    source = write_csv(tmp_path, [valid_row(), valid_row("boat-2", "04-fishing")])
    output = tmp_path / "dataset.json"

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda _: convert_csv_to_json(source, output), range(8)))

    assert results == [output] * 8
    dataset = json.loads(output.read_text(encoding="utf-8"))
    assert set(dataset) == {"boat-1", "boat-2"}
    assert list(tmp_path.glob(f".{output.name}.*.tmp")) == []
