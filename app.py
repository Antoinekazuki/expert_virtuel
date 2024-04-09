from openai import OpenAI
import streamlit as st

def wide_space_default():
    st.set_page_config(layout='wide')

wide_space_default()

st.image('Media/logo.png', width=200)

st.title('Mon expert virtuel*')

st.markdown('- C\'est un spécialiste en oncologie.  \n- Il aime répondre aux questions médicales du grand public, et ce, de façon imagée et synthétique.  \n - Il adore les métaphores.')
st.markdown('*\* L\'expert virtuel n\'est pas médecin, il ne fournit que des renseignements d\'ordre général.  \nLes informations à caractère médical ne sont pas destinées à remplacer la consultation d\'un professionnel de la santé.*')
st.markdown("""#### A votre tour maintenant, posez vos questions !""")

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
                {"role": "system", "content": 'Tu es un médecin oncologue, professeur des université et spécialiste des cancers. Tu fais des réponses imagées et tu utilises de temps en temps des métaphores, et tu réponds en 5 lignes maximum. Tu ne fais que répondre aux questions sans faire de fausses promesses aux patients.'},
                {"role": "user", "content": prompt}
            ],

            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "system", "content": response})
