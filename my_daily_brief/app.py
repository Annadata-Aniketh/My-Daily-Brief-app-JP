import streamlit as st
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

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

# Page Config
st.set_page_config(page_title="CHECK BOX // BRIEF", layout="wide", page_icon="▣")

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
    st.markdown("### About Our Team")
    st.info("AVS Aniketh, Akash, Arun Patil, Arvind")
    st.markdown("### About App")
    st.info("This app provides a daily brief including weather, news, market values, and an AI assistant to help you start your day informed and productive.")

# --- Top Bar Area ---
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    st.markdown(f"<h1 style='margin-bottom: 0;'>My Daily Brief</h1>", unsafe_allow_html=True)
    current_time = datetime.now().strftime("%B %d, %Y | %I:%M %p")
    st.markdown(f"<p style='color: #888; margin-top: -10px;'>{get_greeting()} &nbsp; <span style='color: #ccff00;'>{current_time}</span></p>", unsafe_allow_html=True)

with c2:
    st.markdown(
        f"""
        <div style="background-color: #1a1a1a; padding: 15px; border-radius: 12px; border-left: 4px solid #ccff00;">
            <div style="font-size: 0.8rem; color: #ccff00; font-weight: 600; margin-bottom: 4px;">DAILY WISDOM</div>
            <div style="font-style: italic; color: #ddd; font-size: 0.9rem;">"{get_daily_wisdom()}"</div>
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
    city = st.text_input("Location", "London", label_visibility="collapsed", placeholder="Search City...")
    weather_api_key = os.getenv("WEATHER_API_KEY")
    
    if weather_api_key:
        try:
            # Fetch Current Weather
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
            curr_response = requests.get(current_url)
            curr_data = curr_response.json()
            
            if curr_response.status_code == 200:
                temp = curr_data['main']['temp']
                humidity = curr_data['main']['humidity']
                
                # Custom Metric Display
                m1, m2 = st.columns(2)
                m1.markdown(f"<h2 style='margin:0; color:#fff'>{temp:.1f}°</h2><span style='color:#ccff00'>▲ TEMP</span>", unsafe_allow_html=True)
                m2.markdown(f"<h2 style='margin:0; color:#fff'>{humidity}%</h2><span style='color:#ff9900'>▼ HUMIDITY</span>", unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Forecast Graph
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&units=metric"
                fore_response = requests.get(forecast_url)
                fore_data = fore_response.json()
                
                if fore_response.status_code == 200:
                    forecast_list = fore_data['list'][:8]
                    dates = [datetime.fromtimestamp(item['dt']) for item in forecast_list]
                    temps = [item['main']['temp'] for item in forecast_list]
                    
                    # Plotly Graph - Styled like the image
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
            else:
                st.error("City not found")
        except Exception:
            st.error("Connection Error")

# --- Column 2: News (Timeline Style) ---
with col2:
    st.markdown("### NEWS TIMELINE")
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if news_api_key:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}&pageSize=4"
        try:
            response = requests.get(url)
            data = response.json()
            articles = data.get('articles', [])
            
            for i, article in enumerate(articles):
                # Alternating Colors for "Pills"
                bg_color = "#ccff00" if i % 2 == 0 else "#ff9900"
                text_color = "#000"
                
                st.markdown(
                    f"""
                    <div style="background-color: #1a1a1a; padding: 10px; border-radius: 12px; margin-bottom: 10px; border-left: 5px solid {bg_color};">
                        <div style="font-size: 0.8rem; color: #888;">{article['source']['name']}</div>
                        <div style="font-weight: 600; font-size: 0.9rem;"><a href="{article['url']}" style="color: #fff; text-decoration: none;">{article['title'][:60]}...</a></div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        except Exception:
            st.error("News Unavailable")

# --- Column 3: Currency (Product/Bar Style) ---
with col3:
    st.markdown("### MARKET VALUE")
    
    usd_amount = st.number_input("USD", min_value=0.0, value=1.0, label_visibility="collapsed")
    inr_amount = usd_amount * 89.23
    
    st.markdown(f"<h1 style='color:#fff'>₹ {inr_amount:,.2f}</h1>", unsafe_allow_html=True)
    st.caption("Current Conversion Rate")
    
    # Pill Bar Chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['USD', 'INR'],
        y=[usd_amount, inr_amount/100], # Scaled
        marker_color=['#ccff00', '#ff9900'],
        text=['$', '₹'],
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
    # Round corners workaround for Plotly bars isn't perfect, but we keep it clean
    st.plotly_chart(fig, use_container_width=True)

# --- Bottom Section: AI Assistant ---
st.markdown("---")
st.markdown("### ▣ AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type a command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = model.generate_content(prompt)
        bot_response = response.text
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
    except Exception as e:
        st.error(f"Error: {e}")

