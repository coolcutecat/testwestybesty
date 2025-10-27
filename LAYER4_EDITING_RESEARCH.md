# LAYER 4: VIDEO EDITING RESEARCH

**Status:** 🔍 RESEARCH PHASE - **MOST MURKY/UNCLEAR**  
**Tool:** Adobe Premiere Pro (programmatic approach)  
**Date:** 2025-10-21

---

## THE CORE CHALLENGE

**How do we automate video editing from structured data?**

**Input:**
- Panel images (Layer 0)
- Panel analysis manifest (Layer 1)
- Narration audio (Layer 3)

**Output:**
- Final edited video matching titan-tier quality

**The Gap:** This is not a solved problem in our pipeline.

---

## KNOWN REQUIREMENTS (From Titan Video Analysis)

### Visual Patterns
- Hard cuts (95%+ transitions)
- Ken Burns effect on every panel (slow pan + zoom)
- Impact zooms for emphasis
- Minimal text overlays
- Background music layer

### Timing Patterns
- Speak-then-show rhythm (cuts synced to narration)
- Variable hold times (1-2s fast, 3-6s standard, 5-8s slow)
- Audio-visual sync is CRITICAL

### Quality Markers
- Smooth motion (60fps export)
- Consistent color grading
- Professional polish
- High retention through pacing

---

## POSSIBLE APPROACHES

### Approach A: Premiere Pro Scripting (ExtendScript)

**Concept:** Use Adobe's ExtendScript API to programmatically build timeline

**Pros:**
- Industry-standard tool
- Full feature access
- Professional quality output
- Template system available

**Cons:**
- Complex API (JavaScript-based)
- Limited documentation
- Steep learning curve
- May require manual polish

**Research Needed:**
1. ExtendScript documentation
2. Timeline manipulation capabilities
3. Effect automation (Ken Burns)
4. Audio sync mechanisms
5. Export automation

**Key Questions:**
- Can we programmatically place clips with precise timing?
- Can we apply effects (pan, zoom) via script?
- Can we sync cuts to audio waveform peaks?
- Can we automate export settings?

---

### Approach B: FFmpeg + Python

**Concept:** Pure command-line video processing

**Pros:**
- Complete control
- Fully automated
- Open-source
- No licensing costs

**Cons:**
- VERY complex for advanced effects
- Slower iteration
- Lower-level control required
- May not achieve professional polish easily

**Research Needed:**
1. FFmpeg image sequence processing
2. Pan/zoom effects in FFmpeg
3. Audio-video synchronization
4. Timeline construction logic
5. Effect stacking

**Key Questions:**
- Can FFmpeg achieve smooth Ken Burns effect?
- How to time cuts to audio markers?
- Performance at scale (50+ videos)?
- Quality vs Premiere Pro output?

---

### Approach C: Hybrid (Template + Automation)

**Concept:** Premiere Pro template + ExtendScript population

**Pros:**
- Best of both worlds
- Faster iteration
- Professional quality
- Reusable templates

**Cons:**
- Still requires some manual work
- Template design complexity
- May not be fully automated

**Process:**
1. Design Premiere Pro template structure
2. Use ExtendScript to populate:
   - Panel images in correct order
   - Audio track alignment
   - Effect parameters (timing, intensity)
3. Manual polish pass (if needed)

**Research Needed:**
- Premiere Pro template creation
- Dynamic template population
- Parameterized effects
- Batch processing capabilities

---

### Approach D: Specialized Tool (DaVinci Resolve API)

**Concept:** Use DaVinci Resolve's Python API instead of Premiere

**Pros:**
- Native Python support
- Powerful automation
- Free version available
- Professional features

**Cons:**
- Different tool from initial plan
- API learning curve
- May have limitations vs Premiere

**Research Needed:**
- DaVinci Resolve Python API capabilities
- Timeline automation
- Effect scripting
- Batch processing

---

## CRITICAL TECHNICAL CHALLENGES

### Challenge 1: Audio-Visual Sync
**Problem:** Cuts must happen precisely when narrator finishes phrases

**Approaches:**
1. **Waveform Analysis:**
   - Detect pauses in audio
   - Cut on silence markers
   - Requires audio processing library

2. **Manual Timing from Manifest:**
   - Use Layer 1 hold_time specifications
   - Calculate cumulative timestamps
   - Place cuts at calculated times

3. **Hybrid:**
   - Start with manifest times
   - Adjust based on audio analysis
   - Validate sync quality

**Research Target:** Which approach is most reliable?

---

### Challenge 2: Ken Burns Effect
**Problem:** Every panel needs smooth pan + zoom

**Premiere Pro Approach:**
- Apply Motion effect
- Keyframe Position (X, Y)
- Keyframe Scale
- Set easing (Bezier curves)

**FFmpeg Approach:**
- Use zoompan filter
- Calculate start/end coordinates
- Apply over duration

**Questions:**
- Can we parameterize pan direction based on panel content?
- How to vary zoom intensity for variety?
- How to ensure smoothness at 60fps?

---

### Challenge 3: Timing Calculation
**Problem:** Convert hold times + transitions into precise timeline positions

**Algorithm Needed:**
```python
def calculate_timeline():
    cumulative_time = 0
    for panel in manifest:
        # Start time for this panel
        panel.start_time = cumulative_time
        
        # Duration based on hold_time
        panel.duration = parse_time(panel.hold_time)
        
        # End time
        panel.end_time = cumulative_time + panel.duration
        
        # Add transition overlap if needed
        if panel.transition == "horizontal_wipe":
            # Overlap next panel by 0.5s
            cumulative_time += (panel.duration - 0.5)
        else:
            cumulative_time += panel.duration
    
    return timeline
```

**Validation:** Must match narration audio length exactly

---

### Challenge 4: Effect Parameterization
**Problem:** Different panels need different camera moves

**From Manifest:**
- `camera_move`: "ken_burns", "zoom_in", "pan_right", etc.
- `emphasis`: Describes what to highlight

**Translation Required:**
- "zoom_in" → Scale from 100% to 120%, center on emphasis area
- "pan_right" → Position from left to right, subtle zoom
- "ken_burns" → Slight pan + zoom, direction based on panel content

**Research Needed:**
- How to auto-detect optimal pan direction?
- How to identify emphasis regions in panel?
- How to vary effects to avoid monotony?

---

## RESEARCH QUESTIONS (Priority Order)

### Priority 1: Tool Selection
1. What are Adobe Premiere Pro's automation capabilities?
2. What is ExtendScript? How powerful is it?
3. Can we achieve our requirements with ExtendScript?
4. If not, what are the alternatives?

### Priority 2: Audio Sync
5. How to detect phrase boundaries in audio?
6. Best libraries for audio waveform analysis?
7. How to align cuts with narration pauses?

### Priority 3: Effect Automation
8. How to programmatically apply Motion effects in Premiere?
9. Can we use templates with parameterized effects?
10. How to ensure smooth playback at 60fps?

### Priority 4: Pipeline Integration
11. How to batch process multiple videos?
12. How to validate output quality automatically?
13. What's the render time per video (performance)?

---

## PROOF-OF-CONCEPT PROTOCOL

### POC 1: Manual Baseline
**Objective:** Manually edit ORV Ch 0 to prove quality is achievable

**Steps:**
1. Import all Ch 0 panels
2. Import narration audio
3. Manually place panels and sync to audio
4. Apply Ken Burns effects
5. Export and validate

**Deliverables:**
- Finished 6-minute video
- Time tracking (how long did it take?)
- Notes on repetitive tasks (automation candidates)

**Success Criteria:**
- Video matches titan quality
- Process is repeatable
- Automation opportunities identified

---

### POC 2: Semi-Automated Test
**Objective:** Automate the most tedious parts

**Approach:** Based on POC 1 findings, automate:
- Clip import and ordering
- Basic timing calculation
- Effect application (if possible)

**Steps:**
1. Write script to generate Premiere Pro project file
   OR
   Use ExtendScript to populate template

2. Run script with Ch 0 data
3. Open in Premiere
4. Verify + polish manually
5. Export

**Deliverables:**
- Automation script (Python or ExtendScript)
- Documentation of what's automated
- List of manual steps still required

**Success Criteria:**
- 50%+ time savings vs fully manual
- Output quality maintained
- Process is reliable

---

### POC 3: Full Automation Attempt
**Objective:** Fully automated end-to-end

**Steps:**
1. Refine automation from POC 2
2. Add audio sync automation
3. Add effect parameterization
4. Add quality validation
5. Test with Ch 0 + Ch 1

**Deliverables:**
- Complete automation pipeline
- Performance benchmarks
- Quality assessment vs manual

**Success Criteria:**
- End-to-end automation works
- Quality within 90% of manual
- Render time < 30 minutes per video

---

## WEB RESEARCH TARGETS

### Immediate Research:
1. "Adobe Premiere Pro ExtendScript tutorial"
2. "Premiere Pro automation scripting guide"
3. "programmatic video editing Premiere Pro"
4. "FFmpeg pan zoom effects tutorial"
5. "audio waveform analysis Python"

### Deep Dive Research:
6. "Premiere Pro API documentation"
7. "DaVinci Resolve Python API tutorial"
8. "automated video editing pipeline"
9. "Ken Burns effect programmatic generation"
10. "video editing automation best practices"

---

## FALLBACK STRATEGIES

### If Full Automation Proves Impossible:

**Strategy A: Template + Human Polish**
- Automate 80% (clip placement, basic effects)
- Manual polish pass (10-15 minutes per video)
- Still achieves scaling (1 editor → many videos/day)

**Strategy B: Specialized Editing Tool**
- Build custom web-based editor
- Simplified interface for manhwa recaps
- Specialized for our exact use case
- (Significant development time)

**Strategy C: Hybrid Workflow**
- Automate easy parts (clip sequencing, timing calc)
- Use Premiere for complex parts (effects, polish)
- Optimize for speed, not full automation

---

## DOCUMENTATION DELIVERABLES

### For Opus Handoff:
1. **Tool Selection Document**
   - Chosen approach (Premiere/FFmpeg/Hybrid)
   - Justification
   - Limitations

2. **Automation Guide**
   - Step-by-step process
   - Code/scripts with comments
   - Configuration files

3. **Quality Standards**
   - Output specifications
   - Validation checklist
   - Comparison to titan baseline

4. **Performance Benchmarks**
   - Time per video
   - Resource requirements
   - Scaling projections

5. **Optimization Opportunities**
   - Known bottlenecks
   - Potential improvements
   - Future enhancements

---

## REALISTIC TIMELINE

### Week 1: Research & Tool Selection
- Investigate Premiere Pro automation
- Test FFmpeg capabilities
- Choose primary approach
- Document findings

### Week 2: POC 1 (Manual Baseline)
- Manually edit ORV Ch 0
- Establish quality baseline
- Identify automation targets
- Document process

### Week 3: POC 2 (Semi-Automated)
- Build automation scripts
- Test with Ch 0
- Refine + iterate
- Measure improvements

### Week 4: POC 3 (Full Automation)
- Complete automation pipeline
- Test with multiple chapters
- Performance optimization
- Quality validation

**Deliverable to Opus:** Working editing pipeline, even if not 100% automated.

---

## CRITICAL INSIGHT

**Perfect is the enemy of good.**

The goal is NOT flawless full automation Day 1.

The goal is:
1. ✅ Prove quality is achievable (POC 1)
2. ✅ Automate the tedious parts (POC 2)
3. ✅ Scale to reasonable throughput (POC 3)

Even "80% automated + 15 min polish" is a MASSIVE win.

It transforms:
- 1 video/day (fully manual) 
- → 5-10 videos/day (semi-automated)

That's enough to prove the business model.

Full automation is optimization for Opus.

---

**Status:** Research phase. The most critical unknown. High priority.

🌊💙⚔️
