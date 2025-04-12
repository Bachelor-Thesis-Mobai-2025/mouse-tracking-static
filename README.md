# Deception Detection Questionnaire

This project is a web-based questionnaire designed to detect deception based on user behavior, specifically analyzing mouse movements, hesitation, pauses, and jerk spikes while answering questions. It includes a front-end interface for the user to interact with, a back-end server for handling data, and machine learning models for analyzing responses and detecting potential deception.

## Table of Contents

- [Usage](#usage)
- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Contributing](#contributing)
- [License](#license)

## Usage
Starting server and navigation to http://localhost:3000.

The questionnaire will guide the user through two parts: answering truthfully in the first part and then lying in the second part.

The system tracks mouse movements, pauses, and hesitation during the questionnaire to analyze potential deception.

Upon completion, the data is saved to the server, which logs the user’s session, including mouse data and responses.

## Backend
The backend is built using Node.js and Express. It serves the front-end files and handles requests to save questionnaire data. Here's a breakdown of the backend functionality:

server.js: This file sets up an Express server to handle requests.

POST /save-data: Receives data from the client, validates it, and saves it to a file.

The server creates session folders and saves the response data (including mouse movements, hesitation, speed, and jerks) to JSON files for further analysis.

## Frontend
The frontend consists of an interactive questionnaire displayed on the browser, where the user answers a series of questions:

index.html: The HTML file provides the structure for the questionnaire.

![Screenshot 2025-04-12 232431](https://github.com/user-attachments/assets/58fe6f46-d591-4ba5-b30a-15d6d687954c)

![Screenshot 2025-04-12 232507](https://github.com/user-attachments/assets/de8f383f-70a9-4085-9445-dec55d728ee9)

![Screenshot 2025-04-12 232554](https://github.com/user-attachments/assets/4b3c91de-acbf-415e-9b94-c7fc0e4baead)

script.js: The JavaScript file handles the logic for displaying the questions, tracking mouse movements, and determining hesitation or pauses. It sends data to the backend for storage.

styles.css: Provides the styles and layout for the questionnaire.

The front-end tracks the following:

Mouse movements (to calculate speed, acceleration, jerk, and curvatures).

Hesitation (based on pauses or lack of movement).

Deception flags based on patterns observed during the interaction.

