import streamlit as st
import google.generativeai as genai

# 1. KONFİQURASİYA (Məcburi Bağlantı)
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"
genai.configure(api_key=api_key)

# Modelin adını və versiyasını dəqiq təyin edirik ki, 404 verməsin
try:
    # Biz burada 'gemini-1.5-flash' istifadə edirik, çünki ən yeni və sürətlisidir
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    # Əgər yuxarıdakı alınmasa, köhnə amma stabil 'gemini-pro' modelinə keçir
    model = genai.GenerativeModel('gemini-pro')

# 2. PREMİUM İŞIQLI DİZAYN (Qara deyil!)
st.set_page_config(page_title="ARGOS EXECUTIVE", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    /* Fon: Təmiz Gümüşü və Ağ gradient */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F2F5 100%);
        color: #1C1C1E;
    }
    
    /* Başlıq: Professional Tünd Göy */
    h1 {
        color: #003366;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        text-align: center;
        padding-top: 20px;
    }

    /* Mesaj Qutuları: Apple tərzi kölgəli ağ */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }

    /* Sual Girişi (Chat Input) */
    .stChatInputContainer textarea {
        background-color: #F2F2F7 !important;
        color: #1C1C1E !important;
        border-radius: 20px !important;
        border: 1px solid #D1D1D6 !important;
    }

    /* Yan Panel */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #D1D1D6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. İNTERFEYS
st.markdown("<h1>🏛️ ARGOS EXECUTIVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8E8E93;'>STRATEJİ ANALİZ VƏ İDARƏETMƏ SİSTEMİ</p>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sual Girişi
user_input = st.chat_input("Sualınızı və ya əmrinizi daxil edin...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Analiz edilir..."):
            try:
                # 404 xətasını keçmək üçün birbaşa model çağırışı
                response = model.generate_content(user_input)
                
                # Cavabı göstər
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Əgər hələ də xəta çıxarsa, bu dəfə çox spesifik göstərsin
                st.error(f"Bağlantı xətası: {str(e)}")
                st.info("İpucu: İnternet bağlantınızı və API açarını yenidən yoxlayın.")

# Yan Panel - Status
with st.sidebar:
    st.header("⚙️ Sistem")
    st.success("Status: ON-LINE")
    st.write("İstifadəçi: **Mİkay**")
    if st.button("Söhbəti Təmizlə"):
        st.session_state.messages = []
        st.rerun()
