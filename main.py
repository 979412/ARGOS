import streamlit as st
import google.generativeai as genai
import os

# 1. STRATEJİ BAĞLANTI
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"
genai.configure(api_key=api_key)

# 2. YENİ İŞIQLI VƏ PREMİUM DİZAYN (Gümüşü-Mavi)
st.set_page_config(page_title="ARGOS | Executive", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    /* Fon: İşıqlı gümüşü/boz gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #1a1a1a;
    }
    
    /* Başlıq: Tünd göy və ciddi */
    h1 {
        color: #1e3a8a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: -50px;
    }

    /* Giriş Xanası: Təmiz ağ və kölgəli */
    .stChatInputContainer textarea {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 2px solid #1e3a8a !important;
        border-radius: 15px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* Mesaj Qutuları */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        border: 1px solid #d1d5db !important;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    /* Yan Panel */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #1e3a8a;
    }

    /* Mətn rəngləri */
    .stMarkdown p {
        color: #2d3748;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MODELİN YÜKLƏNMƏSİ
@st.cache_resource
def load_model():
    # 404 xətası almamamaq üçün birbaşa ən stabil modeli seçirik
    return genai.GenerativeModel('gemini-pro')

model = load_model()

# 4. İNTERFEYS QURULUŞU
st.markdown("<h1>🏛️ ARGOS EXECUTIVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a5568;'>ADVANCED STRATEGIC INTELLIGENCE</p>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual Girişi
user_input = st.chat_input("Strategiyanızı bura daxil edin...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Analiz olunur..."):
            try:
                # Cavabı alırıq
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem xətası: {e}")

# Yan Panel
with st.sidebar:
    st.header("📊 Sistem Paneli")
    st.write("İstifadəçi: **Admin**")
    st.write("Vəziyyət: **Aktiv**")
    st.write("Mühərrik: **Gemini Pro**")
    st.write("---")
    if st.button("Söhbəti Təmizlə"):
        st.session_state.messages = []
        st.rerun()
