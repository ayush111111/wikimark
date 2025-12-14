let token = localStorage.getItem('token');

if (!token) {
    window.location.href = '/static/index.html';
}

async function loadBookmarks() {
    const response = await fetch('/articles/', {
        headers: {'Authorization': `Bearer ${token}`}
    });
    
    const articles = await response.json();
    displayBookmarks(articles);
}

function displayBookmarks(articles) {
    const div = document.getElementById('bookmarks-list');
    
    if (articles.length === 0) {
        div.innerHTML = '<p>No bookmarks yet.</p>';
        return;
    }
    
    div.innerHTML = '';
    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'article';
        
        const currentTags = article.tags ? 
            (Array.isArray(article.tags) ? article.tags.join(', ') : article.tags) : '';
        
        const title = document.createElement('h4');
        title.textContent = article.title;
        
        const tagsDisplay = document.createElement('p');
        tagsDisplay.innerHTML = `<strong>Tags:</strong> ${currentTags}`;
        
        const tagsInput = document.createElement('input');
        tagsInput.type = 'text';
        tagsInput.value = currentTags;
        tagsInput.placeholder = 'Enter tags separated by commas';
        
        const saveBtn = document.createElement('button');
        saveBtn.textContent = 'Save Tags';
        saveBtn.onclick = () => updateTags(article.id, tagsInput.value);
        
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = () => deleteBookmark(article.id);
        
        articleDiv.appendChild(title);
        articleDiv.appendChild(tagsDisplay);
        articleDiv.appendChild(tagsInput);
        articleDiv.appendChild(saveBtn);
        articleDiv.appendChild(deleteBtn);
        
        if (article.url) {
            const link = document.createElement('a');
            link.href = article.url;
            link.target = '_blank';
            link.textContent = 'View on Wikipedia';
            articleDiv.appendChild(link);
        }
        
        div.appendChild(articleDiv);
    });
}

async function updateTags(articleId, newTagsStr) {
    const tagsArray = newTagsStr.split(',').map(t => t.trim()).filter(t => t);
    
    const response = await fetch(`/articles/${articleId}`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tags: tagsArray})
    });
    
    if (response.ok) {
        alert('Tags updated!');
        loadBookmarks();
    } else {
        alert('Failed to update');
    }
}

async function deleteBookmark(articleId) {
    if (!confirm('Delete this bookmark?')) return;
    
    const response = await fetch(`/articles/${articleId}`, {
        method: 'DELETE',
        headers: {'Authorization': `Bearer ${token}`}
    });
    
    if (response.ok) {
        loadBookmarks();
    } else {
        alert('Failed to delete');
    }
}

function goToSearch() {
    window.location.href = '/static/index.html';
}

loadBookmarks();