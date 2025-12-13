
import wikipedia


def search_wikipedia(query: str, limit: int = 5):
    """returns search results with summaries"""
    articles = []
    try: 
        search_results = wikipedia.search(query, results = limit)

        for title in search_results:
            try:
                summary_text = wikipedia.summary(title, sentences=1, auto_suggest=False)
                articles.append({"title": title, "summary": summary_text})
                
            except wikipedia.exceptions.DisambiguationError as e: 
                summary_text = wikipedia.summary(e.options[0], sentences=1, auto_suggest=False)
                articles.append({"title": e.options[0], "summary": summary_text})            
            except wikipedia.exceptions.PageError:
                # article not found
                continue
            except Exception as e:
                print(f"Error fetching {title}: {e}")
                articles.append({"title": title, "summary": None})
        return articles
    except Exception as e:
        # log 
        print(f"Exception while searching {e}")
        return []

if __name__== "__main__":
    res = search_wikipedia(query="dolphin", limit=5)
    print(res)