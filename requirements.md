Create a Python (fastapi) web application using the Wikipedia API that allows users to search for
Wikipedia articles based on a keyword. It should display the results and allow users to save their
favorite articles.
Use Gemini Pro (free quota should be enough) to auto-tag each saved article with relevant
categories.
Users should be able to view their saved articles on a separate page along with the LLM generated category tags. This page should also allow users to modify these category tags.
1. Implement Auth
2. Deploy the application on Netlify and Cockroach DB (free quota for both services should
be enough)
3. Use Langchain to invoke the LLM.
If any of the above (Wikipedia API, Netlify, Cockroach DB, Gemini Pro, Langchain) are not
working for you, choose appropriate alternatives and implement.



---------------
implement above EOD
------------
implement below tomorrow
Following are optional but you get extra points if you can demonstrate each of the following
capabilities:
1. Basic Front-end: Use React and use Material Design principles for all the pages
2. Make the app real-time using WebSockets


-----------------------

User journey
1. User signs up/ logs in
2. User enters keywords in the search bar
3. User views displayed results. User clicks on the bookmark icon displayed alongside each result
    a. clicking bookmark icon - triggers the LLM call. article id and tag is saved in the db(?) for the user
4. User clicks on the "bookmarks" page. Only their own saved articles should be visible to them. 
5. Article is displayed with category. User double clicks on the bookmark which leads to a new page. category is an editable field. updated category is saved in the db 


--------------

nice to haves

retry logic for gemini apis (lets start with)

The wikipedia Python library sometimes fails if it hits a disambiguation page (e.g., searching "Apple" might error because it doesn't know if you mean the fruit or the company).

dspy for tagging

-----------------
priority / to do list
1. log in/sign up
2. search + view results
3. tag
4. edit


