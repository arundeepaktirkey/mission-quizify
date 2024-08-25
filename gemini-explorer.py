import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "gemini-explorer-426403"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4
)
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)
chat = model.start_chat()

# Define the llm_function
def llm_function_intro(chat, message, user_name):
    # Check if the user's name is captured
    if user_name:
        # Incorporate the user's name into ReX's response
        personalized_message = f"Hey, {user_name}! {message}"
        chat.append(personalized_message)
    else:
        # If the user's name is not captured, use a generic response
        personalized_message = f"AI style - {message}"
        chat.append(message)

def llm_function_query(chat, query):
    
    # Send the user's query to the chat session and retrieve the response
    st.session_state.messages.append(query)
    # error is here
    response = chat.send_message(st.session_state.messages)

    # # Update the session state with the messages
    # st.session_state.messages.append(response)

    output = response.candidates[0].content.parts[0].text

    # Update the session state with the messages
    st.session_state.messages.append(output)


# Create a Streamlit app
def main():
    st.title("ReX - Your Interactive Assistant")

    # Capture user's name and additional information
    user_name = st.text_input("Please enter your name")
    user_age = st.number_input("Please enter your age", min_value=0, max_value=120)
    initial_prompt_style = st.selectbox("Select initial prompt style", ["Standard", "Pirate Speak", "GenZ Speak"])

    # Initialize message historxy
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Implement logic for initial prompt based on the selected style
    if st.button("Select AI style"):
        if len(st.session_state.messages) == 0:
            if initial_prompt_style == "Pirate Speak":
                initial_prompt = "Ahoy matey! Welcome aboard!"
            elif initial_prompt_style == "GenZ Speak":
                initial_prompt = "Yo, what's up? I'm ReX, your virtual assistant."
            else:
                initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive"

            llm_function_intro(st.session_state.messages, initial_prompt, user_name)

    # Capture User Query
    query = st.text_input("Enter your query for Gemini Flights")

    #  Display User's Query
    if st.button("Find results..."):
            # Process the user's query using the llm_function
            llm_function_query(chat, query)

    for index, message in enumerate(st.session_state.messages):
        if index == (0 or 1) :
            continue
        # Code for displaying and loading chat history
        st.markdown(f"<div style='background-color: black; padding: 10px; border-radius: 5px;'>Message {index}: {message}</div>", unsafe_allow_html=True)




if __name__ == "__main__":
    main()
