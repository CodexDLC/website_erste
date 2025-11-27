// js/index.js

document.addEventListener('DOMContentLoaded', () => {
    // Получаем оба элемента
    const mascotBlock = document.getElementById('mascot-placeholder');
    const gridContainer = document.getElementById('home-gallery-grid');
    const imgMascot = document.querySelector('.animals img'); // Для смены картинки маскота
    
    // Безопасная проверка хранилища
    if (typeof getGalleryData !== 'function') {
        console.error('Storage system missing');
        return;
    }

    const images = getGalleryData();
    const count = images.length;

    // === СЦЕНАРИЙ 1: ГАЛЕРЕЯ ПУСТА (Показываем Маскота) ===
    if (count === 0) {
        if (mascotBlock) mascotBlock.style.display = 'flex'; // Показываем маскота
        if (gridContainer) gridContainer.style.display = 'none'; // Скрываем сетку

        // Твой старый код для рандомного маскота
        const mascots = ['berd.png', 'cat.png', 'dog.png', 'dog2.png', 'dog3.png'];
        if (imgMascot) {
            const randomIndex = Math.floor(Math.random() * mascots.length);
            const selectedImage = mascots[randomIndex];
            imgMascot.src = `data/img/${selectedImage}`;
            imgMascot.alt = `Mascot: ${selectedImage}`;
        }
        return; // На этом все, дальше код не выполняем
    }

    // === СЦЕНАРИЙ 2: ЕСТЬ КАРТИНКИ (Показываем Сетку) ===
    if (mascotBlock) mascotBlock.style.display = 'none'; // Скрываем маскота
    
    if (gridContainer) {
        // Сбрасываем display, чтобы сработал CSS Grid/Flex из классов
        gridContainer.style.display = ''; 
        gridContainer.className = 'smart-gallery'; // Сброс классов

        // Назначаем Layout (раскладку)
        if (count === 1) gridContainer.classList.add('layout-1');
        else if (count === 2) gridContainer.classList.add('layout-2');
        else if (count === 3) gridContainer.classList.add('layout-3');
        else if (count === 4) gridContainer.classList.add('layout-4');
        else if (count === 5) gridContainer.classList.add('layout-5');
        else if (count === 6) gridContainer.classList.add('layout-6');

        // Рендерим картинки (новые сверху)
        const recentImages = images.slice().reverse();

        recentImages.forEach(file => {
            const card = document.createElement('div');
            card.className = 'gallery-card';
            
            // Клик пока простой alert, позже заменим на открытие
            card.onclick = () => {
                alert('Opening image: ' + file.name);
            };

            const img = document.createElement('img');
            img.src = file.src;
            img.alt = file.name;
            
            card.appendChild(img);
            gridContainer.appendChild(card);
        });
    }
});