# 🚦 Real-Time Traffic Management System

A minimal-stack, real-time data engineering project that simulates traffic flow data, stores it in a NoSQL database, and visualizes it using a live interactive dashboard.

## 📋 Project Overview

This project simulates an IoT environment where traffic sensors at various city intersections send data (vehicle count, speed, congestion level) to a central server.

  * **The Simulator (`traffic_simulator.py`)**: Acts as a "Virtual API," generating realistic, random traffic data every 3 seconds.
  * **The Database (MongoDB)**: Stores the streaming data efficiently.
  * **The Dashboard (`dashboard.py`)**: Fetches the latest data and visualizes KPIs, trends, and congestion warnings in real-time.

## 🛠️ Tech Stack

  * **Language**: Python 3.x
  * **Database**: MongoDB (Local or Atlas)
  * **Dashboard Framework**: Streamlit
  * **Data Manipulation**: Pandas & NumPy
  * **Visualization**: Plotly Express

## 📂 Project Structure

```text
Traffic-Management-System/
│
├── traffic_simulator.py   # Script to generate and push dummy data to MongoDB
├── dashboard.py           # Streamlit app for real-time visualization
├── README.md              # Project documentation
└── requirements.txt       # List of dependencies
```

## ⚙️ Prerequisites

1.  **Python 3.7+** installed.
2.  **MongoDB**:
      * **Local**: [Download MongoDB Community Server](https://www.mongodb.com/try/download/community).
      * **Cloud**: Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

## 🚀 Installation

1.  **Clone the repository** (or create a folder with the provided files):

    ```bash
    mkdir traffic_project
    cd traffic_project
    ```

2.  **Install Python Dependencies**:

    ```bash
    pip install streamlit pymongo pandas plotly
    ```

3.  **Configure Database**:

      * If using **Local MongoDB**, the default URI in the code (`mongodb://localhost:27017/`) works automatically.
      * If using **MongoDB Atlas**, open both `traffic_simulator.py` and `dashboard.py` and replace the `MONGO_URI` variable with your connection string:
        ```python
        MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/..."
        ```

## ⚡ How to Run

You need to run two separate terminal windows to see the real-time effect.

### Step 1: Start the Data Simulator

Open your first terminal and run the simulator. This will start "feeding" the database.

```bash
python traffic_simulator.py
```

*Output: You should see logs like `Inserted 3 records...` appearing every few seconds.*

### Step 2: Launch the Dashboard

Open a **second** terminal window and launch the Streamlit app.

```bash
streamlit run dashboard.py
```

*This will automatically open the dashboard in your default web browser (usually at `http://localhost:8501`).*

## 📊 Dashboard Features

1.  **Live KPIs**: Displays current Average Speed, Total Vehicles, and Congestion Rate (updates every 3 seconds).
2.  **Dynamic Metric Colors**: Metrics change color based on severity (e.g., Speed turns red if it drops below 40 km/h).
3.  **Line Chart**: Visualizes vehicle flow trends over time for different intersections.
4.  **Bar Chart**: Compares current speeds across locations, color-coded by congestion level (Green/Orange/Red).
5.  **Raw Data Inspector**: An expandable table to view the raw JSON data coming from MongoDB.

## 🛑 Stopping the Project

1.  Press `Ctrl + C` in the **Simulator** terminal to stop generating data.
2.  Press `Ctrl + C` in the **Dashboard** terminal to stop the web server.
