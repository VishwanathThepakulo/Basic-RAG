User Uploads PDF
       ↓
Extract Text
       ↓
Chunking
       ↓
Create Embeddings
       ↓
Store in Vector DB
       ↓
User asks question
       ↓
Similarity Search
       ↓
Relevant Chunks Retrieved
       ↓
LLM Generates Answer


=================Chunking=================

PyMuPDF
↓
Clean Text
↓
Paragraph Split
↓
RecursiveCharacterTextSplitter
↓
Embeddings
↓
Vector DB


project/
│
├── ingestion/
│   ├── pdf_loader.py
│   ├── cleaner.py
│   ├── chunker.py
│
├── embeddings/
│   ├── embedding_model.py
│
├── vectordb/
│   ├── mongo_store.py
│
├── retrieval/
│   ├── retriever.py
│   ├── reranker.py
│
├── generation/
│   ├── llm.py
│
└── main.py