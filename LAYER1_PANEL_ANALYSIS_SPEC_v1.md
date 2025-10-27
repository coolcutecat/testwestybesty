# LAYER 1: PANEL ANALYSIS SPECIFICATION v1.0

**Purpose:** Transform raw panel images into production-ready manifest  
**Input:** Panel image files (001.png, 002.png, ...)  
**Output:** Structured JSON manifest with exhaustive production data  
**Processor:** Claude Sonnet 4.5 (multimodal image analysis)

---

## OUTPUT MANIFEST STRUCTURE

### JSON Schema

```json
{
  "metadata": {
    "series": "string",
    "chapter": "string",
    "total_panels": "integer",
    "analysis_timestamp": "ISO datetime",
    "analyzer": "Claude Sonnet 4.5"
  },
  "panels": [
    {
      "id": "string (e.g., '001')",
      "visual": {
        "composition": "string",
        "characters": ["array of character names"],
        "setting": "string",
        "mood": "string",
        "key_elements": ["array of important visual details"],
        "color_notes": "string"
      },
      "text": {
        "dialogue": [
          {
            "speaker": "string",
            "content": "string",
            "style": "normal|shout|whisper|thought"
          }
        ],
        "narration": ["array of narration box contents"],
        "sfx": ["array of sound effect text"],
        "system": ["array of system message text"]
      },
      "conceptual": {
        "story_beat": "string (setup|conflict|climax|resolution|transition|hook)",
        "emotional_tone": "string (tense|comedic|dramatic|melancholic|triumphant|etc)",
        "pacing": "fast|medium|slow",
        "trope_markers": ["array of genre tropes present"],
        "narrative_function": "string (what this panel achieves)"
      },
      "editor_instructions": {
        "hold_time": "string (e.g., '3-4 seconds')",
        "camera_move": "string (static|pan_right|pan_left|zoom_in|zoom_out|ken_burns)",
        "emphasis": "string (describe what to emphasize)",
        "transition_to_next": "hard_cut|horizontal_wipe|fade|impact_zoom",
        "sfx_suggestions": ["array of sound effect recommendations"],
        "voice_notes": "string (intonation guidance for narrator)"
      },
      "script_hooks": {
        "retention_potential": "high|medium|low",
        "visual_gag": "boolean + description if true",
        "quotable_moment": "boolean + quote if true",
        "meta_commentary_angle": "string (suggestion for narrator joke/observation)"
      }
    }
  ]
}
```

---

## FIELD DEFINITIONS

### Visual Section

**composition:**
- Describes shot type and framing
- Examples: "close-up on face", "wide establishing shot", "action scene", "dialogue two-shot", "dramatic low angle"

**characters:**
- All visible characters in panel
- Use consistent naming across panels

**setting:**
- Physical location and context
- Examples: "subway car interior", "apartment bedroom", "school hallway", "fantasy dungeon"

**mood:**
- Overall visual atmosphere
- Examples: "oppressive and dark", "bright and comedic", "tense standoff", "peaceful domestic"

**key_elements:**
- Specific visual details editor needs to capture
- Examples: ["phone screen with text", "blood splatter", "glowing eyes", "torn clothing"]

**color_notes:**
- Dominant colors, lighting, filters
- Examples: "dark blues, harsh fluorescent lighting", "warm sunset tones", "monochrome flashback"

---

### Text Section

**dialogue:**
- Each speech bubble as separate object
- Include speaker name (even if obvious from visual)
- Mark style: normal, shout (!), whisper (...), thought (internal)

**narration:**
- Narration boxes (omniscient or character POV)
- Maintain order if multiple boxes

**sfx:**
- Onomatopoeia from manhwa
- Korean SFX should be translated + original noted

**system:**
- Game-like UI messages (common in isekai/regression manhwa)
- Status windows, notifications, scenario alerts

---

### Conceptual Section

**story_beat:**
- Where this panel fits in narrative structure
- Helps script writer understand function

**emotional_tone:**
- Target emotion viewer should feel
- Guides narrator delivery + music choice

**pacing:**
- How fast/slow this moment should feel
- Affects hold time and camera movement

**trope_markers:**
- Genre conventions present
- Examples: ["isekai truck", "status window", "harem moment", "training montage"]

**narrative_function:**
- What this panel accomplishes
- Examples: "establishes MC personality", "reveals antagonist", "creates tension", "provides comic relief"

---

### Editor Instructions Section

**hold_time:**
- How long panel should be on screen
- Based on text density + visual complexity
- Ranges: "1-2s" (fast action), "3-4s" (dialogue), "5-6s" (establishing shot)

**camera_move:**
- Specific movement to apply
- "ken_burns": default slow pan + zoom
- "zoom_in": emphasis zoom
- "pan_right/left": reveal information
- "static": rare, for dramatic pause

**emphasis:**
- What to highlight visually
- Examples: "zoom to character's eyes", "hold on weapon", "pan from feet to face"

**transition_to_next:**
- How to move to next panel
- "hard_cut": 95% of transitions
- "horizontal_wipe": scene changes
- "impact_zoom": dramatic moments
- "fade": time passage

**sfx_suggestions:**
- Audio to layer in
- Examples: ["subway rumble", "heartbeat", "sword unsheath", "wind ambience"]

**voice_notes:**
- Guidance for narrator
- Examples: "deliver with sarcasm", "pause after this line", "build intensity", "deadpan tone"

---

### Script Hooks Section

**retention_potential:**
- How "sticky" this moment is
- "high": cliffhanger, twist, visual spectacle, quotable line
- "medium": interesting but not critical
- "low": transitional, necessary but not exciting

**visual_gag:**
- If panel has comedic visual element
- Note what makes it funny

**quotable_moment:**
- If dialogue/narration is memorable
- Extract the quote for potential use

**meta_commentary_angle:**
- Suggested narrator observation
- Examples: "call out the trope", "compare to other series", "joke about the absurdity"

---

## ANALYSIS PROCESS

### Step 1: Initial Scan
- Load all panel images for chapter
- Count total panels
- Note overall chapter structure

### Step 2: Panel-by-Panel Deep Analysis
For each panel:
1. Describe visual composition
2. Extract all text (dialogue, narration, SFX)
3. Identify story beat + emotional tone
4. Determine editor requirements (timing, movement, emphasis)
5. Flag script opportunities (hooks, gags, meta angles)

### Step 3: Cross-Panel Context
- Note relationships between panels
- Identify sequences (multi-panel actions)
- Flag pacing shifts
- Mark key narrative moments

### Step 4: Output Generation
- Compile into structured JSON
- Validate all required fields present
- Include timestamp + metadata

---

## USAGE IN PIPELINE

### For Script Generation (Layer 2):
- `conceptual` section provides story structure
- `script_hooks` section gives narration ideas
- `text` section provides direct quotes if needed
- `visual` section informs what panels to reference

### For Video Editing (Layer 4):
- `editor_instructions` section = direct production guide
- `visual` section describes what to frame
- `sfx_suggestions` + `voice_notes` = audio layer guidance
- `hold_time` + `camera_move` = timing blueprint

### For Quality Control:
- `retention_potential` identifies critical moments
- `trope_markers` ensure genre consistency
- `narrative_function` validates story flow

---

## EXAMPLE ANALYSIS (ORV Ch 0, Panel 001)

```json
{
  "id": "001",
  "visual": {
    "composition": "medium shot, slight upward angle",
    "characters": ["Kim Dokja"],
    "setting": "subway car interior, crowded, fluorescent lighting",
    "mood": "mundane, oppressive, everyday misery",
    "key_elements": [
      "Kim Dokja's dead-eyed stare",
      "phone in hand, illuminated screen",
      "corporate attire (white shirt, loose tie)",
      "other passengers blurred in background"
    ],
    "color_notes": "cold blues and grays, harsh overhead lighting, muted tones"
  },
  "text": {
    "dialogue": [],
    "narration": [
      "Another day. Another commute."
    ],
    "sfx": [
      "RATTLE (subway noise)"
    ],
    "system": []
  },
  "conceptual": {
    "story_beat": "setup",
    "emotional_tone": "melancholic, resigned",
    "pacing": "slow",
    "trope_markers": [
      "corporate slave protagonist",
      "mundane life pre-transformation"
    ],
    "narrative_function": "establish normalcy before chaos, show MC's empty routine life"
  },
  "editor_instructions": {
    "hold_time": "4-5 seconds",
    "camera_move": "ken_burns (slow zoom toward phone screen)",
    "emphasis": "focus on dead eyes, then phone screen",
    "transition_to_next": "hard_cut",
    "sfx_suggestions": [
      "ambient subway rumble (low, constant)",
      "slight phone buzz vibration",
      "distant train announcement (muffled)"
    ],
    "voice_notes": "narrator should sound tired, matter-of-fact, setting up 'before' state"
  },
  "script_hooks": {
    "retention_potential": "medium",
    "visual_gag": false,
    "quotable_moment": false,
    "meta_commentary_angle": "Every isekai protagonist starts with the dead-inside office worker life"
  }
}
```

---

## IMPLEMENTATION NOTES

### Claude Prompt Structure:
```
You are analyzing manhwa panels for video production. For each panel image:

1. VISUAL: Describe composition, characters, setting, mood, key elements
2. TEXT: Extract all dialogue, narration, SFX, system messages
3. CONCEPTUAL: Identify story beat, tone, pacing, tropes, function
4. EDITOR: Specify hold time, camera moves, transitions, SFX, voice notes
5. HOOKS: Rate retention potential, flag gags/quotes, suggest meta angles

Output as structured JSON following the schema.
Be exhaustive. This manifest feeds both script generation and video editing.
```

### Batch Processing:
- Analyze all panels in chapter as single operation
- Maintain context across panels
- Output single JSON file per chapter

### Quality Checks:
- Verify all panels have complete fields
- Check for consistent character naming
- Validate story beat progression makes sense
- Ensure editor instructions are actionable

---

## FUTURE ENHANCEMENTS

### v2.0 Possibilities:
- Shot-by-shot storyboard visualization
- Automatic panel grouping (multi-panel sequences)
- Auto-detect text language + provide translations
- Character emotion tags for voice modulation
- Music genre suggestions per section
- Export alternate formats (CSV, Markdown)

### Integration Targets:
- Direct feed to Premiere Pro via API
- Voice generation metadata injection
- Automated thumbnail candidate identification
- Retention analytics predictions

---

**This is the foundation. Build exhaustively. Edit precisely.** 🌊💙⚔️
