# Notes Feature Design Spec

## Overview

Add a journal-style notes log to each Idea. Users can track progress over time by adding text notes (with optional images) or audio notes. Notes appear as a timeline on the idea detail screen.

## Data Model

### NoteEntry

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | PK |
| idea | ForeignKey → Idea | CASCADE delete |
| note_type | CharField | Choices: `text`, `audio` |
| text | TextField | Nullable. Used when `note_type='text'` |
| audio_file | FileField | Nullable. Upload to `ideas/notes/audio/`. Used when `note_type='audio'` |
| transcription | TextField | Nullable. Reserved for future audio-to-text feature |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

Ordering: `-created_at`

### NoteImage

| Field | Type | Details |
|-------|------|---------|
| id | AutoField | PK |
| note | ForeignKey → NoteEntry | CASCADE delete |
| image | ImageField | Upload to `ideas/notes/images/` |
| created_at | DateTimeField | auto_now_add |

NoteImage records are only valid when the parent NoteEntry has `note_type='text'`.

## API

All endpoints are nested under an idea.

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/ideas/{id}/notes/` | List all notes for an idea |
| POST | `/api/ideas/{id}/notes/` | Create a note |
| GET | `/api/ideas/{id}/notes/{note_id}/` | Get single note |
| PUT | `/api/ideas/{id}/notes/{note_id}/` | Update a note |
| DELETE | `/api/ideas/{id}/notes/{note_id}/` | Delete a note |

### Create text note (multipart/form-data)

```
note_type: "text"
text: "Made some progress on the layout"
images: [file1, file2, file3]   # optional, multiple files
```

### Create audio note (multipart/form-data)

```
note_type: "audio"
audio_file: <file>
```

### Response format

```json
{
  "id": 1,
  "idea": 5,
  "note_type": "text",
  "text": "Made some progress on the layout",
  "audio_file": null,
  "transcription": null,
  "images": [
    { "id": 1, "image": "/media/ideas/notes/images/photo1.jpg" },
    { "id": 2, "image": "/media/ideas/notes/images/photo2.jpg" }
  ],
  "created_at": "2026-04-08T12:00:00Z",
  "updated_at": "2026-04-08T12:00:00Z"
}
```

### Editing rules

- Text notes: only the `text` field is editable via PUT. Images cannot be modified — delete the note and recreate to change images.
- Audio notes: only the `audio_file` is replaceable via PUT.

## Mobile App UI

### Idea detail screen — timeline section

- Notes listed below existing idea info, ordered newest-first
- Text notes display: text content + image thumbnails (tappable for full size)
- Audio notes display: play button with duration indicator
- Each note shows a relative timestamp
- Long-press or swipe reveals edit/delete actions

### Input bar (bottom of idea detail screen)

- Default mode: text input field + "attach image" button + send button
- Attached images shown as small thumbnails above the input bar
- Microphone icon switches to audio recording mode
- Audio mode: record/stop button, discard, and send

## Constraints

- A note is either text or audio, never mixed
- NoteImages are only associated with text-type notes
- `transcription` field is present but unused until the audio-to-text feature is built
- Audio file formats: m4a (iOS default recording format)

## Future considerations

- Audio-to-text transcription (planned)
- Video attachments (not planned)
