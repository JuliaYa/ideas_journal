# Ideas App — Plans

## Done

- [x] Add colored statuses for the ideas list and idea details screen
- [x] Add filter by status to the ideas list (frontend chips + backend query param)
- [x] Add main picture upload for ideas (stored via Django media)
- [x] Add notes with text, images, and audio to ideas (server-side nested API + mobile timeline UI)
- [x] Add persistent Home button (Back button was unreliable)
- [x] Apply a polished design system (Clay-inspired theme across all screens)

## To Do

- [ ] Delete main picture without replacing it; physically remove the old file from disk (currently orphaned files remain)
- [ ] Design a proper auth flow and user registration form
- [ ] Write tests (backend + mobile)
- [ ] Fix screen flicker when switching status filters (full list re-render)
- [ ] Add reminders for in-progress ideas (settings screen: configure reminder pattern/schedule)
- [ ] Add a Pinterest-style card view for ideas (user can switch view type in settings)
- [ ] Add AI support to help move forward with idea realisation
