# Spotify-Songs-ETL-Music-Insights-Analysis
<img width="1920" height="930" alt="Screenshot (337)" src="https://github.com/user-attachments/assets/edd0d17e-496e-4e51-aa6a-f8d255af84e4" />

<img width="1920" height="924" alt="Screenshot (338)" src="https://github.com/user-attachments/assets/38b8c005-791e-4d4a-b359-312aee6f8472" />

# Spotify Music Insights Dashboard

## Project Overview

This project demonstrates an end-to-end **ETL (Extract, Transform, Load) pipeline** and interactive dashboard built using **Python, Pandas, SQLite, SQL, Streamlit, Matplotlib, and Seaborn**.

The project extracts Spotify music data, cleans and transforms the data, loads it into a SQLite database, performs SQL-based analytics, and visualizes key music trends through an interactive dashboard.

---

## Features

### Extract
- Loaded Spotify dataset from CSV file
- Examined dataset structure and quality

### Transform
- Removed duplicate records
- Handled missing values
- Created new engineered features:
  - Duration (minutes)
  - Mood Category (Happy, Neutral, Sad)
  - Popularity Level
  - Energy Level
  - Tempo Category

### Load
- Stored cleaned data into a SQLite database (`spotify.db`)
- Created SQL-ready tables for analytics

### Analytics
- Top 10 Most Popular Songs
- Top Genres by Popularity
- Mood Analysis
- Energy & Popularity Relationships

---

## Running the Dashboard

Install dependencies:

```bash
pip install streamlit pandas matplotlib seaborn
```

Run the application:

```bash
streamlit run spotify_dashboard.py
```

The dashboard will open locally at:

```text
http://localhost:8501
```
