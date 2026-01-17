/**
 * js/upload.js
 * Handles File Upload logic (Drag & Drop).
 * - Drag & Drop events
 * - File validation
 * - Upload API call
 * - Recent uploads grid rendering
 */

// 1. STRICT AUTH CHECK
if (!api.isLoggedIn()) {
    window.location.href = "index.html?login=true";
}

document.addEventListener("DOMContentLoaded", () => {
  if (!api.isLoggedIn()) return;

  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input-field");
  const resultLinkInput = document.getElementById("result-link");
  const copyBtn = document.getElementById("copy-btn");
  const gridContainer = document.getElementById("my-gallery-grid");
  const dropText = document.querySelector(".drop-text");

  // VIEWER ELEMENTS
  const viewerBlock = document.getElementById("image-viewer");
  const viewerImg = document.getElementById("viewer-img");
  const viewerTitle = document.getElementById("viewer-title");
  const btnBack = document.getElementById("btn-back-gallery");
  const btnCopyViewer = document.getElementById("btn-copy-url-viewer");

  // Initial Load
  loadMyRecentGallery();

  // --- VIEWER LOGIC ---
  function openViewer(file) {
    if (!viewerBlock) return;
    viewerBlock.style.display = "block";
    document.querySelector('.upload-wrapper').style.display = 'none';

    const fullUrl = api.getImageUrl(file.url);
    viewerImg.src = fullUrl;
    viewerTitle.textContent = file.filename;

    // Copy Button in Viewer
    const newBtnCopy = btnCopyViewer.cloneNode(true);
    btnCopyViewer.parentNode.replaceChild(newBtnCopy, btnCopyViewer);
    newBtnCopy.addEventListener("click", () => {
      navigator.clipboard.writeText(fullUrl).then(() => {
        const oldText = newBtnCopy.textContent;
        newBtnCopy.textContent = "COPIED!";
        newBtnCopy.style.backgroundColor = "#10b981";
        setTimeout(() => {
          newBtnCopy.textContent = oldText;
          newBtnCopy.style.backgroundColor = "";
        }, 2000);
      });
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function closeViewer() {
    if (!viewerBlock) return;
    viewerBlock.style.display = "none";
    document.querySelector('.upload-wrapper').style.display = 'flex';
  }

  if (btnBack) btnBack.onclick = closeViewer;


  // --- DRAG & DROP VISUALS ---
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
  });

  // --- FILE HANDLING ---
  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  });

  fileInput.addEventListener('change', function() {
    handleFiles(this.files);
  });

  function handleFiles(files) {
    if (files.length > 0) {
      uploadFile(files[0]);
    }
  }

  // --- UPLOAD LOGIC ---
  async function uploadFile(file) {
    if (!file.type.startsWith('image/')) {
        alert("Only images are allowed!");
        return;
    }

    // UI: Start Upload
    dropZone.classList.add('uploading');
    const originalText = dropText.textContent;
    dropText.textContent = `Uploading ${file.name}...`;
    dropZone.style.pointerEvents = "none";

    try {
        const response = await api.uploadFile(file);

        // Success
        const fullUrl = api.getImageUrl(response.url);
        resultLinkInput.value = fullUrl;

        dropText.textContent = "Upload successful! Select another file.";

        // Refresh Gallery
        await loadMyRecentGallery();

    } catch (err) {
        console.error("Upload failed:", err);
        alert(`Upload failed: ${err.message}`);
        dropText.textContent = "Error. Try again.";
    } finally {
        // UI: Finish Upload
        dropZone.classList.remove('uploading');
        dropZone.style.pointerEvents = "auto";
        fileInput.value = "";
    }
  }

  // --- COPY LINK (Main Page) ---
  copyBtn.addEventListener("click", () => {
    const text = resultLinkInput.value;
    if (!text) return;

    navigator.clipboard.writeText(text).then(() => {
      const oldText = copyBtn.textContent;
      copyBtn.textContent = "COPIED!";
      copyBtn.style.backgroundColor = "#10b981";
      setTimeout(() => {
        copyBtn.textContent = oldText;
        copyBtn.style.backgroundColor = "";
      }, 2000);
    });
  });

  // --- GALLERY GRID LOGIC ---
  async function loadMyRecentGallery() {
      if (!gridContainer) return;

      try {
          const images = await api.get('/media/my?limit=9&offset=0');
          renderGrid(images);
      } catch (err) {
          console.error("Failed to load my gallery:", err);
      }
  }

  function renderGrid(images) {
      gridContainer.innerHTML = "";
      const count = images.length;

      if (count === 0) {
          gridContainer.innerHTML = "<p style='color: gray; text-align: center;'>No uploads yet.</p>";
          return;
      }

      // Smart Grid Layout Logic
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
