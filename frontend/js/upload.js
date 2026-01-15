// js/upload.js

document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("file-input-field");
  const dropZone = document.getElementById("drop-zone");
  const resultInput = document.getElementById("result-link");
  const copyBtn = document.getElementById("copy-btn");
  const galleryBtn = document.getElementById("gallery-tab-btn"); // Находим кнопку галереи

  // --- Функция: Проверяем, нужно ли показывать кнопку Images ---
  function checkGalleryStatus() {
    // Берем данные через функцию из storage.js
    const galleryData = getGalleryData();

    if (galleryData.length > 0) {
      // Если картинки есть — показываем кнопку (display: block или inline-block)
      if (galleryBtn) galleryBtn.style.display = "block";
    } else {
      // Если пусто — скрываем
      if (galleryBtn) galleryBtn.style.display = "none";
    }
  }

  // 1. Запускаем проверку сразу при загрузке страницы
  checkGalleryStatus();

  // --- Обработка инпута ---
  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      handleFiles(e.target.files);
    });
  }

  // --- Drag & Drop ---
  if (dropZone && fileInput) {
    // 1. Клик открывает выбор файлов (твоя новая фишка)
    dropZone.addEventListener("click", () => {
      fileInput.click();
    });

    // 2. ВАЖНО: Разрешаем перетаскивание (без этого drop не сработает!)
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("drag-over");
    });

    // 3. Убираем подсветку, если увели файл
    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("drag-over");
    });

    // 4. Обработка броска файла
    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("drag-over");
      // Важно остановить всплытие, чтобы не открылся клик
      e.stopPropagation();

      if (e.dataTransfer.files.length > 0) {
        handleFiles(e.dataTransfer.files);
      }
    });
  }

  // --- Логика обработки файлов ---
  function handleFiles(files) {
    const allowedTypes = ["image/jpeg", "image/png", "image/gif"];

    Array.from(files).forEach((file) => {
      if (!allowedTypes.includes(file.type)) {
        alert("File format not supported! Please use JPG, PNG or GIF.");
        return;
      }

      const reader = new FileReader();
      reader.onload = function (event) {
        const newRecord = {
          name: file.name,
          src: event.target.result,
          id: Date.now(),
        };

        saveImageToStorage(newRecord);

        if (resultInput) {
          resultInput.value = `https://sharefile.xyz/${file.name}`;
        }

        // 2. ВАЖНО: После успешной загрузки снова проверяем статус!
        // Кнопка "Images" должна появиться прямо сейчас
        checkGalleryStatus();

        alert("Uploaded successfully!");
      };
      reader.readAsDataURL(file);
    });
  }

  // --- Кнопка Копировать ---
  if (copyBtn && resultInput) {
    copyBtn.addEventListener("click", () => {
      if (resultInput.value) {
        navigator.clipboard
          .writeText(resultInput.value)
          .then(() => {
            const originalText = copyBtn.innerText;
            copyBtn.innerText = "COPIED!";
            setTimeout(() => {
              copyBtn.innerText = originalText;
            }, 2000);
          })
          .catch((err) => console.error("Copy failed", err));
      }
    });
  }
});
