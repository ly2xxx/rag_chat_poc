import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback
from ctransformers import AutoModelForCausalLM
from transformers import AutoTokenizer, BitsAndBytesConfig
from langchain.llms import HuggingFacePipeline
import torch
import transformers

#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    qa_template = """
        You are a helpful AI assistant named Robby. The user gives you a file its content is represented by the following pieces of context, use them to answer the question at the end.
        If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
        If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
        Use as much detail as possible when responding.

        context: {context}
        =========
        question: {question}
        ======
        """

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = self.initializeLLM()

        retriever = self.vectors.as_retriever()


        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, verbose=True, return_source_documents=True, max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        #count_tokens_chain(chain, chain_input)
        return result["answer"]

    def initializeLLM(self):
        # llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        # repo_id = "mistralai/Mistral-7B-v0.1"
        # llm = HuggingFaceHub(huggingfacehub_api_token='your huggingface access token here', 
        #                     repo_id=repo_id, model_kwargs={"temperature":0.2, "max_new_tokens":50})

        ##cpu
        #https://discuss.huggingface.co/t/number-of-tokens-2331-exceeded-maximum-context-length-512-error-even-when-model-supports-8k-context-length/57180/4
        # model = AutoModelForCausalLM.from_pretrained("TheBloke/zephyr-7B-beta-GGUF", 
        #                                    model_file="zephyr-7b-beta.Q5_K_M.gguf", 
        #                                    model_type="mistral", 
        #                                    gpu_layers=0,
        #                                    max_new_tokens = 1000,
        #                                    context_length = 6000)     
        model = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            model_type="mistral", 
            gpu_layers=0, hf=True,
            max_new_tokens = 1000,
            context_length = 6000
        )
        tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-v0.1", 
            use_fast=True
        )

        # Create a pipeline
        pipeline = transformers.pipeline(model=model, tokenizer=tokenizer, max_new_tokens=2048, task='text-generation')

        llm = HuggingFacePipeline(
            pipeline=pipeline,
            )

        ##gpu
        # input = torch.randn(2,3)
        # input = input.to("cuda")

        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # print("Device:", device)
        # if device == 'cuda':
        #     print(torch.cuda.get_device_name(0))

        # model_id = "mistralai/Mistral-7B-Instruct-v0.1"
        # #https://huggingface.co/blog/4bit-transformers-bitsandbytes
        # bnb_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_compute_dtype=torch.float16
        # )
        
        # text_generation_pipeline = transformers.pipeline(
        #     "text-generation",
        #     model=model_id,
        #     model_kwargs={"torch_dtype": torch.float16, "load_in_4bit": True, "quantization_config": bnb_config},
        # )

        # llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

        return llm


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    
