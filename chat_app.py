import streamlit as st
import requests

st.title("🧠 Andy 的 Qwen1.5B 小学奥数专家")

VLLM_API_URL = "https://although-symposium-prisoners-incidence.trycloudflare.com/v1/chat/completions"
#VLLM_API_URL = "http://localhost:8000/v1/chat/completions"

MODEL_PATH = "/work/nvme/bdsf/jchen73_data/ckpts/gsm8k_1.5B_ckpt/global_step_175/policy/hf_model"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("出个题考考我吧！(记得加上暗号 Let us think step by step...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        payload = {
            "model": MODEL_PATH,
            "messages": st.session_state.messages,
            "max_tokens": 1024,
            "temperature": 0.0
        }
        
        try:
            response = requests.post(VLLM_API_URL, json=payload).json()
            full_response = response["choices"][0]["message"]["content"]
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"连接大模型失败，请检查 SSH 端口映射是否开启: {e}")
