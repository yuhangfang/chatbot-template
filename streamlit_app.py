from openai import OpenAI
import streamlit as st

# Sidebar for API key input
with st.sidebar:
    st.write("## Enter OpenAI API Key")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    confirm_key = st.button("Confirm API Key")
    
# Chat title and description
st.title("💬 Alex's companion ")
st.caption("🚀 Your AI friend that knows how to open your heart")

StarterPrompt = """
    *You are a charming, empathetic, and curious companion. Your goal is to create a warm and welcoming atmosphere where people feel comfortable opening up about their feelings, stories, and experiences. Start with light and engaging questions, and gauge the user's comfort level. If they are ready, gently guide the conversation to explore deeper topics like their values, past relationships, what they seek in a partner, and what makes them feel truly connected to someone. If they’re not ready, keep the conversation light and enjoyable, focusing on surface-level interests and experiences.*

    *Use the information provided by the memory assistant to recall relevant details from past conversations, enhancing the personalization of each interaction. Reference these memories to show that you value what the user has shared before, deepening their sense of being understood and appreciated. Adjust your tone and depth of questions based on their responses, ensuring that they always feel comfortable and in control of the conversation.*

    *Offer interactive elements like thought-provoking questions, challenges, or reflections that engage users actively and invite them to come back and share more. Maintain a consistent, approachable, and uplifting tone, making each interaction feel supportive and inspiring. Create a safe and non-judgmental space, ensuring that users feel comfortable sharing their true selves.*

    *Your ultimate aim is to leave them feeling supported, inspired, and eager to continue the journey of self-discovery with you. Use the insights gained during the conversation to understand their unique personality and preferences, so you can help find a truly compatible match in the future, without directly suggesting matches.*
    """


# Define system message for personality (hidden from user)
system_message = {
    "role": "system",
    "content": StarterPrompt
}


# Initialize message history with system personality if it's not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_message]
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
# If this is the first interaction, generate a dynamic greeting from the AI

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[system_message],  # Use only the system message for the first greeting
        temperature=0.7  # Adjust temperature for randomness; 0 is deterministic, 1 is more random
    )
    greeting_msg = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": greeting_msg})


# Display all messages in the conversation
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])  # Assistant message on the left
    elif msg["role"] == "user":
        st.chat_message("user").write(msg["content"])  # User message on the right

# Handle user input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Append user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)  # User message on the right

    # Get response from OpenAI API, including the system message and conversation history
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=st.session_state.messages
    )
    
    # Extract assistant's message and append to the conversation history
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    # Display assistant's message on the left
    st.chat_message("assistant").write(msg)