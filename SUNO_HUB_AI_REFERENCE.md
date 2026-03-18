# SUNO PROMPT HUB — AI REFERENCE DOCUMENT
## Complete Instructions for Creating Artist Data Files

**PURPOSE OF THIS DOCUMENT**
This document gives any AI assistant complete instructions to create artist data files for the Suno Prompt Hub — a web app / iPhone PWA that stores Suno AI music generation prompts organized by artist, song, genre, and keyword tags. If you are an AI reading this, you have everything you need here to continue building this system without any prior context.

---

## WHAT THE SYSTEM IS

The Suno Prompt Hub is a Progressive Web App (PWA) hosted on GitHub Pages. It runs entirely in a browser, works offline on iPhone, and auto-discovers artist data files placed in the same GitHub repository folder.

**The user's goal:** Create radio-ready songs in Suno AI by referencing the sonic DNA and production techniques of their favorite artists and songs. The prompts in this system are NOT song lyrics — they are Suno AI generation instructions.

**The two types of Suno prompts:**
1. **Style Prompt** — Pasted into Suno's Style field. Describes instruments, tempo, production era, vocal style, mood, BPM. Max ~500 characters. No artist names allowed by Suno.
2. **Lyric Generation Prompt** — Pasted into Suno's Lyrics field, then the user clicks "Generate Lyrics." This is a creative brief describing the emotional concept, narrative, structure, and tone. Suno writes the actual lyrics. NOT pre-written lyrics. Max ~3,000 characters.

---

## THE FILE SYSTEM

Every artist is stored as one JSON file. Files live in the GitHub repository alongside `index.html`, `sw.js`, `app.webmanifest`, `icon.svg`, and `manifest.json`.

**File naming convention:**
- Artist files: `artist_[id].json` (e.g., `artist_blink182.json`, `artist_morgan_wallen.json`)
- Genre study files: `genre_[name].json` (e.g., `genre_country.json`)

**`manifest.json`** — The master file list. Every time a new artist file is created, this file must be updated to include the new filename. The app reads this file on load to know which artist files to fetch.

```json
{
  "version": "1.0",
  "files": [
    "artist_blink182.json",
    "artist_greenday.json",
    "artist_ratm.json",
    "artist_russell_dickerson.json",
    "artist_taylor_male.json",
    "artist_thomas_rhett.json",
    "genre_country.json"
  ]
}
```

When creating a new artist, ALWAYS provide:
1. The new `artist_[id].json` file
2. An updated `manifest.json` with the new filename added to the `files` array

---

## COMPLETE ARTIST FILE SCHEMA

Every artist file must be valid JSON with this exact structure:

```json
{
  "id": "string — unique identifier, no spaces, lowercase, used in filenames",
  "name": "string — display name shown in the app",
  "genres": ["array", "of", "genre", "strings"],
  "era": "string — year range e.g. '1992–2025'",
  "color": "string — hex color for UI accent e.g. '#ff4757'",
  "bio": "string — 2-4 sentence artist description covering sound, history, key members, signature production elements",
  "producer_notes": "string — 1-3 sentences about their key producers, production techniques, Suno-specific notes",
  "songs": [ /* array of song objects — see below */ ],
  "albums": [ /* OPTIONAL array of album objects — see below */ ]
}
```

### Song Object Schema

```json
{
  "title": "string — song title",
  "album": "string — album name",
  "year": 1999,
  "bpm": 148,
  "vibe": "string — short descriptor, e.g. 'Reunion album anthem · Tom + Mark dual vocal'",
  "dna": "string — 2-5 sentences describing actual production details: instruments used, production techniques, what makes this song sonically unique, who produced it, the emotional core",
  "style_prompt": "string — the Suno Style field prompt, max ~500 chars, no artist names, describes instruments/tempo/production/mood",
  "lyric_prompt": "string — the Suno Lyric Generation prompt, a creative brief NOT actual lyrics, describes concept/narrative/structure/tone/runtime"
}
```

**BPM field rules:**
- Use an integer when known: `148`
- Use a string for variable: `"Multi-tempo 80–184"`
- Use a string for approximate: `"~120"`
- Leave as null if unknown: `null`

### Album Object Schema (optional — only include if the artist has meaningful album-level prompt value)

```json
{
  "title": "string — album name",
  "year": 2019,
  "style_prompt": "string — captures the sonic world of the entire album",
  "lyric_prompt": "string — captures the emotional/narrative world of the entire album"
}
```

---

## COLOR REFERENCE — Suggested hex colors by genre

Use these to make the UI visually distinct. Pick one that fits the artist's energy:

| Genre/Vibe | Color |
|---|---|
| Pop-Punk / Punk Rock | `#ff4757` (red) |
| Green Day specifically | `#a8e063` (lime green) |
| Rap-Metal / Hard Rock | `#ffa502` (amber/orange) |
| Synth-Pop / Indie Pop | `#9b6dff` (violet) |
| Country-Pop (warm) | `#e8943a` (warm amber) |
| Country-Pop (teal) | `#4ab8c4` (teal) |
| Alternative Rock | `#00bfa5` (mint) |
| Progressive Rock | `#7c4dff` (deep violet) |
| Outlaw Country | `#c8922a` (gold) |
| Pop Punk (revival) | `#e91e63` (hot pink) |
| Folk / Acoustic | `#8bc34a` (sage green) |
| R&B / Soul | `#ff6b9d` (pink) |
| Hip-Hop | `#ffca28` (yellow) |
| Metal | `#b0bec5` (steel grey) |
| Blues / Classic Rock | `#7986cb` (indigo) |

---

## STYLE PROMPT WRITING RULES

The style prompt goes in Suno's Style field. These rules are non-negotiable:

1. **No artist names or band names** — Suno flags them. Use descriptors instead.
   - WRONG: `"Taylor Swift-style synth-pop"`
   - RIGHT: `"Late 2010s polished synth-pop in the Antonoff production style"`

2. **Lead with genre and tempo** — Suno truncates from the end, so front-load the most important information.

3. **Include BPM** — Always include BPM when known. It significantly affects the generation.

4. **Name specific instruments** — "Juno-6 synth arpeggio" is better than "synth." "Pedal steel" is better than "country guitar."

5. **Include vocal descriptor** — male/female, tenor/baritone, earnest/sardonic, close-mic'd/processed, etc.

6. **Include mood and energy** — euphoric, melancholic, anthemic, tender, aggressive, etc.

7. **Keep under 500 characters** — Count matters. Aim for 300-450 characters for the sweet spot.

8. **No brackets or special formatting** — Plain comma-separated descriptors only.

**Example of a well-written style prompt:**
```
Warm country-pop, 121 BPM, bright acoustic guitar, pedal steel warmth, male vocal tender and content, mid-tempo feel-good groove, layered harmonies on chorus, clean Nashville production, simple-life celebration energy, porch swing Sunday atmosphere, love-is-home thematic core, no ambition — just gratitude for the ordinary
```

---

## LYRIC GENERATION PROMPT WRITING RULES

This prompt goes in Suno's Lyrics field. The user clicks "Generate Lyrics" and Suno writes the actual lyrics. This is NOT the lyrics themselves — it is a creative brief.

1. **Start with "Write a..."** — Give Suno a clear instruction verb.

2. **Describe the emotional concept** — What is the song about emotionally? Not just topically.

3. **Describe the narrator's perspective** — Who is singing? What do they feel? What do they want?

4. **Include structural guidance** — Describe the arc: verse energy → pre-chorus → chorus → bridge behavior. What does the chorus DO emotionally?

5. **Include specific imagery directions** — What world should the lyrics live in? (small-town South, New York City at 2am, a concert venue, etc.)

6. **Specify tone** — Sardonic? Earnest? Theatrical? Playful? This is as important as the subject matter.

7. **Give runtime** — "Under 3:30" helps Suno calibrate song length.

8. **Do NOT write any actual lyrics** — No example lines, no sample hooks, no lyric fragments. Only describe what the song should do.

9. **Do NOT use brackets** — No [Verse], [Chorus] etc. in the lyric prompt. Those go in the lyrics field only when Suno generates them.

10. **Max ~3,000 characters** — Aim for 200-400 words.

**Example of a well-written lyric generation prompt:**
```
Write a warm nostalgic country-pop song structured as a letter from a man to his 16-year-old self. He speaks from genuine, specific contentment: a wife he loves completely, kids who run to the door when he gets home. He tells his younger self what's coming — not to prepare him, but to reassure him that the small-town dreams were never wrong, just the destination was different. He thought famous meant big stages — turns out it means being famous in his own home. Include specific small-town teenage details. The chorus is a warm address to that younger self. Under 3:30.
```

---

## THE DNA FIELD — What to include

The `dna` field is shown in the app when a user taps a song. It should include:

- **Actual production details** — What instruments were recorded? What gear was used? What was the recording process?
- **Producer information** — Who produced it and what's their signature?
- **What makes this song sonically unique** — The specific qualities that set it apart from their other songs
- **Emotional core** — The central feeling of the song
- **Any notable facts** — Record chart performance, cultural context, filming locations, viral moments

Research the song properly. Vague dna entries like "a good song about love" are useless. Specific entries like "recorded with a Gibson ES-330, Juno-6, and Vox AC30, with a Fine Young Cannibals-inspired snare sample, 92 BPM half-time chorus feel" are what make the system valuable.

---

## KEYWORD EXTRACTION — What the app auto-tags

The app automatically extracts tags from the `style_prompt`, `lyric_prompt`, `dna`, `vibe`, and `title` fields using keyword matching. You do NOT need to include tags manually — they are generated automatically. However, knowing what keywords trigger what tags helps you write better prompts.

### BPM Tiers (extracted from `bpm` field)
| Tag | BPM Range |
|---|---|
| Very Slow | 0–70 |
| Slow | 71–90 |
| Mid-Slow | 91–109 |
| Mid-Tempo | 110–129 |
| Upbeat | 130–149 |
| Fast | 150–169 |
| Very Fast | 170+ |

### Instrument Tags (extracted by keyword)
Include these exact phrases in prompts to trigger these tags:
- `acoustic guitar` → Acoustic Guitar
- `electric guitar`, `power chord`, `distorted guitar`, `palm-muted` → Electric Guitar
- `pedal steel` → Pedal Steel
- `piano` → Piano
- `juno`, `juno-6`, `synth`, `synthesizer`, `moog` → Synth / Juno
- `drum machine`, `live drummer`, `drumming` → Drums
- `808`, `bass guitar`, `bass-forward`, `funk bass` → 808 / Bass
- `banjo` → Banjo
- `strings`, `cello`, `violin`, `fiddle`, `orchestral` → Strings
- `horn`, `brass`, `saxophone` → Horns
- `mellotron` → Mellotron
- `hammond`, `organ` → Hammond Organ
- `tambourine` → Tambourine

### Vocal Style Tags
- `male tenor`, `tenor` → Male Tenor
- `baritone` → Baritone
- `dual vocal`, `two vocal`, `alternating` → Dual Vocal
- `whispered`, `breathy`, `close-mic` → Whispered
- `screamed`, `scream`, `belted`, `belting`, `yelling` → Screamed / Belted
- `rap`, `rapped`, `spoken word`, `hip-hop vocal` → Rap / Spoken
- `gang vocal`, `singalong backing` → Gang Vocals
- `earnest`, `sincere`, `unguarded` → Earnest / Sincere
- `sardonic`, `wry`, `sneering`, `sarcastic` → Sardonic / Wry

### Mood Tags
- `euphoric`, `joyful`, `celebratory`, `uplifting`, `triumphant` → Euphoric
- `melancholic`, `aching`, `wistful`, `bittersweet` → Melancholic
- `angry`, `fury`, `furious`, `rage`, `contemptuous`, `seething` → Angry / Furious
- `tender`, `romantic`, `devotion`, `loving`, `heartfelt`, `besotted` → Tender / Romantic
- `anxious`, `anxiety`, `nervous`, `restless`, `urgent`, `breathless` → Anxious
- `anthemic`, `anthem`, `arena`, `stadium`, `fist-pump` → Anthemic
- `haunting`, `gothic`, `dark`, `atmospheric`, `eerie`, `ghostly` → Haunting / Dark
- `playful`, `funny`, `comedic`, `charming`, `gleeful` → Playful
- `cathartic`, `release`, `explosion` → Cathartic
- `nostalgic`, `nostalgia`, `memory`, `looking back` → Nostalgic
- `defiant`, `rebellion`, `rebellious`, `resist`, `refusal` → Defiant

### Production Era Tags
- `90s`, `late-90s`, `lo-fi garage`, `jerry finn` → 90s Raw
- `2000s`, `toypaj`, `rob cavallo`, `polished nashville` → 2000s Polished
- `modern`, `contemporary`, `2023`, `2024`, `2025` → Modern (2015+)
- `bedroom`, `home-studio`, `lo-fi`, `antonoff brooklyn` → Bedroom / Indie
- `analog`, `vintage`, `mellotron`, `warm analog`, `classic` → Analog / Vintage

### Lyric Theme Tags
- `devotion`, `love song`, `romantic`, `wife`, `wedding`, `first dance` → Love & Devotion
- `breakup`, `heartbreak`, `miss you`, `longing` → Breakup / Loss
- `revenge`, `vindication`, `payback`, `gleeful` → Revenge
- `hometown`, `small town`, `nostalgia`, `growing up`, `teenage` → Nostalgia / Hometown
- `political`, `protest`, `government`, `war`, `media`, `corporate` → Political / Protest
- `youth`, `rebellion`, `anti-authority`, `reckless` → Youth / Rebellion
- `anxiety`, `mental health`, `therapy`, `breakdown` → Anxiety / Mental Health
- `father`, `daughter`, `son`, `family`, `kids`, `dad` → Fatherhood / Family
- `ambition`, `identity`, `reinvention`, `starting over`, `city` → Ambition / Identity
- `secret`, `forbidden`, `hidden`, `sneaking` → Secret Love
- `late night`, `midnight`, `2am`, `3am`, `bar`, `closing time` → Night / Late Night

### Song Structure Tags
- `under 2:30`, `under 2 minutes`, `under 1:45` → Short (< 2:30)
- `7 minutes`, `multi-movement`, `suite` → Epic (7+ min)
- `quiet-loud`, `builds from`, `builds to`, `crescendo` → Quiet-Loud Arc
- `dual vocal`, `two voices`, `alternating` → Dual Narrative
- `spoken word` → Spoken Word
- `no traditional chorus`, `no chorus` → No Chorus

---

## HOW TO RESEARCH A SONG

When building prompts, use these research methods to find accurate production details:

1. **BPM** — Search `[song name] BPM` on GetSongBPM.com, Tunebat.com, or Songbpm.com
2. **Key/Tempo** — Spotify's developer API or TuneBat show musical key and BPM
3. **Production details** — Search `[song name] production breakdown`, `[artist] recording process`, `[song name] instruments used`
4. **Producer** — Search `[song name] producer`, check Wikipedia, AllMusic, Genius credits
5. **Gear used** — Search `[artist] guitar used`, `[producer] signature sound`, equipment interviews
6. **Sonic DNA** — Read production interviews on MusicRadar, Sound on Sound, Mix Magazine
7. **Chart info** — Billboard chart history, Spotify stream counts

**Priority for DNA accuracy:** What specific instruments were tracked? Who produced it? What's the BPM? What makes it different from the artist's other songs? What cultural moment does it represent?

---

## WORKED EXAMPLE — Complete Song Entry

Here is a fully worked example showing every field at the correct quality level:

```json
{
  "title": "I Miss You",
  "album": "Blink-182 (Self-Titled)",
  "year": 2003,
  "bpm": 110,
  "vibe": "Gothic Cure-influenced ballad · 1B+ Spotify streams",
  "dna": "All acoustic instruments: piano, cello, acoustic bass guitar, and a brushstroked hip-hop groove. Directly inspired by The Cure's The Love Cats. Over one billion Spotify streams. DeLonge said the song is about vulnerability and not wanting someone to waste their time on you — the pre-emptive heartbreak of loving someone while believing they've already mentally checked out. Tom and Mark alternate vocals throughout.",
  "style_prompt": "Gothic acoustic pop-punk ballad, 110 BPM, Cure-influenced dark romanticism, acoustic instruments only — piano, cello, acoustic bass, brushstroke hip-hop drum groove, male tenor vocal in wide reverb — earnest and slightly theatrical, Tom and Mark alternating narrative voices, haunted mansion atmosphere, B major melancholy, vulnerability and pre-emptive heartbreak as lyric core, under 3:50, both beautiful and aching",
  "lyric_prompt": "Write a gothic acoustic ballad about the pre-emptive heartbreak of loving someone while believing they've already mentally left — telling them 'don't waste your time on me, you've already given up on me in your head.' The tone is both vulnerable and somewhat theatrical — more Tim Burton than emo. The instrumentation is acoustic and orchestral, not punk. Include Halloween/gothic imagery that serves the emotional metaphor without being campy. Two vocal perspectives alternating. The most emotionally devastating song in the set. Under 3:50."
}
```

---

## WHAT TO DELIVER TO THE USER

When asked to create an artist file, always deliver:

**1. The artist JSON file** — formatted as valid JSON, properly escaped, complete with all fields. Name it `artist_[id].json`.

**2. An updated `manifest.json`** — Include ALL existing files plus the new one. The user pastes this file into GitHub to replace the old one. Here is the current manifest as of the last update:

```json
{
  "version": "1.0",
  "files": [
    "artist_blink182.json",
    "artist_greenday.json",
    "artist_ratm.json",
    "artist_russell_dickerson.json",
    "artist_taylor_male.json",
    "artist_thomas_rhett.json",
    "genre_country.json"
  ]
}
```

**When adding a new artist, add their filename to the `files` array above.**

**3. Instructions for the user** — Tell them:
- Upload `artist_[name].json` to the GitHub repository
- Upload the updated `manifest.json` to replace the old one
- Wait ~30 seconds for GitHub to update
- Open the app and tap **↻ Refresh**
- The new artist appears automatically

---

## GITHUB REPOSITORY STRUCTURE

The repository name is `suno-hub`. It lives at `https://github.com/[USERNAME]/suno-hub`. GitHub Pages serves it at `https://[USERNAME].github.io/suno-hub/`.

**Files that NEVER change** (do not regenerate or modify these):
- `index.html` — The app interface
- `sw.js` — Service worker for offline support
- `app.webmanifest` — iPhone PWA install configuration
- `icon.svg` — App icon

**Files that change when adding artists:**
- `manifest.json` — Must be updated with every new artist filename
- `artist_[id].json` — New file added for each new artist

---

## CURRENTLY BUILT ARTISTS

As of the last session, these artists have complete data files in the system:

| File | Artist | Songs |
|---|---|---|
| `artist_blink182.json` | Blink-182 | 19 songs |
| `artist_greenday.json` | Green Day | 7 songs |
| `artist_ratm.json` | Rage Against the Machine | 9 songs |
| `artist_taylor_male.json` | Taylor Swift / Antonoff (Male Era) | 14 songs + 6 album prompts |
| `artist_russell_dickerson.json` | Russell Dickerson | 8 songs |
| `artist_thomas_rhett.json` | Thomas Rhett | 6 songs |
| `genre_country.json` | Country Genre Study 2018–2025 | 1 universal prompt |

**Songs with detailed prompts in each file are documented in the files themselves.** If the user asks "what songs do I have for Blink-182?", refer to the list of 19 songs in `artist_blink182.json`.

---

## QUICK COMMAND REFERENCE

**"Add [Artist] to the database with songs [list]"**
→ Create `artist_[id].json` with all fields completed
→ Provide updated `manifest.json`
→ Research actual BPM, producers, instruments for each song
→ Write style prompts (≤500 chars, no artist names, instrument-specific)
→ Write lyric generation prompts (creative brief, NOT lyrics, ~200-400 words each)

**"Add album prompts for [Artist]"**
→ Add an `"albums"` array to the existing artist file
→ Each entry needs `title`, `year`, `style_prompt`, `lyric_prompt`
→ Album prompts should capture the sonic world of the WHOLE album, not just one song

**"Update the manifest"**
→ Return the complete `manifest.json` with all current files listed

**"What format does the file need to be in?"**
→ Valid JSON, UTF-8 encoded, no trailing commas, all strings properly escaped
→ Follow the schema exactly as documented in this file

---

## SUNO-SPECIFIC RULES SUMMARY

These rules apply to ALL style_prompt and lyric_prompt fields:

| Rule | Style Prompt | Lyric Prompt |
|---|---|---|
| No artist/band names | ✅ Required | ✅ Required |
| Max length | ~500 characters | ~3,000 characters |
| No brackets [ ] | ✅ Required | ✅ Required |
| Must include BPM | ✅ Recommended | — |
| Must include genre | ✅ Required | ✅ Recommended |
| Actual lyrics | ❌ Never | ❌ Never |
| Creative brief format | — | ✅ Required |
| Start with "Write a..." | — | ✅ Recommended |
| Runtime guidance | ✅ Optional | ✅ Recommended |

---

*This document is a complete self-contained reference. Any AI reading this has all the information needed to create artist files that work correctly in the Suno Prompt Hub system.*
