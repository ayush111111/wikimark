
import wikipedia
wikipedia.set_user_agent("WikiMark/1.0 (lokareaayush@gmail.com)")

def search_wikipedia(query: str, limit: int = 5):
    """returns search results with summaries"""
    articles = []
    try: 
        search_results, suggestion = wikipedia.search(query, results = limit, suggestion= True)

        if not search_results and suggestion:
            search_results = wikipedia.search(query=suggestion, results = limit)
        for title in search_results:
            if title in articles:
                continue
            try:
                summary_text = wikipedia.summary(title, sentences=1, auto_suggest=False)
                articles.append({"title": title, "summary": summary_text})
                
            except wikipedia.exceptions.DisambiguationError as e: 

                for option in e.options[:3]:
                    try:
                        summary_text = wikipedia.summary(option, sentences=1, auto_suggest=False)
                        articles.append({"title": option, "summary": summary_text})     
                        break # if valid article is found - prompt user fpr a clarification in UI?
                    except wikipedia.exceptions.DisambiguationError as e: 
                        continue # cannot handle nested ambiguation, if first three are invalid 
                
            except wikipedia.exceptions.PageError:
                # article not found, retry with auto-suggest to handle typos ("Pytjon" -> "Python")
                summary_text = wikipedia.summary(title, sentences=1, auto_suggest=True) # 
                articles.append({"title": title, "summary": summary_text})    
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