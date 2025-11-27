// js/index.js
// Управляет переключением: Маскот <-> Галерея <-> Просмотр

document.addEventListener('DOMContentLoaded', () => {
    // --- ЭЛЕМЕНТЫ DOM ---
    const mascotBlock = document.getElementById('mascot-placeholder');
    const gridContainer = document.getElementById('home-gallery-grid');
    const viewerBlock = document.getElementById('image-viewer');
    const imgMascot = document.querySelector('.animals img'); 
    
    // Элементы внутри вьювера
    const viewerImg = document.getElementById('viewer-img');
    const viewerTitle = document.getElementById('viewer-title');
    const btnBack = document.getElementById('btn-back-gallery');
    const btnCopy = document.getElementById('btn-copy-url');

    // --- ПРОВЕРКИ ---
    if (typeof getGalleryData !== 'function') {
        console.error('Ошибка: storage.js не подключен!');
        return;
    }

    const images = getGalleryData();
    const count = images.length;

    // --- ФУНКЦИЯ: ОТКРЫТЬ ПРОСМОТР ---
    function openViewer(file) {
        // Скрываем сетку, показываем вьювер
        gridContainer.style.display = 'none';
        viewerBlock.style.display = 'block';
        
        // Заполняем данными
        viewerImg.src = file.src;
        viewerTitle.textContent = file.name;

        // Логика кнопки Copy
        // Удаляем старые слушатели (клонированием), чтобы не плодить их
        const newBtnCopy = btnCopy.cloneNode(true);
        btnCopy.parentNode.replaceChild(newBtnCopy, btnCopy);
        
        newBtnCopy.addEventListener('click', () => {
             const fakeUrl = `https://sharefile.xyz/${file.name}`;
             navigator.clipboard.writeText(fakeUrl).then(() => {
                 const oldText = newBtnCopy.textContent;
                 newBtnCopy.textContent = 'COPIED!';
                 newBtnCopy.style.backgroundColor = '#10b981'; // Зеленый
                 setTimeout(() => {
                     newBtnCopy.textContent = oldText;
                     newBtnCopy.style.backgroundColor = ''; 
                 }, 2000);
             });
        });

        // Скролл наверх (для красоты)
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // --- ФУНКЦИЯ: ЗАКРЫТЬ ПРОСМОТР (НАЗАД) ---
    function closeViewer() {
        viewerBlock.style.display = 'none';
        gridContainer.style.display = 'flex'; // Возвращаем сетку
    }

    // Слушатель на кнопку "Back"
    if (btnBack) {
        btnBack.onclick = closeViewer;
    }

    // === ЛОГИКА ЗАГРУЗКИ СТРАНИЦЫ ===

    // 1. ЕСЛИ ПУСТО
    if (count === 0) {
        if (mascotBlock) mascotBlock.style.display = 'flex';
        if (gridContainer) gridContainer.style.display = 'none';
        if (viewerBlock) viewerBlock.style.display = 'none';

        // Рандомный маскот
        const mascots = ['berd.png', 'cat.png', 'dog.png', 'dog2.png', 'dog3.png'];
        if (imgMascot) {
            imgMascot.src = `data/img/${mascots[Math.floor(Math.random() * mascots.length)]}`;
        }
        return;
    }

    // 2. ЕСЛИ ЕСТЬ КАРТИНКИ (Рендерим сетку)
    if (mascotBlock) mascotBlock.style.display = 'none';
    if (viewerBlock) viewerBlock.style.display = 'none';
    
    if (gridContainer) {
        gridContainer.style.display = 'flex';
        gridContainer.className = 'smart-gallery';
        gridContainer.innerHTML = ''; 

        const recentImages = images.slice().reverse();

        // --- УМНАЯ НАРЕЗКА (Chunking) ---
        let sliceSizes = [];
        if (count === 3) sliceSizes = [2, 1];
        else if (count === 4) sliceSizes = [2, 2];
        else {
            let remaining = count;
            while (remaining > 0) {
                const size = remaining >= 3 ? 3 : remaining;
                sliceSizes.push(size);
                remaining -= size;
            }
        }

        // --- ОТРИСОВКА ---
        let currentIndex = 0;

        sliceSizes.forEach(size => {
            const chunk = recentImages.slice(currentIndex, currentIndex + size);
            currentIndex += size;

            const rowDiv = document.createElement('div');
            rowDiv.className = `gallery-row row-len-${chunk.length}`;
            
            chunk.forEach(file => {
                const card = document.createElement('div');
                card.className = 'gallery-card';
                
                // --- ВАЖНО: ТЕПЕРЬ МЫ НЕ ИДЕМ НА НОВУЮ СТРАНИЦУ ---
                // Мы вызываем функцию внутри этого же скрипта
                card.onclick = () => openViewer(file);

                const img = document.createElement('img');
                img.src = file.src;
                img.alt = file.name;
                
                card.appendChild(img);
                rowDiv.appendChild(card);
            });

            gridContainer.appendChild(rowDiv);
        });
    }
});