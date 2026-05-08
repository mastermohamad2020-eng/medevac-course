#!/usr/bin/env python3
"""
============================================================
MEDEVAC AT SEA - Voice Generator (GitHub Actions Edition)
============================================================
- يقرأ API key من متغير البيئة ELEVEN_API_KEY
- يولّد English-only افتراضياً (للتوفير)
- يعمل auto-resume (يتخطى الموجود)
- يطبع تقدماً واضحاً للـ GitHub Actions log
============================================================
"""

import os
import sys
import json
import time
import re
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ Missing 'requests' library. Run: pip install requests")
    sys.exit(1)

# ============================================================
# CONFIGURATION (read from environment when on GitHub Actions)
# ============================================================

API_KEY = os.environ.get("ELEVEN_API_KEY", "").strip()

# اللغة المطلوبة: 'en' (افتراضي), 'ar', أو 'both'
LANGUAGE = os.environ.get("GENERATE_LANGUAGE", "en").strip().lower()

DATA_FILE = "course_data.json"
OUTPUT_DIR = "audio"
MODEL_ID = "eleven_multilingual_v2"
DELAY_BETWEEN_REQUESTS = 0.4

# ============================================================
# VOICE MAPPING
# ============================================================
VOICES = {
    'master':       {'id': 'pNInz6obpgDQGcFmaJgB', 'name': 'Adam'},
    'chief':        {'id': 'TxGEqnHWrfWFTfGW9XjX', 'name': 'Josh'},
    '3rd':          {'id': 'VR6AewLTigWG4xSOukaG', 'name': 'Arnold'},
    'officer':      {'id': 'VR6AewLTigWG4xSOukaG', 'name': 'Arnold'},
    'bosun':        {'id': 'pqHfZKP75CvOlQylNhV4', 'name': 'Bill'},
    'patient':      {'id': 'IKne3meq5aSn9XLyUdCD', 'name': 'Charlie'},
    'doctor':       {'id': 'JBFqnCBsd6RMkjVDRZzb', 'name': 'George'},
    'mrcc':         {'id': 'iP95p4xoKVk53GoZ742B', 'name': 'Chris'},
    'pilot':        {'id': 'onwK4e9ZLuTAKqWW03F9', 'name': 'Daniel'},
    'helicopter':   {'id': 'onwK4e9ZLuTAKqWW03F9', 'name': 'Daniel'},
    'rescue':       {'id': 'onwK4e9ZLuTAKqWW03F9', 'name': 'Daniel'},
    'helmsman':     {'id': 'IKne3meq5aSn9XLyUdCD', 'name': 'Charlie'},
    'engine':       {'id': 'pqHfZKP75CvOlQylNhV4', 'name': 'Bill'},
    'system':       {'id': 'EXAVITQu4vr4xnSDxMaL', 'name': 'Bella'},
    'simulation':   {'id': 'EXAVITQu4vr4xnSDxMaL', 'name': 'Bella'},
    'all stations': {'id': 'EXAVITQu4vr4xnSDxMaL', 'name': 'Bella'},
    'default':      {'id': 'pNInz6obpgDQGcFmaJgB', 'name': 'Adam'}
}

VOICE_SETTINGS = {
    'stability': 0.55,
    'similarity_boost': 0.78,
    'style': 0.20,
    'use_speaker_boost': True
}

# ============================================================
# HELPERS
# ============================================================

def resolve_voice(speaker):
    if not speaker:
        return VOICES['default']
    s = speaker.lower()
    keys = ['master', 'chief', '3rd', 'bosun', 'patient', 'doctor', 'mrcc',
            'pilot', 'helicopter', 'rescue', 'helmsman', 'engine',
            'system', 'simulation', 'all stations', 'officer']
    for key in keys:
        if key in s:
            return VOICES[key]
    return VOICES['default']

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_skippable(text):
    if not text:
        return True
    cleaned = text.strip()
    return not cleaned or cleaned.upper().startswith("N/A")

def fetch_audio(text, voice_id, output_path, retries=2):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': API_KEY
    }
    body = {
        'text': text,
        'model_id': MODEL_ID,
        'voice_settings': VOICE_SETTINGS
    }
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, json=body, headers=headers, timeout=60)
            if resp.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(resp.content)
                return True, None
            elif resp.status_code == 401:
                return False, "INVALID_API_KEY"
            elif resp.status_code == 429:
                if attempt < retries:
                    time.sleep(30)
                    continue
                return False, "RATE_LIMIT"
            else:
                if attempt < retries:
                    time.sleep(2)
                    continue
                return False, f"HTTP_{resp.status_code}: {resp.text[:120]}"
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                time.sleep(3)
                continue
            return False, f"NETWORK: {e}"
    return False, "UNKNOWN"

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("⚓  MEDEVAC AT SEA - Voice Generator (GitHub Actions)")
    print("=" * 70)
    print(f"  Language: {LANGUAGE}")
    print(f"  Model:    {MODEL_ID}")
    print(f"  Output:   {OUTPUT_DIR}/")
    print("=" * 70)

    if not API_KEY:
        print("❌ ERROR: ELEVEN_API_KEY environment variable is empty")
        print()
        print("If running on GitHub Actions:")
        print("  1. Go to: Settings → Secrets and variables → Actions")
        print("  2. Click 'New repository secret'")
        print("  3. Name: ELEVEN_API_KEY")
        print("  4. Value: your ElevenLabs API key (starts with sk-...)")
        print()
        print("If running locally:")
        print("  export ELEVEN_API_KEY='sk-your-key-here'")
        sys.exit(1)

    if not os.path.exists(DATA_FILE):
        print(f"❌ ERROR: {DATA_FILE} not found in current directory")
        sys.exit(1)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modules = data.get('modules', [])
    print(f"✓ Loaded {len(modules)} modules")

    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Determine which languages to generate
    if LANGUAGE == 'both':
        langs = ['en', 'ar']
    elif LANGUAGE == 'ar':
        langs = ['ar']
    else:
        langs = ['en']

    print(f"✓ Languages: {', '.join(langs)}")

    # Collect all tasks
    tasks = []
    for mod in modules:
        for lesson in mod.get('lessons', []):
            for scene in lesson.get('scenes', []):
                scene_id = scene.get('scene_id', 'unknown')
                for d_idx, line in enumerate(scene.get('dialogue', [])):
                    speaker = line.get('speaker', '')
                    voice = resolve_voice(speaker)
                    for lang in langs:
                        text_field = 'english' if lang == 'en' else 'arabic'
                        text = clean_text(line.get(text_field, ''))
                        if is_skippable(text):
                            continue
                        tasks.append({
                            'scene_id': scene_id,
                            'd_idx': d_idx,
                            'lang': lang,
                            'text': text,
                            'voice_id': voice['id'],
                            'voice_name': voice['name'],
                            'speaker': speaker
                        })

    print(f"✓ Total tasks: {len(tasks)}")
    total_chars = sum(len(t['text']) for t in tasks)
    print(f"✓ Total characters: {total_chars:,}")

    # Filter out already-existing files
    pending = []
    skipped = 0
    for task in tasks:
        filename = f"{task['scene_id']}-d{task['d_idx']}-{task['lang']}.mp3"
        path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(path) and os.path.getsize(path) > 100:
            skipped += 1
        else:
            pending.append(task)

    print(f"✓ Already generated: {skipped}")
    print(f"✓ Need to generate:  {len(pending)}")
    print()

    if not pending:
        print("🎉 All audio files already generated. Nothing to do.")
        return

    # Generate
    print("=" * 70)
    print("🎙  Generating new audio files...")
    print("=" * 70)

    success = 0
    fail = 0
    failed_files = []

    for i, task in enumerate(pending, 1):
        filename = f"{task['scene_id']}-d{task['d_idx']}-{task['lang']}.mp3"
        path = os.path.join(OUTPUT_DIR, filename)
        display_text = task['text'][:55] + ('...' if len(task['text']) > 55 else '')
        print(f"[{i}/{len(pending)}] {filename} | {task['voice_name']} | {display_text}", flush=True)

        ok, err = fetch_audio(task['text'], task['voice_id'], path)
        if ok:
            success += 1
        else:
            fail += 1
            failed_files.append(f"{filename} → {err}")
            print(f"   ❌ FAILED: {err}", flush=True)
            if err == "INVALID_API_KEY":
                print()
                print("=" * 70)
                print("❌ FATAL: Invalid API key. Aborting.")
                print("=" * 70)
                sys.exit(1)

        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Summary
    print()
    print("=" * 70)
    print(f"✅ GENERATION COMPLETE")
    print(f"  ✓ Generated:   {success}")
    print(f"  ⏭  Skipped:    {skipped}")
    print(f"  ❌ Failed:     {fail}")
    print(f"  📁 Output:     {OUTPUT_DIR}/")
    print("=" * 70)

    if failed_files:
        print("Failed files:")
        for f in failed_files[:20]:
            print(f"  - {f}")
        if len(failed_files) > 20:
            print(f"  ... and {len(failed_files) - 20} more")
        # Don't fail the workflow on partial failures
        print()
        print("⚠ Some files failed but workflow continues.")

if __name__ == "__main__":
    main()
