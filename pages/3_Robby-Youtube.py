import os
import streamlit as st
import re
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from st_pages import hide_pages

# st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")
hide_pages(["Robby-Summary-youtube", "down"])

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

st.markdown(
    f"""
    <h1 style='text-align: center;'> Ask Robby to summarize youtube video ! 😁</h1>
    """,
    unsafe_allow_html=True,
)

user_api_key = utils.load_api_key()

sidebar.about()

if not user_api_key:
    layout.show_api_key_missing()

else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    script_docs = []

    def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#]+", url)
        if match :
            video_id = match.group()
        else : 
            match = re.search(r"(?<=youtu.be/)[^&#]+", url)
            if match :
                video_id = match.group()
        return video_id

    video_url = st.text_input(placeholder="Enter Youtube Video URL", label_visibility="hidden", label =" ")
    if video_url :
        video_id = get_youtube_id(video_url)

        if video_id != "":
            t = YouTubeTranscriptApi.get_transcript(video_id, languages=('en','fr','es', 'zh-cn', 'hi', 'ar', 'bn', 'ru', 'pt', 'sw' ))
            finalString = ""
            for item in t:
                text = item['text']
                finalString += text + " "

            text_splitter = CharacterTextSplitter()
            chunks = text_splitter.split_text(finalString)

            #The model `text-davinci-003` has been deprecated
            #https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb
            # summary_chain = load_summarize_chain(OpenAI(temperature=0),
            summary_chain = load_summarize_chain(ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0),
                                            chain_type="map_reduce",verbose=True)
            
            summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

            answer = summarize_document_chain.run(chunks)

            st.subheader(answer)
            sidebar.donation()
