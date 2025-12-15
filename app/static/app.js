let token = localStorage.getItem('token');

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    formData.append('grant_type', 'password');
    
    try {
        const response = await fetch('/auth/jwt/login', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('token', token);
            
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('search-section').style.display = 'block';
            document.getElementById('auth-status').textContent = 'Logged in!';
        } else {
            document.getElementById('auth-status').textContent = 'Login failed';
        }
    } catch (error) {
        document.getElementById('auth-status').textContent = 'Error: ' + error;
    }
}

async function search() {
    const query = document.getElementById('search-query').value;
    
    const response = await fetch(`/wiki/search-rest?query=${query}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const articles = await response.json();
    displayResults(articles);
}

function displayResults(articles) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h3>Results:</h3>';
    
    articles.forEach(article => {
        const div = document.createElement('div');
        div.className = 'article';
        
        const title = document.createElement('h4');
        title.textContent = article.title;
        
        const summary = document.createElement('p');
        summary.textContent = article.summary ? article.summary.substring(0, 200) + '...' : 'No summary';
        
        const bookmarkBtn = document.createElement('button');
        bookmarkBtn.textContent = 'Bookmark';
        bookmarkBtn.onclick = () => bookmark(article.key);  // key instead
        
        div.appendChild(title);
        div.appendChild(summary);
        div.appendChild(bookmarkBtn);
        resultsDiv.appendChild(div);
    });
}
async function bookmark(key) {
    const response = await fetch(`/articles/?article_key=${encodeURIComponent(key)}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (response.ok) {
        alert('Bookmarked!');
    } else {
        alert('Failed to bookmark');
    }
}

function goToBookmarks() {
    window.location.href = '/static/bookmarks.html';
}

if (token) {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('search-section').style.display = 'block';
}

function showSignup() {
    document.querySelector('#auth-section > h2').style.display = 'none';
    document.getElementById('email').style.display = 'none';
    document.getElementById('password').style.display = 'none';
    document.querySelector('#auth-section > button:nth-of-type(1)').style.display = 'none';
    document.querySelector('#auth-section > button:nth-of-type(2)').style.display = 'none';
    document.getElementById('signup-form').style.display = 'block';
}

function showLogin() {
    document.querySelector('#auth-section > h2').style.display = 'block';
    document.getElementById('email').style.display = 'block';
    document.getElementById('password').style.display = 'block';
    document.querySelector('#auth-section > button:nth-of-type(1)').style.display = 'inline-block';
    document.querySelector('#auth-section > button:nth-of-type(2)').style.display = 'inline-block';
    document.getElementById('signup-form').style.display = 'none';
}

async function signup() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    
    const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password})
    });
    
    if (response.ok) {
        document.getElementById('auth-status').textContent = 'Account created! Please login.';
        showLogin();
    } else {
        document.getElementById('auth-status').textContent = 'Signup failed';
    }
}
function logout() {
    localStorage.removeItem('token');
    token = null;
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('search-section').style.display = 'none';
    document.getElementById('results').innerHTML = '';
}