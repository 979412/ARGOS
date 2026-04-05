import streamlit as st
import google.generativeai as genai
import os

# 1. BAĞLANTI AYARLARI
# QEYD: GitHub-a qoymazdan əvvəl açarı bura yazdığından əmin ol.
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"

# Model adını ən stabil versiya ilə əvəzlədik (v1beta xətası verməməsi üçün)
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Əgər yenə 404 versə, bura "gemini-pro" yaz
        system_instruction="""
        Sən ARGOS-san. Dünyanın ən bahalı biznes məsləhətçisisən. 
        Məntiqin alim səviyyəsindən yuxarıdır. 
        Kəskin, strateji və milyarderlərin anlayacağı dildə cavablar ver.
        """
    )
except Exception as e:
    st.error(f"Bağlantı xətası: {e}")

# 2. ULTRA PREMİUM QARA DİZAYN (CSS)
st.set_page_config(page_title="ARGOS ULTRA", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    /* Tam Qara Fon */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Başlıq və Mətnlər */
    h1 {
        color: #D4AF37;
        font-family: 'Playfair Display', serif;
        text-align: center;
        letter-spacing: 5px;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.5);
    }
    
    /* Giriş Xanası (Input) */
    .stChatInputContainer textarea {
        background-color: #0a0a0a !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }

    /* Mesaj Qutuları */
    [data-testid="stChatMessage"] {
        background-color: #050505 !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 20px !important;
        padding: 15px;
    }

    /* Yan Panel */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #D4AF37;
    }

    /* Düymələr və Proqres */
    .stSpinner > div > div {
        border-top-color: #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. İNTERFEYS
st.markdown("<h1>🏛️ ARGOS ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>PREMIUM EXECUTIVE INTELLIGENCE</p>", unsafe_allow_html=True)
st.write("---")

# Yaddaş Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Sənəd Yükləmə (Sidebar)
with st.sidebar:
    st.header("📂 Data Analiz")
    uploaded_file = st.file_uploader("TXT faylı yüklə", type=['txt'])
    st.write("---")
    st.success("Sistem: Aktiv")
    st.info("Model: ARGOS V2.0")

# Mesajları Göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual Girişi
user_input = st.chat_input("Əmrinizi bura daxil edin...")

if user_input:
    # İstifadəçinin mesajını göstər
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ARGOS Analizi
    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Kvant Analizi aparılır..."):
            try:
                # Fayl məlumatı varsa əlavə et
                context = ""
                if uploaded_file:
                    context = f"SƏNƏD: {uploaded_file.getvalue().decode()}\n\n"
                
                response = st.session_state.chat.send_message(context + user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem xətası: {e}. Zəhmət olmasa model adını 'gemini-pro' olaraq dəyişib yoxlayın.")
