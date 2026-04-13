# Ideas App — Progress

## Backend (Django — ideas_journal)

1. **Project setup** — Django + PostgreSQL
2. **Idea model** — with statuses (`new`, `in_progress`, `done`, `archived`) and image field
3. **Admin panel** — ideas are editable via Django admin
4. **Template views** — server-rendered pages at `/ideas/`
5. **REST API** — Django REST Framework, full CRUD (`/api/ideas/`)
6. **Authentication** — JWT (SimpleJWT)
7. **CORS** — django-cors-headers, all origins allowed
8. **Sorting** — ideas ordered from newest to oldest
9. **Networking** — Pinggy tunnel support, then switched to direct Wi-Fi access
10. **Filter by status** — `?status=` query parameter on `/api/ideas/` endpoint (server-side filtering)
11. **Media serving** — `MEDIA_URL`/`MEDIA_ROOT` configured, dev server serves uploaded files
12. **Notes API** — nested CRUD at `/api/ideas/{id}/notes/` via `drf-nested-routers`, supports text+images and audio note types
13. **Media file cleanup** — Django signals (`pre_save`, `post_delete`) auto-delete orphaned files when images are replaced/cleared or models are deleted, including cascade deletes

## Mobile App (React Native/Expo — ideaappmobile)

1. **Expo** with expo-router navigation
2. **Authentication** — login screen, JWT tokens in AsyncStorage
3. **Ideas list** — loaded from API
4. **Idea details screen** — all fields including status and image
5. **Create idea**
6. **Edit idea** with status dropdown
7. **Delete idea**
8. **Custom theme and styles**
9. **Navigation** — titles, back buttons
10. **API client** — axios with token interceptor and auto-refresh
11. **Status color indicators** — colored left border in the ideas list + colored status text on the details screen (`new` — blue, `in_progress` — orange, `done` — green, `archived` — gray). Colors extracted to shared `constants.ts`
12. **Filter by status** — chip row above the ideas list (All, new, in_progress, done, archived) with color-coded active states, server-side filtering via API
13. **Main image upload** — image picker (expo-image-picker) on AddIdea and EditIdea screens, multipart/form-data uploads, image preview on details screen
14. **Notes timeline** — chat-style notes on idea details screen with text+image and audio note types, inline audio playback, NoteInput bar with text/image/audio modes
15. **Clay design system** — warm cream backgrounds, oat borders, multi-layer clay shadows, swatch palette (Ube, Matcha, Slushie, Lemon, Pomegranate, Blueberry). Applied to all screens: login, ideas list, idea details, add/edit forms, notes, home
16. **Home screen** — big stacked card-style buttons for easy tapping ("I have an Idea" primary ube, "Dive into Ideas" secondary white)
17. **Persistent Home button** — home icon in header on all screens except index
18. **Desktop width limit** — app content capped at 480px and centered for browser testing
19. **Smooth filter switching** — no full-screen spinner when changing status filters, stale list stays visible while new data loads

## Infrastructure

- Pinggy tunnel (replaced with direct LAN access)
- Obsidian note with instructions for connecting mobile to local server

---

Both parts work end-to-end: login, list, create, view, edit, delete ideas with notes.
