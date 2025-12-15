import httpx
from typing import List



class WikipediaRestClient:
    def __init__(self):
        self.headers = {"User-Agent":"WikiMark/1.0 (lokareaayush@gmail.com)"}
        self.search_url =  f"https://en.wikipedia.org/w/rest.php/v1/search/page"
        self.summary_url = "https://en.wikipedia.org/api/rest_v1/page/summary"

    async def search(self, query: str, limit: int = 5):
        # https://public-paws.wmcloud.org/User:APaskulin_(WMF)/en-wikipedia-search.ipynb

        async with httpx.AsyncClient() as client:
            # https://en.wikipedia.org/w/rest.php/v1/search/page?q=earth&limit=1
            response = await client.get(
                self.search_url,
                headers=self.headers,
                params = {"q": query, "limit": limit}
            )
            response.raise_for_status()
            data = response.json()

        
        results = []
        for page in data['pages']:
            clean_excerpt =  self._clean_html_tags(page.get('excerpt', ''))
            results.append({
                'title': page['title'],
                'url': 'https://en.wikipedia.org/wiki/' + page['key'],
                'summary': page.get('description') or clean_excerpt,
                'key': page['key']
            })
        return results

    async def get_page_summary(self, key:str):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.summary_url}/{key}",
                headers=self.headers
            )

            response.raise_for_status()
            data = response.json()
        print(data)
        return {
            "title": data["title"],
            "summary": data["extract"],
            "url": data["content_urls"]["desktop"]["page"]
        }
    
    def _clean_html_tags(self,text: str) -> str:
        return (text
            .replace('<span class="searchmatch">', '')
            .replace('</span>', ''))