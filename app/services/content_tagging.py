from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import wikipedia
from fastapi import HTTPException
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"), 
    temperature=0.3  #
)


async def get_content(title: str):

    try:
        wiki_page = wikipedia.page(title=title, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        wiki_page = wikipedia.page(e.options[0], auto_suggest=False)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article not found on Wikipedia")
    return wiki_page

tagging_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert librarian and content curator.
    Analyze the following article text and generate 1-3 representative mutually exclusive category tags.
    
    Rules:
    1. Return ONLY the tags, separated by commas.
    2. Do not number them.
    3. Do not add introductory text like "Here are the tags".
    4. Keep tags simple (e.g., "Technology", "Space", "History").

    Article Text:
    {text}
    """
)


tagging_chain = tagging_prompt | llm | StrOutputParser()

async def generate_tags(article_text: str):
    try:
        short_text = article_text[:2000]

        response = await tagging_chain.ainvoke({"text": short_text})

        tags_list = [tag.strip() for tag in response.split(",")]
        
        return tags_list
    except Exception as e:
        print(f"Error generating tags: {e}")
        # Fallback
        return ["Uncategorized"]


# if __name__== "__main__":
#     res = generate_tags(article_text="title': 'Dolphin', 'summary': 'A dolphin is a common name used for some of the aquatic mammals in the cetacean clade Odontoceti, the toothed whales.")
    
#     .collect(res)
#     print(res)
