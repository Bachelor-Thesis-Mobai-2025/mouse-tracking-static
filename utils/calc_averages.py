import os
import json
import numpy as np
from glob import glob
from scipy.interpolate import CubicSpline

# === Settings ===
INTERPOLATION_POINTS = 100

# === Helper Functions ===

def interpolate_to_fixed_length(array, target_len=INTERPOLATION_POINTS):
    if not array:
        return []

    # Convert dicts {"x": ..., "y": ...} to [x, y]
    if isinstance(array[0], dict) and "x" in array[0] and "y" in array[0]:
        array = [[pt["x"], pt["y"]] for pt in array]

    if len(array) == 1:
        return [array[0] for _ in range(target_len)]

    x_old = np.linspace(0, 1, len(array))
    x_new = np.linspace(0, 1, target_len)

    # 2D coordinate list
    if isinstance(array[0], list) and len(array[0]) == 2:
        xs = [pt[0] for pt in array]
        ys = [pt[1] for pt in array]
        cs_x = CubicSpline(x_old, xs)
        cs_y = CubicSpline(x_old, ys)
        return [[float(x), float(y)] for x, y in zip(cs_x(x_new), cs_y(x_new))]

    # 1D values
    cs = CubicSpline(x_old, array)
    return cs(x_new).tolist()

def average_interpolated(arrays, target_len=INTERPOLATION_POINTS):
    clean_arrays = []

    for arr in arrays:
        try:
            interpolated = interpolate_to_fixed_length(arr, target_len)
            if isinstance(interpolated[0], list):
                if all(len(p) == 2 for p in interpolated):
                    clean_arrays.append(interpolated)
            elif isinstance(interpolated[0], (int, float)):
                clean_arrays.append(interpolated)
        except Exception as e:
            print(f"⚠️ Skipped invalid array: {e}")

    if not clean_arrays:
        return []

    return np.mean(clean_arrays, axis=0).tolist()

def normalize_jerks(jerks):
    mean_abs = np.mean(np.abs(jerks))
    if mean_abs == 0:
        return jerks  # Avoid divide-by-zero
    return [j / mean_abs for j in jerks]

# === Main Function ===

def average_json_from_folder(folder_path):
    json_files = glob(os.path.join(folder_path, "*.json"))
    if not json_files:
        print("No JSON files found.")
        return

    numeric_fields = ["accelerations", "curvatures", "timestamps"]
    array_fields = {
        "mouseMovements": [],
        "pausePoints": []
    }
    scalar_fields = {
        "totalTime": [],
        "averageSpeed": [],
        "jerkSpikeCount": [],
        "hesitation": []
    }

    all_data = {field: [] for field in numeric_fields}

    for file_path in json_files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for field in numeric_fields:
                if field in data:
                    all_data[field].append(data[field])
            for field in array_fields:
                if field in data:
                    array_fields[field].append(data[field])
            for field in scalar_fields:
                if field in data:
                    scalar_fields[field].append(data[field])

    result = {
        "question": f"Average over {len(json_files)} samples",
        "answer": "N/A"
    }

    for field in numeric_fields:
        result[field] = average_interpolated(all_data[field]) if all_data[field] else []

    for field in array_fields:
        result[field] = average_interpolated(array_fields[field]) if array_fields[field] else []

    for field in scalar_fields:
        result[field] = float(np.mean(scalar_fields[field])) if scalar_fields[field] else 0

    # Compute raw jerks and normalized jerks
    if "accelerations" in result and result["accelerations"]:
        jerk_raw = np.diff(result["accelerations"]).tolist()
        jerk_clean = [round(j, 10) if abs(j) > 0 else 0 for j in jerk_raw]
        result["jerks"] = jerk_clean
        result["jerksNormalized"] = normalize_jerks(jerk_clean)

    # Save output
    output_path = os.path.join(folder_path, "averaged_result_interpolated.json")
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✅ Saved averaged result to: {output_path}")
# === Entry Point ===
if __name__ == "__main__":
    average_json_from_folder("questionnaire_sessions/truth")  # Update path as needed
