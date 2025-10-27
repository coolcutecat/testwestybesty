#!/usr/bin/env python3
"""
SEGMENT SLICER v4.0 - Production-grade chunking for Premiere workflow

Philosophy: Predictable, Premiere-safe segments over "smart" detection
Goal: Chunks that work reliably in automated JSX assembly

Output: Fixed-height segments with overlap for smooth transitions
"""

import cv2
import numpy as np
from pathlib import Path
import json

def slice_page_into_segments(image_path, segment_height=1600, overlap=200):
    """
    Slice page into fixed-height segments with overlap
    
    Args:
        segment_height: Target height per segment (1600px = Premiere-safe)
        overlap: Pixels of overlap between segments (200px = smooth transitions)
    
    Returns:
        img, list of segments [(y_start, y_end), ...]
    """
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"❌ Could not read {image_path}")
        return None, []
    
    height, width = img.shape[:2]
    
    segments = []
    current_y = 0
    segment_index = 0
    
    while current_y < height:
        # Calculate segment bounds
        y_start = current_y
        y_end = min(current_y + segment_height, height)
        
        # If this is the last segment and it's very short, merge with previous
        remaining = height - y_end
        if remaining > 0 and remaining < segment_height * 0.3:
            # Extend this segment to include the rest
            y_end = height
        
        segments.append({
            'index': segment_index,
            'y_start': y_start,
            'y_end': y_end,
            'height': y_end - y_start
        })
        
        # Move to next segment (subtract overlap for smooth transitions)
        current_y = y_end - overlap
        segment_index += 1
        
        # Safety: if we've moved to the end, stop
        if y_end >= height:
            break
    
    return img, segments

def calculate_segment_duration(segment_height, base_duration_per_1000px=2.5):
    """
    Calculate duration based on segment height
    Taller segments = more reading time
    
    Args:
        segment_height: Height in pixels
        base_duration_per_1000px: Seconds per 1000px (default: 2.5s)
    
    Returns:
        Duration in seconds (float)
    """
    duration = (segment_height / 1000.0) * base_duration_per_1000px
    
    # Clamp to reasonable bounds
    min_duration = 2.0
    max_duration = 6.0
    
    return max(min_duration, min(duration, max_duration))

def slice_page(image_path, output_dir, page_num, segment_height=1600, overlap=200):
    """
    Slice a single page into Premiere-friendly segments
    """
    img, segments = slice_page_into_segments(image_path, segment_height, overlap)
    
    if img is None or not segments:
        print(f"  ⚠️  Could not process page")
        return []
    
    height, width = img.shape[:2]
    
    print(f"  📐 Page: {width}×{height}px → {len(segments)} segments")
    
    saved_segments = []
    
    for seg in segments:
        y_start = seg['y_start']
        y_end = seg['y_end']
        seg_height = seg['height']
        seg_index = seg['index']
        
        # Crop segment
        segment_img = img[y_start:y_end, 0:width]
        
        # Filename: 001_seg_00.png
        seg_name = f"{page_num:03d}_seg_{seg_index:02d}.png"
        seg_path = output_dir / seg_name
        
        cv2.imwrite(str(seg_path), segment_img)
        
        # Calculate duration
        duration = calculate_segment_duration(seg_height)
        
        saved_segments.append({
            "filename": seg_name,
            "source_page": f"{page_num:03d}.png",
            "segment_index": seg_index,
            "bounds": {
                "x": 0,
                "y": y_start,
                "width": width,
                "height": seg_height
            },
            "duration": round(duration, 1),
            "has_overlap": seg_index > 0  # First segment has no overlap
        })
        
        print(f"    • {seg_name} ({width}×{seg_height}px, {duration:.1f}s)")
    
    return saved_segments

def slice_all_pages(input_dir, output_dir, segment_height=1600, overlap=200):
    """
    Process all pages with consistent segmentation
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    pages = sorted(input_dir.glob("*.png"))
    
    if not pages:
        print(f"❌ No PNG files found in {input_dir}")
        return
    
    print(f"📚 SEGMENT SLICER v4.0")
    print(f"   Processing {len(pages)} pages")
    print(f"   Segment height: {segment_height}px")
    print(f"   Overlap: {overlap}px")
    print()
    
    all_segments = []
    total_duration = 0
    
    for page_path in pages:
        try:
            page_num = int(page_path.stem)
        except ValueError:
            print(f"  ⚠️  Skipping {page_path.name}")
            continue
        
        print(f"  📄 Page {page_num:03d}")
        segments = slice_page(page_path, output_dir, page_num, segment_height, overlap)
        all_segments.extend(segments)
        
        # Sum durations
        page_duration = sum(s['duration'] for s in segments)
        total_duration += page_duration
        print(f"     Total: {page_duration:.1f}s")
        print()
    
    # Save manifest
    manifest = {
        "source_directory": str(input_dir),
        "output_directory": str(output_dir),
        "chunker_version": "4.0_segment_slicer",
        "parameters": {
            "segment_height": segment_height,
            "overlap": overlap,
            "duration_formula": "height_in_px / 1000 * 2.5s (clamped 2-6s)"
        },
        "summary": {
            "total_pages": len(pages),
            "total_segments": len(all_segments),
            "total_duration_seconds": round(total_duration, 1),
            "avg_segments_per_page": round(len(all_segments) / len(pages), 1)
        },
        "segments": all_segments
    }
    
    manifest_path = output_dir / "segment_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"✅ COMPLETE:")
    print(f"   Pages: {len(pages)}")
    print(f"   Segments: {len(all_segments)}")
    print(f"   Avg per page: {len(all_segments) / len(pages):.1f}")
    print(f"   Total duration: {total_duration:.1f}s ({total_duration/60:.1f} min)")
    print(f"   Output: {output_dir}")
    print(f"   Manifest: {manifest_path.name}")

def main():
    input_dir = Path("C:/Collin/Collinism/Claude/panels/omniscient_readers_viewpoint/ch_000")
    output_dir = input_dir / "segments"
    
    # Configurable parameters
    SEGMENT_HEIGHT = 1600  # px - Premiere-safe height
    OVERLAP = 200          # px - smooth transitions
    
    slice_all_pages(input_dir, output_dir, SEGMENT_HEIGHT, OVERLAP)

if __name__ == "__main__":
    main()
