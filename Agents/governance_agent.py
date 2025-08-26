from llm import get_llm_response
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter

def check_governance(recommendations: str, guidelines_path: str):
    """
    Validates recommendations against company guidelines using a RAG system.
    """
    try:
        # 1. Load and process the guidelines document
        loader = TextLoader(guidelines_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        
        # 2. Create embeddings and a vector store (FAISS)
        # THIS IS THE LINE WE ARE FIXING
        embeddings = OllamaEmbeddings(model="tinyllama")
        
        db = FAISS.from_documents(docs, embeddings)
        retriever = db.as_retriever()

    except Exception as e:
        # This will catch errors during the RAG setup
        return f"## Governance Check\n- **Error during analysis:** Error creating vector store: {e}"

    # 3. For each recommendation, retrieve relevant guidelines and get LLM validation
    try:
        prompt = (
            "You are a governance and compliance officer. Your task is to validate a business recommendation "
            "against a specific set of company guidelines. \n\n"
            "Recommendation:\n"
            f"{recommendations}\n\n"
            "Company Guidelines:\n"
            "{retrieved_docs}\n\n"
            "Does the recommendation align with the guidelines? Answer with 'Compliant' or 'Non-Compliant' "
            "and provide a brief, one-sentence justification."
        )
        
        retrieved_docs = retriever.get_relevant_documents(recommendations)
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        
        final_prompt = prompt.format(retrieved_docs=context)
        
        validation = get_llm_response(final_prompt)
        
        return f"## Governance Check\n- **Recommendation Analysis:**\n{validation}"
    except Exception as e:
        return f"## Governance Check\n- **Error during analysis:** Could not get LLM validation: {e}"