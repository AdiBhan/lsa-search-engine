from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from lsa import lsa_search, generate_sim_plot
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()

os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


origins = [
    "http://127.0.0.1:3000",  # Your Angular app's URL
    "http://localhost:3000",  # Optional if you use localhost
]

# Add CORS middleware to allow requests from your Angular app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],  
    allow_headers=["*"])


# Pydantic models for data validation
class Query(BaseModel):
    query: str

class SearchResult(BaseModel):
    index: int
    similarity: float
    content: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    graph_url: str


# Main endpoint for performing lsa, generating graph and returning JSON response of document results, and graph url
@app.post("/api/process_query", response_model=SearchResponse)
async def process_query(query: Query):
    try:
        results = lsa_search(query.query)
        graph_filename = f"graph_{query.query}.png"
        graph_path = generate_sim_plot(results, filename=graph_filename)
        
        # Return the URL of the graph
        return SearchResponse(
            results=[SearchResult(**result) for result in results],
            graph_url=f"/static/{os.path.basename(graph_path)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing your request: {str(e)}")

    

@app.get("/")
async def index():
    return {"Response":"Success. This is a test path!"}