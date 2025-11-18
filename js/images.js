// js/images.js
// Скрипт отвечает за рендеринг (отрисовку) списка загруженных картинок

document.addEventListener('DOMContentLoaded', () => {
    const galleryList = document.getElementById('gallery-list');

    // Основная функция отрисовки галереи
    function renderGallery() {
        // 1. Очищаем текущий список, чтобы избежать дублей
        if (galleryList) galleryList.innerHTML = '';
        
        // 2. Безопасно получаем данные из storage.js
        const files = (typeof getGalleryData === 'function') ? getGalleryData() : [];

        if (!galleryList) return;

        // 3. Если файлов нет, показываем сообщение
        if (files.length === 0) {
            galleryList.innerHTML = '<div style="text-align:center; padding: 20px; color: #555;">List is empty</div>';
            return;
        }

        // 4. Проходимся циклом по каждому файлу и создаем HTML-строку
        files.forEach((file, index) => {
            const row = document.createElement('div');
            row.className = 'list-item'; // Класс для стилизации строки
            
            // Формируем фейковую ссылку для отображения
            const fileUrl = `https://sharefile.xyz/${file.name}`;

            // HTML верстка одной строки таблицы
            row.innerHTML = `
                <div class="col col-name">
                    <div class="file-icon">
                        <img src="${file.src}" alt="thumb" class="thumbnail">
                    </div>
                    <span title="${file.name}">${file.name}</span>
                </div>
                
                <div class="col col-url">
                    <a href="${fileUrl}" target="_blank" style="color: inherit;">${fileUrl}</a>
                </div>
                
                <div class="col col-action">
                    <button class="action-btn copy-btn-icon" onclick="copyUrl('${fileUrl}')" title="Copy Link">
                        <img src="data/img/copy-icon.png" alt="copy" onerror="this.style.display='none'">
                    </button>

                    <button class="action-btn delete-btn" onclick="deleteItem(${index})" title="Delete">
                        <img src="data/img/delete-icon.png" alt="del">
                    </button>
                </div>
            `;

            // Добавляем строку в общий контейнер
            galleryList.appendChild(row);
        });
    }

    // Функция: Копирование ссылки в буфер обмена
    window.copyUrl = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Link copied to clipboard! \nСсылка скопирована: ' + text);
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    };

    // Функция: Удаление картинки
    window.deleteItem = function(index) {
        if(confirm('Are you sure you want to delete this image?')) {
            removeImageFromStorage(index); // Вызов функции из storage.js
            renderGallery(); // Перерисовка списка после удаления
        }
    };

    // Запуск при загрузке страницы
    renderGallery();
});