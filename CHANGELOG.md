# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2023-10-27 (Release Candidate)
**Stabilization & Refactoring Phase.**
The project is now feature-complete and ready for MVP deployment.

### 🛠 Changed
- **Global Refactoring:** Implemented Clean Architecture (API -> Service -> Repository).
- **Logging:** Migrated to `loguru` with structured JSON logs for Grafana/Loki.
- **Nginx:** Split configuration into `nginx-main.conf` and `site.conf`. Added WAF Lite and Rate Limiting.
- **Docker:** Optimized `Dockerfile` (multi-stage build) and `docker-compose.prod.yml`.
- **Docs:** Updated README to be bilingual (EN/RU).

### 🐛 Fixed
- **Critical:** Fixed Race Condition in user registration.
- **Critical:** Fixed Circular Imports in SQLAlchemy models.
- **Critical:** Implemented missing Thumbnail generation and Garbage Collection.

---

## [0.0.4] - 2023-10-20 (Frontend Integration)
**Frontend Phase.**
Integration of Vanilla JS frontend with Backend API.

### 🚀 Added
- **Smart API Client:** `api.js` with auto-auth and error handling.
- **Auth UI:** Single-page Login/Register modal.
- **Gallery UI:** Grid view with Image Viewer and "Copy Link" feature.
- **Upload UI:** Drag & Drop zone with progress indication.

---

## [0.0.3] - 2023-10-15 (Media Domain)
**Core Logic Phase.**
Implementation of the image hosting engine.

### 🚀 Added
- **CAS Storage:** Content-Addressable Storage based on SHA-256 hash.
- **Deduplication:** Uploading the same file twice does not consume extra disk space.
- **API:** `/media/upload`, `/media/feed`, `/media/my`.
- **Validation:** Magic Bytes check (libmagic) to prevent non-image uploads.

---

## [0.0.2] - 2023-10-10 (Users Domain)
**Auth Phase.**
User management and security foundation.

### 🚀 Added
- **Auth:** JWT Access + Refresh Token rotation.
- **Models:** User, RefreshToken (SQLAlchemy).
- **API:** `/auth/register`, `/auth/login`, `/users/me`.
- **Security:** Password hashing with Bcrypt.

---

## [0.0.1] - 2023-10-01 (Foundation)
**Initial Commit.**

### 🚀 Added
- **Monorepo Structure:** `backend/`, `frontend/`, `nginx/`, `docs/`.
- **Core:** FastAPI setup, Asyncpg, Pydantic Settings.
- **Infrastructure:** Basic `docker-compose.yml` with PostgreSQL.
