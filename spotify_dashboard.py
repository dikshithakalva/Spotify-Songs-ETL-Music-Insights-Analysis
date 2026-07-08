import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Spotify Music Insights Dashboard",
    page_icon="🎵",
    layout="wide"
)

# ==========================================
# BACKGROUND IMAGE
# ==========================================

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("wallpaper.png")

# ==========================================
# CSS
# ==========================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background:
            linear-gradient(
                rgba(0,0,0,0.82),
                rgba(0,0,0,0.82)
            ),
            url("data:image/png;base64,{img}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1,h2,h3,h4,p,label {{
        color: white !important;
    }}

    div[data-testid="metric-container"] {{
        background-color: rgba(20,20,20,0.85);
        border: 1px solid #1DB954;
        padding: 15px;
        border-radius: 15px;
    }}

    div[data-testid="stMetricValue"] {{
        color: #1DB954 !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: white !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: rgba(10,10,10,0.9);
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# DATABASE
# ==========================================

conn = sqlite3.connect("spotify.db")

df = pd.read_sql(
    "SELECT * FROM spotify_tracks",
    conn
)

# ==========================================
# CREATE EXTRA COLUMNS
# ==========================================

if "duration_min" not in df.columns:
    df["duration_min"] = df["duration_ms"] / 60000

if "mood" not in df.columns:

    def mood(valence):

        if valence >= 0.7:
            return "Happy"

        elif valence >= 0.4:
            return "Neutral"

        else:
            return "Sad"

    df["mood"] = df["valence"].apply(mood)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <h1 style='text-align:center;'>
        🎵 Spotify Music Insights Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style='text-align:center;color:#1DB954;'>
        ETL Pipeline • SQL Analytics • Visualization
    </h3>
    """,
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Tracks",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Artists",
        f"{df['artists'].nunique():,}"
    )

with col3:
    st.metric(
        "Genres",
        f"{df['track_genre'].nunique()}"
    )

with col4:
    st.metric(
        "Avg Popularity",
        round(df['popularity'].mean(),2)
    )

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎛 Filters")

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    sorted(df["track_genre"].unique())
)

filtered_df = df[
    df["track_genre"] == selected_genre
]

# ==========================================
# CHARTS ROW 1
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Top Genres")

    genre_popularity = (
        df.groupby("track_genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.style.use("dark_background")

    fig1, ax1 = plt.subplots(figsize=(8,5))

    genre_popularity.plot(
        kind="bar",
        color="#1DB954",
        ax=ax1
    )

    ax1.set_ylabel("Popularity")

    st.pyplot(fig1)

with col2:

    st.subheader("😊 Mood Distribution")

    mood_counts = df["mood"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6,5))

    ax2.pie(
        mood_counts,
        labels=mood_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig2)

# ==========================================
# ENERGY SCATTER
# ==========================================

st.subheader("⚡ Energy vs Popularity")

fig3, ax3 = plt.subplots(figsize=(10,5))

sns.scatterplot(
    data=df,
    x="energy",
    y="popularity",
    alpha=0.4,
    color="#1DB954",
    ax=ax3
)

st.pyplot(fig3)

# ==========================================
# CORRELATION HEATMAP
# ==========================================

st.subheader("🔥 Correlation Heatmap")

features = [
    "popularity",
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_min"
]

corr_matrix = df[features].corr()

fig4, ax4 = plt.subplots(figsize=(10,6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="RdYlGn",
    fmt=".2f",
    ax=ax4
)

st.pyplot(fig4)

# ==========================================
# TOP SONGS
# ==========================================

st.subheader("🏆 Top 10 Songs")

top_songs = (
    df.sort_values(
        by="popularity",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_songs[
        [
            "track_name",
            "artists",
            "track_genre",
            "popularity"
        ]
    ],
    use_container_width=True
)

# ==========================================
# FILTERED SONGS
# ==========================================

st.subheader(
    f"🎶 {selected_genre.title()} Songs"
)

st.dataframe(
    filtered_df[
        [
            "track_name",
            "artists",
            "popularity",
            "danceability",
            "energy"
        ]
    ],
    use_container_width=True
)

# ==========================================
# SQL ANALYTICS
# ==========================================

st.subheader("📊 SQL Insights")

query = """
SELECT
    track_genre,
    ROUND(AVG(popularity),2) AS avg_popularity
FROM spotify_tracks
GROUP BY track_genre
ORDER BY avg_popularity DESC
LIMIT 10
"""

sql_data = pd.read_sql(
    query,
    conn
)

st.dataframe(
    sql_data,
    use_container_width=True
)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.success(
    "✅ ETL Pipeline → Data Cleaning → Feature Engineering → SQLite → SQL Analytics → Dashboard"
)