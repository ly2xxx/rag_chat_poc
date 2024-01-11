# rag_chat_poc
Experimented with Retrieval Augmented Generation based on given documents

### An AI chatbot featuring conversational memory, designed to enable users to discuss their CSV, PDF, TXT data, Website page and YTB videos in a more intuitive manner. 🚀
![Robby](demo-pic.jpg)
Robby the Robot from [Forbidden Planet](https://youtu.be/bflfQN_YsTM)

#### For better understanding, see medium article 🖖 : [Build a chat-bot over your CSV data](https://medium.com/@yvann-hub/build-a-chatbot-on-your-csv-data-with-langchain-and-openai-ed121f85f0cd)

## Running Locally 💻
Follow these steps to set up and run the service locally :

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
Clone the repository :
`git clone https://github.com/ly2xxx/rag_chat_poc.git`
(original template app `git clone https://github.com/yvann-hub/Robby-chatbot.git`)


Navigate to the project directory :

`cd rag_chat_poc`


Create a virtual environment :
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Install the required dependencies in the virtual environment :

`pip install -r requirements.txt`
then
`pip install bitsandbytes accelerate xformers einops langchain faiss-cpu transformers sentence-transformers ctransformers`
then IF USE GPU
`pip uninstall torch`
then
`pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121`


Launch the chat service locally :

`streamlit run streamlit_app.py`

#### That's it! The service is now up and running locally. 🤗