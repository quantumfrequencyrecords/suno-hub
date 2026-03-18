#!/usr/bin/env python3
"""
Suno Prompt Hub — Launcher
Double-click to run (or: python3 launch.py)

Scans this folder for all artist_*.json and genre_*.json files,
extracts keywords from every prompt automatically, builds index.json,
then opens hub.html in your default browser.
"""

import json
import os
import re
import sys
import time
import webbrowser
import http.server
import threading
import glob
from pathlib import Path

# ── CONFIGURATION ────────────────────────────────────────────────────────────
PORT = 8765
FOLDER = Path(__file__).parent.resolve()
INDEX_FILE = FOLDER / "index.json"
HUB_FILE = FOLDER / "hub.html"

# ── KEYWORD EXTRACTION RULES ─────────────────────────────────────────────────

BPM_TIERS = [
    ("Very Slow", 0, 70),
    ("Slow", 71, 90),
    ("Mid-Slow", 91, 109),
    ("Mid-Tempo", 110, 129),
    ("Upbeat", 130, 149),
    ("Fast", 150, 169),
    ("Very Fast", 170, 999),
]

INSTRUMENT_KEYWORDS = {
    "Acoustic Guitar": ["acoustic guitar", "acoustic"],
    "Electric Guitar": ["electric guitar", "power chord", "distorted guitar", "palm-muted"],
    "Pedal Steel": ["pedal steel"],
    "Piano": ["piano", "piano-driven"],
    "Synth / Juno": ["juno", "juno-6", "juno synth", "synth", "synthesizer", "moog"],
    "Drums": ["drum machine", "live drummer", "travis barker", "brad wilk", "drumming"],
    "808 / Bass": ["808", "bass guitar", "bass-forward", "funk bass"],
    "Banjo": ["banjo"],
    "Strings": ["strings", "cello", "violin", "fiddle", "orchestral"],
    "Horns": ["horn", "brass", "trumpet", "saxophone"],
    "Mellotron": ["mellotron"],
    "Hammond Organ": ["hammond", "organ"],
    "Tambourine": ["tambourine"],
}

VOCAL_KEYWORDS = {
    "Male Tenor": ["male tenor", "tenor"],
    "Baritone": ["baritone"],
    "Dual Vocal": ["dual vocal", "dual-vocal", "two vocal", "tom and mark", "alternating", "tag team"],
    "Whispered": ["whispered", "breathy", "close-mic"],
    "Screamed / Belted": ["screamed", "scream", "belted", "belting", "yelling"],
    "Rap / Spoken": ["rap", "rapped", "spoken word", "hip-hop vocal", "rhyming"],
    "Gang Vocals": ["gang vocal", "gang-vocal", "crowd", "singalong backing"],
    "Earnest / Sincere": ["earnest", "sincere", "unguarded"],
    "Sardonic / Wry": ["sardonic", "wry", "sneering", "sarcastic"],
}

MOOD_KEYWORDS = {
    "Euphoric": ["euphoric", "euphoria", "joyful", "joy", "celebratory", "uplifting", "triumphant"],
    "Melancholic": ["melancholic", "melancholy", "aching", "wistful", "bittersweet", "anguish"],
    "Angry / Furious": ["angry", "fury", "furious", "rage", "contemptuous", "outrage", "seething"],
    "Tender / Romantic": ["tender", "romantic", "devotion", "loving", "warm", "heartfelt", "besotted"],
    "Anxious": ["anxious", "anxiety", "nervous", "restless", "urgent", "breathless"],
    "Anthemic": ["anthemic", "anthem", "arena", "stadium", "fist-pump", "singalong"],
    "Haunting / Dark": ["haunting", "haunted", "gothic", "dark", "atmospheric", "eerie", "ghostly"],
    "Playful": ["playful", "funny", "comedic", "charming", "humorous", "gleeful"],
    "Cathartic": ["cathartic", "catharsis", "release", "explosion", "climax"],
    "Nostalgic": ["nostalgic", "nostalgia", "memory", "remembering", "looking back"],
    "Defiant": ["defiant", "defiance", "rebellion", "rebellious", "resist", "refusal"],
}

PRODUCTION_ERA = {
    "90s Raw": ["90s", "late-90s", "early 90s", "lo-fi garage", "grunge", "dookie", "jerry finn", "debut era"],
    "2000s Polished": ["2000s", "toypaj", "rob cavallo", "jerry finn", "enema of the state", "polished nashville"],
    "Modern (2015+)": ["modern", "2020s", "current", "contemporary", "2023", "2024", "2025"],
    "Bedroom / Indie": ["bedroom", "home-studio", "lo-fi", "intimate", "cottage", "antonoff brooklyn"],
    "Analog / Vintage": ["analog", "vintage", "mellotron", "hammond", "tape", "warm analog", "classic"],
}

LYRIC_THEME_KEYWORDS = {
    "Love & Devotion": ["devotion", "love song", "romantic", "wife", "husband", "wedding", "first dance", "belonging"],
    "Breakup / Loss": ["breakup", "heartbreak", "ex", "left me", "she left", "he left", "miss you", "longing"],
    "Revenge / Schadenfreude": ["revenge", "vindication", "payback", "sarcastic", "gleeful", "schadenfreude", "you made me"],
    "Nostalgia / Hometown": ["hometown", "small town", "nostalgia", "growing up", "high school", "teenage", "16"],
    "Political / Protest": ["political", "protest", "government", "war", "media", "corporate", "capitalism", "systemic"],
    "Youth / Rebellion": ["youth", "rebellion", "anti-authority", "reckless", "parents", "society", "conform"],
    "Anxiety / Mental Health": ["anxiety", "panic", "mental health", "therapy", "breakdown", "basket case"],
    "Fatherhood / Family": ["father", "daughter", "son", "family", "kids", "dad"],
    "Ambition / Identity": ["ambition", "identity", "reinvention", "who i am", "starting over", "city"],
    "Secret Love": ["secret", "forbidden", "hidden", "can't tell anyone", "sneaking"],
    "Night / Late Night": ["late night", "midnight", "2am", "3am", "night", "bar", "closing time"],
}

STRUCTURAL_KEYWORDS = {
    "Short (< 2:30)": [],  # set by BPM/duration logic
    "Epic (7+ min)": ["7 minutes", "8 minutes", "9 minutes", "multi-movement", "suite", "5 sections"],
    "Quiet-Loud Arc": ["quiet-loud", "builds from", "builds to", "explodes", "crescendo", "dynamic arc"],
    "Call & Response": ["call-and-response", "dual vocal", "two voices", "alternating"],
    "Spoken Word Section": ["spoken word", "spoken section", "spoken-word"],
    "Bridge Focused": ["bridge", "the bridge is"],
    "No Traditional Chorus": ["no traditional chorus", "no chorus", "through-composed", "accumulation"],
}

# ── EXTRACTION FUNCTION ───────────────────────────────────────────────────────

def extract_tags(song: dict) -> dict:
    """Extract structured tags from a song dict."""
    text = " ".join([
        str(song.get("style_prompt", "")),
        str(song.get("lyric_prompt", "")),
        str(song.get("dna", "")),
        str(song.get("vibe", "")),
        str(song.get("title", "")),
    ]).lower()

    tags = {
        "bpm_tier": None,
        "instruments": [],
        "vocals": [],
        "mood": [],
        "production_era": [],
        "lyric_themes": [],
        "structure": [],
    }

    # BPM tier
    bpm = song.get("bpm")
    if bpm and str(bpm).replace(" ", "").isdigit():
        b = int(str(bpm).split()[0])
        for name, lo, hi in BPM_TIERS:
            if lo <= b <= hi:
                tags["bpm_tier"] = name
                break
    elif bpm and "multi" in str(bpm).lower():
        tags["bpm_tier"] = "Variable"

    # Category extraction
    def match_cats(rules, field):
        matched = []
        for label, kws in rules.items():
            if any(kw in text for kw in kws):
                matched.append(label)
        return matched

    tags["instruments"] = match_cats(INSTRUMENT_KEYWORDS, text)
    tags["vocals"] = match_cats(VOCAL_KEYWORDS, text)
    tags["mood"] = match_cats(MOOD_KEYWORDS, text)
    tags["production_era"] = match_cats(PRODUCTION_ERA, text)
    tags["lyric_themes"] = match_cats(LYRIC_THEME_KEYWORDS, text)
    tags["structure"] = match_cats(STRUCTURAL_KEYWORDS, text)

    # Short song heuristic
    short_signals = ["under 2:30", "under 2 minutes", "under 1:45", "short", "2:47", "2:33", "2:54"]
    if any(s in text for s in short_signals):
        if "Short (< 2:30)" not in tags["structure"]:
            tags["structure"].append("Short (< 2:30)")

    return tags


def build_index():
    """Scan folder, load all artist/genre JSON files, extract keywords, write index.json."""
    print(f"\n🎵 Suno Prompt Hub — Building index...")
    print(f"   Scanning: {FOLDER}\n")

    artists = []
    all_tag_counts = {
        "bpm_tier": {},
        "instruments": {},
        "vocals": {},
        "mood": {},
        "production_era": {},
        "lyric_themes": {},
        "structure": {},
        "genres": {},
    }
    total_songs = 0

    # Find all artist/genre data files
    data_files = sorted(
        list(FOLDER.glob("artist_*.json")) +
        list(FOLDER.glob("genre_*.json"))
    )

    if not data_files:
        print("   ⚠️  No artist_*.json or genre_*.json files found.")
        print("   Put your JSON files in the same folder as this script.\n")
        return False

    for fpath in data_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"   ⚠️  Skipping {fpath.name}: {e}")
            continue

        song_count = len(data.get("songs", []))
        print(f"   ✓  {fpath.name} — {song_count} songs")

        # Extract tags for each song
        enriched_songs = []
        for song in data.get("songs", []):
            song["tags"] = extract_tags(song)
            enriched_songs.append(song)
            total_songs += 1

            # Accumulate tag counts
            t = song["tags"]
            if t["bpm_tier"]:
                all_tag_counts["bpm_tier"][t["bpm_tier"]] = all_tag_counts["bpm_tier"].get(t["bpm_tier"], 0) + 1
            for cat in ["instruments", "vocals", "mood", "production_era", "lyric_themes", "structure"]:
                for tag in t[cat]:
                    all_tag_counts[cat][tag] = all_tag_counts[cat].get(tag, 0) + 1

        for g in data.get("genres", []):
            all_tag_counts["genres"][g] = all_tag_counts["genres"].get(g, 0) + 1

        data["songs"] = enriched_songs
        data["_file"] = fpath.name
        artists.append(data)

    # Sort tags by count descending
    sorted_tags = {}
    for cat, counts in all_tag_counts.items():
        sorted_tags[cat] = sorted(counts.items(), key=lambda x: -x[1])

    index = {
        "built_at": time.strftime("%Y-%m-%d %H:%M"),
        "total_artists": len(artists),
        "total_songs": total_songs,
        "tag_counts": sorted_tags,
        "artists": artists,
    }

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\n   ✅ Index built: {len(artists)} artists, {total_songs} songs")
    print(f"   📄 Saved to: {INDEX_FILE.name}\n")
    return True


# ── LOCAL SERVER ──────────────────────────────────────────────────────────────

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FOLDER), **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress request logs


def start_server():
    server = http.server.HTTPServer(("127.0.0.1", PORT), QuietHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 52)
    print("  SUNO PROMPT HUB")
    print("=" * 52)

    if not HUB_FILE.exists():
        print(f"\n❌ hub.html not found in {FOLDER}")
        print("   Make sure all files are in the same folder.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Build/rebuild the index
    ok = build_index()
    if not ok:
        input("Press Enter to exit...")
        sys.exit(1)

    # Start local server
    print(f"   🌐 Starting local server on port {PORT}...")
    try:
        server = start_server()
        time.sleep(0.5)
    except OSError:
        print(f"   ⚠️  Port {PORT} in use, trying {PORT+1}...")
        PORT += 1
        server = start_server()

    url = f"http://127.0.0.1:{PORT}/hub.html"
    print(f"   ✅ Server running at {url}")
    print(f"\n   Opening browser...")
    webbrowser.open(url)

    print("\n   Hub is running. Keep this window open.")
    print("   Press Ctrl+C to stop.\n")
    print("─" * 52)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n   Shutting down. Goodbye!")
        server.shutdown()
