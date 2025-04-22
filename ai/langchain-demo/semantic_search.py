from libs import langfuse_handler
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("data/llm_rec.txt")
docs = loader.load()
print("Loaded documents:", len(docs))

print(docs[0].metadata)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = splitter.split_documents(docs)

print("Total splits:", len(all_splits))
