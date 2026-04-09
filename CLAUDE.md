# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ideas Journal — a Django 5.2 app for tracking personal ideas. Provides both server-rendered template views and a REST API (Django REST Framework) with JWT authentication. Uses PostgreSQL.

## Mobile App (separate repo)

Expo/React Native app at `/Users/julia/dev/ideaappmobile`. Uses Axios + JWT auth against this backend's API. Key files:
- `app/services/api.ts` — Axios instance with token refresh interceptor
- `app/services/ideas.ts` — CRUD operations for ideas
- `app/services/notes.ts` — Notes API service
- `app/IdeaDetails.tsx` — Idea detail screen with notes timeline

**FormData gotcha:** React Native `FormData.append()` accepts `{ uri, name, type }` objects; browsers require `Blob`/`File`. Use `Platform.OS` check when uploading files. Send plain JSON when no file is attached.

## Common Commands

```bash
python manage.py runserver          # Start dev server
python manage.py test               # Run tests
python manage.py makemigrations     # Create migrations after model changes
python manage.py migrate            # Apply migrations
```

## Architecture

**Django project**: `justsite` (settings, root URLs)
**Apps**:
- `ideas` — Core app: Idea model, ViewSet (API), template views
- `api` — API URL routing via DRF's DefaultRouter

**URL structure**:
- `/api/ideas/` — REST CRUD (IdeaViewSet)
- `/api/token/` and `/api/token/refresh/` — JWT auth
- `/ideas/` — Server-rendered template views
- `/admin/` — Django admin

**Key flow**: The Idea model uses `django-model-utils` StatusField for status tracking (`new`, `in_progress`, `done`, `archived`). The API serializer exposes all model fields. Default ordering is `-updated_at`.

## Dependencies

Install with `pip install -r requirements.txt`. Key packages: Django, djangorestframework, djangorestframework-simplejwt, django-cors-headers, django-model-utils, Pillow, psycopg.

## Gotchas

- DRF `ImageField`/`FileField`: model-level `blank=True` doesn't make the serializer accept empty strings. Override `to_internal_value` to convert `""` → `None` if the client may send empty strings.

## Database

PostgreSQL on localhost:5432, database `ideas_db`. Credentials are hardcoded in settings.py.
