import json
import os
import matplotlib.pyplot as plt
import numpy as np

# === Optional smoothing
plt.style.use("default")  # Reset to clean default

def smooth(data, window_size=3):  # Less aggressive smoothing
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

def plot_jerk_from_json(jerks, jerk_spike_count, output_path):
    smoothed_jerk = smooth(jerks)

    # Print jerk values around step 20 for debugging
    print("Jerk values 15–25:", jerks[15:26])

    # Try multiple threshold methods
    mean_abs_jerk = np.mean([abs(j) for j in jerks])
    dynamic_threshold_mean = min(max(mean_abs_jerk * 4, 400000), 1000000)
    dynamic_threshold_percentile = np.percentile(np.abs(jerks), 95)
    fixed_threshold = 20000

    # Choose the lowest of all thresholds for sensitivity
    dynamic_threshold = min(dynamic_threshold_mean, dynamic_threshold_percentile, fixed_threshold)
    print("Final dynamic threshold:", dynamic_threshold)

    # Detect spike locations based on dynamic threshold
    spike_indices = [i for i, val in enumerate(jerks) if abs(val) >= dynamic_threshold]
    spike_values = [smoothed_jerk[i] for i in spike_indices]

    # Plot jerk curve
    plt.figure(figsize=(10, 4), dpi=150)
    plt.plot(smoothed_jerk, linestyle='-', linewidth=2, color='red', label="Jerk")

    # Add threshold line
    plt.axhline(dynamic_threshold, color='gray', linestyle='--', linewidth=1, label='Threshold')

    # Mark spikes
    if spike_indices:
        plt.scatter(spike_indices, spike_values, color='blue', label='Detected Spikes', zorder=5)
        for i in spike_indices:
            plt.axvline(x=i, color='red', linestyle=':', alpha=0.3)

    # Display only detected spikes in title
    title = f"Truth: Jerk Over Time\nDetected Spikes: {len(spike_indices)}"
    plt.title(title, fontsize=13)
    plt.xlabel("Step")
    plt.ylabel("Jerk")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    input_file = "questionnaire_sessions/lie/averaged_result_interpolated.json"
    output_dir = "averaged_charts"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r") as f:
        data = json.load(f)

    if "jerks" in data:
        plot_jerk_from_json(
            data["jerks"],
            data.get("jerkSpikeCount", None),
            os.path.join(output_dir, "lie_jerks.png")
        )

if __name__ == "__main__":
    main()




