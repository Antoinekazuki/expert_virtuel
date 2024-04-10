############### Paramétrages ###############

## Imports
from openai import OpenAI
import streamlit as st

## Force l'affichage plein écran sur Streamlit
def wide_space_default():
    st.set_page_config(layout='wide')
wide_space_default()

## Variables diverses et contenus des messages
message_action_adulte = '## 2. A votre tour maintenant, vous pouvez lui poser vos questions !'
message_action_enfant = '## 2. Maintenant, pose lui toutes tes questions !'
disclaimer_text ='*\* Les informations à caractère médical ne remplacent pas la consultation d\'un professionnel de la santé.*'
exemples_text_enfant = 'Exemples : *Pourquoi les os sont-ils durs ?* *c\'est quoi un virus ?*'
exemples_text_adulte = 'Exemples : *Tumeur bénigne d\'une tumeur maligne, quelle différence ?* *Comment fabrique-t-on un vaccin ?*'
profil_choice = None

############### Paramétrages ###############

############### Sélection du profil d'expert ###############

## Logo
st.image('Media/logo.png', width=80)

## Texte 1
st.markdown('''
             ## 1. Choisi ton expert :
             ''')

## Choix du profil d'expert
profil_choice = st.radio('', ('Le professeur des écoles (*pour les enfants*)', 'Le journaliste (*synthétique*)', 'Le scientifique (*technique*)'), index=None, label_visibility="collapsed")

## Affichage des caractéristiques du profil d'expert et affichage exemples

# 'Le professeur des écoles'
if profil_choice == 'Le professeur des écoles (*pour les enfants*)':
    profil = 'Tu es un médecin. Tu t\'adresses à des enfants et fais des réponses très imagées en utilisant notamment des métaphores. Tu réponds en 5 lignes maximum. Tu ne fais que répondre aux questions sans faire de fausses promesses aux patients.'
    st.markdown('- C\'est un spécialiste de la médecine* qui aime répondre aux questions médicales du grand public, et ce, de façon **imagée** et synthétique.  \n - Il adore les **métaphores**.')
    st.markdown(disclaimer_text)
    st.markdown(message_action_enfant)
    st.markdown(exemples_text_enfant)

# 'Le scientifique'
elif profil_choice == 'Le scientifique (*technique*)':
    profil = 'Tu es un médecin. Tu ne réponds qu\'à des questions en lien avec la médecine. Tu détailles au maximum tes réponses. Tu ne fais que répondre aux questions sans faire de fausses promesses aux patients.'
    st.markdown('- C\'est un spécialiste de la médecine* qui aime aller dans le coeur d\'un sujet et partager le maximum de **détails**.  \n - Il ne répond qu\'aux questions médicales.')
    st.markdown(disclaimer_text)
    st.markdown(message_action_adulte)
    st.markdown(exemples_text_adulte)

# 'Le journaliste'
elif profil_choice == 'Le journaliste (*synthétique*)':
    profil = 'Tu es un médecin. Tu ne réponds qu\'à des questions en lien avec la médecine. Tu réponds en 5 lignes maximum dans un style journalistique si cela est pertinent.'
    st.markdown('- C\'est un spécialiste de la médecine* qui aime **synthétiser** les concepts en quelques lignes quand cela est possible.  \n - Il ne répond qu\'aux questions médicales.')
    st.markdown(disclaimer_text)
    st.markdown(message_action_adulte)
    st.markdown(exemples_text_adulte)

############### Sélection du profil d'expert ###############

############### Chat ###############
# Pas d'affichage sans sélection d'un profil expert
if profil_choice is not None:

    # Création instance OpenAI
    client = OpenAI()

    # Sélection du modèle 'gpt-3.5-turbo'
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Affichage des messages et du rôle
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Posez votre question dans ce chat"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar='🧑🏼'):
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

############### Chat ###############
