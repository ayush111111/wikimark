
import wikipedia
wikipedia.set_user_agent("WikiMark/1.0 (lokareaayush@gmail.com)")
import asyncio
from typing import Set, List
from concurrent.futures import ThreadPoolExecutor



class AsyncWikipediaClient:

    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.seen_titles = set()    
        
    async def search_with_fallback(
            self, 
            query:str, 
            limit: int = 5
        ):
        """parallel search with fallbacks"""

        self.seen_titles.clear()
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

        tasks = [self._fetch_with_fallbacks(title) for title in search_results[:limit]]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        articles = []
        for result in results:
            if result and not isinstance(result, Exception):
                articles.append(result)
        return articles

    async def _fetch_with_fallbacks(
            self,
            title: str,

    ):
        """fetch summary or call specific fallbacks"""
        if title in self.seen_titles:
            return None
        self.seen_titles.add(title) # avoid calling again (in case disambiguation logic fetches it)        
        loop = asyncio.get_event_loop()
        print(f"[START] Fetching: {title}")
        try:
            page = await loop.run_in_executor(
                self.executor,
                lambda: wikipedia.page(title, auto_suggest=False) # suggests resolve spellchecks, but also replaces "Mouse" to "House"
            )

        except wikipedia.exceptions.DisambiguationError as e:
            return await self._handle_ambiguation(e.options)
        except wikipedia.exceptions.PageError as e:
            return await self._handle_page_error(page.title)
        except Exception as e:
            return {"title": title, "summary": None, "url": None}
        
        return {"title": page.title, "summary": page.summary, "url":page.url}

    async def _handle_ambiguation(
            self,
            options: List[str]
    ):
        loop = asyncio.get_event_loop()
        for option in options:
            if option in self.seen_titles:
                continue
            self.seen_titles.add(option)
            
            try:
                page = await loop.run_in_executor(
                    self.executor,
                    lambda current_option=option:wikipedia.page(current_option, auto_suggest=False)
                ) # store in another variable so that it is passed correctly
                return {"title": page.title, "summary": page.summary, "url": page.url}
                # break
            except wikipedia.exceptions.DisambiguationError as e:
                continue 
            except wikipedia.exceptions.PageError as e:
                page = await loop.run_in_executor(
                    self.executor,
                    lambda: wikipedia.page(option, auto_suggest=True) # suggests resolve spellchecks
                )
                return {"title": page.title, "summary": page.summary, "url": page.url}
            
    async def _handle_page_error(
            self,
            title : str
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
    
    async def streaming_search(self, query: str, limit: int = 5):
        """yield results as they are completed"""

        self.seen_titles.clear()
        loop = asyncio.get_event_loop()

        search_results, suggestion = await loop.run_in_executor(
            self.executor,
            lambda: wikipedia.search(query=query, results=limit, suggestion=True)
        )

        if not search_results and suggestion:
            search_results = await loop.run_in_executor(
                self.executor,
                lambda: wikipedia.search(query=suggestion, results=limit, suggestion=False)
            )
        

        tasks = [self._fetch_with_fallbacks(title=title) for title in search_results[:limit]]
        
        # results = await asyncio.gather(*tasks, return_exceptions=True)
        
        articles = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result and not isinstance(result, Exception):
                yield result 

        # return articles

async_wiki_client = AsyncWikipediaClient(max_workers=10)


# async def main():

#     stream = async_wiki_client.streaming_search(query="blue", limit=5)
#     async for result in stream:
#         print(result)

# asyncio.run(main(), debug=True)