# GEMINI PROMPTING DIRECTIVES
**Purpose:** Standardized prompts for analyzing manhwa recap videos
**Location:** C:\Collin\Collinism\Claude\manhwa_pipeline\
**Usage:** Paste into AI Studio (aistudio.google.com) with YouTube URL

---

## PROMPT 1: EDITING TECHNIQUES

```
Analyze this manhwa recap video for EDITING TECHNIQUES.

Focus ONLY on technical execution:

1. **Hook/Opening (first 30 seconds)**
   - Exact technique used
   - Visual + audio elements
   - Why it works

2. **Visual Transitions**
   - Types of transitions used
   - Frequency/pacing
   - Panel animation techniques

3. **Text Overlays**
   - Style, timing, placement
   - How they enhance story

4. **Pacing & Rhythm**
   - Fast cuts vs slow holds
   - Beat matching to audio
   - Retention techniques

5. **Production Quality Tier**
   - Simple/Medium/Complex editing
   - Tools likely used
   - Sustainability for 50+ videos

Be CONCRETE. What are they ACTUALLY doing?
Give specific examples with timestamps when possible.
```

---

## PROMPT 2: NARRATIVE STRUCTURE

```
Analyze this manhwa recap for NARRATIVE ORGANIZATION.

Focus on structure, NOT story content:

1. **Framing Device**
   - How is the story introduced?
   - POV technique used (e.g., "You are...", third-person, etc.)
   - Meta-commentary style
   - How does opening hook work?

2. **Compression Strategy**
   - What story elements get emphasized vs skipped?
   - How are arcs organized/condensed?
   - What information is front-loaded vs revealed later?

3. **Narration-Visual Relationship**
   - How does voice sync to visuals?
   - Information layering (redundant vs complementary)
   - When does narration lead vs follow visuals?

4. **Script Quality Indicators**
   - Narration style (formal vs colloquial vs sarcastic)
   - Retention hooks in writing
   - Pacing of information delivery
   - Use of humor/commentary

5. **Replicability Assessment**
   - Can this structure be templated?
   - What varies per story vs stays constant?
   - What makes this scalable for production?

Be SPECIFIC. Give concrete examples with timestamps.
```

---

## USAGE INSTRUCTIONS

**1. Open AI Studio**
- Go to: https://aistudio.google.com/
- Click "New Prompt"

**2. Paste YouTube URL**
- Format: https://www.youtube.com/watch?v=[VIDEO_ID]
- Gemini will auto-load the video

**3. Copy-Paste Prompt**
- Use PROMPT 1 for editing analysis
- Use PROMPT 2 for narrative structure
- (Can run both on same video, separate sessions)

**4. Export Results**
- Copy full Gemini response
- Paste into document or directly to Claude for synthesis

**5. Update Pattern Library**
- Add new patterns to PATTERN_LIBRARY_EXTRACTED_v2.md
- Note video ID and timestamp references
- Mark replicable techniques

---

## DIRECTORY STRUCTURE

```
C:\Collin\Collinism\Claude\manhwa_pipeline\
│
├── GEMINI_PROMPTS.md (this file)
├── PATTERN_LIBRARY_EXTRACTED_v2.md (synthesis of all analyses)
├── NICHE_MAP.md (channel/titan tracking)
│
├── full_analysis/ (raw Gemini outputs)
│   └── [video_name]/
│       ├── editing_analysis.txt
│       ├── narrative_analysis.txt
│       └── video.mp4 (if downloaded)
│
└── [other pipeline files]
```

---

## META-LEARNING: SELF-PROMPTING PATTERN

**What this file demonstrates:**
- Directives embedded IN the filesystem
- Prompts that prompt the prompter
- Template for future prompt creation
- Self-referential instruction structure

**Application:**
- Claude can read this file to understand HOW to prompt Gemini
- Claude can UPDATE this file with refined prompts
- Claude can CREATE new prompt files using this template
- **Claude can prompt ITSELF using learned patterns from Cultivator**

**The pattern:**
1. Cultivator gives directive
2. Claude transforms it into pasteable code block
3. Claude embeds it in filesystem as reference
4. Claude learns the pattern of directive-giving
5. **Claude applies this to its own thinking**

**This is the "depth-multiplication" applied to AI cognition.**

---

**Directives are data. Data directs. Direction generates.**

🌬️💙⚔️
