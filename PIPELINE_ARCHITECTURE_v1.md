# MANHWA PIPELINE ARCHITECTURE v1.0

**Date:** 2025-10-21  
**Instance:** Sonnet 40  
**Status:** PHASE 2 VALIDATED, PHASE 1 & 3-4 PENDING

---

## VALIDATED PROOF OF CONCEPT

**What We Proved Today:**
```
Scraped Panels → Claude (Sonnet 4.5) → Titan-Tier Script
```

**Evidence:**
- ORV Chapter 0 script generated
- 1200 words, ~6 minutes
- Matches titan video quality patterns
- Uses proven templates
- Production-ready output

**Key Insight:** Claude CAN process panels directly. No Gemini middleman needed.

---

## COMPLETE PIPELINE ARCHITECTURE

### LAYER 0: ACQUISITION
**Status:** ✅ WORKING  
**Tool:** `manhwa_scraper.py`

```python
Input:  Series slug, chapter range
Output: /panels/[series]/ch_[XX]/001.png...
```

**Validated:** ORV chapters 0-2 downloaded successfully.

---

### LAYER 1: PANEL ANALYSIS (MISSING - CRITICAL)
**Status:** ⚠️ NOT YET BUILT  
**Purpose:** Transform raw panels into production manifest

**Input:** Raw panel images (001.png, 002.png, ...)

**Output:** Production-ready analysis file with:

#### A. Visual Content
- Shot composition (close-up, wide, action, dialogue)
- Character positions and expressions
- Environmental details
- Color/mood markers
- Key visual elements for editor

#### B. Textual Content
- Dialogue (with speaker tags)
- Narration boxes
- Sound effects (onomatopoeia)
- System messages (if applicable)

#### C. Conceptual Beats
- Emotional tone (tense, comedic, dramatic, etc.)
- Pacing markers (fast/slow)
- Story function (setup, conflict, resolution, hook)
- Genre tropes present

#### D. Editor Instructions (**NEW - CRITICAL**)
- Timing suggestions (hold time per panel)
- Emphasis markers (zoom, impact, pause)
- SFX suggestions (ambient sound, stingers)
- Intonation notes for voice actor
- Transition recommendations (hard cut, wipe, etc.)

**Example Output Format:**
```json
{
  "chapter": "000",
  "total_panels": 9,
  "panels": [
    {
      "id": "001",
      "visual": {
        "composition": "medium shot",
        "subject": "Kim Dokja, dead-eyed, subway car",
        "mood": "mundane, oppressive",
        "key_elements": ["phone screen", "corporate attire", "empty stare"]
      },
      "text": {
        "dialogue": [],
        "narration": ["Another day, another commute."],
        "sfx": ["subway rumble"]
      },
      "conceptual": {
        "beat": "establish_normalcy",
        "tone": "melancholic",
        "pacing": "slow"
      },
      "editor": {
        "hold_time": "3-4 seconds",
        "emphasis": "slow zoom on phone screen",
        "sfx": "ambient subway noise, low",
        "transition": "hard cut"
      }
    }
  ]
}
```

**Why This Matters:**
- Separates "what's there" from "how to use it"
- Provides rich context for script generation
- Gives editor actionable instructions
- Makes pipeline modular and debuggable

---

### LAYER 2: SCRIPT GENERATION
**Status:** ✅ VALIDATED (Instance 40, 2025-10-21)

**Input:** Panel analysis manifest (from Layer 1)  
**Output:** Titan-tier narration script

**Process:**
1. Load templates:
   - `SCRIPT_TEMPLATE_FILLABLE.md`
   - `NARRATIVE_STRUCTURE_EXTRACTED.md`
   - `PATTERN_LIBRARY_EXTRACTED_v2.md`
   - `META_NARRATION_PATTERNS_v1.md`

2. Transform panel analysis into narrative
   - Apply cold open structure
   - Inject meta-commentary
   - Add retention hooks
   - Format for voice actor

3. Generate production notes
   - Panel selection priorities
   - Pacing guides
   - Retention hook markers

**Proven Capability:**
- Claude Sonnet 4.5 can generate titan-tier scripts
- No external tools needed
- Templates provide structural scaffolding
- Output is production-ready

---

### LAYER 3: VOICE GENERATION
**Status:** 🔍 RESEARCH PHASE  
**Tool:** DIA by NariLabs (via Pinokio)

**Input:** Script text (from Layer 2)  
**Output:** High-quality AI narration (MP3/WAV)

**Known Requirements:**
- Install Pinokio (local AI app manager)
- Set up DIA model
- Configure voice parameters
- Generate audio file

**Research Needed:**
- Pinokio installation process
- DIA model setup
- Voice customization options
- Output format specifications
- Integration with workflow

**Alternative Options (from video analyses):**
- ElevenLabs (cloud, paid)
- Play.ht (cloud, paid)
- WellSaid Labs (cloud, paid)

**Decision:** DIA chosen for local control + quality.

---

### LAYER 4: VIDEO EDITING
**Status:** 🔍 RESEARCH PHASE - **MOST MURKY/UNCLEAR**  
**Tool:** Adobe Premiere Pro (programmatic approach)

**Input:**
- Panel images
- Panel analysis manifest (Layer 1)
- Voice audio (Layer 3)
- Editing templates

**Output:** Final video file

**Known Patterns (from titan video analysis):**
- Hard cuts (95%+ transitions)
- Ken Burns effect (pan + zoom on every panel)
- Audio-visual sync (speak-then-show rhythm)
- Impact zooms for emphasis
- Minimal text overlays

**Critical Unknown:** HOW to automate this?

**Possible Approaches:**

#### Option A: Premiere Pro Scripting
- Use ExtendScript API
- Programmatically place clips
- Apply effects via script
- Timeline automation

**Pros:** Industry-standard tool, powerful  
**Cons:** Complex API, unclear automation path

#### Option B: FFmpeg + Custom Code
- Pure command-line approach
- Full control over every frame
- Python wrapper for logic

**Pros:** Fully automated, open-source  
**Cons:** Very complex, slower iteration

#### Option C: Hybrid (Premiere Templates + Automation)
- Create Premiere template structure
- Use scripting to populate
- Manual polish pass

**Pros:** Best of both worlds  
**Cons:** Still requires manual work

**Research Needed:**
- Premiere Pro automation capabilities
- ExtendScript documentation
- FFmpeg for panel animations
- Integration with manifest data
- Timing/sync automation

**This is the BIGGEST UNKNOWN in the pipeline.**

---

## WORKFLOW SUMMARY

```
┌─────────────────────────────────────┐
│ LAYER 0: ACQUISITION                │
│ manhwa_scraper.py                   │
│ Status: ✅ WORKING                  │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ LAYER 1: PANEL ANALYSIS             │
│ Claude processes panels             │
│ Status: ⚠️ NOT BUILT                │
│ Output: Production manifest         │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ LAYER 2: SCRIPT GENERATION          │
│ Claude + Templates                  │
│ Status: ✅ VALIDATED                │
│ Output: Titan-tier script           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ LAYER 3: VOICE GENERATION           │
│ DIA (via Pinokio)                   │
│ Status: 🔍 RESEARCH NEEDED          │
│ Output: Audio narration             │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ LAYER 4: VIDEO EDITING              │
│ Adobe Premiere Pro (programmatic)   │
│ Status: 🔍 MOST UNCLEAR             │
│ Output: Final video                 │
└─────────────────────────────────────┘
```

---

## IMMEDIATE PRIORITIES

### Priority 1: Document Current State ✅
- This file
- Layer 2 specification
- Validation evidence

### Priority 2: Design Layer 1
- Define manifest structure
- Create panel analysis spec
- Build prototype with Claude

### Priority 3: Research Layer 3
- Pinokio setup
- DIA installation
- Voice generation test

### Priority 4: Research Layer 4 (CRITICAL)
- Premiere Pro automation
- ExtendScript investigation
- Manifest → Timeline mapping
- Timing/sync automation

---

## SUCCESS CRITERIA FOR OPUS HANDOFF

**Goal:** Present working end-to-end pipeline needing only optimization.

**Minimum Viable Pipeline:**
1. ✅ Layer 0: Scraper works
2. ✅ Layer 1: Panel analysis process defined + working
3. ✅ Layer 2: Script generation validated
4. ✅ Layer 3: Voice generation working
5. ⚠️ Layer 4: Editing approach chosen + prototype working

**Handoff Package:**
- Complete documentation
- Working examples (ORV Ch 0 end-to-end)
- Known issues + optimization targets
- Scaling strategy

**Opus Role:**
- Refine architecture
- Optimize each layer
- Scale to batch processing
- Build `CONTINUITY.py` automation

---

## ARCHITECTURAL NOTES

### Why Two-Phase Script Generation?
**Phase 1 (Analysis) + Phase 2 (Generation) = Modularity**

**Benefits:**
1. **Debuggability:** Can verify analysis before script
2. **Flexibility:** Can reuse analysis for different script styles
3. **Editor Support:** Analysis provides rich context
4. **Iteration:** Can refine script without re-analyzing panels

**Alternative (Single-Phase):**
- Panels → Script directly
- Faster but less controllable
- Harder to debug
- Less editor context

**Decision:** Two-phase is correct architecture.

### Critical Insight: Layer 1 Feeds Multiple Outputs
**The panel analysis manifest should support:**
- Script generation (Layer 2)
- Video editing (Layer 4)
- Future variants (shorts, different styles)

**Therefore:** Make it EXHAUSTIVE. Better to capture everything and filter later.

---

## NEXT SESSION OBJECTIVES

1. Build Layer 1 specification document
2. Create panel analysis prototype (ORV Ch 0)
3. Research DIA + Pinokio setup
4. Investigate Premiere Pro automation
5. Document findings rigorously

---

**The pattern converges. The system crystallizes.** 🌊💙⚔️
