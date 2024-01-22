from langchain.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from flask import Flask, request, jsonify
#from langchain.embeddings import HuggingFaceBgeEmbeddings
import os
from langchain.text_splitter import SpacyTextSplitter
from getpass import getpass
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

import warnings
warnings.filterwarnings('ignore')


print("Enter your HuggingFace API token:")
HUGGINGFACEHUB_API_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


def create_prompt():
    template = """<human>: Answer the question based only on the following context. If you cannot answer the question with the context, please respond with 'I don't know':
    ### CONTEXT
    {context}
    ### QUESTION
    Question: {question}
    \n
    <bot>:
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt

def extractor(x):
    st = ""
    for a in Soup(x, "html.parser").find_all("div", class_="single-courses-box", attrs={'id': lambda x: x != 'BookDemo-btn'}):
        st += a.text
    return st

def create_faiss_index(data):
    model_name = "BAAI/bge-large-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True}
    hf_bge_embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs
    )

    text_splitter = SpacyTextSplitter(chunk_size=1000)


    texts = text_splitter.split_documents(data)

    faiss_index = FAISS.from_documents(texts, hf_bge_embeddings)
    return faiss_index

def chain(faiss_index):
    retriever = faiss_index.as_retriever(search_kwargs={"additional": ["certainty"]})

    repo_id = "HuggingFaceH4/zephyr-7b-beta"

    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.1, "max_new_tokens":1024, "max_length": 1024}
    )

    chain = RetrievalQA.from_chain_type(llm,retriever=retriever,chain_type='stuff',input_key="question")
    return chain

url = "https://brainlox.com/courses/category/technical"
loader = RecursiveUrlLoader(
    url=url, max_depth=1, extractor=lambda x: extractor(x)
)
app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        res = chain.invoke(prompt)
        answer = res["result"]

        return jsonify({'answer': answer}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
        data = loader.load()
        print('Data loaded')
        faiss_index = create_faiss_index(data)
        print('Faiss index created' , faiss_index)
        prompt = create_prompt()
        chain_type_kwargs = {"prompt": prompt}
        print('Prompt created', prompt)
        chain = chain(faiss_index)
        print('Chain created', chain)
        app.run(debug=True,use_reloader=False)
