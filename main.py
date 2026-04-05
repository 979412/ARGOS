import streamlit as st
import google.generativeai as genai
import os

# 1. STRATEJİ BAĞLANTI (MƏCBURİ REJİM)
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"

try:
    genai.configure(api_key=api_key)
    # Model adını tam formatda yazırıq ki, sistem çaşmasın
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Bağlantı xətası: {e}")

# 2. ULTRA PREMİUM QARA-QIZILI DİZAYN (CSS)
st.set_page_config(page_title="ARGOS ULTRA", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Arial Black'; letter-spacing: 3px; }
    .stChatInputContainer textarea { 
        background-color: #0a0a0a !important; 
        color: #D4AF37 !important; 
        border: 1px solid #D4AF37 !important; 
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

# 3. İNTERFEYS
st.markdown("<h1>🏛️ ARGOS ULTRA</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual Girişi
user_input = st.chat_input("Əmrinizi bura daxil edin...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("ARGOS düşünür..."):
            try:
                # Ən sadə və birbaşa metodla cavab alırıq
                response = model.generate_content(
                    user_input,
                    generation_config=genai.types.GenerationConfig(
                        candidate_count=1,
                        max_output_tokens=1000,
                        temperature=0.7
                    )
                )
                
                # Cavabı göstər
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Xəta mesajını daha detallı göstərək ki, nə baş verdiyini bilək
                st.error(f"Sistem xətası: {str(e)}")
                st.info("İpucu: 'pip install --upgrade google-generativeai' komandası ilə kitabxananı yeniləməyi yoxlayın.")

# Yan Panel
with st.sidebar:
    st.header("Sistem Statusu")
    st.success("Hazır və aktiv")
    st.info("Mühərrik: Gemini Pro (v1)")
