import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from transformers import AutoModelForCausalLM
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory


loader = CSVLoader(file_path="model\google_games_info.csv", encoding='utf-8')
data = loader.load()

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
docsearch = Chroma.from_documents(texts, embeddings)
retriever = docsearch.as_retriever()

# Initialize the language model
llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"max_length": 150, "temperature": 0.9, "top_k": 50, "top_p": 0.95, "num_return_sequences": 1})

# Define the RetrievalQA instance
prompt_template = """

Form a grammatically correct sentence as a response.
Recommend the games from the retriever based on category given in question.
Return game title, description (upto 50 words), package name and icon_url.

question: {question}
context: {context}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": prompt})
memory = ConversationBufferWindowMemory(
    k=2,
    memory_key="chat_history",
    output_key="answer",
    return_messages=True,
)

qa_conversation = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type='stuff',
    retriever=docsearch.as_retriever(),
    return_source_documents=True,
    memory=memory,
    condense_question_prompt=prompt,

)

app = FastAPI()

class QueryModel(BaseModel):
    query: str

@app.post("/qa")
async def get_recommendation(query_model: QueryModel):
    response = qa.run({"query": query_model.query})
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
