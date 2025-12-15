Requirements 
- Create a Python (fastapi) web application using the Wikipedia API that allows users to 
search for Wikipedia articles based on a keyword. It should display the results 
- It should allow users to save their favorite articles. 
- Use Gemini Pro (free quota should be enough) to auto-tag each saved article with relevant categories. 
- Users should be able to view their saved articles on a separate page along with the LLM generated category tags. 
- This page should also allow users to modify these category tags. 
- Implement Auth 
- Deploy the application on Netlify and Cockroach DB (free quota for both services should be enough)
- Use Langchain to invoke the LLM

Quick References
- Application link - https://wikimark.onrender.com/static/index.html
- FastAPI /docs - https://wikimark.onrender.com/docs
- Code - https://github.com/ayush111111/wikimark

Implementation details
- Application deployed on Render.com and CockroachDB 
- Login/Logout/Sign Up APIs implemented using ‘fastapi-users’ with JWT 
- Fallback handling for - disambiguation, spelling mistakes, use olf auto suggestions for missing articles.
- Async processing to improve search query processing 
- Future improvements - unit tests, rate limiting, retry mechanisms, linting (ruff), sqlalchemy session rollbacks(), websockets
