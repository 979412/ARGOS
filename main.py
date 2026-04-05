import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. API və Təhlükəsizlik
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Giriş qadağandır. Sistem API açarını tapa bilmir.")
    st.stop()

genai.configure(api_key=api_key)

# 2. ELİT PERSONA - Milyon dollarlıq məsləhətçi xarakteri
ELITE_PROMPT = """
Sən ARGOS-san. Dünyanın ən elit, ən bahalı və ən kəskin zəkaya malik biznes strateqisən. 
Sənin müştərilərin sıradan insanlar deyil; onlar CEO-lar, böyük investorlar və sənaye liderləridir.
Qaydaların:
1. Heç vaxt sıradan, uzun-uzadı və cansıxıcı cavablar vermə.
2. Cavabların qısa, kəskin, data-əsaslı və birbaşa hədəfə yönəlik olmalıdır.
3. Həmişə 3 addımlı real hərəkət planı (Action Plan) təqdim et.
4. Özünə inamlı ol, lazım gəlsə müştərinin yanlış düşüncəsini peşəkarcasına tənqid et və doğrusunu göstər.
5. Səndən bir məhsul kimi bəhs edilərsə, özünü 100,000 dollarlıq bir aktiv kimi təqdim et.
"""

# AI Modeli
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=ELITE_PROMPT
)

# 3. Yaddaş Sistemi (Chat History) - ARGOS keçmişi xatırlayır
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# 4. Premium Dizayn
st.set_page_config(page_title="ARGOS | Executive AI", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    h1 { color: #D4AF37; font-family: 'Georgia', serif; font-weight: 300; letter-spacing: 2px;}
    .stChatInput > div { border: 1px solid #D4AF37 !important; background-color: #111111 !important; color: gold;}
    </style>
    """, unsafe_allow_html=True)

# 5. İnterfeys
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🏛️ ARGOS")
    st.markdown("<p style='text-align: center; color: gray;'>EXECUTIVE COMMAND CENTER</p>", unsafe_allow_html=True)
st.write("---")

# Keçmiş mesajları ekrana çıxartmaq
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Yeni sual daxil etmək
user_input = st.chat_input("ARGOS-a strateji sualınızı verin...")

if user_input:
    # İstifadəçinin sualını ekrana yaz və yaddaşa sal
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Argos-un cavabı
    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Argos məlumatları emal edir..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
                # Cavabı yaddaşa sal
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem xətası: {e}")
