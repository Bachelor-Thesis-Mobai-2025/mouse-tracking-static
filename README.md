# Deception Detection Questionnaire

This project is a web-based questionnaire designed to detect deception based on user behavior, specifically analyzing mouse movements, hesitation, pauses, and jerk spikes while answering questions. It includes a front-end interface for the user to interact with, a back-end server for handling data, and machine learning models for analyzing responses and detecting potential deception.

## Table of Contents

- [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Saved data](#saved-data)
- [Analysis of collected data](#analysis-of-collected-data)
- [Neural network modeling](#neural-network-modeling)
- [Contributing](#contributing)
- [License](#license)

## Usage

The questionnaire will guide the user through two parts: answering truthfully in the first part and then lying in the second part.

The system tracks mouse movements, pauses, and hesitation during the questionnaire to analyze potential deception.

Upon completion, the data is saved to the server, which logs the user’s session, including mouse data and responses.

## Features
- Single layout design
- Mouse tracking and collecting data like position, velocity, acceleration, pause, hesitation, jerks
- Experimental design:
  - Truthful vs. Deceptive response tracking
  - Fixed yes/no button placement
  - Comprehensive data logging
- Data Analysis:
  - Calculating average values
  - Graphical presentation of results

## Project Structure

```
project-folder
├──averaged_charts                                   
│   ├──acceleration_comparison.png
│   ├──comparison_stats_chart.png
│   ├──curvature_comparison.png
│   ├──jerk_comparison.png
│   ├──lie_average_mouse_pattern.png
│   ├──lie_jerks.png
│   ├──truth_average_mouse_pattern.png
│   └──truth_jerks.png
├──averaged_json
│   ├──lie_average_mouse_path.json
│   ├──lie_mouse_stats_summary.json
│   ├──truth_average_mouse_path.json
│   └──truth_mouse_stats_summary.json
├──public
│   ├──index.html
│   ├──script.js
│   └──styles.css
├──questionnaire_sessions                 # Notice: Folder contains collected and sorted data
│   ├──lie                                # Subfolders are not included
│   ├──truth                              # They are here for graphical presentation
│   └──session_1743403663235
│      ├──part_1
│      └──part_2
├──utils
│   ├──average_mouse_pattern.py
│   ├──average_mouse_stats_chart.py
│   ├──average_mouse_stats.py
│   ├──calc_averages.py
│   ├──plot_mouse_analyse.py
│   └──plot_mouse_jerk.py
├──package-lock.json
├──package.json
└──server.js
```
Descripton of project folder:

- **`project_folder`**: contains **server.js**, backend server for handling requests and saving data
- **`averaged_charts`**: contains graphical representations, chart and analysys of collected data.
- **`averaged_json`**: contains json files with calculated averaged values from collected data.
- **`public`**: contains **script.js** with algorithm for collecting and saving necessary data through the questionare(**index.html**, **style.css**).
- **`questionnaire_sessions`**: contains saved data in json files from user input, through questionare.
- **`utils`**: contains programs for calculating average values of collected data and visual representation of results for further analysys.



## Backend
The backend is built using Node.js and Express. It serves the front-end files and handles requests to save questionnaire data. Here's a breakdown of the backend functionality:

server.js: This file sets up an Express server to handle requests.

POST /save-data: Receives data from the client, validates it, and saves it to a file.

The server creates session folders and saves the response data (including mouse movements, hesitation, speed, and jerks) to JSON files for further analysis.

## Frontend
The frontend consists of an interactive questionnaire displayed on the browser, where the user answers a series of questions. One layout has been used in this prototype:

<img src="https://github.com/user-attachments/assets/46696f14-2746-45bd-883c-92590c5f4fc2" width="600" />

<img src="https://github.com/user-attachments/assets/4d0992b5-9f28-422b-ab17-9d43278e9aeb" width="600" />

<img src="https://github.com/user-attachments/assets/d02d63b7-42ac-4790-a152-7a3882ce7622" width="600" />

**`index.html`**: The HTML file provides the structure for the questionnaire.

**`script.js`**: The JavaScript file handles the logic for displaying the questions, tracking mouse movements, and determining hesitation or pauses. It sends data to the backend for storage.

**`styles.css`**: Provides the styles and layout for the questionnaire.

The front-end tracks the following:

- Mouse movements (to calculate speed, acceleration, jerk, and curvatures).
- Hesitation (based on pauses or lack of movement).
- Deception flags based on patterns observed during the interaction.

## Saved data

During questionare, mouse movement data are saved as **`JSON`** file. Example:
```
{
    "question": "Are you currently a student at NTNU?",
    "answer": "Yes",
    "mouseMovements": [
        [524, 571], [525, 570], [526, 568], ...
    ],
    "timestamps": [1.237, 1.246, 1.254, ...],
    "accelerations": [0, -52152.97, 15296.70, ...],
    "jerks": [0, 0, 0, ...],
    "curvatures": [0, 0, 0, 0.1789, ...],
    "pausePoints": [],
    "hesitation": 0,
    "hesitationLevel": "low",
    "totalTime": 2.545,
    "averageSpeed": 345.146,
    "deceptionFlag": false,
    "jerkSpikeCount": 7,
    "label": 0
}
```
Description of parameters:

#### **1. `question`**:
   - The question asked to the user.

#### **2. `answer`**:
   - The user's response to the question.

#### **3. `mouseMovements`**:
   - An array of **[x, y]** coordinates tracking the mouse position over time.

#### **4. `timestamps`**:
   - An array of timestamps corresponding to each mouse movement.

#### **5. `accelerations`**:
   - The rate of change of the mouse's velocity at each timestamp.

#### **6. `jerks`**:
   - The rate of change of acceleration (jerk) in the mouse movement.

#### **7. `curvatures`**:
   - The curvature of the mouse’s path, indicating sharpness of movement.

#### **8. `pausePoints`**:
   - Points where the user paused, usually representing breaks in mouse movement.

#### **9. `hesitation`**:
   - A numerical value representing the amount of hesitation in the response.

#### **10. `hesitationLevel`**:
   - A qualitative measure of hesitation, e.g., "low", "medium", or "high".

#### **11. `totalTime`**:
   - Total time (in seconds) the user took to answer the question.

#### **12. `averageSpeed`**:
   - The average speed of the mouse movement during the response.

#### **13. `deceptionFlag`**:
   - A flag indicating whether deception was detected (true/false).

#### **14. `jerkSpikeCount`**:
   - The number of jerk spikes (abrupt changes in acceleration) during the response.

#### **15. `label`**:
   - The label for the response (0 for truthful, 1 for deceptive).

## Analysis of collected data
Programs used for analysing collected data:
- **`average_mouse_pattern.py`**: processes and visualizes mouse movement data to generate an average mouse movement path for a given set of trajectories (each path is resampled to 100 points using cubic spline interpolation).<br>
- **`average_mouse_stats.py`** and **`average_mouse_stats_chart.py`**: designed to summarize and visualy represent mouse movement statistics from a set of JSON files in a given folder.<br>
- **`calc_averages.py`**: designed for mouse movement analysis that computes averages and derived metrics (like jerk and curvature) from JSON data files.<br>
- **`plot_mouse_analyse.py`**: compares averaged mouse movement metrics (acceleration, curvature, jerk).<br>
- **`plot_mouse_jerk.py`**: analyzes jerk (derivative of acceleration) to detect spikes (sudden movements).<br>

![comparison_stats_chart](https://github.com/user-attachments/assets/a930ab5c-9014-4514-a28a-d6f996d937f8)

![truth_average_mouse_pattern](https://github.com/user-attachments/assets/43ec3c1b-eb31-4c3e-9f06-8cad8d399dbf)
- Truthful mouse movements likely follows a straighter or smoother trajectory.

![lie_average_mouse_pattern](https://github.com/user-attachments/assets/ef773b3c-ab75-43dd-9e58-129da9c3b2fa)
- Deceptive mouse movements deviates more from the straight "Start-End" line, indicating less direct or more erratic movement.

![curvature_comparison](https://github.com/user-attachments/assets/57b82f95-91bc-4584-b430-f76ddc7dd6ab)
- The graph robustly demonstrates that truthful mouse movements are straighter, while lies introduce measurable curvature.

![acceleration_comparison](https://github.com/user-attachments/assets/20e865b1-b6ba-40cf-8d45-8c6c67ca1199)
- Truthful mouse movements exhibit smoother acceleration, while deceptive ones are more erratic and variable.

![truth_jerks](https://github.com/user-attachments/assets/df0abc36-60a3-4d32-b1ec-8a5f90ef3f0f)
- Deceptive mouse movements shows a much higher peak jerk than truthful mouse movements, indicating more abrupt changes in movement, possibly reflecting hesitation or correction.

![lie_jerks](https://github.com/user-attachments/assets/8f26b30b-4c14-4ee1-84ad-af12b28db87c)
- 6 spike counts were detected in truthful mouse movements and 12 spike counts in deceptive mouse movements which suggests more frequent rapid changes in motion during deception.

## Neural network modeling 

![neural_network_architecture_final (1)](https://github.com/user-attachments/assets/1908e9db-dfa2-4bdf-8724-8d86076cf9bd)

<svg width="1100" height="800" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="140" y="50" font-family="Helvetica Neue, sans-serif" font-size="26" fill="#2C3E50" font-weight="bold">
    Neural Network Architecture
  </text>

  <!-- Style Definitions -->
  <defs>
    <style type="text/css"><![CDATA[
      .layer {
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: bold;
        fill: white;
        text-anchor: middle;
      }
      .label {
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        fill: #1C2833;
        text-anchor: middle;
      }
      .desc {
        font-family: 'Segoe UI', sans-serif;
        font-size: 11px;
        fill: #626567;
        font-style: italic;
        text-anchor: middle;
      }
    ]]></style>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#34495E"/>
    </marker>
  </defs>

  <!-- Input Layer -->
  <rect x="80" y="220" rx="15" ry="15" width="140" height="60" fill="#5DADE2"/>
  <text x="150" y="248" class="layer">Input Layer</text>
  <text x="150" y="270" class="label">Sequence: 150 × 6</text>
  <text x="150" y="290" class="desc">x, y, velocity, acceleration, jerk, curvature</text>

  <!-- LSTM Layer -->
  <rect x="260" y="220" rx="15" ry="15" width="140" height="60" fill="#F4D03F"/>
  <text x="330" y="248" class="layer">LSTM (64)</text>
  <text x="330" y="270" class="label">Temporal feature extraction</text>
  <text x="330" y="290" class="desc">Learns long-term motion patterns</text>

  <!-- GRU Layer -->
  <rect x="440" y="220" rx="15" ry="15" width="140" height="60" fill="#AF7AC5"/>
  <text x="510" y="248" class="layer">GRU (64)</text>
  <text x="510" y="270" class="label">Sequential refinement</text>
  <text x="510" y="290" class="desc">Captures recent dynamics efficiently</text>

  <!-- Dense Layer -->
  <rect x="620" y="220" rx="15" ry="15" width="140" height="60" fill="#58D68D"/>
  <text x="690" y="248" class="layer">Dense (64)</text>
  <text x="690" y="270" class="label">Fully connected ReLU</text>
  <text x="690" y="290" class="desc">Final abstract feature representation</text>

  <!-- Dropout Layer -->
  <rect x="620" y="320" rx="15" ry="15" width="140" height="50" fill="#EC7063"/>
  <text x="690" y="345" class="layer">Dropout (0.3)</text>
  <text x="690" y="365" class="desc">Prevents overfitting</text>

  <!-- Output Layer (moved down) -->
  <rect x="620" y="450" rx="15" ry="15" width="180" height="60" fill="#82E0AA"/>
  <text x="710" y="475" class="layer">Output: Sigmoid</text>
  <text x="710" y="495" class="label">Truthful vs. Deceptive</text>
  <text x="710" y="515" class="desc">Probability thresholded at 0.5</text>

  <!-- Arrows -->
  <line x1="220" y1="250" x2="260" y2="250" stroke="#34495E" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="400" y1="250" x2="440" y2="250" stroke="#34495E" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="580" y1="250" x2="620" y2="250" stroke="#34495E" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="690" y1="280" x2="690" y2="320" stroke="#34495E" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="690" y1="370" x2="690" y2="450" stroke="#34495E" stroke-width="2" marker-end="url(#arrow)"/>
</svg>


## Contributing
Fork the repository.

Create a new branch: git checkout -b feature/new-feature.

Commit your changes: git commit -m 'Add new feature'.

Push to the branch: git push origin feature/new-feature.

Open a pull request.

## License
This project is licensed under the MIT License 

