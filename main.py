import streamlit as st
import google.generativeai as genai
import os

# 1. STRATEJİ BAĞLANTI (BİRBAŞA REJİM)
# API Açarın (Dəyişməmişik, olduğu kimi qalır)
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"

# Google AI Konfiqurasiyası
genai.configure(api_key=api_key)

# 2. ULTRA PREMİUM DİZAYN (CSS)
st.set_page_config(page_title="ARGOS ULTRA", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Arial Black'; letter-spacing: 5px; }
    .stChatInputContainer textarea { 
        background-color: #0a0a0a !important; 
        color: #D4AF37 !important; 
        border: 1px solid #D4AF37 !important; 
        border-radius: 10px;
    }
    [data-testid="stChatMessage"] { 
        background-color: #050505 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 15px !important; 
    }
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 1px solid #D4AF37; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MODELİN HAZIRLANMASI (XƏTASIZ VERSİYA)
@st.cache_resource
def load_argos_model():
    # Biz burada 1.5-flash modelini çağırırıq
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Sən ARGOS-san. Dahi strateq və alimsən. Cavabların qısa, kəskin və elit olmalıdır."
    )

try:
    model = load_argos_model()
except:
    # Əgər 1.5-flash işləməsə, ehtiyat olaraq gemini-pro-nu işə salırıq
    model = genai.GenerativeModel('gemini-pro')

# 4. İNTERFEYS
st.markdown("<h1>🏛️ ARGOS ULTRA</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Əmr Girişi
user_input = st.chat_input("Əmrinizi bura daxil edin...")

if user_input:
    # İstifadəçi mesajını göstər
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ARGOS Cavabı
    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Strateji analiz..."):
            try:
                # Sualı göndər
                response = model.generate_content(user_input)
                
                # Cavabı göstər və yaddaşa yaz
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Əgər hələ də model tapılmasa, bu dəfə çox konkret xəta göstərəcək
                st.error(f"Sistem xətası: {str(e)}")
                st.info("İpucu: API açarının aktivliyini yoxlayın.")

# Yan Panel
with st.sidebar:
    st.title("Sistem")
    st.success("Kitabxanalar: OK (0.8.6)")
    st.info("Mühərrik: ARGOS Engine")
