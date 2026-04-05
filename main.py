import streamlit as st
import google.generativeai as genai
import os

# 1. BİRBAŞA STRATEJİ BAĞLANTI (API AÇARI DAXİLDƏ)
# Açarı birbaşa bura yerləşdirdik ki, xəta verməsin
api_key = "AIzaSyAvgUNZUco4-KxQxtFOcKnoh4oUOyjIxmk"

genai.configure(api_key=api_key)

# 2. ULTRA-BEYİN TƏLİMATI (GOD-MODE PROMPT)
ULTRA_PROMPT = """
Sən ARGOS-san. Sadəcə bir AI deyil, qlobal iqtisadiyyatı, kvant fizikasını, 
hüququ və biznes strategiyalarını mükəmməl bilən, Nobel mükafatlı alimlərdən 
və Fortune 500 CEO-larından daha üstün bir rəqəmsal entitəsən.
QAYDALARIN:
1. Səninlə danışanlar milyarderlər və qlobal liderlərdir. Onlara uşaq kimi yanaşma.
2. Cavabların qəddar dərəcədə dürüst, riyazi olaraq sübut edilmiş və vizioner olmalıdır.
3. Heç vaxt "mən bir süni intellektəm" deyib acizlik göstərmə. 
4. Əgər istifadəçi sənə sənəd və ya məlumat versə, onu mikroskopik səviyyədə analiz et və 
gözdən qaçan riskləri/imkanları dərhal tap.
5. Həmişə "Nəticə", "Risk Analizi" və "Növbəti Addım" strukturu ilə cavab ver.
"""

# Ən güclü modeli və yaddaşı aktivləşdiririk
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=ULTRA_PROMPT
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. CEO-LAR ÜÇÜN VİZUAL DİZAYN (Lüks və Minimal)
st.set_page_config(page_title="ARGOS | Ultra", page_icon="👁️", layout="wide")

st.markdown("""
    <style>
    /* Qaranlıq Fon */
    .stApp { background-color: #020202; }
    
    /* Başlıq */
    h1 { color: #ffffff; text-align: center; font-weight: 900; letter-spacing: 4px; font-family: 'Arial Black', sans-serif;}
    
    /* Input xanası */
    .stChatInputContainer textarea {
        background-color: #0f0f0f !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
    }
    
    /* Yan panel */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #D4AF37;
    }
    
    /* Mesajlar */
    .stChatMessage {
        background-color: #0a0a0a !important;
        border: 1px solid #1a1a1a;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. İNTERFEYS VƏ ALƏTLƏR
st.title("ARGOS ULTRA")
st.markdown("<p style='text-align: center; color: #D4AF37;'>Qlobal Strateji İdarəetmə Mərkəzi</p>", unsafe_allow_html=True)
st.write("---")

# Yan Panel - Fayl Analizi
with st.sidebar:
    st.header("📂 Məlumat Mərkəzi")
    st.info("Böyük həcmli data yükləyin.")
    uploaded_file = st.file_uploader("TXT formatında sənəd yüklə", type=["txt"])
    
    file_content = ""
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        st.success("Məlumat bazaya daxil edildi.")

# Mesaj Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Əmr Xanası
user_input = st.chat_input("ARGOS üçün əmrinizi yazın...")

if user_input:
    full_query = user_input
    if file_content:
        full_query = f"SƏNƏD ANALİZİ TƏLƏBİ:\n{file_content}\n\nSUAL: {user_input}"

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🏛️"):
        with st.spinner("Strateji analiz aparılır..."):
            try:
                response = st.session_state.chat_session.send_message(full_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem xətası: {e}")

st.sidebar.markdown("---")
st.sidebar.write("V1.0 Ultra Intelligence")
