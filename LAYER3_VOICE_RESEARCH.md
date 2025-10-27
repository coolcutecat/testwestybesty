# LAYER 3: VOICE GENERATION RESEARCH

**Status:** 🔍 RESEARCH PHASE  
**Tool:** DIA by NariLabs (via Pinokio)  
**Date:** 2025-10-21

---

## OBJECTIVE

Generate high-quality AI narration from script text using DIA (local, controllable alternative to ElevenLabs).

---

## KNOWN INFORMATION

### Tool: DIA by NariLabs
- AI voice synthesis model
- Designed for natural, emotive speech
- Local inference (vs cloud services)
- Accessed via Pinokio app manager

### Tool: Pinokio
- Local AI app manager/launcher
- Simplifies installation of AI models
- Handles dependencies automatically
- One-click setup for supported models

### Why DIA Over Alternatives?
**Alternatives from video analyses:**
- ElevenLabs (cloud, subscription, industry leader)
- Play.ht (cloud, subscription)
- WellSaid Labs (cloud, subscription, professional quality)

**DIA Advantages:**
- Local control (no API limits)
- No recurring costs
- Data privacy (scripts stay local)
- Customization potential

---

## RESEARCH OBJECTIVES

### Phase 1: Installation
**Questions:**
1. How to install Pinokio?
   - OS requirements (Windows/Mac/Linux)
   - Download source
   - Installation process

2. How to install DIA through Pinokio?
   - Model size/requirements
   - GPU requirements (CUDA? Apple Silicon?)
   - Storage space needed
   - Installation time

3. Dependencies?
   - Python version
   - Additional packages
   - System libraries

### Phase 2: Configuration
**Questions:**
1. How to configure DIA?
   - Voice selection/creation
   - Quality settings
   - Output format options

2. Voice customization?
   - Pre-trained voices available
   - Voice cloning capability
   - Fine-tuning process

3. Performance optimization?
   - GPU vs CPU inference
   - Batch processing support
   - Real-time vs offline generation

### Phase 3: Integration
**Questions:**
1. How to automate voice generation?
   - Command-line interface
   - Python API
   - Batch script processing

2. Input format requirements?
   - Plain text
   - SSML support
   - Markup for intonation/emphasis

3. Output specifications?
   - Audio format (WAV, MP3, etc.)
   - Sample rate
   - Bitrate
   - Mono vs stereo

### Phase 4: Quality Control
**Questions:**
1. How to control narration style?
   - Speed/pace adjustments
   - Emotion/tone settings
   - Emphasis markers

2. How to handle special cases?
   - Character voices (dialogue)
   - Sound effects in text
   - Foreign words/names
   - Numbers and dates

3. Quality validation?
   - Listening checkpoints
   - Automated quality checks
   - Regeneration workflow

---

## WORKFLOW DESIGN

### Ideal Pipeline: Script → Voice

```
┌────────────────────────────┐
│ Layer 2: Script Generation │
│ Output: script.md          │
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ Preprocessing:             │
│ - Extract narration text   │
│ - Add intonation markup    │
│ - Split by segments        │
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ DIA Voice Generation:      │
│ - Load script segments     │
│ - Apply voice model        │
│ - Generate audio chunks    │
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ Post-processing:           │
│ - Concatenate segments     │
│ - Normalize audio levels   │
│ - Export final narration   │
└────────────────────────────┘
           ↓
┌────────────────────────────┐
│ Layer 4: Video Editing     │
│ Input: narration.mp3       │
└────────────────────────────┘
```

### Script Preprocessing Needs

**Extract Narration Only:**
- Filter out production notes
- Remove panel references
- Keep only spoken text

**Add Markup:**
- Pauses: `[pause: 0.5s]`
- Emphasis: `*word*` or `**WORD**`
- Tone shifts: `[tone: sarcastic]`
- Speed: `[speed: fast]` or `[speed: slow]`

**Segment for Control:**
- Break at natural pauses
- Separate by conceptual beats
- Allow per-segment regeneration

### Quality Validation Checklist

**Technical:**
- [ ] Clear pronunciation
- [ ] Consistent volume
- [ ] No artifacts/glitches
- [ ] Proper pacing

**Stylistic:**
- [ ] Matches script tone
- [ ] Appropriate energy
- [ ] Natural inflection
- [ ] Engaging delivery

**Narrative:**
- [ ] Emphasizes key points
- [ ] Retention hook delivery
- [ ] Joke timing lands
- [ ] Emotional beats hit

---

## TESTING PROTOCOL

### Test 1: Installation Validation
**Objective:** Verify DIA works on local machine

**Steps:**
1. Install Pinokio
2. Install DIA through Pinokio
3. Generate test audio from simple text
4. Confirm output quality

**Success Criteria:**
- Installation completes without errors
- Audio generation works
- Output is intelligible

### Test 2: Script Processing
**Objective:** Test with actual ORV script

**Steps:**
1. Extract narration from ORV Ch 0 script
2. Add basic markup
3. Generate full narration
4. Time the output

**Success Criteria:**
- Narration length ~5-7 minutes
- Quality matches titan video standards
- Pacing feels natural

### Test 3: Customization
**Objective:** Achieve specific narrator voice/style

**Steps:**
1. Test different voice models
2. Adjust tone/speed settings
3. Add emphasis markup
4. Compare variants

**Success Criteria:**
- Voice matches intended style (casual, energetic, genre-savvy)
- Can control emphasis effectively
- Regeneration is fast enough for iteration

---

## DOCUMENTATION REQUIREMENTS

### For Pipeline Integration:
- Installation guide (step-by-step)
- Configuration guide (voice setup, settings)
- Usage guide (command-line, Python API)
- Troubleshooting guide (common issues)

### For Handoff to Opus:
- Performance benchmarks (generation time per minute)
- Quality assessment (vs ElevenLabs baseline)
- Optimization opportunities identified
- Scaling considerations (batch processing)

---

## FALLBACK OPTIONS

### If DIA Doesn't Work:

**Option A: ElevenLabs API**
- Proven quality
- Fast setup
- Cost: ~$5-30/month depending on usage
- Requires API key management

**Option B: Other Local TTS**
- Coqui TTS
- Bark
- StyleTTS2
- Research required for each

**Option C: Hybrid Approach**
- DIA for bulk narration
- ElevenLabs for critical segments
- Cost optimization

**Decision Point:** After Test 2, if DIA quality insufficient, pivot to Option A.

---

## RESEARCH TIMELINE

### Immediate (This Session):
- [ ] Web search: Pinokio installation guide
- [ ] Web search: DIA by NariLabs documentation
- [ ] Web search: DIA + Pinokio integration
- [ ] Compile installation steps

### Next Session:
- [ ] Install Pinokio
- [ ] Install DIA
- [ ] Run Test 1 (basic audio generation)
- [ ] Document installation process

### Following Session:
- [ ] Run Test 2 (ORV script processing)
- [ ] Run Test 3 (voice customization)
- [ ] Write integration guide
- [ ] Validate with full pipeline test

---

## QUESTIONS FOR WEB RESEARCH

1. "Pinokio AI app manager installation guide"
2. "DIA by NariLabs voice synthesis setup"
3. "DIA Pinokio integration tutorial"
4. "DIA voice generation command line"
5. "Best local text-to-speech AI models 2025"
6. "DIA vs ElevenLabs quality comparison"

---

**Status:** Ready for research phase. Pinokio + DIA is the path forward.

🌊💙⚔️
