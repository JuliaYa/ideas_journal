# Notes Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add journal-style notes (text+images or audio) to Ideas, with a nested REST API and a chat-like input UI on the idea detail screen.

**Architecture:** Two new Django models (NoteEntry, NoteImage) in the existing `ideas` app. Nested DRF viewset under `/api/ideas/{id}/notes/`. Mobile app gets a new notes service, timeline component on IdeaDetails, and a chat-style input bar. Audio recording via `expo-av`.

**Tech Stack:** Django 5.2, DRF, `drf-nested-routers`, Expo SDK 54, `expo-av`, `expo-image-picker`, React Native Paper

---

### Task 1: Backend — NoteEntry and NoteImage models

**Files:**
- Modify: `/Users/julia/dev/ideas_journal/ideas/models.py`
- Create: `/Users/julia/dev/ideas_journal/ideas/migrations/0004_noteentry_noteimage.py` (auto-generated)

- [ ] **Step 1: Add NoteEntry and NoteImage models**

Add to `ideas/models.py` after the `Idea` class:

```python
class NoteEntry(models.Model):
    NOTE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('audio', 'Audio'),
    ]

    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=5, choices=NOTE_TYPE_CHOICES)
    text = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='ideas/notes/audio/', null=True, blank=True)
    transcription = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class NoteImage(models.Model):
    note = models.ForeignKey(NoteEntry, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ideas/notes/images/')
    created_at = models.DateTimeField(auto_now_add=True)
```

- [ ] **Step 2: Generate and apply migration**

Run:
```bash
cd /Users/julia/dev/ideas_journal
python manage.py makemigrations ideas
python manage.py migrate
```

Expected: Migration `0004_noteentry_noteimage` created and applied.

- [ ] **Step 3: Commit**

```bash
git add ideas/models.py ideas/migrations/0004_*.py
git commit -m "feat: add NoteEntry and NoteImage models"
```

---

### Task 2: Backend — Serializers for notes

**Files:**
- Modify: `/Users/julia/dev/ideas_journal/ideas/serializers.py`

- [ ] **Step 1: Add NoteImage and NoteEntry serializers**

Add to `ideas/serializers.py`:

```python
from .models import Idea, NoteEntry, NoteImage


class NoteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteImage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class NoteEntrySerializer(serializers.ModelSerializer):
    images = NoteImageSerializer(many=True, read_only=True)

    class Meta:
        model = NoteEntry
        fields = ['id', 'idea', 'note_type', 'text', 'audio_file', 'transcription', 'images', 'created_at', 'updated_at']
        read_only_fields = ['id', 'idea', 'transcription', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context['request']
        note = NoteEntry.objects.create(**validated_data)
        images = request.FILES.getlist('images')
        for img in images:
            NoteImage.objects.create(note=note, image=img)
        return note
```

Also update the existing import at the top of the file from `from .models import Idea` to `from .models import Idea, NoteEntry, NoteImage`.

- [ ] **Step 2: Commit**

```bash
git add ideas/serializers.py
git commit -m "feat: add NoteEntry and NoteImage serializers"
```

---

### Task 3: Backend — Notes ViewSet and URL routing

**Files:**
- Modify: `/Users/julia/dev/ideas_journal/ideas/views.py`
- Modify: `/Users/julia/dev/ideas_journal/api/urls.py`
- Modify: `/Users/julia/dev/ideas_journal/requirements.txt` (add drf-nested-routers)

- [ ] **Step 1: Install drf-nested-routers**

```bash
cd /Users/julia/dev/ideas_journal
pip install drf-nested-routers
```

Add `drf-nested-routers` to `requirements.txt`.

- [ ] **Step 2: Add NoteEntryViewSet to views.py**

Add to `ideas/views.py`:

```python
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import IdeaSerializer, NoteEntrySerializer
from .models import Idea, NoteEntry


class NoteEntryViewSet(viewsets.ModelViewSet):
    serializer_class = NoteEntrySerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return NoteEntry.objects.filter(idea_id=self.kwargs['idea_pk'])

    def perform_create(self, serializer):
        serializer.save(idea_id=self.kwargs['idea_pk'])
```

- [ ] **Step 3: Update api/urls.py with nested routing**

Replace `api/urls.py` contents:

```python
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from ideas.views import IdeaViewSet, NoteEntryViewSet

router = routers.DefaultRouter()
router.register(r'ideas', IdeaViewSet)

ideas_router = nested_routers.NestedDefaultRouter(router, r'ideas', lookup='idea')
ideas_router.register(r'notes', NoteEntryViewSet, basename='idea-notes')

urlpatterns = router.urls + ideas_router.urls
```

- [ ] **Step 4: Verify endpoints work**

Run:
```bash
python manage.py runserver
```

Test with curl:
```bash
# List notes for idea 1
curl http://localhost:8000/api/ideas/1/notes/

# Create a text note
curl -X POST http://localhost:8000/api/ideas/1/notes/ \
  -F "note_type=text" \
  -F "text=First progress note"
```

Expected: 200/201 responses with JSON.

- [ ] **Step 5: Commit**

```bash
git add ideas/views.py api/urls.py requirements.txt
git commit -m "feat: add notes API with nested routing under ideas"
```

---

### Task 4: Backend — Register NoteEntry in Django admin

**Files:**
- Modify: `/Users/julia/dev/ideas_journal/ideas/admin.py`

- [ ] **Step 1: Add NoteEntry and NoteImage to admin**

```python
from django.contrib import admin
from .models import Idea, NoteEntry, NoteImage


class NoteImageInline(admin.TabularInline):
    model = NoteImage
    extra = 0


@admin.register(NoteEntry)
class NoteEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'idea', 'note_type', 'created_at']
    list_filter = ['note_type', 'created_at']
    inlines = [NoteImageInline]


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'created_at']
    list_filter = ['status']
```

- [ ] **Step 2: Commit**

```bash
git add ideas/admin.py
git commit -m "feat: register NoteEntry and NoteImage in Django admin"
```

---

### Task 5: Mobile — Install expo-av and add notes service

**Files:**
- Modify: `/Users/julia/dev/ideaappmobile/package.json` (via npm)
- Create: `/Users/julia/dev/ideaappmobile/app/services/notes.ts`

- [ ] **Step 1: Install expo-av**

```bash
cd /Users/julia/dev/ideaappmobile
npx expo install expo-av
```

- [ ] **Step 2: Create notes service**

Create `/Users/julia/dev/ideaappmobile/app/services/notes.ts`:

```typescript
import { Platform } from 'react-native';
import api from './api';

export type NoteImage = {
  id: number;
  image: string;
  created_at: string;
};

export type NoteEntry = {
  id: number;
  idea: number;
  note_type: 'text' | 'audio';
  text: string | null;
  audio_file: string | null;
  transcription: string | null;
  images: NoteImage[];
  created_at: string;
  updated_at: string;
};

export async function getNotes(ideaId: string): Promise<NoteEntry[]> {
  const res = await api.get(`/ideas/${ideaId}/notes/`);
  return res.data;
}

export async function createTextNote(
  ideaId: string,
  text: string,
  imageUris: string[]
): Promise<NoteEntry> {
  if (imageUris.length > 0) {
    const form = new FormData();
    form.append('note_type', 'text');
    form.append('text', text);
    for (const uri of imageUris) {
      const filename = uri.split('/').pop() || 'photo.jpg';
      const ext = filename.split('.').pop()?.toLowerCase() || 'jpg';
      const mimeType = ext === 'png' ? 'image/png' : 'image/jpeg';
      if (Platform.OS === 'web') {
        const response = await fetch(uri);
        const blob = await response.blob();
        form.append('images', blob, filename);
      } else {
        form.append('images', { uri, name: filename, type: mimeType } as any);
      }
    }
    const res = await api.post(`/ideas/${ideaId}/notes/`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  }
  const res = await api.post(`/ideas/${ideaId}/notes/`, {
    note_type: 'text',
    text,
  });
  return res.data;
}

export async function createAudioNote(
  ideaId: string,
  audioUri: string
): Promise<NoteEntry> {
  const form = new FormData();
  form.append('note_type', 'audio');
  const filename = audioUri.split('/').pop() || 'recording.m4a';
  if (Platform.OS === 'web') {
    const response = await fetch(audioUri);
    const blob = await response.blob();
    form.append('audio_file', blob, filename);
  } else {
    form.append('audio_file', {
      uri: audioUri,
      name: filename,
      type: 'audio/m4a',
    } as any);
  }
  const res = await api.post(`/ideas/${ideaId}/notes/`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

export async function updateNote(
  ideaId: string,
  noteId: number,
  text: string
): Promise<NoteEntry> {
  const res = await api.put(`/ideas/${ideaId}/notes/${noteId}/`, {
    note_type: 'text',
    text,
  });
  return res.data;
}

export async function deleteNote(
  ideaId: string,
  noteId: number
): Promise<void> {
  await api.delete(`/ideas/${ideaId}/notes/${noteId}/`);
}
```

- [ ] **Step 3: Commit**

```bash
cd /Users/julia/dev/ideaappmobile
git add package.json app/services/notes.ts
git commit -m "feat: add expo-av dependency and notes API service"
```

---

### Task 6: Mobile — NoteTimeline component

**Files:**
- Create: `/Users/julia/dev/ideaappmobile/app/components/NoteTimeline.tsx`

- [ ] **Step 1: Create NoteTimeline component**

This component renders the list of notes for an idea. It handles text notes (with image thumbnails) and audio notes (with a play button).

Create `/Users/julia/dev/ideaappmobile/app/components/NoteTimeline.tsx`:

```tsx
import React, { useState } from 'react';
import { Alert, Image, Pressable, StyleSheet, View } from 'react-native';
import { Text, IconButton } from 'react-native-paper';
import { Audio } from 'expo-av';
import { NoteEntry } from '../services/notes';

type Props = {
  notes: NoteEntry[];
  onDelete: (noteId: number) => void;
  onEdit: (note: NoteEntry) => void;
};

function formatTimestamp(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

function AudioPlayer({ uri }: { uri: string }) {
  const [playing, setPlaying] = useState(false);
  const [sound, setSound] = useState<Audio.Sound | null>(null);

  const togglePlay = async () => {
    if (playing && sound) {
      await sound.pauseAsync();
      setPlaying(false);
      return;
    }
    if (sound) {
      await sound.playAsync();
      setPlaying(true);
      return;
    }
    const { sound: newSound } = await Audio.Sound.createAsync({ uri });
    setSound(newSound);
    newSound.setOnPlaybackStatusUpdate((status) => {
      if (status.isLoaded && status.didJustFinish) {
        setPlaying(false);
      }
    });
    await newSound.playAsync();
    setPlaying(true);
  };

  return (
    <Pressable onPress={togglePlay} style={styles.audioRow}>
      <IconButton icon={playing ? 'pause-circle' : 'play-circle'} size={32} />
      <Text variant="bodyMedium">Audio note</Text>
    </Pressable>
  );
}

function NoteItem({ note, onDelete, onEdit }: { note: NoteEntry; onDelete: () => void; onEdit: () => void }) {
  const confirmDelete = () => {
    Alert.alert('Delete note', 'Are you sure?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Delete', style: 'destructive', onPress: onDelete },
    ]);
  };

  return (
    <View style={styles.noteCard}>
      <View style={styles.noteHeader}>
        <Text variant="labelSmall" style={styles.timestamp}>
          {formatTimestamp(note.created_at)}
        </Text>
        <View style={styles.actions}>
          {note.note_type === 'text' && (
            <IconButton icon="pencil" size={16} onPress={onEdit} />
          )}
          <IconButton icon="delete" size={16} onPress={confirmDelete} />
        </View>
      </View>

      {note.note_type === 'text' && (
        <>
          {note.text && <Text variant="bodyMedium" style={styles.noteText}>{note.text}</Text>}
          {note.images.length > 0 && (
            <View style={styles.imageRow}>
              {note.images.map((img) => (
                <Image key={img.id} source={{ uri: img.image }} style={styles.thumbnail} />
              ))}
            </View>
          )}
        </>
      )}

      {note.note_type === 'audio' && note.audio_file && (
        <AudioPlayer uri={note.audio_file} />
      )}
    </View>
  );
}

export default function NoteTimeline({ notes, onDelete, onEdit }: Props) {
  if (notes.length === 0) {
    return <Text variant="bodySmall" style={styles.empty}>No notes yet</Text>;
  }

  return (
    <View>
      {notes.map((note) => (
        <NoteItem
          key={note.id}
          note={note}
          onDelete={() => onDelete(note.id)}
          onEdit={() => onEdit(note)}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  noteCard: {
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
  },
  noteHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  timestamp: { color: '#888' },
  actions: { flexDirection: 'row' },
  noteText: { marginTop: 4 },
  imageRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginTop: 8,
  },
  thumbnail: {
    width: 80,
    height: 80,
    borderRadius: 6,
  },
  audioRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  empty: {
    color: '#aaa',
    textAlign: 'center',
    marginVertical: 20,
  },
});
```

- [ ] **Step 2: Commit**

```bash
cd /Users/julia/dev/ideaappmobile
git add app/components/NoteTimeline.tsx
git commit -m "feat: add NoteTimeline component with audio playback"
```

---

### Task 7: Mobile — NoteInput component

**Files:**
- Create: `/Users/julia/dev/ideaappmobile/app/components/NoteInput.tsx`

- [ ] **Step 1: Create NoteInput component**

This is the chat-style input bar at the bottom of the idea detail screen. Default mode is text + image attach. Mic icon switches to audio recording mode.

Create `/Users/julia/dev/ideaappmobile/app/components/NoteInput.tsx`:

```tsx
import React, { useState, useRef } from 'react';
import { Image, StyleSheet, View } from 'react-native';
import { IconButton, TextInput } from 'react-native-paper';
import * as ImagePicker from 'expo-image-picker';
import { Audio } from 'expo-av';

type Props = {
  onSendText: (text: string, imageUris: string[]) => Promise<void>;
  onSendAudio: (audioUri: string) => Promise<void>;
};

export default function NoteInput({ onSendText, onSendAudio }: Props) {
  const [mode, setMode] = useState<'text' | 'audio'>('text');
  const [text, setText] = useState('');
  const [imageUris, setImageUris] = useState<string[]>([]);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [sending, setSending] = useState(false);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsMultipleSelection: true,
      quality: 0.8,
    });
    if (!result.canceled) {
      setImageUris((prev) => [...prev, ...result.assets.map((a) => a.uri)]);
    }
  };

  const removeImage = (index: number) => {
    setImageUris((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSendText = async () => {
    if (!text.trim() && imageUris.length === 0) return;
    setSending(true);
    try {
      await onSendText(text, imageUris);
      setText('');
      setImageUris([]);
    } finally {
      setSending(false);
    }
  };

  const startRecording = async () => {
    await Audio.requestPermissionsAsync();
    await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
    const { recording: rec } = await Audio.Recording.createAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );
    setRecording(rec);
  };

  const stopAndSend = async () => {
    if (!recording) return;
    setSending(true);
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      if (uri) await onSendAudio(uri);
    } finally {
      setSending(false);
      setMode('text');
    }
  };

  const discardRecording = async () => {
    if (recording) {
      await recording.stopAndUnloadAsync();
      setRecording(null);
    }
    setMode('text');
  };

  if (mode === 'audio') {
    return (
      <View style={styles.container}>
        <View style={styles.audioBar}>
          <IconButton icon="close" onPress={discardRecording} disabled={sending} />
          {recording ? (
            <IconButton icon="stop-circle" iconColor="#e53935" size={36} onPress={stopAndSend} disabled={sending} />
          ) : (
            <IconButton icon="record-circle" iconColor="#e53935" size={36} onPress={startRecording} />
          )}
          {recording && (
            <IconButton icon="send" onPress={stopAndSend} disabled={sending} />
          )}
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {imageUris.length > 0 && (
        <View style={styles.previewRow}>
          {imageUris.map((uri, i) => (
            <View key={i} style={styles.previewWrap}>
              <Image source={{ uri }} style={styles.previewImage} />
              <IconButton icon="close-circle" size={16} style={styles.removeBtn} onPress={() => removeImage(i)} />
            </View>
          ))}
        </View>
      )}
      <View style={styles.inputRow}>
        <IconButton icon="image-plus" onPress={pickImage} disabled={sending} />
        <TextInput
          mode="outlined"
          placeholder="Add a note..."
          value={text}
          onChangeText={setText}
          style={styles.textInput}
          dense
        />
        <IconButton icon="microphone" onPress={() => setMode('audio')} disabled={sending} />
        <IconButton icon="send" onPress={handleSendText} disabled={sending || (!text.trim() && imageUris.length === 0)} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    backgroundColor: '#fff',
    paddingHorizontal: 4,
    paddingVertical: 4,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  textInput: {
    flex: 1,
    backgroundColor: 'transparent',
  },
  previewRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    paddingHorizontal: 8,
    paddingTop: 6,
  },
  previewWrap: { position: 'relative' },
  previewImage: {
    width: 56,
    height: 56,
    borderRadius: 6,
  },
  removeBtn: {
    position: 'absolute',
    top: -8,
    right: -8,
  },
  audioBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
```

- [ ] **Step 2: Commit**

```bash
cd /Users/julia/dev/ideaappmobile
git add app/components/NoteInput.tsx
git commit -m "feat: add NoteInput component with text, image, and audio modes"
```

---

### Task 8: Mobile — Integrate notes into IdeaDetails screen

**Files:**
- Modify: `/Users/julia/dev/ideaappmobile/app/IdeaDetails.tsx`

- [ ] **Step 1: Add notes state, fetching, and CRUD handlers**

Replace the contents of `IdeaDetails.tsx` with:

```tsx
import { useLocalSearchParams, useRouter, useNavigation } from 'expo-router';
import React, { useCallback, useEffect, useState } from 'react';
import { Image, Pressable, ScrollView, StyleSheet, View, KeyboardAvoidingView, Platform } from 'react-native';
import { ActivityIndicator, Button, Snackbar, Text } from 'react-native-paper';
import { getIdea, deleteIdea, Idea } from './services/ideas';
import { getNotes, createTextNote, createAudioNote, updateNote, deleteNote, NoteEntry } from './services/notes';
import { Ionicons } from '@expo/vector-icons';
import { STATUS_COLORS } from './constants';
import NoteTimeline from './components/NoteTimeline';
import NoteInput from './components/NoteInput';

export default function IdeaDetailsScreen() {
  const router = useRouter();
  const navigation = useNavigation();
  const [idea, setIdea] = useState<Idea>();
  const [notes, setNotes] = useState<NoteEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [editingNote, setEditingNote] = useState<NoteEntry | null>(null);

  const { id } = useLocalSearchParams<{ id: string }>();

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (!id) throw new Error('Missing idea id');
      const [ideaData, notesData] = await Promise.all([
        getIdea(id),
        getNotes(id),
      ]);
      setIdea(ideaData as Idea);
      setNotes(notesData);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, [id]);

  const deleteItem = async () => {
    setLoading(true);
    setError(null);
    try {
      if (!id) throw new Error('Missing idea id');
      await deleteIdea(id);
      router.push('/IdeasList');
    } catch (err: any) {
      setError(err.message || 'Failed to delete idea');
    } finally {
      setLoading(false);
    }
  };

  const handleSendText = async (text: string, imageUris: string[]) => {
    if (!id) return;
    await createTextNote(id, text, imageUris);
    const updated = await getNotes(id);
    setNotes(updated);
  };

  const handleSendAudio = async (audioUri: string) => {
    if (!id) return;
    await createAudioNote(id, audioUri);
    const updated = await getNotes(id);
    setNotes(updated);
  };

  const handleDeleteNote = async (noteId: number) => {
    if (!id) return;
    await deleteNote(id, noteId);
    setNotes((prev) => prev.filter((n) => n.id !== noteId));
  };

  const handleEditNote = (note: NoteEntry) => {
    // For now, edit is a simple prompt — a future task can add inline editing
    setEditingNote(note);
  };

  useEffect(() => {
    navigation.setOptions({ headerShown: true, title: 'Idea Details' });
    if (!navigation.canGoBack()) {
      navigation.setOptions({
        headerLeft: () => (
          <Pressable onPress={() => router.push('/IdeasList')}>
            <Ionicons name="arrow-back" size={24} color="black" style={{ marginLeft: 15, marginRight: 15 }} />
          </Pressable>
        ),
      });
    }
    loadData();
  }, [loadData, navigation]);

  if (loading) {
    return <ActivityIndicator animating size="large" />;
  }

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={90}
    >
      <ScrollView style={styles.scroll} contentContainerStyle={styles.scrollContent}>
        <Button onPress={() => router.push({ pathname: '/EditIdea', params: { id } })} style={{ alignSelf: 'flex-end' }}>
          Edit
        </Button>
        <Text variant="headlineMedium">{idea?.title}</Text>
        <Text
          variant="labelLarge"
          style={{ color: STATUS_COLORS[idea?.status ?? 'new'] ?? STATUS_COLORS['new'], marginBottom: 10 }}
        >
          {idea?.status}
        </Text>
        {idea?.main_picture && <Image source={{ uri: idea.main_picture }} style={styles.image} />}
        <Text variant="bodyLarge" style={{ marginBottom: 20 }}>{idea?.description}</Text>
        <Text variant="bodySmall">Created: {new Date(idea?.created_at || '').toLocaleDateString()}</Text>
        <Text variant="bodySmall" style={{ marginBottom: 20 }}>
          Updated: {new Date(idea?.updated_at || '').toLocaleDateString()}
        </Text>
        <Button onPress={deleteItem} style={{ alignSelf: 'flex-end' }}>Delete</Button>

        <Text variant="titleMedium" style={styles.notesTitle}>Notes</Text>
        <NoteTimeline notes={notes} onDelete={handleDeleteNote} onEdit={handleEditNote} />
      </ScrollView>

      <NoteInput onSendText={handleSendText} onSendAudio={handleSendAudio} />

      <Snackbar visible={!!error} onDismiss={() => setError(null)} action={{ label: 'Retry', onPress: loadData }}>
        {error}
      </Snackbar>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  scroll: { flex: 1 },
  scrollContent: { padding: 20 },
  image: { width: '100%', height: 250, borderRadius: 8, marginBottom: 10 },
  notesTitle: { marginTop: 16, marginBottom: 8 },
});
```

- [ ] **Step 2: Commit**

```bash
cd /Users/julia/dev/ideaappmobile
git add app/IdeaDetails.tsx
git commit -m "feat: integrate notes timeline and input into IdeaDetails"
```

---

### Task 9: End-to-end manual test

- [ ] **Step 1: Start Django backend**

```bash
cd /Users/julia/dev/ideas_journal
python manage.py runserver 0.0.0.0:8000
```

- [ ] **Step 2: Start Expo app**

```bash
cd /Users/julia/dev/ideaappmobile
npx expo start
```

- [ ] **Step 3: Test on mobile (Expo Go)**

1. Open an existing idea
2. Type a text note and send — verify it appears in the timeline
3. Attach 2 images to a text note — verify thumbnails appear
4. Switch to audio mode, record a short clip, send — verify audio note appears with play button
5. Tap play on the audio note — verify playback
6. Delete a note — verify it disappears
7. Edit a text note's text — verify it updates

- [ ] **Step 4: Test in browser (expo web)**

1. Repeat the text note test (with and without images)
2. Audio recording may not work in all browsers — verify graceful behavior

- [ ] **Step 5: Commit any fixes found during testing**
