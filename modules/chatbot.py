import streamlit as st
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
# from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
import time

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
        start_time = time.time()
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever(search_type="similarity", search_kwargs={"k":3})


        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever, 
            # chain_type="map_reduce",
            verbose=True, 
            return_source_documents=True, 
            max_tokens_limit=4097, 
            combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))

        end_time = time.time()
        execution_time = end_time - start_time
        #count_tokens_chain(chain, chain_input)
        return (
            result["answer"]
            + "\n["
            + f"Query time: {execution_time:.4f} seconds"
            + "]\n "
            # + "\n".join(map(str, result['source_documents']))
        )


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    
