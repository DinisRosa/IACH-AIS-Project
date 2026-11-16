"""Convert the source CSV into the trajectory-indexed JSON dataset."""

from __future__ import annotations

import json
import math
import os
import csv
import tempfile
from pathlib import Path
from typing import Final

import pandas as pd


FEATURE_COLUMNS: Final[tuple[str, ...]] = (
    "x",
    "y",
    "signed_turn",
    "time_gap",
    "euc_speed",
    "distanceToShore",
)
columns_to_remove: Final[frozenset[str]] = frozenset(
    {"longitude", "latitude", "t", "bearing", "distance_gap"}
)
OUTPUT_COLUMNS: Final[tuple[str, ...]] = ("label", *FEATURE_COLUMNS)
REQUIRED_COLUMNS: Final[tuple[str, ...]] = ("id", *OUTPUT_COLUMNS)
LABEL_MAPPING: Final[dict[str, int]] = {
    "01-sailing": 0,
    "02-fishing": 1,
    "03-sailing": 0,
    "04-fishing": 1,
    "05-sailing": 0,
}


class DatasetValidationError(ValueError):
    """Raised when the source CSV cannot produce a valid dataset."""


def _error(
    csv_path: Path,
    line: int,
    identifier: object,
    column: str,
    value: object,
    reason: str,
) -> DatasetValidationError:
    return DatasetValidationError(
        f"{csv_path}: line {line}, id={identifier!r}, column={column!r}, "
        f"value={value!r}: {reason}"
    )


def _validate_columns(frame: pd.DataFrame, csv_path: Path) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise DatasetValidationError(
            f"{csv_path}: missing required column(s): {', '.join(missing)}"
        )


def _physical_record_lines(csv_path: Path) -> list[int]:
    """Return starting lines for pandas' non-blank data records."""
    starts: list[int] = []
    with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # header is always physical line 1
        previous_end = reader.line_num
        for row in reader:
            start = previous_end + 1
            previous_end = reader.line_num
            if row and any(cell.strip() for cell in row):
                starts.append(start)
    return starts


def convert_csv_to_json(
    csv_path: str | os.PathLike[str],
    output_path: str | os.PathLike[str],
) -> Path:
    """Validate *csv_path* and atomically write its trajectory-indexed JSON."""
    source = Path(csv_path)
    destination = Path(output_path)
    frame = pd.read_csv(
        source,
        dtype=str,
        keep_default_na=False,
        na_filter=False,
    )
    _validate_columns(frame, source)
    if frame.empty:
        raise DatasetValidationError(f"{source}: CSV contains no data rows")
    record_lines = _physical_record_lines(source)
    if len(record_lines) != len(frame):
        raise DatasetValidationError(
            f"{source}: could not map pandas rows to physical CSV records"
        )

    identifiers = frame["id"].astype(str)
    for index, identifier in identifiers.items():
        line = record_lines[index]
        if not identifier.strip():
            raise _error(source, line, identifier, "id", identifier, "ID is empty")

    converted: dict[str, pd.Series] = {}
    for column in FEATURE_COLUMNS:
        numeric = pd.to_numeric(frame[column], errors="coerce")
        converted[column] = numeric
        for index, value in numeric.items():
            raw_value = frame.at[index, column]
            line = record_lines[index]
            identifier = frame.at[index, "id"]
            if pd.isna(value):
                reason = (
                    "value is not finite"
                    if str(raw_value).strip().lower() in {"nan", "+nan", "-nan"}
                    else "value is not numeric"
                )
                raise _error(
                    source, line, identifier, column, raw_value, reason,
                )
            if not bool(pd.notna(value)) or not math.isfinite(float(value)):
                raise _error(
                    source, line, identifier, column, raw_value,
                    "value is not finite",
                )

    labels: dict[int, int] = {}
    for index, raw_label in frame["label"].items():
        label = raw_label.strip()
        if label not in LABEL_MAPPING:
            raise _error(
                source,
                record_lines[index],
                frame.at[index, "id"],
                "label",
                raw_label,
                "unknown label; expected one of "
                + ", ".join(LABEL_MAPPING),
            )
        labels[index] = LABEL_MAPPING[label]

    dataset: dict[str, dict[str, list[float | int]]] = {}
    for index, identifier in identifiers.items():
        trajectory = dataset.setdefault(identifier, {column: [] for column in OUTPUT_COLUMNS})
        trajectory["label"].append(labels[index])
        for column in FEATURE_COLUMNS:
            trajectory[column].append(float(converted[column].at[index]))

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary = Path(temporary_handle.name)
    try:
        with temporary_handle:
            json.dump(dataset, temporary_handle, indent=4, ensure_ascii=False, allow_nan=False)
            temporary_handle.write("\n")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    return destination
