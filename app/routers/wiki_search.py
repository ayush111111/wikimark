# search and tagging routesx
from fastapi import Depends, APIRouter, HTTPException
from .. import schemas
from ..services import wikipedia_client
from ..users import current_active_user
from typing import List

wikisearch_router = APIRouter(prefix="/wiki", tags=["Search"])

@wikisearch_router.get("/search",response_model=List[schemas.WikiSearchItem])
def search(
    query : str,
    user = Depends(current_active_user)
):
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        articles = wikipedia_client.search_wikipedia(query, limit=5)
        return articles
    except Exception as e:
        raise e
