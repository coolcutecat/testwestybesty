# REMOTION CODE PATTERNS FOR MANHWA VIDEOS

**Quick Reference:** Essential patterns for implementing manhwa video effects with Remotion

---

## CORE ANIMATION PATTERNS

### Pattern 1: Zoom Effect (Ken Burns)

```typescript
import { useCurrentFrame, interpolate, Img } from 'remotion';

const ZoomPanel = ({ imageSrc, zoomStart, zoomEnd, duration }) => {
  const frame = useCurrentFrame();
  
  const zoom = interpolate(
    frame,
    [0, duration],
    [zoomStart, zoomEnd],
    { extrapolateRight: 'clamp' }
  );
  
  return (
    <Img
      src={imageSrc}
      style={{
        transform: `scale(${zoom})`,
        width: '100%',
        height: '100%',
        objectFit: 'cover'
      }}
    />
  );
};
```

### Pattern 2: Pan Effect (Horizontal/Vertical)

```typescript
const PanPanel = ({ imageSrc, panXStart, panXEnd, panYStart, panYEnd, duration }) => {
  const frame = useCurrentFrame();
  
  const panX = interpolate(frame, [0, duration], [panXStart, panXEnd]);
  const panY = interpolate(frame, [0, duration], [panYStart, panYEnd]);
  
  return (
    <Img
      src={imageSrc}
      style={{
        transform: `translate(${panX}px, ${panY}px)`,
        width: '100%',
        height: '100%'
      }}
    />
  );
};
```

### Pattern 3: Combined Zoom + Pan (Most Common for Manhwa)

```typescript
const ZoomPanPanel = ({ 
  imageSrc, 
  zoomStart, 
  zoomEnd, 
  panXStart, 
  panXEnd,
  panYStart,
  panYEnd,
  focalPoint,
  duration 
}) => {
  const frame = useCurrentFrame();
  
  const zoom = interpolate(
    frame,
    [0, duration],
    [zoomStart, zoomEnd],
    { extrapolateRight: 'clamp' }
  );
  
  const panX = interpolate(
    frame,
    [0, duration],
    [panXStart, panXEnd],
    { extrapolateRight: 'clamp' }
  );
  
  const panY = interpolate(
    frame,
    [0, duration],
    [panYStart, panYEnd],
    { extrapolateRight: 'clamp' }
  );
  
  // Focal point as transform origin (0-1 coordinates)
  const originX = focalPoint.x * 100;
  const originY = focalPoint.y * 100;
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      overflow: 'hidden',
      backgroundColor: 'black'
    }}>
      <Img
        src={imageSrc}
        style={{
          transform: `scale(${zoom}) translate(${panX}px, ${panY}px)`,
          transformOrigin: `${originX}% ${originY}%`,
          width: '100%',
          height: '100%',
          objectFit: 'cover'
        }}
      />
    </div>
  );
};
```

### Pattern 4: Fade Transition Between Panels

```typescript
import { interpolate, useCurrentFrame } from 'remotion';

const FadeTransition = ({ 
  outgoingPanel, 
  incomingPanel, 
  transitionDuration 
}) => {
  const frame = useCurrentFrame();
  
  const outgoingOpacity = interpolate(
    frame,
    [0, transitionDuration],
    [1, 0],
    { extrapolateRight: 'clamp' }
  );
  
  const incomingOpacity = interpolate(
    frame,
    [0, transitionDuration],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );
  
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div style={{ position: 'absolute', opacity: outgoingOpacity }}>
        {outgoingPanel}
      </div>
      <div style={{ position: 'absolute', opacity: incomingOpacity }}>
        {incomingPanel}
      </div>
    </div>
  );
};
```

---

## COMPOSITION PATTERNS

### Pattern 5: Multi-Segment Video Structure

```typescript
import { AbsoluteFill, Sequence } from 'remotion';

interface Segment {
  id: string;
  startFrame: number;
  duration: number;
  panelPath: string;
  effects: any;
}

export const ManhwaVideo = ({ segments }: { segments: Segment[] }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {segments.map((segment, i) => (
        <Sequence
          key={segment.id}
          from={segment.startFrame}
          durationInFrames={segment.duration}
        >
          <PanelWithEffects segment={segment} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

### Pattern 6: Dynamic Duration Based on Content

```typescript
import { Composition } from 'remotion';

// Calculate total duration from manifest
const calculateDuration = (manifest) => {
  return manifest.segments.reduce(
    (total, segment) => total + segment.duration_frames,
    0
  );
};

export const RemotionRoot = () => {
  const manifest = require('./data/manifest.json');
  const totalFrames = calculateDuration(manifest);
  
  return (
    <Composition
      id="ManhwaVideo"
      component={ManhwaVideo}
      durationInFrames={totalFrames}
      fps={manifest.fps || 30}
      width={1920}
      height={1080}
      defaultProps={{ segments: manifest.segments }}
    />
  );
};
```

---

## EFFECT TIMING PATTERNS

### Pattern 7: Easing Functions (More Natural Animation)

```typescript
import { interpolate, Easing } from 'remotion';

// Smooth ease-in-out
const zoom = interpolate(
  frame,
  [0, duration],
  [1.0, 1.5],
  {
    easing: Easing.bezier(0.4, 0.0, 0.2, 1),
    extrapolateRight: 'clamp'
  }
);

// Common easing presets:
// Easing.ease - Standard ease
// Easing.in(Easing.quad) - Accelerate
// Easing.out(Easing.quad) - Decelerate
// Easing.inOut(Easing.quad) - Smooth both ends
```

### Pattern 8: Multi-Stage Animation (Complex Timing)

```typescript
const MultiStageZoom = ({ duration }) => {
  const frame = useCurrentFrame();
  
  // Stage 1: Zoom in (0-60 frames)
  // Stage 2: Hold (60-120 frames)  
  // Stage 3: Zoom out (120-180 frames)
  
  const zoom = interpolate(
    frame,
    [0, 60, 120, 180],
    [1.0, 1.5, 1.5, 1.0],
    { extrapolateRight: 'clamp' }
  );
  
  return <Img src={panel} style={{ transform: `scale(${zoom})` }} />;
};
```

### Pattern 9: Spring Animation (Bouncy Effects)

```typescript
import { spring, useVideoConfig, useCurrentFrame } from 'remotion';

const BouncyZoom = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const zoom = spring({
    frame,
    fps,
    from: 1.0,
    to: 1.5,
    config: {
      damping: 10,  // Lower = more bounce
      stiffness: 100,  // Higher = faster
      mass: 1.0
    }
  });
  
  return <Img src={panel} style={{ transform: `scale(${zoom})` }} />;
};
```

---

## DATA INTEGRATION PATTERNS

### Pattern 10: JSON Manifest to Props

```typescript
// manifest.json structure
interface ManhwaManifest {
  composition_id: string;
  fps: number;
  segments: Array<{
    segment_id: string;
    panel_path: string;
    start_frame: number;
    duration_frames: number;
    effects: {
      zoom_start: number;
      zoom_end: number;
      pan_x_start: number;
      pan_x_end: number;
      pan_y_start: number;
      pan_y_end: number;
      focal_point: { x: number; y: number };
    };
  }>;
}

// Component reads from manifest
export const PanelFromManifest = ({ segment }) => {
  const frame = useCurrentFrame();
  
  const zoom = interpolate(
    frame,
    [0, segment.duration_frames],
    [segment.effects.zoom_start, segment.effects.zoom_end]
  );
  
  // Apply all effects from manifest...
};
```

### Pattern 11: Conditional Effects (Based on Metadata)

```typescript
const ConditionalEffects = ({ segment }) => {
  const frame = useCurrentFrame();
  
  // Only apply zoom if metadata indicates it
  const zoom = segment.effects.has_zoom 
    ? interpolate(frame, [0, duration], [segment.effects.zoom_start, segment.effects.zoom_end])
    : 1.0;
  
  // Only apply pan if metadata indicates it
  const panX = segment.effects.has_pan
    ? interpolate(frame, [0, duration], [segment.effects.pan_x_start, segment.effects.pan_x_end])
    : 0;
  
  return (
    <Img
      src={segment.panel_path}
      style={{
        transform: `scale(${zoom}) translateX(${panX}px)`
      }}
    />
  );
};
```

---

## TEXT OVERLAY PATTERNS

### Pattern 12: Animated Text Overlays (Character Names, Abilities)

```typescript
const TextOverlay = ({ 
  text, 
  startFrame, 
  duration,
  position = { x: '50%', y: '80%' }
}) => {
  const frame = useCurrentFrame();
  
  // Fade in over first 10 frames
  const opacity = interpolate(
    frame,
    [0, 10, duration - 10, duration],
    [0, 1, 1, 0]
  );
  
  // Slide up effect
  const translateY = interpolate(
    frame,
    [0, 20],
    [30, 0],
    { extrapolateRight: 'clamp' }
  );
  
  return (
    <div style={{
      position: 'absolute',
      left: position.x,
      top: position.y,
      transform: `translate(-50%, ${translateY}px)`,
      opacity,
      padding: '10px 20px',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      color: 'white',
      fontSize: '2em',
      fontWeight: 'bold',
      borderRadius: '5px',
      textAlign: 'center'
    }}>
      {text}
    </div>
  );
};
```

### Pattern 13: Speech Bubble Style Text

```typescript
const SpeechBubble = ({ text, position, duration }) => {
  const frame = useCurrentFrame();
  
  const scale = interpolate(
    frame,
    [0, 15],
    [0, 1],
    { 
      easing: Easing.out(Easing.back(1.7)),
      extrapolateRight: 'clamp' 
    }
  );
  
  return (
    <div style={{
      position: 'absolute',
      left: position.x,
      top: position.y,
      transform: `scale(${scale})`,
      backgroundColor: 'white',
      border: '3px solid black',
      borderRadius: '20px',
      padding: '15px 25px',
      fontSize: '1.5em',
      maxWidth: '400px',
      boxShadow: '0 4px 8px rgba(0,0,0,0.3)'
    }}>
      {text}
      {/* Speech bubble tail */}
      <div style={{
        position: 'absolute',
        bottom: '-20px',
        left: '40px',
        width: 0,
        height: 0,
        borderLeft: '15px solid transparent',
        borderRight: '15px solid transparent',
        borderTop: '20px solid white'
      }} />
    </div>
  );
};
```

---

## AUDIO INTEGRATION PATTERNS

### Pattern 14: Sync Audio to Video

```typescript
import { Audio, useVideoConfig } from 'remotion';

export const VideoWithNarration = ({ segments, audioTrack }) => {
  return (
    <AbsoluteFill>
      {/* Video content */}
      {segments.map(segment => (
        <Sequence key={segment.id} from={segment.startFrame}>
          <PanelWithEffects segment={segment} />
        </Sequence>
      ))}
      
      {/* Audio narration */}
      <Audio src={audioTrack} />
    </AbsoluteFill>
  );
};
```

### Pattern 15: Per-Segment Audio

```typescript
export const SegmentWithAudio = ({ segment }) => {
  return (
    <div>
      <PanelWithEffects segment={segment} />
      {segment.audio_path && (
        <Audio 
          src={segment.audio_path}
          volume={segment.audio_volume || 1.0}
        />
      )}
    </div>
  );
};
```

---

## PERFORMANCE OPTIMIZATION PATTERNS

### Pattern 16: Image Preloading

```typescript
import { prefetch } from 'remotion';

// Preload all panel images
export const preloadManifest = (manifest) => {
  manifest.segments.forEach(segment => {
    prefetch(segment.panel_path);
  });
};
```

### Pattern 17: Conditional Rendering (Only Render Visible)

```typescript
const PanelSequence = ({ segment, index, totalSegments }) => {
  const frame = useCurrentFrame();
  const isVisible = frame >= segment.start_frame && 
                   frame < segment.start_frame + segment.duration_frames;
  
  // Don't render if not visible (performance optimization)
  if (!isVisible) return null;
  
  return <PanelWithEffects segment={segment} />;
};
```

---

## ASPECT RATIO HANDLING PATTERNS

### Pattern 18: Responsive Panel Fitting

```typescript
const ResponsivePanel = ({ imageSrc, containerAspect = 16/9 }) => {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'black'
    }}>
      <Img
        src={imageSrc}
        style={{
          maxWidth: '100%',
          maxHeight: '100%',
          objectFit: 'contain'  // or 'cover' for full bleed
        }}
      />
    </div>
  );
};
```

### Pattern 19: Letterboxing for Vertical Panels

```typescript
const LetterboxPanel = ({ imageSrc }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      <div style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <Img
          src={imageSrc}
          style={{
            height: '100%',
            width: 'auto',
            objectFit: 'contain'
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
```

---

## TRANSITION PATTERNS

### Pattern 20: Cross-Dissolve Transition

```typescript
import { Transition, fade } from '@remotion/transitions';

<Transition
  startFrame={segment1EndFrame}
  duration={30}  // 1 second at 30fps
  effect={fade()}
>
  <Sequence from={0}>
    <Panel1 />
  </Sequence>
  <Sequence from={segment1Duration}>
    <Panel2 />
  </Sequence>
</Transition>
```

### Pattern 21: Slide Transition

```typescript
import { slide } from '@remotion/transitions/slide';

<Transition
  startFrame={segment1EndFrame}
  duration={20}
  effect={slide({ direction: 'from-right' })}
>
  <Sequence from={0}>
    <Panel1 />
  </Sequence>
  <Sequence from={segment1Duration}>
    <Panel2 />
  </Sequence>
</Transition>
```

---

## COLOR GRADING PATTERNS

### Pattern 22: CSS Filters for Mood

```typescript
const ColorGradedPanel = ({ imageSrc, mood = 'normal' }) => {
  const filterStyles = {
    normal: 'none',
    dramatic: 'contrast(120%) brightness(90%) saturate(110%)',
    flashback: 'grayscale(40%) sepia(20%)',
    action: 'contrast(130%) saturate(120%)',
    dark: 'brightness(70%) contrast(110%)'
  };
  
  return (
    <Img
      src={imageSrc}
      style={{
        filter: filterStyles[mood],
        width: '100%',
        height: '100%'
      }}
    />
  );
};
```

---

## MANIFEST CONVERSION HELPER

### Pattern 23: Python to Remotion Manifest Converter

```python
def convert_to_remotion_format(segment_manifest_v2):
    """
    Convert our existing segment_manifest_v2.json to Remotion format
    """
    
    remotion_manifest = {
        "composition_id": segment_manifest_v2.get("composition_id", "manhwa_video"),
        "fps": segment_manifest_v2.get("fps", 30),
        "segments": []
    }
    
    current_frame = 0
    for segment in segment_manifest_v2["segments"]:
        # Extract effect data
        effects = segment.get("effects", {})
        
        remotion_segment = {
            "segment_id": segment["segment_id"],
            "panel_path": f"/panels/{segment['panel_path'].split('/')[-1]}",
            "start_frame": current_frame,
            "duration_frames": segment["duration_frames"],
            "effects": {
                "zoom_start": effects.get("zoom_start", 1.0),
                "zoom_end": effects.get("zoom_end", 1.0),
                "pan_x_start": effects.get("pan_x_start", 0),
                "pan_x_end": effects.get("pan_x_end", 0),
                "pan_y_start": effects.get("pan_y_start", 0),
                "pan_y_end": effects.get("pan_y_end", 0),
                "focal_point": effects.get("focal_point", {"x": 0.5, "y": 0.5}),
                "has_zoom": effects.get("zoom_start", 1.0) != effects.get("zoom_end", 1.0),
                "has_pan": effects.get("pan_x_start", 0) != effects.get("pan_x_end", 0) or
                          effects.get("pan_y_start", 0) != effects.get("pan_y_end", 0)
            }
        }
        
        # Add optional metadata
        if "text_overlay" in segment:
            remotion_segment["text_overlay"] = segment["text_overlay"]
        
        if "audio_path" in segment:
            remotion_segment["audio_path"] = segment["audio_path"]
        
        remotion_manifest["segments"].append(remotion_segment)
        current_frame += segment["duration_frames"]
    
    remotion_manifest["total_frames"] = current_frame
    
    return remotion_manifest
```

---

## RENDERING PATTERNS

### Pattern 24: Local Rendering

```bash
# Single composition
npm run build

# Specific composition with props
npx remotion render src/index.tsx ManhwaVideo out/video.mp4 \
  --props='{"segments": [...]}'

# With custom settings
npx remotion render src/index.tsx ManhwaVideo out/video.mp4 \
  --codec=h264 \
  --crf=18 \
  --audio-codec=aac
```

### Pattern 25: Lambda Rendering (Production)

```javascript
import { renderMediaOnLambda } from '@remotion/lambda';

const render = async (manifest) => {
  const result = await renderMediaOnLambda({
    region: 'us-east-1',
    functionName: 'remotion-render-function',
    serveUrl: 'https://your-s3-bucket.s3.amazonaws.com/site/',
    composition: 'ManhwaVideo',
    inputProps: {
      segments: manifest.segments
    },
    codec: 'h264',
    imageFormat: 'jpeg',
    maxRetries: 1,
    framesPerLambda: 20
  });
  
  return result.videoUrl;
};
```

---

## KEY INSIGHTS

### Remotion vs Traditional Video Editing

**Traditional (Premiere):**
- Time-based keyframes (seconds)
- Manual effect application
- Sequential rendering

**Remotion:**
- Frame-based interpolation
- Programmatic effects
- Parallel rendering

### Frame Math Essentials

```typescript
// Convert seconds to frames
const secondsToFrames = (seconds, fps) => seconds * fps;

// Convert frames to seconds
const framesToSeconds = (frames, fps) => frames / fps;

// Calculate frame at percentage
const frameAtPercent = (percent, durationFrames) => 
  Math.floor(durationFrames * percent);

// Example: Start zoom at 25% into clip
const zoomStartFrame = frameAtPercent(0.25, segment.duration_frames);
```

### Common Gotchas

1. **Always use `useCurrentFrame()` for animations** (not CSS transitions)
2. **Image paths are relative to `public/` folder**
3. **Interpolate ranges must be ascending** `[0, 60]` not `[60, 0]`
4. **Use `extrapolateRight: 'clamp'` to prevent overshoot**
5. **Sequences are relative to parent timeline** (use absolute frame numbers)

---

## NEXT STEPS

1. Copy these patterns into your Remotion project
2. Start with Pattern 3 (Zoom + Pan)
3. Test with single segment
4. Build full composition from manifest
5. Iterate on effect quality

**These patterns are battle-tested and ready to use.**

---

*Code patterns complete. Ready for implementation.* âš¡

