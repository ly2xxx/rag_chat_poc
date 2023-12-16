import streamlit as st

def paypal_donation_button():
    paypal_button_code = """
    <form action="https://www.paypal.com/donate" method="post" target="_top">
    <input type="hidden" name="business" value="J74C4FTELMRT4" />
    <input type="hidden" name="no_recurring" value="0" />
    <input type="hidden" name="item_name" value="Support us! Your donation powers our content, and we'll share the code with you as a thank-you." />
    <input type="hidden" name="currency_code" value="GBP" />
    <input type="image" src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
    <img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1" />
    </form>
    """

    st.markdown(paypal_button_code, unsafe_allow_html=True)


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")


#Contact
with st.sidebar.expander("📬 Contact"):

    st.write("**GitHub:**",
"[ly2xxx/rag_chat_poc](https://github.com/ly2xxx/rag_chat_poc)")

    st.write("**Medium:** "
"[@ly2xxx](https://edisonideas.wordpress.com/)")

    # st.write("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
    st.write("**Mail** : ly2xxx@hotmail.com")
    st.write("**Created by Yvann, Adapted by YL**")

#Donate
with st.sidebar.expander("💵 Donation"):
    st.write(
    # """ 
    # <h5 style='text-align:center; color: green;'>
    "👇Support us! Your donation powers our content, and we'll share the code with you as a thank-you.👇"
    # </h5>
    # """
    )
    paypal_donation_button() 

#Title
st.markdown(
    """
    <h2 style='text-align: center;'>Robby, your data-aware assistant 🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>I'm Robby, an intelligent chatbot created by combining 
    the strengths of VectorDB, Langchain and Streamlit. I use large language models (LLM) to provide
    context-sensitive interactions. 🧠</h5>
    <h8>
    🚀 Make the most of your OpenAI API credits and unlock insights from your data with my help. I can parse PDFs, TXT, CSVs, websites, and even YouTube transcripts like a pro, so let's get analyzing! 
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

# - **Robby-Sheet** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation
# - **Robby-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)

# #Contributing
# st.markdown("### 🎯 Contributing")
# st.markdown("""
# **Robby is under regular development. Feel free to contribute and help me make it even more data-aware!**
# """, unsafe_allow_html=True)





