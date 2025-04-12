import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.collections import LineCollection

def load_mouse_movements_from_json(folder_path):
    all_movements = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            with open(os.path.join(folder_path, file), 'r') as f:
                data = json.load(f)
                all_movements.append(data["mouseMovements"])
    return all_movements

def interpolate_movements(movements, num_points=100):
    interpolated = []
    for path in movements:
        path = np.array(path)
        t = np.linspace(0, 1, len(path))
        new_t = np.linspace(0, 1, num_points)

        kind = 'cubic' if len(path) >= 4 else 'linear'
        interp_x = interp1d(t, path[:, 0], kind=kind)
        interp_y = interp1d(t, path[:, 1], kind=kind)
        interp_path = np.stack((interp_x(new_t), interp_y(new_t)), axis=-1)
        interpolated.append(interp_path)
    return np.array(interpolated)

def average_mouse_movements(interpolated_paths):
    return np.mean(interpolated_paths, axis=0)

def save_average_to_json(avg_array, output_path):
    result = {
        "averageMouseMovements": avg_array.tolist()
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)

def plot_mouse_path(avg_array):
    x, y = avg_array[:, 0], avg_array[:, 1]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw orange path
    ax.plot(x, y, color='blue', linewidth=2, label="Mouse Path")

    # Mark first point
    ax.plot(x[0], y[0], 'go', color='grey', label="Start", markersize=6)
    # Mark last point
    ax.plot(x[-1], y[-1], 'ro', color='grey', label="End", markersize=6)
    # Line between first and last point
    ax.plot([x[0], x[-1]], [y[0], y[-1]], 'k--', color='grey', label="Start-End Line", linewidth=1.5)

    ax.set_title("Truth: Average Mouse Movement Path")
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")
    ax.invert_yaxis()  # typical screen coords
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()

# === USAGE ===
folder_path = "questionnaire_sessions/truth"  # Replace with your actual folder

movements = load_mouse_movements_from_json(folder_path)
interpolated = interpolate_movements(movements, num_points=100)
avg_array = average_mouse_movements(interpolated)
plot_mouse_path(avg_array)

