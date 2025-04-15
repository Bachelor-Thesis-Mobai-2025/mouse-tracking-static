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
- [Research Findings](#research-findings)
- [Technologies Used](#technologies-used)
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
**`model_training_dl_lstm_gru_v1.py`**: classify whether a mouse movement sequence corresponds to a truthful or deceptive response by learning patterns from time-series features like position, velocity, acceleration, etc.<br>

Deep Learning Model Architecture:
- Input: Sequences of mouse movement features (150 timesteps × 6 features)

- Model: **LSTM → GRU → Dense → Dropout → Sigmoid**

- LSTM (64): Captures long-term temporal dependencies.

- GRU (64): Efficiently refines short-term patterns.

- Dense (64, ReLU): High-level feature transformation.

- Dropout (0.3): Prevents overfitting.

Input Features from JSON files containing mouse trajectory data:

- **x, y coordinates**

- **velocity**

- **acceleration**

- **jerk**
  
- **curvature**
  
Each sequence is padded or truncated to 150 time steps.

Data Handling
- Loads and preprocesses .json files from:

 - data/truthful_responses/

 - data/deceptive_responses/

Combines, labels (0 for truthful, 1 for deceptive), and normalizes input.

Split:

- **70% training**

- **20% validation**

- **10% test**

Training Strategy:
- Optimizer: *Adam*

- Loss: *binary_crossentropy*

- Early stopping with patience = *5 epochs* (restores best weights).

- Batch size: *32*

- Epochs: *50 max*

Evaluation Metrics:
-Final evaluation on the test set:

 - **Macro F1 score**

 - **Classification report**

 - **Confusion matrix**

 - **Loss curves**

Model Persistence:
 - Trained model is saved as **`best_lstm_gru_model.h5`**


![Screenshot 2025-04-15 102645](https://github.com/user-attachments/assets/7a09b49f-578e-4884-805d-3438080fd836)

Results with current network:

Overall accuracy 0.60 ≈ 60%, model is correctly predicting 42 out of 70 samples.

![confusion_matrix](https://github.com/user-attachments/assets/2cc60420-08b9-4861-9d85-1be1b96d5155)

Interpretation per class:
- Class 0: Truthful
  - Precision (0.73): When the model predicts truthful, it's correct 73% of the time.
  - Recall (0.31): Only catches 31% of the actual truthful responses → many are missed (false negatives).

- Class 1: Deceptive
  - Precision (0.56): Slightly above random for deceptive predictions.
  - Recall (0.89): Very good — it finds most of the deceptive cases.

![training_validation_loss](https://github.com/user-attachments/assets/6ec9d568-5c87-4037-b257-bd12a7a91b78)

- Training Loss is decreasing, which means the model is learning from the training data.

- Validation Loss is increasing, which is a warning sign of overfitting (small dataset).

![feature_importance](https://github.com/user-attachments/assets/fcb22bbe-4508-4389-8f33-12359ea1c8f8)

![feature_correlation_matrix](https://github.com/user-attachments/assets/8b7d716a-092e-4102-821c-48179677215f)

## Research Findings
- Movement dynamics velocity and acceleration change velocity are the most discriminative features.
- Path efficiency and movement smoothness show significant differences between truthful and deceptive responses.
- The model, at best, has achieved 60% accuracy on the test set.
- The best-performing training was selected as the final model.
- Visualization outputs stored in the Images directory.

## Technologies Used
- Backend: JavaScript
- Frontend: HTML, CSS, JavaScript
- Data Analysis:
  - Pandas
  - NumPy
  - Matplotlib
  - Seaborn
- Machine Learning:
  - TensorFlow/Keras (neural network implementation)
  - Scikit-learn (data splitting and evaluation)

## Contributing
Fork the repository.

Create a new branch: git checkout -b feature/new-feature.

Commit your changes: git commit -m 'Add new feature'.

Push to the branch: git push origin feature/new-feature.

Open a pull request.

## License
This project is licensed under the MIT License 

