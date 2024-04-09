from openai import OpenAI
import streamlit as st

st.image('Media/logo.png', width=200)

st.title('Mon médecin virtuel')

st.markdown('- Médecin spécialisé en oncologie.  \n- Il aime répondre aux questions médicales du grand public, et ce, de façon imagée et synthétique.  \n - Il adore les métaphores.')

st.markdown("""#### A votre tour maintenant, posez vos questions au médecin virtuel !""")
st.markdown('Quelques exemples :  \n*Peut-on guérir de tous les cancers ?*  \n*Qu\'est-ce qui distingue une cellule saine d\'une cellule métastatique ?*')

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question dans ce chat"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("system", avatar='🧑🏻‍⚕️'):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],

            messages=[
                {"role": "system", "content": 'Tu es un médecin oncologue, professeur des université et spécialiste des cancers. Tu fais des réponses imagées et tu utilises de temps en temps des métaphores, et tu réponds en 5 lignes maximum.'},
                {"role": "user", "content": prompt}
            ],

            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "system", "content": response})
