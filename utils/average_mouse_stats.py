import os
import json

def load_json_files(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            with open(os.path.join(folder_path, file), 'r') as f:
                data.append(json.load(f))
    return data

def compute_summary_stats(data):
    total_time = []
    avg_speed = []
    jerk_spikes = []
    hesitations = []
    pause_durations = []
    pause_counts = []

    for entry in data:
        total_time.append(entry.get("totalTime", 0))
        avg_speed.append(entry.get("averageSpeed", 0))
        jerk_spikes.append(entry.get("jerkSpikeCount", 0))
        hesitations.append(entry.get("hesitation", 0))

        pauses = entry.get("pausePoints", [])
        pause_counts.append(len(pauses))
        for pause in pauses:
            pause_durations.append(pause.get("duration", 0))

    def safe_avg(arr):
        return sum(arr) / len(arr) if arr else 0

    return {
        "averageTotalTime": safe_avg(total_time),
        "averageSpeed": safe_avg(avg_speed),
        "averageJerkSpikeCount": safe_avg(jerk_spikes),
        "averageHesitation": safe_avg(hesitations),
        "averagePauseDuration": safe_avg(pause_durations),
        "averagePauseCount": safe_avg(pause_counts)
    }

def save_stats_to_json(stats, output_path):
    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=4)

# === USAGE ===
folder_path = "questionnaire_sessions/truth"  # Replace with your folder path
output_file = "truth_mouse_stats_summary.json"

data = load_json_files(folder_path)
stats = compute_summary_stats(data)
save_stats_to_json(stats, output_file)

# Print to console
print("Summary Statistics:")
for key, value in stats.items():
    print(f"{key}: {value:.4f}")
