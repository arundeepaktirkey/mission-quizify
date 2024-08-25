import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "gemini-explorer-426403"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature= 0.4,
    top_k=10
)

model = GenerativeModel(
    model_name= "gemini-pro",
    generation_config= config
)

chat = model.start_chat()

def llm_function(chat:ChatSession, query):
    response = chat.send_message(content=query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)
    
    st.session_state.messages.append(
        {
            "role":"user",
            "content":query
        }
    )
    st.session_state.messages.append(
        {
            "role":"model",
            "content":output
        }
    )

st.title("Gemini Explorer")
if "messages" not in st.session_state:
    st.session_state.messages = []

for index, message in enumerate(st.session_state.messages):
    content = Content(
        role= message["role"],
        parts= [Part.from_text(message["content"])]
    )
    chat.history.append(content)

if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself saying 'Hi, Welcome to ReX'"
    llm_function(chat, initial_prompt)

query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)