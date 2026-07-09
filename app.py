# app.py

import streamlit as st
from groq import Groq
#==========================
#PAGE CONFIG
#===========================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# =========================
# CUSTOM CSS & UI OVERHAUL
# =========================
custom_css = """
<style>
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean up the padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom header styling */
    .custom-title {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 0px;
    }
    .custom-subtitle {
        text-align: center;
        font-size: 0.9rem;
        color: #888;
        margin-bottom: 2rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h2 class='custom-title'>🤖 Peak Solution AI</h2>", unsafe_allow_html=True)
st.markdown("<p class='custom-subtitle'>Powered by Groq + Llama 3.1</p>", unsafe_allow_html=True)

# =========================
# GROQ API KEY
# =========================
# Option 1:
# Put your key directly (NOT recommended for production)
client = Groq(api_key="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")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# =========================
# DISPLAY CHAT HISTORY
# =========================
for message in st.session_state.messages[1:]:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# =========================
# USER INPUT
# =========================
prompt = st.chat_input("Ask something...")

if prompt:

    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # =========================
    # AI RESPONSE
    # =========================
    with st.chat_message("assistant", avatar="🤖"):

        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True
        )

        for chunk in stream:

            content = chunk.choices[0].delta.content

            if content:
                full_response += content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
