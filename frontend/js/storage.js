/**
 * js/storage.js
 * LocalStorage wrapper for offline gallery data (Legacy/Fallback).
 * Currently used only if backend is unavailable or for caching.
 */

const STORAGE_KEY = "my_gallery_data";

/**
 * Retrieve gallery data from LocalStorage.
 * @returns {Array} List of image objects.
 */
function getGalleryData() {
  const rawData = localStorage.getItem(STORAGE_KEY);
  return rawData ? JSON.parse(rawData) : [];
}

/**
 * Save a new image object to LocalStorage.
 * @param {object} fileObj
 */
function saveImageToStorage(fileObj) {
  const currentGallery = getGalleryData();
  currentGallery.push(fileObj);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(currentGallery));
}

/**
 * Remove an image from LocalStorage by index.
 * @param {number} index
 */
function removeImageFromStorage(index) {
  const list = getGalleryData();
  list.splice(index, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}
