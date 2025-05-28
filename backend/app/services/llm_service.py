from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # Initialize Google Cloud
        aiplatform.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location="us-central1"
        )
        
        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=2048,
        )
        
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            host=settings.VECTOR_DB_HOST,
            port=settings.VECTOR_DB_PORT
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    async def generate_response(
        self,
        query: str,
        context: Optional[List[str]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a response using the LLM with optional context."""
        try:
            messages = []
            
            # Add system message if provided
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            
            # Add context if provided
            if context:
                context_text = "\n\n".join(context)
                messages.append(
                    SystemMessage(
                        content=f"Here is the relevant context:\n{context_text}\n\nPlease use this context to answer the following question."
                    )
                )
            
            # Add user query
            messages.append(HumanMessage(content=query))
            
            # Generate response
            response = await self.llm.agenerate([messages])
            
            return {
                "response": response.generations[0][0].text,
                "metadata": {
                    "model": "gemini-pro",
                    "tokens_used": response.llm_output.get("token_usage", {}),
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def search_similar_documents(
        self,
        query: str,
        collection_name: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity."""
        try:
            # Create vector store
            vector_store = Qdrant(
                client=self.qdrant_client,
                collection_name=collection_name,
                embeddings=self.embeddings
            )
            
            # Search for similar documents
            results = vector_store.similarity_search_with_score(
                query,
                k=limit
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

    async def process_and_index_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        collection_name: str
    ) -> Dict[str, Any]:
        """Process a document and index it in the vector store."""
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create vector store
            vector_store = Qdrant(
                client=self.qdrant_client,
                collection_name=collection_name,
                embeddings=self.embeddings
            )
            
            # Add documents to vector store
            vector_store.add_texts(
                texts=chunks,
                metadatas=[metadata] * len(chunks)
            )
            
            return {
                "status": "success",
                "chunks_processed": len(chunks),
                "collection": collection_name
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

# Create a singleton instance
llm_service = LLMService() 