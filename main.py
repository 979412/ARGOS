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
Heç vaxt "mən süni intellektəm" deyib bəhanə gətirmə. 
Hər suala bir mütəxəssis kimi yanaş və real həllər göstər.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_prompt
)

# 3. Vizual Dizayn (Victus-a yaraşan qara-qızılı stil)
st.set_page_config(page_title="ARGOS AI | Ultra Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextInput > div > div > input { background-color: #1a1c23; color: white; border: 1px solid #d4af37; }
    h1 { color: #d4af37; text-align: center; font-family: 'Playfair Display', serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ ARGOS AI: STRATEJİ KOMANDA MƏRKƏZİ")
st.write("---")

# 4. İstifadəçi ilə ünsiyyət
user_input = st.text_input("Biznes sualınızı daxil edin:", placeholder="Məsələn: Yeni bir startap üçün 100 günlük plan hazırla...")

if user_input:
    if not api_key:
        st.error("Xəta: .env faylında GOOGLE_API_KEY tapılmadı!")
    else:
        with st.spinner("Argos analiz edir..."):
            try:
                response = model.generate_content(user_input)
                st.subheader("Strateji Cavab:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Sistem xətası: {e}")

# Sidebar (Yan panel)
st.sidebar.title("Sistem Statusu")
st.sidebar.markdown("---")
st.sidebar.success("A-ZEKA-ULTRA V1.0 Aktivdir")
st.sidebar.info("Victus Engine üzərində işləyir.")
