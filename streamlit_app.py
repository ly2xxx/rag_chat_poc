import streamlit as st
from st_pages import hide_pages, show_pages_from_config, add_page_title, show_pages, Page, Section
from PIL import Image
import os

# if not hasattr(st, 'already_started_server'):
#     # Hack the fact that Python modules (like st) only load once to
#     # keep track of whether this file already ran.
#     st.already_started_server = True

#     st.write('''
#         The first time this script executes it will run forever because it's
#         running a Flask server.

#         Just close this browser tab and open a new one to see your Streamlit
#         app.
#     ''')

#     from flask import Flask

#     app = Flask(__name__)

#     @app.route('/foo')
#     def serve_foo():
#         return 'This page is served via Flask!'

#     app.run(port=8888)

def paypal_donation_button():
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

add_page_title()
show_pages_from_config()

show_pages(
    [
        Page("./streamlit_app.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("./pages/1_Robby-Chat-file.py", "Robby-Chat-file", "📄"),
        Page("./pages/2_Robby-Chat-web.py", "Robby-Chat-web", "🌐"),
        Page("./pages/3_Robby-Youtube.py", "Robby-Summary-youtube", "🎬"),
        Page("./pages/download.py", "down", "⤓"),
    ]
)

hide_pages(["down"])

#Config
# st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")


#Contact
with st.sidebar.expander("📬 Contact"):

    st.write("**GitHub:**",
"[jupyter notebook demo](https://github.com/ly2xxx/py_playground/blob/main/mistralai-cpu.ipynb)")

    st.write("**Medium:** "
"[@ly2xxx](https://edisonideas.wordpress.com/)")

    # st.write("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
    st.write("**Mail** : ly2xxx@hotmail.com")
    # st.write("**Inspired by Yvann's pdf chatbot project, Adapted by YL**")

#Donate
with st.sidebar.expander("💵 Donation"):
    st.write(
    # """ 
    # <h5 style='text-align:center; color: green;'>
    "👇Support a tool that helps you get stuff done. Your donation fuels our improvements. Thank-you! 👇"
    # </h5>
    # """
    )
    paypal_donation_button() 

#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Robby, your multilingual research assistant 🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")

def generate_thumbnail(image_path, thumbnail_size=(500, 500)):
    original_image = Image.open(image_path)
    thumbnail = original_image.resize(thumbnail_size)
    return thumbnail

mascot_image_file = "Gallery/mascot/01_mascot.jpeg"
thumbnail = generate_thumbnail(mascot_image_file)
st.image(thumbnail, caption="Robby", use_column_width=True)

#Description
typing_script = """
<style>
    #typed-text {
        overflow: hidden;
        white-space: nowrap; /* Set to nowrap to prevent line breaks */
        border-right: .15em solid orange;
        font-size: 13px; /* Adjust font size as needed */
        margin: 0 auto;
        letter-spacing: .15em;
        animation: typing 6s steps(100, end), blink-caret .5s step-end infinite; /* Adjust timing and steps */
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: orange; }
    }
</style>

<div id="typed-text">Ever felt like you've wasted hours of time wading through documents on the internet?</div>

<script>
    // Function to remove animation after completion
    function removeAnimation() {
        document.getElementById("typed-text").style.animation = "none";
    }

    // Call the removeAnimation function after the animation completes
    document.getElementById("typed-text").addEventListener("animationend", removeAnimation);
</script>
"""

st.markdown(typing_script, unsafe_allow_html=True)
st.markdown(
    """ 
    <h9 style='text-align:left;'>- What if..you had a tireless personal assistant that could pre-analyze all your documents, websites, and videos, highlighting the parts that are most relevant to your needs?</h9>
    <br/>
    <h9 style='text-align:left;'>- So that, this digital assistant could be your secret weapon for staying on top of your workload and staying informed, saving you time and effort by identifying the most important information for you.</h9>
    <h5 style='text-align:center;'>I'm Robby, an intelligent chatbot created for exactly this purpose, by combining 
    the strengths of VectorDB, Langchain and Streamlit. I use Retrieval-augmented generation (RAG) technique and large language models (LLM) to provide
    context-sensitive interactions. 🧠</h5>
    <h8>
    🚀 Make the most of your OpenAI API credits and unlock insights from your data with my help. I can parse PDFs, TXT, CSVs, websites, and even YouTube transcripts like a pro, so let's get analyzing! 
    </h8>
    <br>
    <h8>
    🚀 December 2023 - added new feature to Upload your research materials in a zip file(PDFs, TXT, CSVs, and .pkl files generated by this site) and let Robby turn it into a comprehensive chat for a complete overview! 
    </h8>
    <br>
    <h8>
    🚀 January 2024 - added new feature to Download chat history to read anytime offline. Or for regroup research! 
    </h8>
    <br>
    <h8>
    🚀 January 2024 - discovery: OpenAI's language models understand and generate texts in multiple languages, enabling cross-lingual communication and versatile applications. 
    <a href="https://media.licdn.com/dms/image/D4E2CAQEQhEyFeV6GLw/comment-image-shrink_8192_1280/0/1704827136134?e=1706140800&v=beta&t=Qh4o9wbA50E2Q1PAZiju-PMlmkFqNNMJ7EprNvzygJ0">Proof of uploaded PDF in English, queried in Chinese</a>
    </h8>
    <h4 style='text-align:center; color: green;'>*We don't store your API key or uploaded files.</h4>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Robby's Pages
st.subheader("⬅️☜ Robby's Pages")
st.write("""
- **Robby-Chat-file**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
- **Robby-Chat-web**: General Chat about given website with [langchain-Sitemaploader](https://python.langchain.com/docs/integrations/document_loaders/sitemap) stored in a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
- **Robby-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)         
""")
# st.markdown("""
# - **Robby-Chat-file**: General Chat on data (PDF, TXT, CSV) with a <a href="https://github.com/facebookresearch/faiss" target="_blank">vectorstore</a> (index useful parts (max 4) for responding to the user) | works with <a href="https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html" target="_blank">ConversationalRetrievalChain</a>
# - **Robby-Chat-web**: General Chat about a given website with <a href="https://python.langchain.com/docs/integrations/document_loaders/sitemap" target="_blank">langchain-Sitemaploader</a> stored in a <a href="https://github.com/facebookresearch/faiss" target="_blank">vectorstore</a> (index useful parts (max 4) for responding to the user) | works with <a href="https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html" target="_blank">ConversationalRetrievalChain</a>
# - **Robby-Youtube**: Summarize YouTube videos with <a href="https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html" target="_blank">summarize-chain</a>
# """)

st.markdown("---")

# Add PayPal donation button
paypal_donation_button()

st.markdown("---")

# Specify the directory path containing image files
directory_path = "Gallery/"

# Get a list of image files in the directory
image_files = [file for file in os.listdir(directory_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

# Display thumbnails
for image_file in image_files:
    image_path = os.path.join(directory_path, image_file)
    st.image(image_path)
    
# hide_img_fs = '''
# <style>
# button[title="View fullscreen"]{
#     visibility: hidden;}
# </style>
# '''

# st.markdown(hide_img_fs, unsafe_allow_html=True)
    # thumbnail = generate_thumbnail(image_path)

    # st.image(thumbnail, caption=image_file, use_column_width=True)


# - **Robby-Sheet** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation
# - **Robby-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)

# #Contributing
# st.markdown("### 🎯 Contributing")
# st.markdown("""
# **Robby is under regular development. Feel free to contribute and help me make it even more data-aware!**
# """, unsafe_allow_html=True)





