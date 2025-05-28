from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.services.llm_service import llm_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    llm_response: Optional[Dict[str, Any]] = None

@router.get("/", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    use_llm: bool = Query(True, description="Whether to use LLM for response generation"),
    collection: str = Query("documents", description="Collection to search in"),
    limit: int = Query(5, description="Maximum number of results to return")
):
    """
    Search endpoint that combines vector search with LLM-powered response generation.
    """
    try:
        # Search for similar documents
        search_results = await llm_service.search_similar_documents(
            query=q,
            collection_name=collection,
            limit=limit
        )
        
        # Extract context from search results
        context = [result["content"] for result in search_results]
        
        # Generate LLM response if requested
        llm_response = None
        if use_llm:
            llm_response = await llm_service.generate_response(
                query=q,
                context=context,
                system_prompt="You are a helpful assistant that provides accurate and concise answers based on the given context."
            )
        
        return SearchResponse(
            results=search_results,
            llm_response=llm_response
        )
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your search request"
        )

@router.post("/analyze")
async def analyze_document(
    content: str,
    metadata: Dict[str, Any],
    collection: str = Query("documents", description="Collection to store the document in")
):
    """
    Analyze and index a document for future searching.
    """
    try:
        result = await llm_service.process_and_index_document(
            content=content,
            metadata=metadata,
            collection_name=collection
        )
        return result
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the document"
        ) 