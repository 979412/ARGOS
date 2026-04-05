import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Təhlükəsizlik: .env faylından API açarını yükləyirik
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. AI Konfiqurasiyası
genai.configure(api_key=api_key)

# Canavar/İntellektual Persona Təlimatı
system_prompt = """
Sən ARGOS AI-sən. Dünyanın ən bahalı və ən ağıllı biznes məsləhətçisisən. 
İstifadəçiyə kəskin, dəqiq və strateji cavablar ver. 
Hər suala bir mütəxəssis kimi yanaş və real həllər göstər.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_prompt
)

# 3. Vizual Dizayn (Qara-qızılı premium stil)
st.set_page_config(page_title="ARGOS AI | Ultra Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput > div > div > input { background-color: #1a1c23; color: white; border: 1px solid #d4af37; }
    h1 { color: #d4af37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ ARGOS AI: STRATEJİ KOMANDA MƏRKƏZİ")
st.write("---")

user_input = st.text_input("Sualınızı bura daxil edin:", placeholder="Məsələn: Strateji plan hazırla...")

if user_input:
    if not api_key:
        st.error("Xəta: .env faylında API açarı tapılmadı!")
    else:
        with st.spinner("Argos analiz edir..."):
            try:
                response = model.generate_content(user_input)
                st.subheader("Strateji Analiz:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Sistem xətası: {e}")

st.sidebar.success("V1.0 Aktivdir")
