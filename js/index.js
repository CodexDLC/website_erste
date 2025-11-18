// js/index.js

document.addEventListener('DOMContentLoaded', () => {
    // Список твоих картинок, которые лежат в data/img/
    // Имена должны совпадать с файлами в папке!
    const mascots = [
        'berd.png',
        'cat.png',
        'dog.png',
        'dog2.png',
        'dog3.png'
    ];

    const imgContainer = document.querySelector('.animals img');
    
    if (imgContainer) {
        // Выбираем случайный индекс
        const randomIndex = Math.floor(Math.random() * mascots.length);
        const selectedImage = mascots[randomIndex];
        
        // Устанавливаем путь
        imgContainer.src = `data/img/${selectedImage}`;
        imgContainer.alt = `Random mascot: ${selectedImage}`;
    }
});