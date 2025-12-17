
# 🚀 My Daily Brief

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) 
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

> **"Your entire day, decoded in seconds."**  
> A next-gen personal dashboard that blends AI intelligence, real-time data, and mindful productivity into a single, breathtaking interface.

---

## 📸 Visual Preview

![Dashboard Preview](https://via.placeholder.com/800x450?text=Dashboard+Action+Shot+Placeholder)
*The Command Center: Weather, News, Finance, and AI Insights at a glance.*

---

## 📑 Table of Contents

- [🚀 My Daily Brief](#-my-daily-brief)
  - [📸 visual Preview](#-visual-preview)
  - [� Table of Contents](#-table-of-contents)
  - [💡 About](#-about)
  - [🛠️ Tech Stack](#-tech-stack)
  - [⚙️ Architecture & Flow](#-architecture--flow)
  - [📦 Installation](#-installation)
  - [🚀 Usage](#-usage)
  - [✨ Features](#-features)
  - [⚠️ Limitations](#-limitations)
  - [🔮 Roadmap](#-roadmap)
  - [🤝 Contributors](#-contributors)

---

## 💡 About

**My Daily Brief** solves the problem of "tab fatigue." Instead of opening five different apps for weather, news, stocks, todos, and music, this application aggregates them all into a high-performance, dark-mode dashboard.

Powered by **Google Gemini AI**, it doesn't just show you data—it interprets it. It generates a witty executive summary of your morning, recommends outfits based on live weather patterns, and even analyzes the sentiment of your journal entries to give you life advice.

---

## �️ Tech Stack

*   **Core:** Python 3.9+ 🐍
*   **Web Framework:** Streamlit (Custom CSS & Components)
*   **AI Engine:** Google Gemini (2.0 Flash/Pro Fallback System) 🤖
*   **Data Visualization:** Plotly & Plotly Express 📊
*   **Financial Data:** yFinance (Yahoo Finance) 📈
*   **APIs:** OpenWeatherMap, NewsAPI, ExchangeRate-API

---

## ⚙️ Architecture & Flow

The application follows a **Data-Driven Retrieval & Generation (RAG-lite)** pipeline:

`User Input (City/Interactions)` ➡️ `State Management` ➡️ `Data Aggregation` ➡️ `AI Synthesis` ➡️ `UI Rendering`

1.  **Input Layer**: User selects city or types journal entry.
2.  **Orchestration**: `session_state` checks if data is cached (Lazy Loading).
3.  **Data Fetching**:
    *   *Weather Node*: Calls OpenWeatherMap API.
    *   *News Node*: Calls NewsAPI.
    *   *Market Node*: Calls yFinance.
4.  **AI Inference Layer (Gemini)**:
    *   *System*: Takes raw Weather + News data.
    *   *Prompt*: "Act as a personal assistant, generate witty summary."
    *   *Output*: Natural language briefing.
5.  **Presentation**: Custom CSS renders the "Neo-Dark" UI with Plotly charts.

---

## � Installation

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

```bash
python --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/my-daily-brief.git
cd my-daily-brief
```

### 3. Install Dependencies
```bash
pip install -r my_daily_brief/requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the `my_daily_brief` directory:

```env
GEMINI_API_KEY=your_gemini_key_here
WEATHER_API_KEY=your_openweather_key_here
NEWS_API_KEY=your_newsapi_key_here
```

---

## 🚀 Usage

Run the dashboard locally:

```bash
streamlit run my_daily_brief/app.py
```

*The app will open automatically in your browser at `http://localhost:8501`*

---

## ✨ Features

*   **🤖 AI Morning Briefing**: A synthesized summary of the world and your local conditions.
*   **🌦️ Weather Monitor**: Real-time stats + 5-Day Forecast Graph.
*   **📰 News Timeline**: Color-coded top headlines with source links.
*   **🧣 Smart Outfit**: AI-logic suggestions based on temperature and rain.
*   **📈 Market Watch**: Live BTC, S&P 500, and NIFTY 50 tracking.
*   **🎧 Vibe Station**: Embedded Spotify player that shifts genres based on time of day (Morning Chill vs. Upbeat Energy).
*   **⚡ Focus Zone**: Built-in Todo list that persists during your session.
*   **🧠 Mindful Journal**: Write your thoughts and get an AI Mood Score (1-10) and actionable advice.

---

## ⚠️ Limitations

*   **API Rate Limits**: Dependent on the free tiers of OpenWeather and NewsAPI.
*   **Session Persistence**: Tasks and Journal entries are lost if the browser tab is fully closed (uses temporary Session State).
*   **Local Execution**: Currently designed for local hosting; cloud deployment requires setting secrets in the host platform.

---

## 🔮 Roadmap

- [ ] **Database Integration**: Save Journal entries and Todos permanently (SQLite/Postgres).
- [ ] **Voice Mode**: Speak to the dashboard using Speech-to-Text.
- [ ] **Calendar Sync**: Google Calendar integration for agenda view.
- [ ] **Mobile Responsive**: Optimize CSS for phone screens.

---

## 🤝 Contributors

| Name | Role |
| :--- | :--- |
| **AVS Aniketh** | Lead Developer |
| **Akash** | Developer |
| **Arun Patil** | Developer |
| **Arvind** | Developer |

---

*Built with ❤️ in Python.*