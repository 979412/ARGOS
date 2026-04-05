import streamlit as st
import google.generativeai as genai

# 1. STRATEJİ BAĞLANTI (MƏCBURİ V1)
# API Açarını bura birbaşa qoyuruq
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"
genai.configure(api_key=api_key)

# 2. MODELİ SİYAHIDAN AVTOMATİK SEÇƏN FUNKSİYA
# Bu hissə 404 xətasını keçmək üçündür
def get_model():
    try:
        # Ən yeni model
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        # Əgər o yoxdursa, ən köhnə və stabil model
        return genai.GenerativeModel('gemini-pro')

model = get_model()

# 3. PREMİUM İŞIQLI DİZAYN (Apple Style)
st.set_page_config(page_title="ARGOS | Executive", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #FFFFFF 0%, #F5F7F9 100%); color: #1C1C1E; }
    h1 { color: #003366; text-align: center; font-family: 'Helvetica'; font-weight: 800; }
    [data-testid="stChatMessage"] { 
        background-color: #FFFFFF !important; 
        border: 1px solid #E5E5EA !important; 
        border-radius: 20px !important; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stChatInputContainer textarea { border-radius: 20px !important; border: 1px solid #003366 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. İNTERFEYS
st.markdown("<h1>🏛️ ARGOS EXECUTIVE</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
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
        with st.spinner("Analiz olunur..."):
            try:
                # 404-ü keçmək üçün ən sadə çağırış
                response = model.generate_content(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Əgər yenə 404 versə, deməli açarın özündə problem var
                st.error(f"Sistem hələ tam aktiv deyil: {str(e)}")
                st.info("💡 Məsləhət: Google AI Studio-dan yeni bir API KEY alıb yoxlayın.")

# Yan Panel
with st.sidebar:
    st.header("Sistem Statusu")
    st.success("Hər şey qaydasındadır")
    if st.button("Söhbəti Təmizlə"):
        st.session_state.messages = []
        st.rerun()
