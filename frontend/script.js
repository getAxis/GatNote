// API URL (твой бэкенд)
const API_URL = 'http://localhost:8000';
// ID пользователя (пока жестко зададим 1)
// TODO: потом добавим выбор пользователя
const USED_ID = 1;


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
    container.innerHTML = notes.map
}