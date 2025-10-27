# REMOTION POC - TACTICAL IMPLEMENTATION GUIDE

**Goal:** Working single-segment manhwa video with zoom effect in < 4 hours

---

## PHASE 1: SETUP (30 minutes)

### Step 1: Install Remotion

```bash
cd C:\Collin\Collinism\Claude\manhwa_pipeline
npm init video -- --template=blank
# Name it: remotion-manhwa
cd remotion-manhwa
npm install
npm start
```

This opens Remotion Studio at `localhost:3000`. You should see a blank composition.

### Step 2: Verify Installation

Check that you see:
- Left sidebar: Composition list (empty)
- Center: Player/preview
- Right: Properties panel
- Timeline at bottom

**Test:** The blank template should render without errors.

---

## PHASE 2: SINGLE PANEL TEST (1 hour)

### Step 3: Create Panel Component

**File:** `src/PanelTest.tsx`

```typescript
import { useCurrentFrame, useVideoConfig, interpolate, Img } from 'remotion';

export const PanelTest: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Zoom from 1.0x to 1.5x over duration
  const zoom = interpolate(
    frame,
    [0, durationInFrames],
    [1.0, 1.5],
    { extrapolateRight: 'clamp' }
  );

  return (
    <div
      style={{
        backgroundColor: 'black',
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Img
        src="path/to/test/panel.png"
        style={{
          transform: `scale(${zoom})`,
          maxWidth: '100%',
          maxHeight: '100%',
        }}
      />
    </div>
  );
};
```

### Step 4: Register Composition

**File:** `src/Root.tsx`

```typescript
import { Composition } from 'remotion';
import { PanelTest } from './PanelTest';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PanelTest"
        component={PanelTest}
        durationInFrames={120}  // 4 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

### Step 5: Test Panel Image

1. Copy a test panel image to `public/test_panel.png`
2. Update `src` in PanelTest.tsx to: `src="/test_panel.png"`
3. Refresh Remotion Studio
4. Should see panel with zoom animation

**Validation:**
- âœ… Panel image loads
- âœ… Zoom animation visible in preview
- âœ… Can scrub timeline and see zoom change
- âœ… Can render to video (`npm run build`)

---

## PHASE 3: MANIFEST INTEGRATION (1 hour)

### Step 6: Import Manifest Data

**File:** `src/data/test_segment.json`

```json
{
  "segment_id": "seg_001",
  "panel_path": "/test_panel.png",
  "duration_frames": 120,
  "effects": {
    "zoom_start": 1.0,
    "zoom_end": 1.5,
    "pan_x_start": 0,
    "pan_x_end": 50,
    "focal_point": {"x": 0.5, "y": 0.3}
  }
}
```

### Step 7: Data-Driven Component

**File:** `src/PanelSegment.tsx`

```typescript
import { useCurrentFrame, useVideoConfig, interpolate, Img } from 'remotion';

interface SegmentData {
  segment_id: string;
  panel_path: string;
  duration_frames: number;
  effects: {
    zoom_start: number;
    zoom_end: number;
    pan_x_start: number;
    pan_x_end: number;
    focal_point: { x: number; y: number };
  };
}

export const PanelSegment: React.FC<{ data: SegmentData }> = ({ data }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const zoom = interpolate(
    frame,
    [0, durationInFrames],
    [data.effects.zoom_start, data.effects.zoom_end],
    { extrapolateRight: 'clamp' }
  );

  const panX = interpolate(
    frame,
    [0, durationInFrames],
    [data.effects.pan_x_start, data.effects.pan_x_end],
    { extrapolateRight: 'clamp' }
  );

  // Calculate transform origin from focal point
  const originX = data.effects.focal_point.x * 100;
  const originY = data.effects.focal_point.y * 100;

  return (
    <div
      style={{
        backgroundColor: 'black',
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}
    >
      <Img
        src={data.panel_path}
        style={{
          transform: `scale(${zoom}) translateX(${panX}px)`,
          transformOrigin: `${originX}% ${originY}%`,
          maxWidth: '100%',
          maxHeight: '100%',
        }}
      />
    </div>
  );
};
```

### Step 8: Update Composition

**File:** `src/Root.tsx`

```typescript
import { Composition } from 'remotion';
import { PanelSegment } from './PanelSegment';
import testSegment from './data/test_segment.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TestSegment"
        component={PanelSegment}
        durationInFrames={testSegment.duration_frames}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ data: testSegment }}
      />
    </>
  );
};
```

**Validation:**
- âœ… Reads effect data from JSON
- âœ… Applies zoom correctly
- âœ… Applies pan correctly
- âœ… Focal point respected

---

## PHASE 4: MULTI-SEGMENT VIDEO (1 hour)

### Step 9: Create Multi-Segment Manifest

**File:** `src/data/test_video.json`

```json
{
  "composition_id": "test_manhwa_video",
  "fps": 30,
  "total_frames": 360,
  "segments": [
    {
      "segment_id": "seg_001",
      "panel_path": "/panels/panel_001.png",
      "start_frame": 0,
      "duration_frames": 120,
      "effects": {
        "zoom_start": 1.0,
        "zoom_end": 1.5,
        "pan_x_start": 0,
        "pan_x_end": 0
      }
    },
    {
      "segment_id": "seg_002",
      "panel_path": "/panels/panel_002.png",
      "start_frame": 120,
      "duration_frames": 120,
      "effects": {
        "zoom_start": 1.2,
        "zoom_end": 1.0,
        "pan_x_start": 0,
        "pan_x_end": 100
      }
    },
    {
      "segment_id": "seg_003",
      "panel_path": "/panels/panel_003.png",
      "start_frame": 240,
      "duration_frames": 120,
      "effects": {
        "zoom_start": 1.0,
        "zoom_end": 1.8,
        "pan_x_start": 0,
        "pan_x_end": -50
      }
    }
  ]
}
```

### Step 10: Create Video Composition

**File:** `src/ManhwaVideo.tsx`

```typescript
import { AbsoluteFill, Sequence } from 'remotion';
import { PanelSegment } from './PanelSegment';

interface VideoManifest {
  composition_id: string;
  fps: number;
  total_frames: number;
  segments: Array<{
    segment_id: string;
    panel_path: string;
    start_frame: number;
    duration_frames: number;
    effects: any;
  }>;
}

export const ManhwaVideo: React.FC<{ data: VideoManifest }> = ({ data }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {data.segments.map((segment) => (
        <Sequence
          key={segment.segment_id}
          from={segment.start_frame}
          durationInFrames={segment.duration_frames}
        >
          <PanelSegment
            data={{
              ...segment,
            }}
          />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

### Step 11: Register Multi-Segment Composition

**File:** `src/Root.tsx`

```typescript
import { Composition } from 'remotion';
import { ManhwaVideo } from './ManhwaVideo';
import videoManifest from './data/test_video.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ManhwaVideo"
        component={ManhwaVideo}
        durationInFrames={videoManifest.total_frames}
        fps={videoManifest.fps}
        width={1920}
        height={1080}
        defaultProps={{ data: videoManifest }}
      />
    </>
  );
};
```

**Validation:**
- âœ… All 3 segments render in sequence
- âœ… Each segment has correct effects
- âœ… Transitions between segments work
- âœ… Total duration is correct (12 seconds)

---

## PHASE 5: RENDER & VALIDATE (30 minutes)

### Step 12: Render Video

```bash
# In remotion-manhwa directory
npm run build

# Output will be in out/video.mp4
```

### Step 13: Compare to Competitor

1. Open rendered video
2. Open competitor video side-by-side
3. Compare:
   - âœ… Animation smoothness
   - âœ… Zoom quality
   - âœ… Pan quality
   - âœ… Timing/pacing
   - âœ… Visual polish

**Success Criteria:**
- Quality ≥ competitor videos
- Effects work as expected
- No technical glitches
- Acceptable render time (< 5 min for 12-second video)

---

## PHASE 6: PRODUCTION INTEGRATION (Next)

### Step 14: Connect to Existing Pipeline

**New Python script:** `generate_remotion_manifest.py`

```python
import json
from pathlib import Path

def convert_segment_manifest_to_remotion(input_manifest: dict) -> dict:
    """
    Convert segment_manifest_v2.json to Remotion format
    """
    
    remotion_manifest = {
        "composition_id": input_manifest.get("composition_id", "manhwa_video"),
        "fps": input_manifest.get("fps", 30),
        "total_frames": sum(s["duration_frames"] for s in input_manifest["segments"]),
        "segments": []
    }
    
    current_frame = 0
    for segment in input_manifest["segments"]:
        remotion_segment = {
            "segment_id": segment["segment_id"],
            "panel_path": f"/panels/{Path(segment['panel_path']).name}",
            "start_frame": current_frame,
            "duration_frames": segment["duration_frames"],
            "effects": segment["effects"]
        }
        remotion_manifest["segments"].append(remotion_segment)
        current_frame += segment["duration_frames"]
    
    return remotion_manifest

def main():
    # Read existing manifest
    with open('segment_manifest_v2.json', 'r') as f:
        input_manifest = json.load(f)
    
    # Convert to Remotion format
    remotion_manifest = convert_segment_manifest_to_remotion(input_manifest)
    
    # Write to Remotion project
    output_path = 'remotion-manhwa/src/data/manifest.json'
    with open(output_path, 'w') as f:
        json.dump(remotion_manifest, f, indent=2)
    
    print(f"âœ… Generated Remotion manifest: {output_path}")

if __name__ == "__main__":
    main()
```

### Step 15: Automated Render Pipeline

**New Python script:** `render_remotion_video.py`

```python
import subprocess
import json
from pathlib import Path

def render_video(manifest_path: str, output_path: str):
    """
    Render Remotion video from manifest
    """
    
    # Change to Remotion project directory
    remotion_dir = Path("remotion-manhwa")
    
    # Run Remotion render
    cmd = [
        "npm", "run", "build",
        "--", 
        "--composition=ManhwaVideo",
        f"--output={output_path}"
    ]
    
    result = subprocess.run(
        cmd,
        cwd=remotion_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"âœ… Video rendered: {output_path}")
    else:
        print(f"❌ Render failed: {result.stderr}")

def main():
    # Convert manifest
    subprocess.run(["python", "generate_remotion_manifest.py"])
    
    # Render video
    output_path = "../pipeline_output/videos/test_video.mp4"
    render_video("remotion-manhwa/src/data/manifest.json", output_path)

if __name__ == "__main__":
    main()
```

### Step 16: Full Automation

**Updated:** `RUN_PIPELINE_V3.bat`

```batch
@echo off
echo ========================================
echo MANHWA PIPELINE v3.0 - REMOTION
echo ========================================

echo.
echo [1/5] Scraping manhwa panels...
python manhwa_scraper_selenium.py

echo.
echo [2/5] Segmenting panels...
python production_chunker_v4.py

echo.
echo [3/5] Generating enhanced manifest...
python generate_enhanced_manifest.py

echo.
echo [4/5] Converting to Remotion format...
python generate_remotion_manifest.py

echo.
echo [5/5] Rendering video...
python render_remotion_video.py

echo.
echo ========================================
echo âœ… PIPELINE COMPLETE!
echo ========================================
echo.
echo Output: pipeline_output/videos/test_video.mp4
echo.
pause
```

---

## SUCCESS CHECKLIST

**Phase 1: Setup**
- [ ] Remotion installed
- [ ] Studio opens correctly
- [ ] Blank template works

**Phase 2: Single Panel**
- [ ] Panel image displays
- [ ] Zoom animation works
- [ ] Can render to MP4

**Phase 3: Manifest Integration**
- [ ] JSON manifest loads
- [ ] Effects read from manifest
- [ ] Data-driven animation works

**Phase 4: Multi-Segment**
- [ ] Multiple panels sequence correctly
- [ ] All segments have effects
- [ ] Total duration correct

**Phase 5: Validation**
- [ ] Render completes successfully
- [ ] Quality ≥ competitors
- [ ] No glitches
- [ ] Acceptable render time

**Phase 6: Production**
- [ ] Python integration works
- [ ] Manifest conversion works
- [ ] Automated rendering works
- [ ] Full pipeline end-to-end

---

## TROUBLESHOOTING

**Issue:** Remotion won't install
- **Solution:** Check Node.js version (needs 16+)

**Issue:** Image won't load
- **Solution:** Check path is relative to `public/` folder

**Issue:** Animation looks choppy
- **Solution:** Increase FPS or use `spring()` instead of `interpolate()`

**Issue:** Render fails
- **Solution:** Check FFmpeg is installed: `ffmpeg -version`

**Issue:** Manifest not loading
- **Solution:** Verify JSON is valid, check import path

**Issue:** Effects not working
- **Solution:** Check frame ranges in interpolate()

---

## NEXT STEPS AFTER POC

**Immediate:**
1. Add transitions between segments
2. Add audio narration layer
3. Add text overlays (character names)
4. Optimize render performance

**Short-term:**
1. Deploy to Remotion Lambda
2. Test batch rendering
3. Scale to full video (10+ minutes)
4. Quality iteration

**Medium-term:**
1. Add advanced effects (motion blur, color grading)
2. Build content library (reusable components)
3. Optimize for different aspect ratios
4. A/B test different styles

---

## TIME ESTIMATES

**Conservative:**
- Phase 1 (Setup): 30 min
- Phase 2 (Single Panel): 1 hour
- Phase 3 (Manifest): 1 hour
- Phase 4 (Multi-Segment): 1 hour
- Phase 5 (Validation): 30 min
- **Total: 4 hours**

**Optimistic:**
- Phase 1: 15 min
- Phase 2: 30 min
- Phase 3: 30 min
- Phase 4: 45 min
- Phase 5: 15 min
- **Total: 2 hours 15 min**

**Realistic (with troubleshooting):**
- **Total: 3-5 hours**

---

## RESOURCES

**Official Docs:**
- Quickstart: https://www.remotion.dev/docs/the-fundamentals
- API Reference: https://www.remotion.dev/docs/api
- Examples: https://github.com/remotion-dev/remotion/tree/main/packages/example

**Community:**
- Discord: Very active, quick responses
- GitHub Discussions: Good for technical questions

**Video Tutorials:**
- Official channel: https://www.youtube.com/@remotion-dev
- Third-party: Search "Remotion React tutorial"

---

**STATUS:** READY TO EXECUTE  
**ESTIMATED TIME:** 3-5 hours  
**RISK:** LOW  
**DEPENDENCIES:** Node.js, FFmpeg (both installed)

**COMMAND TO START:**
```bash
cd C:\Collin\Collinism\Claude\manhwa_pipeline
npm init video
```

**Let's build it.** âš¡ðŸŽ¯

---

*Tactical guide complete. Execute when ready.*

🚀
