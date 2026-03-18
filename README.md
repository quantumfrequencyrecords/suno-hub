# Suno Prompt Hub — Database Folder

## Files in This Folder

| File | Purpose |
|------|---------|
| `hub.html` | **Main hub** — open this in your browser |
| `registry.json` | Master index of all artists and files |
| `artist_blink182.json` | Blink-182 — 19 songs |
| `artist_greenday.json` | Green Day — 7 songs |
| `artist_ratm.json` | Rage Against the Machine — 9 songs |
| `artist_taylor_male.json` | Taylor Swift / Antonoff Male Era — 14 songs + 6 album prompts |
| `artist_russell_dickerson.json` | Russell Dickerson — 8 songs |
| `artist_thomas_rhett.json` | Thomas Rhett — 6 songs |
| `genre_country.json` | Country genre study 2018–2025 |
| `genre_poppunk.json` | Pop punk genre study 2018–2025 |
| `genre_progrock.json` | Progressive rock genre study 2018–2025 |
| `genre_altrock.json` | Alternative rock genre study 2018–2025 |

---

## How to Open the Hub

### Option A — Local Python Server (Recommended)

Browser security blocks local JSON loading by default. Run this once:

```bash
cd /path/to/this/folder
python3 -m http.server 8080
```

Then open: **http://localhost:8080/hub.html**

### Option B — VS Code Live Server
If you use VS Code, install the "Live Server" extension, right-click `hub.html` → Open with Live Server.

### Option C — Direct File (Chrome only workaround)
Launch Chrome with: `google-chrome --allow-file-access-from-files`
Then open hub.html directly.

---

## How to Add a New Artist

1. **Ask Claude** to build prompts for a new artist in the same format
2. Claude gives you a new JSON file (e.g., `artist_morgan_wallen.json`)
3. Drop it into this folder
4. Claude gives you an updated `registry.json` — replace the old one
5. Refresh the hub — the new artist appears automatically

### JSON Structure for New Artist Files

```json
{
  "id": "unique_id_no_spaces",
  "name": "Artist Display Name",
  "genres": ["Genre1", "Genre2"],
  "era": "2010–2025",
  "color": "#hexcolor",
  "bio": "Artist bio text...",
  "producer_notes": "Production notes...",
  "songs": [
    {
      "title": "Song Title",
      "album": "Album Name",
      "year": 2020,
      "bpm": 120,
      "vibe": "Short description",
      "dna": "Longer sonic DNA description...",
      "style_prompt": "Paste into Suno Style field...",
      "lyric_prompt": "Paste into Suno Lyrics field → Generate Lyrics..."
    }
  ],
  "albums": [
    {
      "title": "Album Name",
      "year": 2020,
      "style_prompt": "Album-wide style prompt...",
      "lyric_prompt": "Album-wide lyric generation prompt..."
    }
  ]
}
```

### registry.json Entry Format

```json
{
  "id": "unique_id_no_spaces",
  "name": "Artist Display Name",
  "file": "artist_filename.json",
  "genres": ["Genre1", "Genre2"],
  "era": "2010–2025",
  "song_count": 10,
  "color": "#hexcolor",
  "description": "Short description shown on the home card."
}
```

---

## Current Database Stats

- **6 artists** fully built
- **4 genre studies** included
- **63 songs** with Style + Lyric Generation prompts
- **6 album-level** prompts (Taylor/Antonoff era)

Every time you add an artist, drop the file in and update registry.json. The hub reads it dynamically — no code changes needed.
