import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_memory():
    # 1. SETUP PATHS
    base_dir = "knowledge_base"
    pdf_path = os.path.join(base_dir, "sensor.pdf")
    text_path = os.path.join(base_dir, "rules.txt")
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # 2. CREATE A BACKUP TEXT FILE (In case your PDF is unreadable)
    with open(text_path, "w") as f:
        f.write("""
        VENTILATOR DESIGN RULES:
        1. Pressure Range: The device must maintain 5 to 40 cmH2O.
        2. Sensor: Use MPX5010DP for airway pressure monitoring.
        3. Safety: Must have a mechanical pop-off valve set at 60 cmH2O.
        4. Power: Must have a 2-hour battery backup.
        """)

    print("--- Level 1: Building AI Memory ---")
    
    documents = []
    
    # 3. TRY LOADING PDF
    if os.path.exists(pdf_path):
        try:
            print("Reading PDF...")
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        except Exception as e:
            print(f"PDF Error: {e}. Moving to text backup.")

    # 4. ALWAYS LOAD TEXT BACKUP (Ensures the list is never empty)
    print("Reading Rules text file...")
    loader = TextLoader(text_path)
    documents.extend(loader.load())
    
    # 5. SPLIT DATA
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    print(f"Success: Found {len(docs)} knowledge chunks.")

    # 6. CREATE AI BRAIN (EMBEDDINGS)
    print("Converting to AI memory (this uses your CPU)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 7. SAVE TO DATABASE
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory="./medical_db"
    )
    
    print("\n" + "="*30)
    print("SUCCESS! LEVEL 1 COMPLETE.")
    print("Your AI now has a 'Medical Library' in the folder: medical_db")
    print("="*30)

if __name__ == "__main__":
    build_memory()