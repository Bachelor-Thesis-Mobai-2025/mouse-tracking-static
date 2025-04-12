import json
import matplotlib.pyplot as plt
import numpy as np

def load_summary_metrics(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def plot_comparison_chart(lie_data, truth_data):
    metric_labels = ["Total Time (s)", "Average Speed (px/s)", "Jerk Spikes", "Hesitation", "Pause Duration", "Pause Count"]
    keys = ["TotalTime", "averageSpeed", "JerkSpikeCount", "Hesitation", "PauseDuration", "PauseCount"]

    lie_values = [lie_data.get(k, 0) for k in keys]
    truth_values = [truth_data.get(k, 0) for k in keys]

    x = np.arange(len(metric_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, lie_values, width, label='Lie', color='red', alpha=0.9)
    bars2 = ax.bar(x + width/2, truth_values, width, label='Truth', color='blue', alpha=0.9)

    ax.set_ylabel('Values')
    ax.set_title('Summary Statistics: Lie vs Truth')
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, rotation=15)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("averaged_charts/comparison_stats_chart.png")
    plt.show()

# === USAGE ===
lie_file = "averaged_json/lie_mouse_stats_summary.json"
truth_file = "averaged_json/truth_mouse_stats_summary.json"

lie_metrics = load_summary_metrics(lie_file)
truth_metrics = load_summary_metrics(truth_file)

plot_comparison_chart(lie_metrics, truth_metrics)
