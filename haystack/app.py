from fastapi import FastAPI
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import clean_wiki_text, convert_files_to_docs
import uvicorn
import os

app = FastAPI(title="Haystack API", version="1.0.0")

# Initialize document store
document_store = ElasticsearchDocumentStore(
    host="elasticsearch",
    port=9200,
    index="knowledge_base"
)

# Initialize retriever and reader
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

# Create pipeline
pipe = ExtractiveQAPipeline(reader, retriever)

@app.get("/")
async def root():
    return {"message": "Haystack API is running"}

@app.post("/query")
async def query_documents(query_data: dict):
    try:
        query = query_data.get("query", "")
        params = query_data.get("params", {})
        
        prediction = pipe.run(
            query=query,
            params=params
        )
        
        return {
            "query": query,
            "answers": [
                {
                    "answer": answer.answer,
                    "confidence": answer.score,
                    "context": answer.context
                }
                for answer in prediction["answers"]
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/index")
async def index_documents():
    try:
        # Example: Index documents from BookStack
        # This would typically be called via n8n workflow
        docs = convert_files_to_docs(dir_path="./data/documents")
        document_store.write_documents(docs)
        
        return {"message": f"Indexed {len(docs)} documents"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
