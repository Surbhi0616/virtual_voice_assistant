import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings  # Swapped to cloud-safe embeddings
from langchain_chroma import Chroma

def initialize_knowledge_base():
    # Use generic slashes so it works on both Windows and Linux cloud servers
    DATA_DIR = os.path.join("data", "policy_documents")
    PERSIST_DIR = "vector_db"
    
    print("\nStep 1: Loading PDF documents from your folder...")
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print(f"Error: Your '{DATA_DIR}' folder is empty! Put a PDF file in there first.")
        return None

    loader = PyPDFDirectoryLoader(DATA_DIR)
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} pages of text.")

    print("\nStep 2: Splitting text into small context chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    doc_chunks = text_splitter.split_documents(raw_documents)
    print(f"Created {len(doc_chunks)} smaller context blocks.")

    print("\nStep 3: Launching cloud-safe HuggingFace Embedding engine...")
    # This runs entirely within the app container anywhere without needing Ollama
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("\nStep 4: Generating vectors and creating database...")
    vector_store = Chroma.from_documents(
        documents=doc_chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print("SUCCESS: Your vector database has been created and saved.")
    return vector_store

def query_knowledge_base(user_question):
    PERSIST_DIR = "vector_db"
    # Must use the exact same embedding model used to build the database
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Connect back to the database
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    
    print(f"\nSearching database for: '{user_question}'")
    results = db.similarity_search(user_question, k=2)
    return results

if __name__ == "__main__":
    # --- REBUILD DATABASE WITH NEW EMBEDDINGS ---
    db_store = initialize_knowledge_base()
    
    if db_store is not None:
        sample_query = "How long does the authorization expire?" 
        matches = query_knowledge_base(sample_query)
        
        print("\nTOP DATA MATCH RECOVERED FROM DATABASE:")
        if matches:
            print(matches[0].page_content)
        else:
            print("No matches found.")