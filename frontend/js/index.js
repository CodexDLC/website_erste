// js/index.js
// Управляет главной страницей: Загрузка ленты, Маскот, Просмотр, Защита ссылки Upload

document.addEventListener("DOMContentLoaded", async () => {
  // --- ЭЛЕМЕНТЫ DOM ---
  const mascotBlock = document.getElementById("mascot-placeholder");
  const gridContainer = document.getElementById("home-gallery-grid");
  const viewerBlock = document.getElementById("image-viewer");
  const imgMascot = document.querySelector(".animals img");
  const showcaseBtn = document.querySelector(".showcase-btn"); // Кнопка перехода на Upload

  // Элементы внутри вьювера
  const viewerImg = document.getElementById("viewer-img");
  const viewerTitle = document.getElementById("viewer-title");
  const btnBack = document.getElementById("btn-back-gallery");
  const btnCopy = document.getElementById("btn-copy-url");

  // --- ЗАЩИТА ССЫЛКИ UPLOAD ---
  if (showcaseBtn) {
    showcaseBtn.addEventListener("click", (e) => {
      if (!api.isLoggedIn()) {
        e.preventDefault(); // Отменяем переход
        // Открываем модалку входа (через auth.js логику или напрямую)
        const modal = document.getElementById('login-modal');
        if (modal) {
            // Сбрасываем на логин
            const viewLogin = document.getElementById('view-login');
            const viewRegister = document.getElementById('view-register');
            if (viewLogin) viewLogin.style.display = 'block';
            if (viewRegister) viewRegister.style.display = 'none';

            modal.showModal();
        } else {
            alert("Please login to upload.");
        }
      }
    });
  }

  // --- ЗАГРУЗКА ДАННЫХ ---
  let images = [];
  try {
    images = await api.get('/media/feed?limit=50&offset=0');
  } catch (err) {
    console.error("Failed to load feed:", err);
  }

  const count = images.length;

  // --- ФУНКЦИЯ: ОТКРЫТЬ ПРОСМОТР ---
  function openViewer(file) {
    // Скрываем сетку, показываем вьювер
    gridContainer.style.display = "none";
    viewerBlock.style.display = "block";
    if (mascotBlock) mascotBlock.style.display = "none";

    // Заполняем данными
    // FIX: Используем api.getImageUrl для полного пути
    const fullUrl = api.getImageUrl(file.url);
    viewerImg.src = fullUrl;
    viewerTitle.textContent = file.filename;

    // Логика кнопки Copy
    const newBtnCopy = btnCopy.cloneNode(true);
    btnCopy.parentNode.replaceChild(newBtnCopy, btnCopy);

    newBtnCopy.addEventListener("click", () => {
      navigator.clipboard.writeText(fullUrl).then(() => {
        const oldText = newBtnCopy.textContent;
        newBtnCopy.textContent = "COPIED!";
        newBtnCopy.style.backgroundColor = "#10b981"; // Зеленый
        setTimeout(() => {
          newBtnCopy.textContent = oldText;
          newBtnCopy.style.backgroundColor = "";
        }, 2000);
      });
    });

    // Скролл наверх
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // --- ФУНКЦИЯ: ЗАКРЫТЬ ПРОСМОТР (НАЗАД) ---
  function closeViewer() {
    viewerBlock.style.display = "none";
    // Если картинок нет, показываем маскота, иначе сетку
    if (count > 0) {
        gridContainer.style.display = "flex";
    } else {
        if (mascotBlock) mascotBlock.style.display = "flex";
    }
  }

  if (btnBack) {
    btnBack.onclick = closeViewer;
  }

  // === ЛОГИКА ОТОБРАЖЕНИЯ ===

  // 1. ЕСЛИ ПУСТО
  if (count === 0) {
    if (mascotBlock) mascotBlock.style.display = "flex";
    if (gridContainer) gridContainer.style.display = "none";
    if (viewerBlock) viewerBlock.style.display = "none";

    // Рандомный маскот
    const mascots = ["berd.png", "cat.png", "dog.png", "dog2.png", "dog3.png"];
    if (imgMascot) {
      imgMascot.src = `data/img/${mascots[Math.floor(Math.random() * mascots.length)]}`;
    }
    return;
  }

  // 2. ЕСЛИ ЕСТЬ КАРТИНКИ (Рендерим сетку)
  if (mascotBlock) mascotBlock.style.display = "none";
  if (viewerBlock) viewerBlock.style.display = "none";

  if (gridContainer) {
    gridContainer.style.display = "flex";
    gridContainer.className = "smart-gallery";
    gridContainer.innerHTML = "";

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

    sliceSizes.forEach((size) => {
      const chunk = images.slice(currentIndex, currentIndex + size);
      currentIndex += size;

      const rowDiv = document.createElement("div");
      rowDiv.className = `gallery-row row-len-${chunk.length}`;

      chunk.forEach((file) => {
        const card = document.createElement("div");
        card.className = "gallery-card";
        card.onclick = () => openViewer(file);

        const img = document.createElement("img");
        // FIX: Используем api.getImageUrl для миниатюры
        img.src = api.getImageUrl(file.src);
        img.alt = file.filename;
        img.loading = "lazy";

        card.appendChild(img);
        rowDiv.appendChild(card);
      });

      gridContainer.appendChild(rowDiv);
    });
  }
});
