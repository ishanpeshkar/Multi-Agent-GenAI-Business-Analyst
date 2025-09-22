import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain_community.document_loaders import TextLoader, CSVLoader, DirectoryLoader

def initialize_chatbot(csv_path: str, emails_dir: str, guidelines_path: str):
    """Create and cache the RAG chain for the chatbot."""
    # Load all documents
    loaders = [
        # --- THIS IS THE LINE WE ARE FIXING ---
        CSVLoader(file_path=csv_path, encoding="windows-1252"), # Explicitly set the encoding
        
        TextLoader(file_path=guidelines_path),
        DirectoryLoader(emails_dir, glob="**/*.txt", silent_errors=True)
    ]

    docs = []
    # Add a try-except block for more robust document loading
    for loader in loaders:
        try:
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading documents from {loader}: {e}")

    # Create vector store
    embeddings = OllamaEmbeddings(model="tinyllama")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Create conversational chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=Ollama(model="tinyllama"),
        retriever=vectorstore.as_retriever(),
    )
    return chain

def display_chat_interface():
    st.header("Chat With Your Business Documents")
    st.write("Ask questions about your sales data, emails, and guidelines.")

    if 'conversation_chain' not in st.session_state or st.session_state.conversation_chain is None:
        st.warning("Please go to the Report page and click 'Generate Business Report' first to initialize the chatbot.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question, e.g., 'Which region had the highest sales?'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_history = st.session_state.get("chat_history", [])
                response = st.session_state.conversation_chain({"question": prompt, "chat_history": chat_history})
                st.markdown(response['answer'])
        
        st.session_state.chat_history = chat_history + [(prompt, response['answer'])]
        st.session_state.messages.append({"role": "assistant", "content": response['answer']})