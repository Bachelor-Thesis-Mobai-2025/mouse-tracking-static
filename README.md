# Deception Detection Questionnaire

This project is a web-based questionnaire designed to detect deception based on user behavior, specifically analyzing mouse movements, hesitation, pauses, and jerk spikes while answering questions. It includes a front-end interface for the user to interact with, a back-end server for handling data, and machine learning models for analyzing responses and detecting potential deception.

## Table of Contents

- [Usage](#usage)
- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Saved data](#saved-data)
- [Contributing](#contributing)
- [License](#license)

## Usage
Starting server and navigation to http://localhost:3000.

The questionnaire will guide the user through two parts: answering truthfully in the first part and then lying in the second part.

The system tracks mouse movements, pauses, and hesitation during the questionnaire to analyze potential deception.

Upon completion, the data is saved to the server, which logs the user’s session, including mouse data and responses.

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
│   ├──truth                              # They are presented here for graphical representation
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

- **project_folder**: Contains **server.js**, backend server for handling requests and saving data
- **averaged_charts**: Folder contains graphical representations, chart and analysys of collected data.
- **averaged_json**: Folder contains json files with calculated averaged values from collected data.
- **public**: Folder contains **script.js** with algorithm for collecting and saving necessary data through the questionare(**index.html**, **style.css**).
- **questionnaire_sessions**: Folder for saving data in json files from user input, through questionare.
- **utils**: Folder contains programs for calculating average values of collected data and visual representation of results for further analysys.



## Backend
The backend is built using Node.js and Express. It serves the front-end files and handles requests to save questionnaire data. Here's a breakdown of the backend functionality:

server.js: This file sets up an Express server to handle requests.

POST /save-data: Receives data from the client, validates it, and saves it to a file.

The server creates session folders and saves the response data (including mouse movements, hesitation, speed, and jerks) to JSON files for further analysis.

## Frontend
The frontend consists of an interactive questionnaire displayed on the browser, where the user answers a series of questions:

<img src="https://github.com/user-attachments/assets/46696f14-2746-45bd-883c-92590c5f4fc2" width="600" />

<img src="https://github.com/user-attachments/assets/4d0992b5-9f28-422b-ab17-9d43278e9aeb" width="600" />

<img src="https://github.com/user-attachments/assets/d02d63b7-42ac-4790-a152-7a3882ce7622" width="600" />

**index.html**: The HTML file provides the structure for the questionnaire.

**script.js**: The JavaScript file handles the logic for displaying the questions, tracking mouse movements, and determining hesitation or pauses. It sends data to the backend for storage.

**styles.css**: Provides the styles and layout for the questionnaire.

The front-end tracks the following:

- Mouse movements (to calculate speed, acceleration, jerk, and curvatures).
- Hesitation (based on pauses or lack of movement).
- Deception flags based on patterns observed during the interaction.

## Saved data

During questionare, mouse movment data are saved in JSON file. Example:
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

## Contributing
Fork the repository.

Create a new branch: git checkout -b feature/new-feature.

Commit your changes: git commit -m 'Add new feature'.

Push to the branch: git push origin feature/new-feature.

Open a pull request.

## License
This project is licensed under the MIT License 

