# URL-loader-retrieval-app-using-Langchain
RAG app that retrieves information from url through vector store to answer your prompts
This app is fully open source.

## How to run:
- Execute the app by running `python main.py` after installing requirements and python modules.
- You will be able to make requests to the given app through the `/ask` endpoint on the hosted web url(like localhost:5000 as default). 
## Requirements :
Langchain
Faiss
Flask
Spacy
BeautifulSoup
Hugging Face API key(optional)

## About :
This RAG app uses 
- HuggingFace opensource model - `HuggingFaceH4/zephyr-7b-beta`
- Vector store - `FAISS`
- Huggingface Embeddings - `BAAI/bge-large-en-v1.5`

## Workflow
This app first parses the website text and extracts the necessary info with the help of Beautiful Soup and RecursiveURLloader from Langchain then it splits the given info using Spacy Text Spiltter when turned out to be more efficient when tested as compared to other splitters. After which it stores it into FAISS vector store with support of BGE embeddings from Hugging face. This vector store is later used as an retrival. The retrieverQA chain from Langchain has been used to make things easier. A proper template was selected appropriate for this RAG app. Lastly this app was configured into a REST api using Flask which accepts the prompt and gives answer as reponse.
