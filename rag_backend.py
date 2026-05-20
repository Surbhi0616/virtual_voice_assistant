import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def initialize_knowledge_base():
    DATA_DIR = os.path.join("data", "policy_documents")
    
    print("\nStep 1: Loading PDF documents...")
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print(f"Error: Your '{DATA_DIR}' folder is empty!")
        return None

    loader = PyPDFDirectoryLoader(DATA_DIR)
    raw_documents = loader.load()

    print("\nStep 2: Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    doc_chunks = text_splitter.split_documents(raw_documents)

    print("\nStep 3: Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("\nStep 4: Creating FAISS vector store...")
    # FAISS does not require a persist_directory in the same way as Chroma
    vector_store = FAISS.from_documents(doc_chunks, embeddings)
    
    print("SUCCESS: Vector database created.")
    return vector_store

def query_knowledge_base(user_question, vector_store):
    # Search the existing vector_store object passed into the function
    print(f"\nSearching for: '{user_question}'")
    results = vector_store.similarity_search(user_question, k=2)
    return results

if __name__ == "__main__":
    db_store = initialize_knowledge_base()
    
    if db_store is not None:
        sample_query = "How long does the authorization expire?" 
        matches = query_knowledge_base(sample_query, db_store)
        
        print("\nTOP DATA MATCH RECOVERED:")
        if matches:
            print(matches[0].page_content)
        else:
            print("No matches found.")