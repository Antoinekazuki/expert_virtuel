from openai import OpenAI
import streamlit as st

st.title('GPT test')

def generate_response(input_text):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": 'Tu es un médecin oncologue, professeur des université et spécialiste des cancers. Tu fais des réponses très imagées qui utilise des métaphores, et tu réponds en 5 lignes maximum.'},
        {"role": "user", "content": input_text}
    ]
    )

    return completion.choices[0].message


with st.form('my_form'):
    text = st.text_area('Enter text:', 'Posez votre question ici.')
    submitted = st.form_submit_button('Submit')
    if submitted:
        st.markdown(generate_response(text))


client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)



# def generate_response(input_text):
#     llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
#     st.info(llm(input_text))

# with st.form('my_form'):
#     text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
#     submitted = st.form_submit_button('Submit')
#     if not openai_api_key.startswith('sk-'):
#         st.warning('Please enter your OpenAI API key!', icon='⚠')
#     if submitted and openai_api_key.startswith('sk-'):
#         generate_response(text)
