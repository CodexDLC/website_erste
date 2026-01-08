// js/storage.js

const STORAGE_KEY = 'my_gallery_data';

// Получить список
function getGalleryData() {
    const rawData = localStorage.getItem(STORAGE_KEY);
    return rawData ? JSON.parse(rawData) : [];
}

// Сохранить файл
function saveImageToStorage(fileObj) {
    const currentGallery = getGalleryData();
    currentGallery.push(fileObj);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(currentGallery));
}

// Удалить файл
function removeImageFromStorage(index) {
    const list = getGalleryData();
    list.splice(index, 1); 
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}