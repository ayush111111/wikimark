from fastapi import Depends, APIRouter, HTTPException, status
from ..services.wikipedia_rest_client import WikipediaRestClient
from .. import schemas, database
from ..users import current_active_user
from ..services import content_tagging
from sqlalchemy import select, desc
from typing import List

article_router = APIRouter(prefix="/articles",tags=["Article"])


# save article
@article_router.post("/", response_model=schemas.ArticleRead)
async def save_article(
        article_key : str,
        user = Depends(current_active_user),
        session = Depends(database.get_async_session)
):
    wiki_client = WikipediaRestClient()
    page = await wiki_client.get_page_summary(key=article_key)
    # check if title exists already - return
    sql = select(database.Article).where(
        database.Article.user_id == user.id,  
        database.Article.title == page["title"]
    )
    result = await session.execute(sql)
    article = result.scalars().first()
    if article:
        return article
    
    # introduce rollback on failure

    # fetch the content of the article from the search using page api
    # page = await content_tagging.get_content(title=title) # check if link can be obtained
    
    # pass to the LLM to generate tags
    tags = await content_tagging.generate_tags(page["summary"])
    
    # save link, tag, title to db
    new_article = database.Article(
        title = page["title"],
        url = page["url"],
        tags = tags,
        user_id = user.id
    )

    session.add(new_article)

    await session.commit()

    await session.refresh(new_article)

    return new_article

# view all articles
@article_router.get("/", response_model=List[schemas.ArticleRead])
async def get_all_articles(
        session = Depends(database.get_async_session),
        user = Depends(current_active_user)
):
    sql = select(database.Article).where(
        database.Article.user_id == user.id
    ).order_by(desc(database.Article.id))

    result = await session.execute(sql)

    articles = result.scalars().all()
    return articles


# update article
@article_router.patch("/{article_id}", response_model=schemas.ArticleRead)
async def update_article_tag(
        article_id: str,
        new_tags: schemas.ArticleUpdateTags,
        user = Depends(current_active_user),
        session = Depends(database.get_async_session)
):
    
    sql = select(database.Article).where(
        database.Article.id == int(article_id),
        database.Article.user_id == user.id
    )

    result = await session.execute(sql)
    article = result.scalar()

    if not article:
        raise HTTPException(status_code=404, detail="Article to be updated is not found")
    
    article.tags = new_tags.tags

    await session.commit()

    await session.refresh(article)

    return article




# update article
@article_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        article_id: str,
        user = Depends(current_active_user),
        session = Depends(database.get_async_session)
):
    
    sql = select(database.Article).where(
        database.Article.id == int(article_id),
        database.Article.user_id == user.id
    )

    result = await session.execute(sql)
    article = result.scalar()

    if not article:
        raise HTTPException(status_code=404, detail="Article to be deleted is not found")
    
    await session.delete(article)
    await session.commit()

    return None


