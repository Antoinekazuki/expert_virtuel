from openai import OpenAI
import streamlit as st

st.title('Je discute avec mon PDS')

# Set OpenAI API key from Streamlit secrets
client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],

            messages=[
                {"role": "system", "content": 'Tu es un médecin oncologue, professeur des université et spécialiste des cancers. Tu fais des réponses très imagées qui utilise des métaphores, et tu réponds en 5 lignes maximum.'},
                {"role": "user", "content": prompt}
            ],

            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
