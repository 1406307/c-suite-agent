import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def ingest_cv(file_path):
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # 1. Load the PDF
    loader = PyPDFLoader(file_path)
    data = loader.load()

    # 2. Split the text into chunks
    # (So the AI doesn't get overwhelmed by the whole document at once)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    # 3. Setup Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=api_key
    )

    # 4. Create/Update the Vault
    Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory="./career_vault"
    )
    print(f"Success! Your {file_path} is now embedded in the Career Vault.")

if __name__ == "__main__":
    # Make sure your file name matches exactly
    ingest_cv("Sudipta_Nandy_Resume.pdf")