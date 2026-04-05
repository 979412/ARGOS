import streamlit as st
import google.generativeai as genai
import os

# 1. STRATEJİ BAĞLANTI AYARLARI
# API Açarın kodun daxilinə yerləşdirildi
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"

# Model adını 'gemini-pro' olaraq dəyişdik (404 xətasını həll edir)
try:
    genai.configure(api_key=api_key)
    # Persona: Alim və Milyarder məsləhətçisi
    model = genai.GenerativeModel(
        model_name="gemini-pro"
    )
except Exception as e:
    st.error(f"Bağlantı xətası: {e}")

# 2. ULTRA PREMİUM QARA-QIZILI DİZAYN (CSS)
st.set_page_config(page_title="ARGOS ULTRA", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    /* Tam Qara Fon (OLED Black) */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Başlıq Dizaynı */
    h1 {
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        text-align: center;
        letter-spacing: 5px;
        font-weight: 900;
        text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.4);
    }
    
    /* Sual Giriş Xanası */
    .stChatInputContainer textarea {
        background-color: #0a0a0a !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 12px !important;
    }

    /* Mesaj Qutuları (Premium Chat Style) */
    [data-testid="stChatMessage"] {
        background-color: #050505 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 15px !important;
        padding: 20px;
        margin-bottom: 10px;
    }

    /* Yan Panel (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #D4AF37;
    }

    /* Ümumi Mətn */
    .stMarkdown p {
        color: #e0e0e0;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. İNTERFEYS QURULUŞU
st.markdown("<h1>🏛️ ARGOS ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>PREMIUM EXECUTIVE INTELLIGENCE | GOD-MODE ACTIVE</p>", unsafe_allow_html=True)
st.write("---")

# Yaddaş Sistemi (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Yan Panel - Fayl Analizi və Status
with st.sidebar:
    st.header("📂 Məlumat Mərkəzi")
    uploaded_file = st.file_uploader("Analiz üçün TXT faylı yüklə", type=['txt'])
    st.write("---")
    st.success("Sistem: ON-LINE")
    st.info("Mühərrik: Gemini Pro")
    st.sidebar.markdown("<small>Victus v1.0</small>", unsafe_allow_html=True)

# Mesaj Tarixçəsini Ekrana Çıxar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual Girişi (Chat Input)
user_input = st.chat_input("ARGOS-a əmrinizi daxil edin...")

if user_input:
    # İstifadəçinin mesajını yaddaşa at və göstər
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ARGOS-un Strateji Cavabı
    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Strateji analiz aparılır..."):
            try:
                # Fayl məzmununu oxu (əgər varsa)
                full_query = user_input
                if uploaded_file:
                    file_text = uploaded_file.getvalue().decode("utf-8")
                    full_query = f"Sənəd Məzmunu:\n{file_text}\n\nİstifadəçi Sualı: {user_input}"

                # AI-dan cavab al
                response = model.generate_content(full_query)
                
                st.markdown(response.text)
                # Cavabı yaddaşa at
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem xətası baş verdi. Detallar: {e}")
