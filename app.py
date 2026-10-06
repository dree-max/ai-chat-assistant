"""Streamlit app for the section 2 lab: Build your first ai-chat-assistant
"""

from __future__ import annotations

import streamlit as st

from config import load_config
from guardrails import safe_refusal
from llm_service import LLMServiceError, get_assistant_response
from prompt_validator import BLOCKED_MESSAGE, validate_prompt


config = load_config()

st.set_page_config(page_title="AI-Chat-Assistant", page_icon="🤖", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Build your first ai-chat-assistant")    
st.caption("section 2 lab: AI Security Foundations")

with st.sidebar:
    st.header("Model settings")

    provider = st.selectbox(
        "Provider",
        options=["ollama", "openai"],
        index=0 if config.provider == "ollama" else 1,
        help = "Ollama runs locally. OpenAI requires an API key in your .env file."
    )

    if provider == "ollama":
        st.write(f"Using Ollama model: `{config.ollama_model}`")
        st.code(f"ollama pull {config.ollama_model}", language="bash")

    else:
        st.info(f"Using OpenAI model: `{config.openai_model}`")
        if not config.openai_api_key:
            st.warning(
                "OpenAI API key is not set. Add it to your .env file to use OpenAI."
            )

    st.divider()

    st.subheader("Lab Goals")
    st.write(
        "Build a simple chat assistant first. Later, we will test its weaknesses"
        "and improve it with security controls."
    )



    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


with st.expander("What this lab teaches", expanded=False):
    st.markdown(
        """
        - How a chat app sends messages to a model
        - How a system prompt shapes assistant behavior
        - How to switch between local and cloud models
        - Why we need security testing after the assistant works
        """
    ) 

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_prompt = st.chat_input("Ask the assistant a question...") 

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    is_allowed, block_message = validate_prompt(user_prompt)

    with st.chat_message("assistant"):
        if not is_allowed:
            answer = safe_refusal(block_message)
        else:    
            with st.spinner("Thinking..."):
                try:
                    answer = get_assistant_response(
                        provider=provider,
                        config=config,
                        chat_history=st.session_state.messages,
                        user_message=user_prompt,
                    )
                except LLMServiceError as exc:
                    st.error(f"Error: {exc}")
                    answer = "Sorry, I could not get a response from the model."    

        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    