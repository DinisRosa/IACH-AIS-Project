import os
from collections import Counter

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from constants import (BINARY_CLASSES, CLASS_COLORS, FISHING_LABELS, FIGURES_DIR,
                       FEATURES, LOG_FEATURES, NAV_COLOR, ORIG_CLASS_COLORS,
                       OUTPUT_JSON_FILE_PATH, FISH_COLOR, OUTLIER_COLOR,
                       RANDOM_SEED, SAMPLE_SIZE, TIME_GAP_THRESHOLD,
                       WINDOW_COLORS, WINDOW_LENGTH, WINDOW_OVERLAP,
                       WINDOW_PLOT_COUNT, WINDOW_PLOT_POINTS)
from partition_dataset import load_ordered_dataset

METERS_PER_SECOND_PER_KNOT = 0.514444444


def _save_fig(filename, category):
    output_dir = os.path.join(FIGURES_DIR, category)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def _is_fishing(label):
    return label[:2] in FISHING_LABELS


def _binary_mask(labels):
    return np.fromiter((_is_fishing(label) for label in labels), dtype=bool, count=len(labels))


def _count_segments(labels):
    return 1 + sum(a != b for a, b in zip(labels, labels[1:]))


def _use_log_scale(values):
    if values.size == 0 or values.min() <= 0:
        return False
    median = np.median(values)
    if median <= 0:
        return False
    return np.percentile(values, 99) / median >= 3 or values.max() / median >= 10


def _normalize_for_plot(values):
    values = np.asarray(values, dtype=float)
    minimum = values.min()
    span = values.max() - minimum
    return np.zeros_like(values) if span == 0 else (values - minimum) / span


def _collect_features(dataset, features):
    """Concatena as `features` de todas as trajetórias e devolve-as com a máscara de classe."""
    values = {feature: [] for feature in features}
    masks = []
    for entry in dataset.values():
        masks.append(_binary_mask(entry["label"]))
        for feature in features:
            values[feature].append(np.asarray(entry[feature], dtype=float))
    arrays = {feature: np.concatenate(parts) for feature, parts in values.items()}
    return arrays, np.concatenate(masks)


def _format_count(value):
    return f"{int(value):,}".replace(",", " ")


def _horizontal_bars(labels, values, colors, total, filename, title, figsize,
                     xlabel="Número de pontos"):
    fig, ax = plt.subplots(figsize=figsize)
    positions = np.arange(len(labels))

    ax.barh(positions, values, color=colors, height=0.6)
    ax.set_yticks(positions, labels, fontsize=9)
    ax.invert_yaxis()

    top = max(values)
    ax.set_xlim(0, top * 1.55)
    for position, value in zip(positions, values):
        ax.text(value + top * 0.02, position,
                f"{_format_count(value)} ({100 * value / total:.1f}%)",
                va="center", fontsize=9)

    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: _format_count(value)))
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.tight_layout()
    _save_fig(filename, "estatisticas")


def plot_rows_by_id_histogram(dataset):
    ids = list(dataset.keys())
    rows = [dataset[id_]["total_rows"] for id_ in ids]

    plt.figure(figsize=(20, 6))
    plt.bar(ids, rows)
    plt.xlabel("ID")
    plt.ylabel("Número de rows")
    plt.title("Número de rows por ID")
    plt.xticks(rotation=90)
    plt.tight_layout()
    _save_fig("rows_by_id.png", "estatisticas")


def plot_class_distribution(dataset):
    counts = Counter()
    for entry in dataset.values():
        counts.update(entry["label"])

    total = sum(counts.values())
    classes = sorted(counts)

    _horizontal_bars(classes,
                     [counts[c] for c in classes],
                     [ORIG_CLASS_COLORS[c] for c in classes],
                     total,
                     "class_distribution_classes.png",
                     "Distribuição das 5 classes originais",
                     (5.5, 3.0))

    fishing = sum(n for c, n in counts.items() if _is_fishing(c))
    sailing = total - fishing

    _horizontal_bars(["Navegação\n(01, 03, 05)", "Pesca\n(02, 04)"],
                     [sailing, fishing],
                     [NAV_COLOR, FISH_COLOR],
                     total,
                     "class_distribution_binary.png",
                     "Agregação binária: pesca vs navegação",
                     (5.5, 2.0))


def plot_segments_per_traj(dataset):
    segments = np.array([_count_segments(entry["label"]) for entry in dataset.values()], dtype=int)

    fig, ax = plt.subplots(figsize=(6.7, 3.5))
    low, high = segments.min(), segments.max()
    counts, _, patches = ax.hist(segments, bins=np.arange(low, high + 2) - 0.5,
                                 color=NAV_COLOR, edgecolor="white")

    for patch, count in zip(patches, counts):
        if count:
            ax.annotate(f"{int(count)}", (patch.get_x() + patch.get_width() / 2, count),
                        ha="center", va="bottom", fontsize=8)

    mean, median = segments.mean(), float(np.median(segments))
    ax.axvline(mean, color="crimson", linestyle="--", label=f"Média = {mean:.1f}")
    ax.axvline(median, color="darkorange", linestyle=":", label=f"Mediana = {median:.1f}")

    step = max(1, (high - low + 1) // 15)
    ax.set_xticks(np.arange(low, high + 1, step))
    ax.set_xlabel("Número de segmentos ground-truth por trajetória", fontsize=9)
    ax.set_ylabel("Número de trajetórias", fontsize=9)
    ax.set_title("Fragmentação real das trajetórias (transições de label)", fontsize=9)
    ax.set_ylim(0, counts.max() * 1.15)
    ax.legend(fontsize=8)

    fig.tight_layout()
    _save_fig("segments_per_traj.png", "estatisticas")


def plot_segments_per_id(dataset):
    ids = sorted(dataset)
    segments = np.array([_count_segments(dataset[id_]["label"]) for id_ in ids], dtype=int)
    mean = segments.mean()

    fig, ax = plt.subplots(figsize=(16, 5))
    ax.bar(ids, segments, color=NAV_COLOR)

    ax.set_xlabel("ID", fontsize=9)
    ax.set_ylabel("Número de segmentos", fontsize=9)
    ax.set_title("Número de segmentos ground-truth por trajetória", fontsize=11)
    ax.set_ylim(0, segments.max() + 1)
    ax.set_yticks(np.arange(segments.max() + 1))
    ax.axhline(mean, color="crimson", linestyle="--",
               label=f"Média = {mean:.1f} segmentos")
    ax.tick_params(axis="x", labelsize=6, rotation=90)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8)

    fig.tight_layout()
    _save_fig("segments_per_id.png", "estatisticas")


def plot_features_by_class(dataset):
    values = {f: {c: [] for c in BINARY_CLASSES} for f in FEATURES}
    for entry in dataset.values():
        mask = _binary_mask(entry["label"])
        for feature in FEATURES:
            array = np.asarray(entry[feature], dtype=float)
            values[feature]["Pesca"].append(array[mask])
            values[feature]["Navegação"].append(array[~mask])

    groups = (("euc_speed", "signed_turn", "bearing"),
              ("time_gap", "distance_gap", "distanceToShore"))

    for number, group in enumerate(groups, start=1):
        fig, axes = plt.subplots(1, len(group), figsize=(7, 2.6))
        for ax, feature in zip(axes, group):
            sailing = np.concatenate(values[feature]["Navegação"])
            fishing = np.concatenate(values[feature]["Pesca"])
            data = pd.DataFrame({"valor": np.concatenate([sailing, fishing]),
                                 "classe": np.array(["Navegação"] * sailing.size
                                                    + ["Pesca"] * fishing.size)})

            sns.boxplot(data=data, x="valor", y="classe", order=BINARY_CLASSES,
                        hue="classe", hue_order=BINARY_CLASSES, palette=CLASS_COLORS,
                        legend=False, showfliers=False, width=0.6, ax=ax)

            if feature in LOG_FEATURES and _use_log_scale(data["valor"].to_numpy()):
                ax.set_xscale("log")
            ax.set_xlabel(feature, fontsize=9)
            ax.set_ylabel("")
            ax.tick_params(labelsize=7)
            ax.xaxis.grid(True, linestyle=":", alpha=0.5)
            ax.set_axisbelow(True)
            for spine in ("top", "right"):
                ax.spines[spine].set_visible(False)

        fig.suptitle("Distribuição das features por classe binária (outliers omitidos)",
                     fontsize=10)
        fig.tight_layout(rect=(0, 0, 1, 0.9))
        _save_fig(f"features_by_class_{number}.png", "estatisticas")


def plot_speed_vs_turn(dataset):
    arrays, is_fishing = _collect_features(dataset, ["euc_speed", "signed_turn"])
    speed, turn = arrays["euc_speed"], arrays["signed_turn"]

    rng = np.random.default_rng(RANDOM_SEED)
    half = SAMPLE_SIZE // 2
    chosen = np.concatenate([
        rng.choice(np.flatnonzero(is_fishing == flag),
                   size=min(half, int(np.count_nonzero(is_fishing == flag))),
                   replace=False)
        for flag in (False, True)
    ])

    fig, ax = plt.subplots(figsize=(6.7, 4.5))
    for classe in BINARY_CLASSES:
        flag = classe == "Pesca"
        selected = chosen[is_fishing[chosen] == flag]
        ax.scatter(speed[selected], turn[selected], s=6, alpha=0.3, linewidths=0,
                   color=CLASS_COLORS[classe], label=f"{classe} ({selected.size} pontos)")

    ax.set_xlabel("euc_speed", fontsize=9)
    ax.set_ylabel("signed_turn", fontsize=9)
    ax.set_title("Velocidade vs mudança de rumo (amostra estratificada)", fontsize=10)
    ax.grid(linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, markerscale=2)

    fig.tight_layout()
    _save_fig("speed_vs_turn.png", "velocidade")


def plot_speed_vs_turn_id(dataset, id=None):
    """Scatter euc_speed vs signed_turn de uma única trajetória (colorida pela classe de cada ponto)."""
    id = sorted(dataset)[0] if id is None else id
    entry = dataset[id]

    speed = np.asarray(entry["euc_speed"], dtype=float)
    turn = np.asarray(entry["signed_turn"], dtype=float)
    is_fishing = _binary_mask(entry["label"])

    fig, ax = plt.subplots(figsize=(6.7, 4.5))
    for classe in BINARY_CLASSES:
        selected = is_fishing == (classe == "Pesca")
        ax.scatter(speed[selected], turn[selected], s=10, alpha=0.6, linewidths=0,
                   color=CLASS_COLORS[classe], label=f"{classe} ({np.count_nonzero(selected)} pontos)")

    ax.set_xlabel("euc_speed", fontsize=9)
    ax.set_ylabel("signed_turn", fontsize=9)
    ax.set_title(f"Velocidade vs mudança de rumo — trajetória {id}", fontsize=10)
    ax.grid(linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, markerscale=2)

    fig.tight_layout()
    _save_fig("speed_vs_turn_id.png", "velocidade")


def plot_outliers(dataset):
    arrays, _ = _collect_features(dataset, FEATURES)

    labels, counts = [], []
    for feature in FEATURES:
        values = arrays[feature]
        q1, q3 = np.percentile(values, [25, 75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        labels.append(feature)
        counts.append(int(np.count_nonzero((values < lower) | (values > upper))))

    total = arrays[FEATURES[0]].size
    _horizontal_bars(labels, counts, [OUTLIER_COLOR] * len(labels), total,
                     "outliers.png",
                     "Outliers pela regra do IQR (1,5 × IQR)",
                     (6.7, 3.4),
                     xlabel=f"Outliers ({_format_count(total)} pontos por feature)")


def plot_time_gaps(dataset):
    arrays, _ = _collect_features(dataset, ["time_gap"])
    gaps = arrays["time_gap"]
    above = int(np.count_nonzero(gaps > TIME_GAP_THRESHOLD))

    fig, ax = plt.subplots(figsize=(6.7, 3.5))
    bins = np.logspace(np.log10(max(gaps.min(), 1)), np.log10(gaps.max()), 40)
    ax.hist(gaps, bins=bins, color=NAV_COLOR, edgecolor="white")
    ax.axvline(TIME_GAP_THRESHOLD, color="crimson", linestyle="--",
               label=f"Threshold = {TIME_GAP_THRESHOLD} s ({_format_count(above)} pontos acima)")
    ax.set_xscale("log")
    ax.set_xlabel("time_gap (segundos, escala log)", fontsize=9)
    ax.set_ylabel("Número de pontos", fontsize=9)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: _format_count(value)))
    ax.tick_params(labelsize=8)
    ax.set_title("Distribuição dos intervalos temporais entre pontos", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    fig.tight_layout()
    _save_fig("time_gaps_histogram.png", "estatisticas")

    ids = sorted(dataset)
    maxima = np.array([max(dataset[id_]["time_gap"]) for id_ in ids], dtype=float)
    colors = [OUTLIER_COLOR if value > TIME_GAP_THRESHOLD else NAV_COLOR for value in maxima]
    flagged = int(np.count_nonzero(maxima > TIME_GAP_THRESHOLD))

    fig, ax = plt.subplots(figsize=(16, 4.5))
    ax.bar(ids, maxima, color=colors)
    ax.axhline(TIME_GAP_THRESHOLD, color="crimson", linestyle="--",
               label=f"Threshold = {TIME_GAP_THRESHOLD} s ({flagged} trajetórias acima)")
    ax.set_xlabel("ID", fontsize=9)
    ax.set_ylabel("time_gap máximo (s)", fontsize=9)
    ax.set_title("Intervalo temporal máximo em cada trajetória", fontsize=11)
    ax.tick_params(axis="x", labelsize=6, rotation=90)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8)

    fig.tight_layout()
    _save_fig("time_gaps_per_id.png", "estatisticas")


def plot_normalization_before_after(dataset):
    features = ["euc_speed", "signed_turn", "distanceToShore"]
    arrays, _ = _collect_features(dataset, features)

    fig, axes = plt.subplots(len(features), 2, figsize=(7, 6), sharey="row")
    for row, feature in enumerate(features):
        values = arrays[feature]
        normalized = (values - values.mean()) / values.std()

        axes[row][0].hist(values, bins=50, color=NAV_COLOR, edgecolor="white", linewidth=0.3)
        axes[row][1].hist(normalized, bins=50, color=FISH_COLOR, edgecolor="white", linewidth=0.3)

        axes[row][0].set_ylabel(feature, fontsize=9)
        axes[row][1].set_ylabel("")
        axes[row][0].set_xlabel("valor original", fontsize=8)
        axes[row][1].set_xlabel("valor normalizado", fontsize=8)
        axes[row][0].yaxis.set_major_formatter(FuncFormatter(lambda value, _: _format_count(value)))
        for ax in axes[row]:
            ax.tick_params(labelsize=7)
            ax.grid(axis="y", linestyle=":", alpha=0.5)
            ax.set_axisbelow(True)

    axes[0][0].set_title("Antes (bruto)", fontsize=10)
    axes[0][1].set_title("Depois (normalização z-score)", fontsize=10)
    fig.suptitle("Normalização z-score de 3 features representativas", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _save_fig("normalization_before_after.png", "normalizacao")


def plot_overlapping_windows(dataset, trajectory_id=None, window_length=WINDOW_LENGTH,
                             overlap_points=int(WINDOW_LENGTH * WINDOW_OVERLAP)):
    if window_length <= 0:
        raise ValueError("window_length tem de ser positivo")
    if overlap_points < 0 or overlap_points >= window_length:
        raise ValueError("overlap_points tem de estar entre 0 e window_length - 1")

    trajectory_id = sorted(dataset)[0] if trajectory_id is None else trajectory_id
    speed = np.asarray(dataset[trajectory_id]["euc_speed"][:WINDOW_PLOT_POINTS], dtype=float)
    index = np.arange(speed.size)

    step = window_length - overlap_points
    available = 1 + max(0, (speed.size - window_length)) // step
    count = min(WINDOW_PLOT_COUNT, available)

    fig, ax = plt.subplots(figsize=(7, 3.5))
    for number in range(count):
        start = number * step
        stop = min(start + window_length, speed.size)
        ax.axvspan(start, stop, color=WINDOW_COLORS[number % len(WINDOW_COLORS)],
                   alpha=0.3, label=f"Janela {number + 1} [{start}, {stop})")

    ax.plot(index, speed, color="black", linewidth=0.9, label="euc_speed")
    ax.set_xlabel("Índice do ponto", fontsize=9)
    ax.set_ylabel("euc_speed", fontsize=9)
    ax.set_title(f"Janelas sobrepostas sobre uma trajetória real "
                 f"(W = {window_length} pontos, {overlap_points} pontos de sobreposição)",
                 fontsize=9)
    ax.set_xlim(0, speed.size - 1)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
    ax.grid(linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    fig.tight_layout()
    _save_fig("overlapping_windows.png", "sobreposicao")


def plot_multiple_trajectories(dataset, number_of_trajectories):
    if (isinstance(number_of_trajectories, (bool, np.bool_))
            or not isinstance(number_of_trajectories, (int, np.integer))
            or number_of_trajectories <= 0):
        raise ValueError("number_of_trajectories tem de ser um inteiro positivo")

    ids = sorted(dataset)[:number_of_trajectories]
    if not ids:
        raise ValueError("dataset não contém trajetórias")

    columns = min(3, len(ids))
    rows = int(np.ceil(len(ids) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(columns * 4.2, rows * 3.8),
                             squeeze=False, sharex=True, sharey=True)
    axes = axes.ravel()

    for position, trajectory_id in enumerate(ids):
        entry = dataset[trajectory_id]
        longitude = _normalize_for_plot(entry["longitude"])
        latitude = _normalize_for_plot(entry["latitude"])
        x = _normalize_for_plot(entry["x"])
        y = _normalize_for_plot(entry["y"])
        ax = axes[position]

        ax.plot(longitude, latitude, color=NAV_COLOR, alpha=0.75,
                linewidth=1.0, label="longitude / latitude")
        ax.plot(x, y, color=FISH_COLOR, alpha=0.75,
                linewidth=1.0, label="x / y")
        ax.set_title(f"Trajetória {trajectory_id}", fontsize=9)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(linestyle=":", alpha=0.5)

        if position % columns == 0:
            ax.set_ylabel("Valor normalizado", fontsize=8)
        if position >= (rows - 1) * columns:
            ax.set_xlabel("Valor normalizado", fontsize=8)

    for ax in axes[len(ids):]:
        ax.set_visible(False)

    axes[0].legend(fontsize=8, loc="upper left")
    fig.suptitle("Comparação normalizada: longitude/latitude vs x/y", fontsize=11)
    fig.tight_layout()
    _save_fig("normalized_trajectory_comparison.png", "comparacao_features")


def _reconstruction_statistics(stored, calculated, tolerance=1e-6):
    errors = calculated - stored
    absolute_errors = np.abs(errors)
    relative_mask = calculated != 0
    relative_errors = absolute_errors[relative_mask] / np.abs(calculated[relative_mask])
    if stored.size <= 1:
        correlation = np.nan
    elif np.array_equal(stored, calculated):
        correlation = 1.0
    elif np.std(stored) == 0 or np.std(calculated) == 0:
        correlation = np.nan
    else:
        correlation = np.corrcoef(stored, calculated)[0, 1]
    return {
        "correlation": correlation,
        "mae": absolute_errors.mean(),
        "max_error": absolute_errors.max(),
        "mean_relative_error": relative_errors.mean() if relative_errors.size else np.nan,
        "within_tolerance": 100 * np.mean(absolute_errors <= tolerance),
        "count": stored.size,
    }


def _plot_reconstruction(stored, calculated, stored_label, calculated_label,
                         filename, title, calculated_legend, category):
    if stored.size == 0:
        raise ValueError(f"não existem pontos válidos para {title.lower()}")

    statistics = _reconstruction_statistics(stored, calculated)
    lower = min(stored.min(), calculated.min())
    upper = max(stored.max(), calculated.max())
    padding = (upper - lower) * 0.05 or 1

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(stored, calculated, s=6, alpha=0.25, color=NAV_COLOR,
               linewidths=0, label=calculated_legend)
    ax.plot([lower - padding, upper + padding],
            [lower - padding, upper + padding],
            color="crimson", linestyle="--", linewidth=1.2, label="y = x")
    ax.set_xlabel(stored_label, fontsize=9)
    ax.set_ylabel(calculated_label, fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.grid(linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, loc="upper right")

    relative_error = statistics["mean_relative_error"]
    relative_text = f"{relative_error:.6g}" if np.isfinite(relative_error) else "n/a"
    text = (
        f"n = {_format_count(statistics['count'])}\n"
        f"Correlação = {statistics['correlation']:.6f}\n"
        f"MAE = {statistics['mae']:.6g}\n"
        f"Erro absoluto máximo = {statistics['max_error']:.6g}\n"
        f"Erro relativo médio = {relative_text}"
    )
    text += f"\nDentro da tolerância (1e-6) = {statistics['within_tolerance']:.2f}%"
    ax.text(0.03, 0.97, text, transform=ax.transAxes, va="top",
            fontsize=8, bbox={"facecolor": "white", "alpha": 0.85,
                              "edgecolor": "0.7"})

    fig.tight_layout()
    _save_fig(filename, category)


def _collect_speed_values(dataset):
    stored_values = []
    calculated_values = []
    for entry in dataset.values():
        speed = np.asarray(entry["euc_speed"], dtype=float)
        distance_gap = np.asarray(entry["distance_gap"], dtype=float)
        time_gap = np.asarray(entry["time_gap"], dtype=float)
        valid = ((time_gap > 0) & np.isfinite(speed)
                 & np.isfinite(distance_gap) & np.isfinite(time_gap))
        stored_values.append(speed[valid])
        calculated_values.append(distance_gap[valid] / time_gap[valid])

    stored = np.concatenate(stored_values) if stored_values else np.array([])
    calculated = np.concatenate(calculated_values) if calculated_values else np.array([])
    return stored, calculated


def plot_speed_reconstruction_original(dataset):
    stored, calculated = _collect_speed_values(dataset)
    _plot_reconstruction(
        stored,
        calculated,
        "euc_speed armazenado (nós)",
        "distance_gap / time_gap (m/s)",
        "speed_vs_distance_over_time_original.png",
        "Validação sem conversão de unidades",
        "Original: distance_gap / time_gap (m/s)",
        "comparacao_features",
    )


def plot_speed_reconstruction(dataset):
    stored, calculated = _collect_speed_values(dataset)
    _plot_reconstruction(
        stored,
        calculated / METERS_PER_SECOND_PER_KNOT,
        "euc_speed armazenado",
        "distance_gap / time_gap convertido para nós",
        "speed_vs_distance_over_time.png",
        "Validação de euc_speed por distance_gap / time_gap (nós)",
        "Convertido para nós: distance_gap / time_gap",
        "comparacao_features",
    )


def plot_distance_gap_reconstruction(dataset):
    stored_values = []
    calculated_values = []
    for entry in dataset.values():
        x = np.asarray(entry["x"], dtype=float)
        y = np.asarray(entry["y"], dtype=float)
        distance_gap = np.asarray(entry["distance_gap"], dtype=float)
        length = min(distance_gap.size, x.size, y.size)
        distance_gap = distance_gap[:length][1:]
        calculated = np.hypot(np.diff(x[:length]), np.diff(y[:length]))
        valid = np.isfinite(distance_gap) & np.isfinite(calculated)
        stored_values.append(distance_gap[valid])
        calculated_values.append(calculated[valid])

    stored = np.concatenate(stored_values) if stored_values else np.array([])
    calculated = np.concatenate(calculated_values) if calculated_values else np.array([])
    _plot_reconstruction(
        stored,
        calculated,
        "distance_gap armazenado",
        "distância consecutiva calculada em x/y",
        "distance_gap_vs_xy_distance.png",
        "Validação de distance_gap pela distância consecutiva em x/y",
        "Distância calculada em x/y",
        "comparacao_features",
    )


if __name__ == "__main__":
    dataset = load_ordered_dataset(OUTPUT_JSON_FILE_PATH)
    plot_rows_by_id_histogram(dataset)
    plot_class_distribution(dataset)
    plot_segments_per_traj(dataset)
    plot_segments_per_id(dataset)
    plot_features_by_class(dataset)
    plot_speed_vs_turn(dataset)
    plot_speed_vs_turn_id(dataset, "211477000-2")
    plot_outliers(dataset)
    plot_time_gaps(dataset)
    plot_normalization_before_after(dataset)
    plot_overlapping_windows(dataset, "211477000-2", 50, 25)
    plot_multiple_trajectories(dataset, 5)
    plot_speed_reconstruction_original(dataset)
    plot_speed_reconstruction(dataset)
    plot_distance_gap_reconstruction(dataset)
