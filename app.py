import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="MindMate AI", page_icon="💚", layout="wide")
st.title("💚 MindMate AI: Teman Cerita & Pendamping Kesehatan Mental")
st.caption("Aplikasi AI Pertolongan Pertama Emosional | Final Project LLM")

st.info("⚠️ **Penting:** MindMate AI adalah asisten virtual pertolongan pertama emosional, bukan pengganti psikolog/psikiater. Jika butuh bantuan darurat, hubungi Hotline Kesehatan Mental Indonesia: **119 (Ext. 8)**.")

# Sidebar Pengaturan Parameter
with st.sidebar:
    st.header("⚙️ Pengaturan Pendamping")
    api_key = st.text_input("Gemini API Key:", type="password", help="Masukkan API Key dari Google AI Studio")
    
    mode_option = st.selectbox("Mode Pendampingan:", [
        "Empathetic Listener (Teman Curhat)",
        "Mindfulness & Calming (Penenangan Diri)",
        "Professional Referral (Arahkan ke Ahli)"
    ])
    
    temperature = st.slider("Temperature (Empati/Variasi):", 0.1, 0.8, 0.5)
    
    if st.button("Hapus Riwayat Curhat"):
        st.session_state.messages = []
        st.rerun()

# Instruksi Sistem
system_instructions = {
    "Empathetic Listener (Teman Curhat)": "Anda adalah MindMate, pendamping kesehatan mental yang empati dan hangat. Dengarkan curhat pengguna tanpa menghakimi. JANGAN beri diagnosis medis. Ingatkan secara halus jika mereka butuh konsultasi ke Psikolog/Psikiater.",
    "Mindfulness & Calming (Penenangan Diri)": "Anda adalah pemandu relaksasi. Bantu pengguna mengurangi cemas dengan teknik pernapasan atau grounding exercise sederhana.",
    "Professional Referral (Arahkan ke Ahli)": "Bantu pengguna memahami cara berkonsultasi ke Psikolog atau Psikiater (via BPJS/Puskesmas/Telemedicine) dan beri dorongan agar tidak ragu ke ahli."
}

# Session State Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Proses Chat
if prompt := st.chat_input("Tuliskan perasaanmu hari ini..."):
    if not api_key:
        st.error("Masukkan Gemini API Key di sidebar kiri terlebih dahulu!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"temperature": temperature},
            system_instruction=system_instructions[mode_option]
        )
        history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
        chat = model.start_chat(history=history)

        with st.chat_message("assistant"):
            response = chat.send_message(prompt)
            st.markdown(response.text)

        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
