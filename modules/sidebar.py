import streamlit as st
import base64
import re

class Sidebar:

    MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def donation():
        paypal_button_code = """
        <form action="https://www.paypal.com/donate" method="post" target="_blank">
        <input type="hidden" name="business" value="J74C4FTELMRT4" />
        <input type="hidden" name="no_recurring" value="0" />
        <input type="hidden" name="item_name" value="Support a tool that helps you get stuff done. Your donation fuels our improvements. Thank-you!" />
        <input type="hidden" name="currency_code" value="GBP" />
        <input type="image" src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
        <img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1" />
        </form>
        """
        st.markdown(paypal_button_code, unsafe_allow_html=True)
        st.write(
        "👆 *Support a tool that helps you get stuff done. Your donation fuels our improvements. Thank-you🎯*"
        )

    @staticmethod
    def about():
        about = st.sidebar.expander("🧠 About Robby ")
        sections = [
            "#### Robby is an AI chatbot with a conversational memory, designed to allow users to discuss their data in a more intuitive way. 📄",
            "#### It uses large language models to provide users with natural language interactions about user data content. 🌐",
            "#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡",
            "#### Source code: ly2xxx/rag_chat_poc](https://github.com/ly2xxx/rag_chat_poc)",
        ]
        for section in sections:
            about.write(section)

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def model_selector(self):
        model = st.selectbox(label="Model", options=self.MODEL_OPTIONS)
        st.session_state["model"] = model

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
        )
        st.session_state["temperature"] = temperature
        
    def show_options(self):
        with st.sidebar.expander("🛠️ Robby's Tools", expanded=False):

            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)

    def download_model(self, vectormodel):
        with open(vectormodel, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:file/pkl;base64,{b64}" download=\'{vectormodel}\'>\
                Download Trained Model .pkl\
            </a> <span style="color:green; font-weight:bold;">(Combine multiple .pkl files into a .zip for deeper AI analysis later)</span>'
            st.markdown(href, unsafe_allow_html=True)

    def download_conversation(self, chathistory, chat_filename):
        # Convert the list to a string
        chat_text = "\n".join(map(str, chathistory))

        # Convert the string to bytes
        bytes_content = chat_text.encode()

        # Clean the filename by removing or replacing disallowed characters
        # clean_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', str(chathistory))

        # Create a base64-encoded link for downloading
        b64 = base64.b64encode(bytes_content).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download=\'{chat_filename}.txt\'>\
            Download Chat History .txt\
        </a> <span style="color:green; font-weight:bold;">(Combine multiple .txt files into a .zip for deeper AI analysis later)</span>'

        # Display the download link
        st.markdown(href, unsafe_allow_html=True)

    