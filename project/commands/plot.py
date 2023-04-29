import click
import os
import pandas as pd
from matplotlib import pyplot as plt
from rich import print


@click.group()
def plot() -> None:
    """
    Plot the data.
    """
    pass


@plot.command()
@click.option(
    "--folder",
    "-f",
    required=True,
    type=str,
)
def data(folder: str) -> None:
    # load all json files from given folder to pandas
    df = pd.concat(
        [
            pd.read_json(f"{folder}/{file}", lines=True)
            for file in os.listdir(folder)
            if file.endswith(".json")
        ]
    ).reset_index(drop=True)
    print(f"Datafrome:\n{df}")

    # title: average n, average time
    # x: true_positive, false_positive, true_negative, false_negative
    # x: accuracy, detection_rate, false_positive_rate
    # y: percentage and number
    average_n = df["n"].mean()
    average_time = df["time"].mean()
    average_attack = average_n / average_time
    print(f"Average n: {average_n} requests")
    print(f"Average time: {average_time} seconds")
    print(f"Average attack: {average_attack} requests per second")

    # plot
    fig = plt.figure(figsize=(7.5, 10))
    fig.suptitle(
        f"Average of {average_n:.2f} requests, completed in {average_time:.2f} seconds, {average_attack:.2f} requests per second",
    )

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_ylabel("Count")
    ax1.set_xticklabels(
        ["True Positive", "False Positive", "True Negative", "False Negative"],
        rotation=45,
    )
    ax1.bar(
        ["True Positive", "False Positive", "True Negative", "False Negative"],
        [
            df["true_positives"].mean(),
            df["false_positives"].mean(),
            df["true_negatives"].mean(),
            df["false_negatives"].mean(),
        ],
    )
    for i, v in enumerate(
        [
            df["true_positives"].mean(),
            df["false_positives"].mean(),
            df["true_negatives"].mean(),
            df["false_negatives"].mean(),
        ]
    ):
        ax1.text(i, v + 0.01, f"{v:.2f}", ha="center", va="bottom")

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_ylabel("Percentage")
    ax2.set_xticklabels(
        ["True Positive", "False Positive", "True Negative", "False Negative"],
        rotation=45,
    )
    # show actual count in :.2f
    ax2.bar(
        ["True Positive", "False Positive", "True Negative", "False Negative"],
        [
            (df["true_positives"].mean() / average_n) * 100,
            (df["false_positives"].mean() / average_n) * 100,
            (df["true_negatives"].mean() / average_n) * 100,
            (df["false_negatives"].mean() / average_n) * 100,
        ],
    )
    for i, v in enumerate(
        [
            (df["true_positives"].mean() / average_n) * 100,
            (df["false_positives"].mean() / average_n) * 100,
            (df["true_negatives"].mean() / average_n) * 100,
            (df["false_negatives"].mean() / average_n) * 100,
        ]
    ):
        ax2.text(i, v + 0.01, f"{v:.2f}%", ha="center", va="bottom")

    plt.savefig(f"{folder}/data.png")
