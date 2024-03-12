import multiprocessing
from ChatChain import *
import streamlit as st

Avaiable_Models = ['gemini-pro', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo', 'gpt-3.5-turbo-instruct', 'gpt-4',
                   'gpt-4-0613']  # ,'gpt-4-32k-0613','gpt-4-32k']

def home():
    col1,col2=st.columns([1,4])
    with col1:
        st.image("images/Logo.png", caption="ChartFi Pine Script Code Generation Chatbot",
                 use_column_width=True)
    with col2:
        description = """
        # Overview
        The ChartFi Pine Script Generator Chatbot is an innovative tool designed to simplify the process of creating Pine Script code for custom indicators and strategies in trading. Developed by ChartFi, this chatbot leverages advanced AI algorithms to understand user requirements and generate accurate Pine Script code that can be directly used in the TradingView platform.
        
        This chatbot is not just a code generator; it's a virtual assistant for traders who want to bring their trading ideas to life without the hassle of manual coding. Whether you're a seasoned trader with complex strategy requirements or a beginner looking to experiment with simple indicators, the ChartFi Pine Script Generator Chatbot is your go-to solution. It streamlines the code creation process, making it accessible, efficient, and error-free.
        
        """
        st.write(description)

    st.write("""
        ## Features
            Intuitive Interaction: Engage in natural language conversations with the chatbot to specify your indicator or strategy requirements.
            Custom Code Generation: Receive tailor-made Pine Script code based on your specific trading criteria and technical analysis needs.
            Time-Saving: Reduce the time spent on coding and debugging by getting accurate and ready-to-use scripts.
            Versatility: Suitable for generating code for a wide range of indicators and strategies, from simple moving averages to complex trading algorithms.

        ## How It Works
            Start a Conversation: Initiate a chat with the ChartFi Pine Script Generator Chatbot.
            Describe Your Requirements: Clearly explain the indicator or strategy you want to develop. You can specify technical details, conditions, and parameters.
            Receive Pine Script Code: The chatbot processes your input and generates the corresponding Pine Script code.
            Implement in TradingView: Copy the generated code and paste it into the Pine Editor on TradingView to create your custom indicator or strategy.
        
        ## Get Started
        To start using the ChartFi Pine Script Generator Chatbot, visit ChartFi's website and navigate to the chatbot section. No prior coding experience is required, making it accessible for traders of all skill levels.
        """)


def get_responce(query, selected_model):
    with multiprocessing.Pool(processes=1) as pool:
        answer, reference_docuemnts_sources = pool.apply(Get_Conversation_chain, args=( query, st.session_state.previous_chat,str(selected_model).lower()))
    st.session_state.previous_chat.append({'human': query, 'ai': answer})
    st.session_state.interface_chats.append(
        # {'Me': query, 'AI Chat Bot': answer, 'Reference Sources and Context': reference_docuemnts_sources})
        {'Me': query, 'ChartFi Bot': answer,'Reference Code':refrence_docuemnts_sources})
    st.rerun()


def chat_interface():
    st.title("Pine Script Code Generator")
    st.markdown("---")

    st.subheader("Chat Interface")
    global Avaiable_Models
    Avaiable_Models = [string.upper() for string in Avaiable_Models]
    selected_model = st.selectbox("Select Large Language Model for Augmentation (by Default it uses GPT 4)",
                                      Avaiable_Models, index=Avaiable_Models.index("GPT-4"))
    if 'previous_chat' and 'interface_chats' not in st.session_state:
        st.session_state.previous_chat = []
        st.session_state.interface_chats = []

    with st.form('Messages-Form'):
        st.write('Previous Chat History and Reference Sources')
        for previous_message in st.session_state.interface_chats:
            st.write(previous_message)
        message = st.text_input("Post a message")
        if st.form_submit_button("Ask AI Bot") and message:
            get_responce(message, selected_model)
        else:
            st.warning("Please write any Query to Proceed.")

# Set the title at the top of the Streamlit app
st.set_page_config(
    page_title="ChartFi",
    page_icon="images/clipped-logo.png",  # You can use an emoji or provide a URL to an icon
    layout="wide",  # Set the layout to wide
)

st.markdown("""
<script>
document.body.style.zoom = 0.7;
</script>
""", unsafe_allow_html=True)


# Main function to handle page navigation
def main():
    pages = {
        "Home": home,
        "Chat Interface": chat_interface,
    }
    st.sidebar.image("images/Logo-sidebar.png", caption="ChartFi Pine Script Code Generator", use_column_width=True)

    st.sidebar.title("ChartFi")
    selection = st.sidebar.selectbox("Select Page to Navigate", list(pages.keys()))
    page = pages[selection]
    page()


if __name__ == "__main__":
    main()
