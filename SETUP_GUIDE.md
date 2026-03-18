# Suno Prompt Hub — GitHub Pages Setup Guide

## What You're Building

A web app that lives at `https://YOUR-USERNAME.github.io/suno-hub/`
- Works on iPhone like a native app (add to home screen)
- Fully offline after first load
- Updates automatically when you upload new artist files

---

## STEP 1 — Create a GitHub Account (if you don't have one)

1. Go to **github.com**
2. Click **Sign up**
3. Choose a username (this becomes part of your URL)
4. Verify your email

---

## STEP 2 — Create a New Repository

1. After logging in, click the **+** icon (top right) → **New repository**
2. Repository name: `suno-hub` (exactly this, lowercase)
3. Set to **Public** (required for free GitHub Pages)
4. Check **"Add a README file"**
5. Click **Create repository**

---

## STEP 3 — Upload Your Files

You need to upload ALL files from the `suno_pwa` folder:

**Files to upload:**
- `index.html`
- `sw.js`
- `app.webmanifest`
- `manifest.json`
- `icon.svg`
- `artist_blink182.json`
- `artist_greenday.json`
- `artist_ratm.json`
- `artist_russell_dickerson.json`
- `artist_taylor_male.json`
- `artist_thomas_rhett.json`
- `genre_country.json`

**How to upload:**
1. In your repository, click **"uploading an existing file"** (or drag files onto the page)
2. Drag ALL files from the `suno_pwa` folder into the upload area
3. Scroll down, click **"Commit changes"**

---

## STEP 4 — Enable GitHub Pages

1. In your repository, click **Settings** (top tab)
2. Scroll down to **Pages** (left sidebar)
3. Under **Source**, select **"Deploy from a branch"**
4. Branch: **main**, Folder: **/ (root)**
5. Click **Save**

Wait 1–2 minutes, then your site is live at:
```
https://YOUR-USERNAME.github.io/suno-hub/
```

---

## STEP 5 — Add to iPhone Home Screen

1. Open Safari on your iPhone (must be Safari, not Chrome)
2. Go to your URL: `https://YOUR-USERNAME.github.io/suno-hub/`
3. Tap the **Share button** (box with arrow pointing up)
4. Scroll down and tap **"Add to Home Screen"**
5. Name it **"Suno Hub"**
6. Tap **Add**

It now appears on your home screen as an app icon. When you open it, there's no browser address bar — it looks and feels like a native app.

---

## ADDING NEW ARTISTS (the ongoing workflow)

Every time you ask Claude to build an artist:

**Claude gives you:**
- `artist_morgan_wallen.json` (or whatever artist)
- An updated `manifest.json`

**You do (takes 2 minutes):**
1. Go to your GitHub repository
2. Click **"Add file"** → **"Upload files"**
3. Upload the new `artist_name.json`
4. Also upload the new `manifest.json` (replaces the old one)
5. Click **"Commit changes"**
6. Wait ~30 seconds → open your app → tap **↻ Refresh**

The new artist appears automatically.

---

## HOW TO USE THE APP

### Search
- Tap the search bar at the top
- Type any word — song title, artist, mood, instrument, BPM, theme
- Results show matches from all prompts, not just titles

### Browse by Tag
- Tap **Browse** in the bottom tab bar
- Type in the search box to filter tags
- Tap any tag pill to filter all songs by that attribute
- Multiple filters stack (Tempo: Fast + Mood: Anthemic = fast anthemic songs)

### Artist → Song → Prompts
- Tap an artist → tap a song → sheet slides up from bottom
- **Copy Style Prompt** → paste into Suno's Style field
- **Copy Lyric Prompt** → paste into Suno's Lyrics field → tap "Generate Lyrics"
- Tap any colored tag in the sheet to filter all songs by that tag

### Offline
- After first load, the app caches everything
- You can use it fully offline on iPhone
- An amber banner appears at the top when offline

---

## ASKING CLAUDE FOR NEW ARTISTS

Say something like:

> "Add Morgan Wallen to my Suno database. Songs: Wasted on You, Sand in My Boots, Last Night, 7 Summers, Thought You Should Know, Whiskey Glasses, More Than My Hometown, cover me up"

Claude will give you `artist_morgan_wallen.json` and an updated `manifest.json`.
Upload both to GitHub → refresh the app → done.

---

## FILE STRUCTURE

```
suno-hub/ (your GitHub repo)
├── index.html          ← The app (never changes)
├── sw.js               ← Offline service worker (never changes)
├── app.webmanifest     ← iPhone install config (never changes)
├── icon.svg            ← App icon (never changes)
├── manifest.json       ← LIST OF ARTIST FILES (update when adding artists)
├── artist_blink182.json
├── artist_greenday.json
├── artist_ratm.json
├── artist_russell_dickerson.json
├── artist_taylor_male.json
├── artist_thomas_rhett.json
├── genre_country.json
└── (new artist files go here)
```

Only two files ever change: `manifest.json` (add new filename) and new `artist_*.json` files.
`index.html`, `sw.js`, `app.webmanifest`, and `icon.svg` never need to change.
