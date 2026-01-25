import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import streamlit as st
from dotenv import load_dotenv
from rag_chain import build_chain

load_dotenv()

SAMPLE_QUESTIONS = [
    "What all topics you can help?",
    "My queries will be answered by which LLM?",
    "Weather my data saved into the server",
    "I need to pay using the credit card?",
    "DOes it has subscription plans for using it?",
    "Why is my response takes time?",
    "How can i get most out of this system?",
]

st.set_page_config(
    page_title="General Support Chat",
    page_icon="common\neural-network-stroke-rounded.png",
    layout="centered",
)

@st.cache_resource
def get_chain():
    return build_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📡 General Support")
    st.caption("Powered by RAG · Qwen3-32B on Groq")
    st.divider()

    st.markdown("***Sample questions***")
    st.caption("Click one to send it instantly.")
    for q in SAMPLE_QUESTIONS:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []

# ── Main ─────────────────────────────────────────────────────────────────────
st.title("General SUpport Assistant")
st.caption("Ask me about your question — physology, legal, medical, and more.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Describe your issue…")
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        chain = get_chain()
        response = st.write_stream(chain.stream(question))

    st.session_state.messages.append({"role": "assistant", "content": response})
