// API URL (твой бэкенд)
const API_URL = 'http://localhost:8000';
// ID пользователя (пока жестко зададим 1)
// TODO: потом добавим выбор пользователя
const USER_ID = 1;


// Загрузка заметок при открытии страницы
async function loadNotes() {
    try {
        const response = await fetch(`${API_URL}/notes/user/${USER_ID}`);
        const notes = await response.json();
        displayNotes(notes);
    } catch (error) {
        console.error('Ошибка загрузки заметок:', error);
    }
}

// Отображение загрузок на странице

function displayNotes(notes){
    const container = document.getElementById('notesContainer');

    if(notes.lenght === 0){
        container.innerHTML = '<div class="empty-state">📭 No notes here. You can create the first!</div>';
        return;
    }
    container.innerHTML = notes.map(note => `
        <div class="note-card" data-id="${note.id}">
            <div class="note-title">${escapeHtml(note.title)}</div>
            <div class="note-content">${escapeHtml(note.content)}</div>
            <div class="note-date">📅 ${new Date(note.created_at).toLocaleString()}</div>
            <button class="delete-btn" onclick="deleteNote(${note.id})">🗑 Delete</button>
        </div>
    `).join('');
}

//создание новой заметки

async function createNote() {
    const title = document.getElementById('titleInput').value;
    const content = document.getElementById('contentInput').value;

    if (!title || !content){
        alert('Заполните заголовок и текст заметки!');
        return;
    }

    try{
        const response = await fetch(`${API_URL}/notes/?user_id=${USER_ID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, content })
        });

        if (response.ok){
            // очистить форму
            document.getElementById('titleInput').value = '';
            document.getElementById('contentInput').value = '';
            // перезагрузить список
            loadNotes();
        } else{
            alert('Ошибка при создании заметки')
        }
    } catch(error){
        console.error('Ошибка:', error);
        alert('Не удалось создать заметку');
    }
    
}


// Удаление заметки
async function deleteNote(id) {
    if (confirm('Удалить заметку?')) {
        try {
            const response = await fetch(`${API_URL}/notes/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadNotes();
            } else {
                alert('Ошибка при удалении');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    }
}

// Защита от XSS (чтобы нельзя было вставить вредоносный код)
function escapeHtml(text){
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML
}

// Навесить обработчики после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    loadNotes();
    document.getElementById('saveBtn').addEventListener('click', createNote);
});