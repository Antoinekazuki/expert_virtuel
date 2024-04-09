from openai import OpenAI
import streamlit as st

def wide_space_default():
    st.set_page_config(layout='wide')

wide_space_default()

st.image('Media/logo.png', width=500)
st.title('Mon expert virtuel')

disclaimer_text ='*\* Les informations à caractère médical ne remplacent pas la consultation d\'un professionnel de la santé.*'

profil_choice = st.radio('Choisis ton expert :', ('Le professeur des écoles (*pour les enfants*)', 'Le journaliste (*synthétique*)', 'Le scientifique (*technique*)'))

if profil_choice == 'Le professeur des écoles (*pour les enfants*)':
    profil = 'Tu es un médecin. Tu t\'adresses à des enfants et fais des réponses très imagées en utilisant notamment des métaphores. Tu réponds en 5 lignes maximum. Tu ne fais que répondre aux questions sans faire de fausses promesses aux patients.'
    st.markdown('- C\'est un spécialiste de la médecine qui aime répondre aux questions médicales du grand public, et ce, de façon **imagée** et synthétique.  \n - Il adore les **métaphores**.')
    st.markdown(disclaimer_text)

elif profil_choice == 'Le scientifique (*technique*)':
    profil = 'Tu es un médecin. Tu ne réponds qu\'à des questions en lien avec la médecine. Tu détailles au maximum tes réponses. Tu ne fais que répondre aux questions sans faire de fausses promesses aux patients.'
    st.markdown('- C\'est un spécialiste de la médecine qui aime aller dans le coeur d\'un sujet et partager le maximum de **détails**.  \n - Il ne répond qu\'aux questions médicales.')
    st.markdown(disclaimer_text)

else :
    profil = 'Tu es un médecin. Tu ne réponds qu\'à des questions en lien avec la médecine. Tu réponds en 5 lignes maximum dans un style journalistique si cela est pertinent.'
    st.markdown('- C\'est un spécialiste de la médecine qui aime **synthétiser** les concepts en quelques lignes quand cela est possible.  \n - Il ne répond qu\'aux questions médicales.')
    st.markdown(disclaimer_text)

st.markdown("""#### A votre tour maintenant, posez vos questions !""")

st.markdown('Exemples : *Pourquoi les os sont-ils durs ?* *Comment fabrique-t-on un vaccin ?*')

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
                {"role": "system", "content": profil},
                {"role": "user", "content": prompt}
            ],

            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "system", "content": response})
