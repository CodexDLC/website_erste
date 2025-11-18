// js/images.js

document.addEventListener('DOMContentLoaded', () => {
    // Находим контейнер, куда будем вставлять строки
    const galleryList = document.getElementById('gallery-list');

    // Функция отрисовки списка
    function renderGallery() {
        // Очищаем список перед обновлением
        galleryList.innerHTML = '';

        // Получаем данные через storage.js
        const files = getGalleryData();

        // Если файлов нет
        if (files.length === 0) {
            galleryList.innerHTML = '<div style="text-align:center; padding: 20px; color: #555;">List is empty</div>';
            return;
        }

        // Проходимся по каждому файлу
        files.forEach((file, index) => {
            const row = document.createElement('div');
            row.className = 'list-item';

            row.innerHTML = `
                <div class="col col-name">
                    <div class="file-icon">
                         <img src="data/img/image-icon.png" alt="img" onerror="this.style.display='none'">
                    </div>
                    <span title="${file.name}">${file.name}</span>
                </div>
                
                <div class="col col-url">
                    <a href="https://sharefile.xyz/${file.name}" target="_blank" style="color: inherit;">https://sharefile.xyz/${file.name}</a>
                </div>
                
                <div class="col col-action">
                    <button class="delete-btn" onclick="deleteItem(${index})">
                        <img src="data/img/delete-icon.png" alt="del">
                    </button>
                </div>
            `;

            galleryList.appendChild(row);
        });
    }

    // Глобальная функция удаления
    window.deleteItem = function(index) {
        if(confirm('Delete this image?')) {
            removeImageFromStorage(index); // Из storage.js
            renderGallery(); // Перерисовываем
        }
    };

    // Запускаем отрисовку
    renderGallery();
});