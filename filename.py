import streamlit as st
# from langchain.chains import StringDistanceEvalChain
from langchain.evaluation import load_evaluator
#StringDistanceEvalChain or EmbeddingDistanceEvalChain?
evaluator = load_evaluator("string_distance")

st.title("Text Similarity Calculator")

text1 = st.text_input("Enter first text:", "")
text2 = st.text_input("Enter second text:", "")

# if st.button("Calculate similarity"):
#     chain = StringDistanceEvalChain()
#     similarity = chain.run(text1, text2)
#     st.write(f"Similarity score: {similarity}")

if st.button("Calculate similarity"):
    similarity = evaluator.evaluate_strings(    
        prediction=text1,
        reference=text2,
    )
    st.write(f"Similarity score: {similarity}")
#https://juejin.cn/post/7273293183873384488
#"I hear you." vs "I see what you mean" = 0.3101187311713627
#"I shall go" vs "I shan't go" = 0.0945454545454546
#"I shall go" vs "I will go" = 0.1392592592592592
#"I love you" vs "I like you" = 0.09333333333333327
#"I love you" vs "I hate you" = 0.16000000000000003
#"I love you" vs "我爱你" = 1.0
