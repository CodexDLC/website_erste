/**
 * js/images.js
 * Manages "My Gallery" page logic.
 * - Loads user images
 * - Renders list view
 * - Handles Image Viewer (Modal)
 * - Deletion logic
 */

// 1. STRICT AUTH CHECK
if (!api.isLoggedIn()) {
    window.location.href = "index.html?login=true";
}

document.addEventListener("DOMContentLoaded", () => {
    if (!api.isLoggedIn()) return;

    const listContainer = document.getElementById("gallery-list");

    // VIEWER ELEMENTS
    const viewerBlock = document.getElementById("image-viewer");
    const viewerImg = document.getElementById("viewer-img");
    const viewerTitle = document.getElementById("viewer-title");
    const btnBack = document.getElementById("btn-back-gallery");
    const btnCopyViewer = document.getElementById("btn-copy-url-viewer");

    // Initial Load
    loadGalleryList();

    // --- VIEWER LOGIC ---
    function openViewer(file) {
        if (!viewerBlock) return;
        viewerBlock.style.display = "block";
        document.querySelector('.upload-wrapper').style.display = 'none';

        const fullUrl = api.getImageUrl(file.url);
        viewerImg.src = fullUrl;
        viewerTitle.textContent = file.filename;

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


    async function loadGalleryList() {
        try {
            const images = await api.get('/media/my?limit=100&offset=0');
            renderList(images);
        } catch (err) {
            console.error("Failed to load gallery:", err);
            listContainer.innerHTML = `<div style="padding: 20px; text-align: center; color: #ef4444;">Error loading gallery: ${err.message}</div>`;
        }
    }

    function renderList(images) {
        listContainer.innerHTML = "";

        if (images.length === 0) {
            listContainer.innerHTML = `<div style="padding: 40px; text-align: center; color: gray;">You haven't uploaded any images yet.</div>`;
            return;
        }

        images.forEach(file => {
            const item = createListItem(file);
            listContainer.appendChild(item);
        });
    }

    function createListItem(file) {
        const row = document.createElement("div");
        row.className = "list-item";

        // 1. NAME COLUMN
        const colName = document.createElement("div");
        colName.className = "col col-name";

        const iconDiv = document.createElement("div");
        iconDiv.className = "file-icon";
        iconDiv.style.cursor = "pointer";
        iconDiv.onclick = () => openViewer(file);

        const img = document.createElement("img");
        img.className = "thumbnail";
        img.src = api.getImageUrl(file.src);
        img.loading = "lazy";
        iconDiv.appendChild(img);

        const nameSpan = document.createElement("span");
        nameSpan.textContent = file.filename;
        nameSpan.style.overflow = "hidden";
        nameSpan.style.textOverflow = "ellipsis";
        nameSpan.style.cursor = "pointer";
        nameSpan.onclick = () => openViewer(file);

        colName.appendChild(iconDiv);
        colName.appendChild(nameSpan);

        // 2. URL COLUMN
        const colUrl = document.createElement("div");
        colUrl.className = "col col-url";
        const fullUrl = api.getImageUrl(file.url);
        colUrl.textContent = fullUrl;
        colUrl.title = fullUrl;

        // 3. ACTION COLUMN
        const colAction = document.createElement("div");
        colAction.className = "col col-action";

        // Button: Copy
        const btnCopy = document.createElement("button");
        btnCopy.className = "action-btn copy-btn-icon";
        btnCopy.title = "Copy URL";
        btnCopy.innerHTML = `<img src="data/img/copy-icon.svg" alt="C" onerror="this.style.display='none'; this.parentNode.textContent='📋'">`;

        btnCopy.onclick = () => {
            navigator.clipboard.writeText(fullUrl).then(() => {
                btnCopy.style.backgroundColor = "#10b981";
                setTimeout(() => btnCopy.style.backgroundColor = "", 1000);
            });
        };

        // Button: Delete
        const btnDelete = document.createElement("button");
        btnDelete.className = "action-btn delete-btn";
        btnDelete.title = "Delete Image";
        btnDelete.innerHTML = `<img src="data/img/trash-icon.svg" alt="D" onerror="this.style.display='none'; this.parentNode.textContent='🗑️'">`;

        btnDelete.onclick = async () => {
            if (confirm(`Delete ${file.filename}? This cannot be undone.`)) {
                try {
                    await api.delete(`/media/${file.id}`);
                    row.style.opacity = "0";
                    setTimeout(() => row.remove(), 300);
                } catch (err) {
                    alert("Delete failed: " + err.message);
                }
            }
        };

        colAction.appendChild(btnCopy);
        colAction.appendChild(btnDelete);

        row.appendChild(colName);
        row.appendChild(colUrl);
        row.appendChild(colAction);

        return row;
    }
});
