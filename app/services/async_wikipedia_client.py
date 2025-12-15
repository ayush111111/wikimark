
import wikipedia
wikipedia.set_user_agent("WikiMark/1.0 (lokareaayush@gmail.com)")
import asyncio
from typing import Set, List
from concurrent.futures import ThreadPoolExecutor



class AsyncWikipediaClient:

    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
          
        
    async def search_with_fallback(
            self, 
            query:str, 
            limit: int = 5
        ):
        """parallel search with fallbacks"""

        seen_titles = set() 
        loop = asyncio.get_event_loop()
        
        search_results, suggestion = await loop.run_in_executor(
            self.executor,
            lambda: wikipedia.search(query, results = limit, suggestion= True)
        )
        

        if not search_results and suggestion:
            search_results = await loop.run_in_executor(
                self.executor,
                lambda: wikipedia.search(query=suggestion, results = limit)
            )

        if not search_results: return []

        tasks = [self._fetch_with_fallbacks(title, seen_titles) for title in search_results[:limit]]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        articles = []
        for result in results:
            if result and not isinstance(result, Exception):
                articles.append(result)
        return articles

    async def _fetch_with_fallbacks(
            self,
            title: str,
            seen_titles : set
    ):
        """fetch summary or call specific fallbacks"""
        if title in seen_titles:
            return None
        seen_titles.add(title) # avoid calling again (in case disambiguation logic fetches it)        
        loop = asyncio.get_event_loop()
        print(f"[START] Fetching: {title}")
        try:
            page = await loop.run_in_executor(
                self.executor,
                lambda: wikipedia.page(title, auto_suggest=False) # suggests resolve spellchecks, but also replaces "Mouse" to "House"
            )

        except wikipedia.exceptions.DisambiguationError as e:
            return await self._handle_ambiguation(e.options, seen_titles)
        except wikipedia.exceptions.PageError as e:
            return await self._handle_page_error(page.title, seen_titles)
        except Exception as e:
            return {"title": title, "summary": None, "url": None}
        
        return {"title": page.title, "summary": page.summary, "url":page.url}

    async def _handle_ambiguation(
            self,
            options: List[str],
            seen_titles : set
    ):
        loop = asyncio.get_event_loop()
        
        for option in options:
            print(f"[START] -disambiguation Fetching: {option}") # add async here
            if option in seen_titles:
                continue
            seen_titles.add(option)
            
            try:

                page = await loop.run_in_executor(
                    self.executor,
                    lambda current_option=option:wikipedia.page(current_option, auto_suggest=False)
                ) # store in another variable so that it is passed correctly
                return {"title": page.title, "summary": page.summary, "url": page.url}
                # break
            except wikipedia.exceptions.DisambiguationError as e:
                continue
            
    async def _handle_page_error(
            self,
            title : str,
            seen_titles : set
    ):
        loop = asyncio.get_event_loop()

        try:
            page = await loop.run_in_executor(
                self.executor,
                lambda: wikipedia.page(title, auto_suggest=True) # suggests resolve spellchecks
            )
            
        except wikipedia.exceptions.PageError as e:
            return None
        except Exception as e:
            return {"title": title, "summary": None, "url": None}

        new_title = page.title

        return {"title": new_title, "summary": page.summary, "url": page.url}
    


async_wiki_client = AsyncWikipediaClient(max_workers=10)