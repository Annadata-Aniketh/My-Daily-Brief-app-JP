import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import yfinance as yf

# Load environment variables
load_dotenv(override=True)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def generate_gemini_content_safe(prompt):
    """
    Wrapper to handle model fallback across multiple available Gemini versions.
    Tries 2.5 Pro/Flash, then 2.0 Pro/Flash.
    """
    models_to_try = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-pro-exp-02-05",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-preview-02-05" 
    ]
    
    last_exception = None
    for model_name in models_to_try:
        try:
            curr_model = genai.GenerativeModel(model_name)
            return curr_model.generate_content(prompt)
        except Exception as e:
            last_exception = e
            continue
            
    # If all fail, raise the last exception
    if last_exception:
        raise last_exception
    else:
        raise Exception("All models failed silently.")

# --- Helper Functions ---
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def get_daily_wisdom():
    quotes = [
        "The best way to predict the future is to create it.",
        "Small progress is still progress.",
        "Don't watch the clock; do what it does. Keep going.",
        "Your potential is endless.",
        "Focus on being productive instead of busy.",
        "Every day is a fresh start.",
        "Believe you can and you're halfway there."
    ]
    return random.choice(quotes)

def get_fun_fact():
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
        "Bananas are berries, but strawberries aren't.",
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
        "A group of flamingos is called a 'flamboyance'.",
        "Wombat poop is cube-shaped.",
        "The shortest war in history lasted 38 minutes between Britain and Zanzibar on August 27, 1896.",
        "Avocados are a fruit, not a vegetable. They're technically a single-seeded berry, much like a peach.",
        "The unicorn is the national animal of Scotland."
    ]
    return random.choice(facts)

@st.cache_data(ttl=300)
def get_market_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period="2d")
        if len(history) >= 2:
            current_price = history['Close'].iloc[-1]
            prev_price = history['Close'].iloc[-2]
            change = ((current_price - prev_price) / prev_price) * 100
            return current_price, change
        elif len(history) == 1: # Market might be open but only 1 data point for "2d" if yfinance is weird, try just current
             current_price = history['Close'].iloc[-1]
             return current_price, 0.0
        return None, None
    except Exception:
        return None, None

def get_outfit_recommendation(temp, weather_desc):
    recommendation = "Dress comfortably."
    if temp < 10:
        recommendation = "🧥 Wear a heavy jacket, it's cold!"
    elif 10 <= temp < 20:
        recommendation = "🧥 Bring a light jacket or sweater."
    elif temp >= 20:
        recommendation = "👕 T-shirt weather! Stay cool."
    
    if "rain" in weather_desc.lower() or "drizzle" in weather_desc.lower():
        recommendation += " ☔ Don't forget an umbrella!"
    
    return recommendation

def load_data_on_click(session_key, btn_text, fetch_func):
    """
    Generic helper to load data only when a button is clicked.
    Stores result in st.session_state[session_key].
    """
    if session_key not in st.session_state:
        if st.button(btn_text):
            with st.spinner("Loading..."):
                data = fetch_func()
                st.session_state[session_key] = data
            st.rerun()
        return None
    return st.session_state[session_key]

def generate_daily_briefing(weather_summary, news_headlines):
    try:
        # Fallback if no news/weather
        if not weather_summary or not news_headlines:
             return "Welcome to your day! Check the dashboard for the latest updates."

        prompt = f"""
        Generate a witty, 3-sentence executive summary of the day based on this info:
        Weather: {weather_summary}
        News: {news_headlines}
        
        Keep it professional yet engaging, like a personal assistant.
        Keep it professional yet engaging, like a personal assistant.
        """
        response = generate_gemini_content_safe(prompt)
        return response.text
    except Exception:
        return "Ready to conquer the day? Check out your dashboard below!"

# Page Config
st.set_page_config(page_title="Now Brief", layout="wide", page_icon="▣")

# --- Custom CSS for 'Check Box' Design ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Main Background */
    .stApp {
        background-color: #000000; /* Deep Black */
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #1a1a1a;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    /* Cards/Containers */
    .css-1r6slb0, .stColumn, [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background-color: #111111; /* Dark Grey Card */
        border-radius: 24px;
        padding: 20px;
        border: 1px solid #222;
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 10px 15px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #ccff00; /* Neon Green */
        color: #000000;
        border: none;
        border-radius: 30px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #b3e600;
        transform: scale(1.02);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #ffffff;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888;
        font-size: 0.9rem;
    }
    
    /* Divider */
    hr {
        border-color: #222;
    }
    
    /* Chat */
    .stChatMessage {
        background-color: #111111;
        border-radius: 16px;
        border: 1px solid #222;
    }
    
    /* Custom Classes for Accents */
    .accent-green { color: #ccff00; }
    .accent-orange { color: #ff9900; }
    
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation (About Team) ---
with st.sidebar:
    st.title("▣")
    
    # City Selection
    city_options = ["Bengaluru", "Mumbai", "Delhi", "New York", "London", "Tokyo", "Singapore", "Dubai", "Paris", "Berlin", "Type your own..."]
    selected_city = st.selectbox("Select Location", city_options, label_visibility="collapsed")
    
    if selected_city == "Type your own...":
        sidebar_city = st.text_input("Enter City Name", placeholder="e.g. Chicago")
    else:
        sidebar_city = selected_city

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    
    st.markdown("### About Our Team")
    st.info("AVS Aniketh, Akash, Arun Patil, Arvind")
    st.markdown("### About App")
    st.info("This app provides a daily brief including weather, news, market values, and an AI assistant to help you start your day informed and productive.")

    st.markdown("---")
    


# --- Global Data Fetching ---
# --- Data Fetching Functions (Lazy Loading) ---
@st.cache_data(ttl=3600)
def fetch_weather_data(city_name):
    weather_api_key = os.getenv("WEATHER_API_KEY")
    if weather_api_key and city_name:
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=metric"
            w_response = requests.get(weather_url)
            if w_response.status_code == 200:
                data = w_response.json()
                # Create simplified summary for top bar
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                summary = f"{temp:.1f}°C, {desc}"
                return {"full": data, "summary": summary}
        except Exception:
            pass
    return None

@st.cache_data(ttl=3600)
def fetch_news_data():
    news_api_key = os.getenv("NEWS_API_KEY")
    if news_api_key:
        try:
            news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}&pageSize=4"
            n_response = requests.get(news_url)
            if n_response.status_code == 200:
                articles = n_response.json().get('articles', [])
                headlines = ", ".join([a['title'] for a in articles[:3]])
                return {"articles": articles, "headlines": headlines}
        except Exception:
            pass
    return None

@st.cache_data(ttl=3600)
def fetch_market_metrics():
    curr_tickers = {
        "BTC": "BTC-USD",
        "S&P 500": "SPY",
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN"
    }
    results = []
    for name, symbol in curr_tickers.items():
        price, change = get_market_data(symbol)
        results.append((name, price, change))
    return results

# --- Top Bar Area ---
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    st.markdown(f"<h1 style='margin-bottom: 0;'>My Daily Brief</h1>", unsafe_allow_html=True)
    current_time = datetime.now().strftime("%B %d, %Y | %I:%M %p")
    st.markdown(f"<p style='color: #888; margin-top: -10px;'>{get_greeting()} &nbsp; <span style='color: #ccff00;'>{current_time}</span></p>", unsafe_allow_html=True)

with c2:
    # Check Session State for Briefing Data
    w_data = st.session_state.get('weather_data')
    n_data = st.session_state.get('news_data')
    
    w_summary = w_data['summary'] if w_data else "Load Weather below"
    n_headlines = n_data['headlines'] if n_data else "Load News below"
    
    # Only generate fresh briefing if data exists and no briefing is cached, OR just show generic
    # To save API, we'll only generate if both are present.
    if w_data and n_data:
        briefing = generate_daily_briefing(w_summary, n_headlines)
    else:
        briefing = "Please load Weather and News to generate your AI Briefing."

    outfit = "Check outside!"
    if w_data:
        outfit = get_outfit_recommendation(w_data['full']['main']['temp'], w_data['full']['weather'][0]['description'])
        
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 15px; border-radius: 12px; border-left: 4px solid #ccff00; height: 100%;">
            <div style="font-size: 0.8rem; color: #ccff00; font-weight: 600; margin-bottom: 4px;">DAILY BRIEFING</div>
            <div style="color: #ddd; font-size: 0.9rem; margin-bottom: 8px;">{briefing}</div>
            <div style="font-size: 0.85rem; color: #888; font-style: italic;">{outfit}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 15px; border-radius: 12px; border-left: 4px solid #00bfff;">
            <div style="font-size: 0.8rem; color: #00bfff; font-weight: 600; margin-bottom: 4px;">DID YOU KNOW?</div>
            <div style="font-style: italic; color: #ddd; font-size: 0.9rem;">"{get_fun_fact()}"</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.markdown("---")

# --- Main Dashboard Layout ---
col1, col2, col3 = st.columns(3)

# --- Column 1: Weather (Customer/Monitoring Style) ---
with col1:
    st.markdown("### WEATHER MONITOR")
    
    # 1. Get Weather Button (Uses Sidebar Input)
    # We use a unique key for the button or just rely on logic
    if st.button("Get Weather", use_container_width=True):
        if sidebar_city:
             with st.spinner("Fetching Weather..."):
                 data = fetch_weather_data(sidebar_city)
                 st.session_state['weather_data'] = data
                 st.session_state['current_city'] = sidebar_city
             st.rerun()
    
    # 3. Display Data (Persistent)
    weather_result = st.session_state.get('weather_data')
    
    if weather_result:
        full_data = weather_result['full']
        temp = full_data['main']['temp']
        humidity = full_data['main']['humidity']
        
        # Custom Metric Display
        m1, m2 = st.columns(2)
        m1.markdown(f"<h2 style='margin:0; color:#fff'>{temp:.1f}°</h2><span style='color:#ccff00'>▲ TEMP</span>", unsafe_allow_html=True)
        m2.markdown(f"<h2 style='margin:0; color:#fff'>{humidity}%</h2><span style='color:#ff9900'>▼ HUMIDITY</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Forecast Graph
        # We use the city from session state or logic to ensure consistency
        current_city = st.session_state.get('current_city', sidebar_city)
        
        try:
            weather_api_key = os.getenv("WEATHER_API_KEY")
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={current_city}&appid={weather_api_key}&units=metric"
            fore_response = requests.get(forecast_url)
            fore_data = fore_response.json()
            
            if fore_response.status_code == 200:
                forecast_list = fore_data['list'][:8]
                dates = [datetime.fromtimestamp(item['dt']) for item in forecast_list]
                temps = [item['main']['temp'] for item in forecast_list]
                
                # Plotly Graph
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates, y=temps,
                    mode='lines',
                    line=dict(color='#ccff00', width=3, shape='spline'),
                    fill='tozeroy',
                    fillcolor='rgba(204, 255, 0, 0.1)'
                ))
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#888', family="Inter"),
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=True, gridcolor='#222'),
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=150
                )
                st.plotly_chart(fig, use_container_width=True)
        except:
             st.info("Forecast unavailable")
    else:
        st.info("Enter city and click 'Get Weather'")

with col2:
    st.markdown("### NEWS TIMELINE")
    
    news_result = load_data_on_click("news_data", "📰 Load News", fetch_news_data)
    
    if news_result:
        articles = news_result['articles']
        for i, article in enumerate(articles):
            # Alternating Colors for "Pills"
            bg_color = "#ccff00" if i % 2 == 0 else "#ff9900"
            
            st.markdown(
                f"""
                <div style="background-color: #1a1a1a; padding: 10px; border-radius: 12px; margin-bottom: 10px; border-left: 5px solid {bg_color};">
                    <div style="font-size: 0.8rem; color: #888;">{article['source']['name']}</div>
                    <div style="font-weight: 600; font-size: 0.9rem;"><a href="{article['url']}" style="color: #fff; text-decoration: none;">{article['title'][:60]}...</a></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("News Unavailable / No Data")

    st.markdown("---")
    
    # 3. Commute Helper (Moved to Column 2)
    st.markdown("### 🚗 Commute Check")
    
    # Vertical layout to fit column Width
    src = st.text_input("From", "Home", label_visibility="collapsed", placeholder="From")
    dest = st.text_input("To", "Work", label_visibility="collapsed", placeholder="To")
    
    if st.button("Open Live Route", use_container_width=True):
        if src and dest:
            maps_url = f"https://www.google.com/maps/dir/{src}/{dest}"
            st.markdown(f"**[➢ Open Maps]({maps_url})**", unsafe_allow_html=True)
        else:
            st.warning("Enter locations")

# --- Column 3: Finance & Market ---
with col3:
    st.markdown("### MARKET VALUE")
    
    # 1. Market Indices (Finance) - On Demand
    market_metrics = load_data_on_click("market_data", "📈 Load Markets", fetch_market_metrics)
    
    # Create 2x2 grid for metrics
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2 = st.columns(2)
    
    if market_metrics:
        # Display Metrics
        # Helper to display simple metric
        def display_mini_metric(col, label, val, chg):
            if val is not None:
                color = "#ccff00" if chg >= 0 else "#ff4444"
                arrow = "▲" if chg >= 0 else "▼"
                col.markdown(
                    f"""
                    <div style="background-color: #1a1a1a; padding: 8px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #333;">
                        <div style="font-size: 0.75rem; color: #888;">{label}</div>
                        <div style="font-size: 1rem; font-weight: 700; color: #fff;">{val:,.0f}</div>
                        <div style="font-size: 0.75rem; color: {color};">{arrow} {abs(chg):.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                col.info(f"{label} N/A")

        if len(market_metrics) >= 4:
            display_mini_metric(row1_c1, market_metrics[0][0], market_metrics[0][1], market_metrics[0][2]) # BTC
            display_mini_metric(row1_c2, market_metrics[1][0], market_metrics[1][1], market_metrics[1][2]) # SPY
            display_mini_metric(row2_c1, market_metrics[2][0], market_metrics[2][1], market_metrics[2][2]) # NIFTY
            display_mini_metric(row2_c2, market_metrics[3][0], market_metrics[3][1], market_metrics[3][2]) # SENSEX
    else:
        st.info("Load data to see live markets.")
    
    st.markdown("---")

    # 2. Currency Converter (Existing)
    # Currency Selection
    currency_options = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"]
    
    c_sel, c_input = st.columns([1, 2])
    with c_sel:
        base_currency = st.selectbox("Currency", currency_options, label_visibility="collapsed")
    with c_input:
        amount = st.number_input("Amount", min_value=0.0, value=1.0, label_visibility="collapsed")

    # Fetch Exchange Rate
    try:
        # Using open.er-api.com (No API Key required)
        forex_url = f"https://open.er-api.com/v6/latest/{base_currency}"
        forex_response = requests.get(forex_url)
        forex_data = forex_response.json()
        
        if forex_response.status_code == 200:
            inr_rate = forex_data['rates']['INR']
            converted_amount = amount * inr_rate
            
            st.markdown(f"<h1 style='color:#fff'>₹ {converted_amount:,.2f}</h1>", unsafe_allow_html=True)
            st.caption(f"1 {base_currency} = ₹ {inr_rate:,.2f}")
            
            # Simple Bar Chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[base_currency, 'INR'],
                y=[amount, converted_amount], 
                marker_color=['#ccff00', '#ff9900'],
                text=[f"{amount:,.0f}", f"₹{converted_amount:,.0f}"],
                textposition='auto',
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fff', family="Inter"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False, showticklabels=False),
                margin=dict(l=0, r=0, t=20, b=0),
                height=200,
                bargap=0.4
            )
            fig.update_traces(marker_line_width=0, selector=dict(type="bar"))
            st.plotly_chart(fig, use_container_width=True)
        else:
             st.error("Rate Unavailable")
    except Exception:
        st.error("Connection Error")

# --- Focus Zone & Vibe Station ---
st.markdown("---")
c_focus, c_vibe = st.columns([2, 1])

# --- Focus Zone (Left) ---
with c_focus:
    st.markdown("### ⚡ FOCUS ZONE")
    
    if 'tasks' not in st.session_state:
        st.session_state['tasks'] = []
    
    # Add Task
    with st.form("focus_form", clear_on_submit=True):
        c_in, c_submit = st.columns([3, 1])
        with c_in:
            task_input = st.text_input("New Task", placeholder="What needs to be done?", label_visibility="collapsed")
        with c_submit:
            submitted = st.form_submit_button("Add")
        
        if submitted and task_input:
            st.session_state['tasks'].append(task_input)
            st.rerun()

    # Task List
    if st.session_state['tasks']:
         # Use list so we can modify it while iterating (though pop/rerun breaks loop anyway so enumeration is fine)
         # Using a copy just in case, but rerun stops script immediately.
         for i, task in enumerate(st.session_state['tasks']):
            # Use the task name AS the label so it aligns perfectly
            if st.checkbox(task, key=f"fz_task_{i}"):
                st.session_state['tasks'].pop(i)
                st.rerun()
    else:
        st.info("No active tasks. Time to relax or plan ahead! 🚀")

# --- Vibe Station (Right) ---
with c_vibe:
    st.markdown("### 🎧 VIBE STATION")
    
    mood_options = {
        "Morning Chill": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2sUQwD7tbmL",
        "Focus Flow": "https://open.spotify.com/embed/playlist/37i9dQZF1DWWQRwui0ExPn",
        "Upbeat Energy": "https://open.spotify.com/embed/playlist/37i9dQZF1DX6VdMW310YC7", 
        "Lo-Fi Study": "https://open.spotify.com/embed/playlist/0vvXsWCC9xrXsKd4FyS8kM" 
    }
    
    # Auto-select based on time for default
    default_mood = "Morning Chill"
    h = datetime.now().hour
    if 12 <= h < 18: default_mood = "Focus Flow"
    elif h >= 18: default_mood = "Upbeat Energy"

    # Ensure index is valid
    try:
        def_index = list(mood_options.keys()).index(default_mood)
    except ValueError:
        def_index = 0

    selected_mood_name = st.selectbox("Select Mood", list(mood_options.keys()), index=def_index)
    
    url = mood_options[selected_mood_name]
    components.iframe(src=url, height=152)

# --- Bottom Section: Mindful Journal ---
st.markdown("---")
st.markdown("### 🧠 Mindful Journal")

if 'journal_result' not in st.session_state:
    st.session_state['journal_result'] = None

# Input Area
journal_entry = st.text_area("What's on your mind?", height=100, placeholder="Pour your thoughts here...")

if st.button("Reflect & Analyze", type="primary"):
    if journal_entry:
        try:
            # Define prompt with JSON structure instruction
            prompt = f"""
            Analyze the sentiment of this journal entry. Return a valid JSON response with two keys:
            1) "score" (integer 1-10)
            2) "advice" (string, max 2 sentences)
            
            Entry: "{journal_entry}"
            
            Output format:
            {{
                "score": 7,
                "advice": "Your advice here."
            }}
            """
            
            response = generate_gemini_content_safe(prompt)
            # Simple parsing
            
            import json
            import re
            
            text_res = response.text
            # Try to find JSON block
            match = re.search(r'\{.*\}', text_res, re.DOTALL)
            if match:
                json_str = match.group(0)
                result = json.loads(json_str)
                st.session_state['journal_result'] = result
            else:
                 # Fallback if no JSON found
                st.session_state['journal_result'] = {"score": "?", "advice": text_res}
                
        except Exception as e:
            st.error(f"Analysis failed: {e}")

# Display Result (Persistent)
if st.session_state['journal_result']:
    res = st.session_state['journal_result']
    
    # Mood Metric
    st.metric("Mood Score", f"{res.get('score', '?')}/10")
    
    # Advice
    st.success(f"**Insight:** {res.get('advice', 'No advice generated.')}")

