import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Konfiqurasiya və Açarın Yüklənməsi
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Səhifə Ayarları (Mənim stilimdə)
st.set_page_config(page_title="ARGOS AI | Executive", page_icon="🏛️", layout="wide")

# CSS: Dizaynı "Canavar" səviyyəsinə qaldırırıq
st.markdown("""
    <style>
    /* Ümumi Fon */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        color: #e0e0e0;
    }
    
    /* Başlıq Dizaynı */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(#D4AF37, #C0C0C0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
    }

    /* Giriş Xanası (Input) */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    section[data-testid="stChatInput"] {
        border-radius: 15px;
        border: 1px solid #D4AF37 !important;
        background-color: #111 !important;
    }

    /* Mesaj Qovucuqları */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin-bottom: 10px;
        border: 0.5px solid rgba(212, 175, 55, 0.2);
    }

    /* Yan Panel (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #222;
    }

    /* Error Mesajı (Custom Style) */
    .stAlert {
        background-color: rgba(255, 75, 75, 0.1);
        color: #ff4b4b;
        border: 1px solid #ff4b4b;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. AI Modeli Ayarı
if api_key:
    genai.configure(api_key=api_key)
    # Elit Strateq Personası
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Sən ARGOS AI-sən. Kəskin, dahi və strateji məsləhətçisən. Cavabların qısa, baha və birbaşa gəlir gətirən olmalıdır."
    )
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    if "messages" not in st.session_state:
        st.session_state.messages = []
else:
    st.error("⚠️ SİSTEM XƏTASI: .env faylında API açarı tapılmadı!")
    st.stop()

# 4. İnterfeys Elementləri
st.markdown("<h1>🏛️ ARGOS AI: STRATEJİ KOMANDA MƏRKƏZİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>V1.0 ULTRA INTELLIGENCE ACTIVE</p>", unsafe_allow_html=True)
st.write("---")

# Chat Tarixçəsini Göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual Daxil Etmə (Chat Input)
user_query = st.chat_input("Sualınızı bura daxil edin...")

if user_query:
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Argos-un cavabı
    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Analiz edilir..."):
            try:
                response = st.session_state.chat_session.send_message(user_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta: {e}")

# Sidebar
st.sidebar.title("Sistem Statusu")
st.sidebar.success("✅ Canavar Aktivdir")
st.sidebar.markdown("---")
st.sidebar.info("Bu tətbiq HP Victus üzərində ARGOS mühərriki ilə işləyir.")
