import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. MÜTƏLƏQ TƏHLÜKƏSİZLİK VƏ BAĞLANTI
base_path = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_path, '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ KRİTİK XƏTA: API açarı tapılmadı. Sistem bloklandı.")
    st.stop()

genai.configure(api_key=api_key)

# 2. ULTRA-BEYİN TƏLİMATI (GOD-MODE PROMPT)
# Bu hissə ARGOS-un necə düşünəcəyini müəyyən edir.
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
    .stApp { background-color: #020202; }
    h1 { color: #ffffff; text-align: center; font-weight: 900; letter-spacing: 4px; font-family: 'Arial Black', sans-serif;}
    .stTextInput input { background-color: #0f0f0f !important; color: #fff !important; border: 1px solid #333 !important; }
    .stTextInput input:focus { border: 1px solid #D4AF37 !important; }
    .stFileUploader { background-color: #0a0a0a; border: 1px dashed #D4AF37; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 4. İNTERFEYS VƏ ALƏTLƏR
st.title("ARGOS ULTRA")
st.markdown("<p style='text-align: center; color: #D4AF37;'>Qlobal Strateji İdarəetmə Mərkəzi</p>", unsafe_allow_html=True)
st.write("---")

# Yan Panel - Biznesmenlər üçün Sənəd Yükləmə (Fayl Analizi)
with st.sidebar:
    st.header("📂 Məlumat Mərkəzi")
    st.info("ARGOS böyük məlumatları emal edə bilər.")
    uploaded_file = st.file_uploader("Hesabat, məqalə və ya data (TXT formatında) yüklə", type=["txt"])
    
    file_content = ""
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        st.success("Məlumat bazaya əlavə edildi! İndi bu fayl haqqında sual verə bilərsiniz.")

# Chat Tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CEO-nun Əmrləri (Sual Xanası)
user_input = st.chat_input("ARGOS, məlumatları analiz et və əmrini gözləyirəm...")

if user_input:
    # Əgər fayl yüklənibsə, suala o faylın məzmununu da gizlicə əlavə edirik ki, AI oxusun
    full_query = user_input
    if file_content:
        full_query = f"Yüklənmiş sənədin məzmunu: \n{file_content}\n\nİstifadəçinin Sualı: {user_input}"

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="👁️"):
        with st.spinner("Kvant Analizi aparılır..."):
            try:
                response = st.session_state.chat_session.send_message(full_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistem stabilizasiya xətası: {e}")
