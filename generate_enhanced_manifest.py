#!/usr/bin/env python3
"""
ENHANCED MANIFEST GENERATOR v2.0
Adds effect/transition parameters for full automation

Output: segment_manifest_v2.json with complete automation data
"""

import cv2
import numpy as np
from pathlib import Path
import json

def calculate_motion_effect(segment_height, segment_index, total_segments):
    """
    Intelligently assign motion effect based on segment characteristics
    
    Returns: motion type ("pan_down", "zoom_in", "static", etc.)
    """
    
    # Vary effects for visual interest
    effects = ["pan_down", "zoom_in", "zoom_out", "static"]
    
    # Simple pattern: alternate effects
    return effects[segment_index % len(effects)]

def generate_enhanced_manifest(segments_dir):
    """
    Generate manifest v2 with full automation parameters
    """
    
    segments_dir = Path(segments_dir)
    
    # Load existing basic manifest if it exists
    basic_manifest_path = segments_dir / "segment_manifest.json"
    
    if not basic_manifest_path.exists():
        print("❌ Basic manifest not found. Run production_chunker_v4.py first!")
        return
    
    with open(basic_manifest_path, 'r', encoding='utf-8') as f:
        basic_manifest = json.load(f)
    
    # Enhance with effect parameters
    enhanced_segments = []
    
    for i, seg in enumerate(basic_manifest['segments']):
        # Calculate motion effect
        motion_type = calculate_motion_effect(
            seg['bounds']['height'],
            i,
            len(basic_manifest['segments'])
        )
        
        enhanced_seg = {
            **seg,  # Keep all original data
            "effects": {
                "motion": {
                    "type": motion_type,
                    "intensity": 1.1,  # Zoom factor (1.0 = no zoom, 1.2 = 20% zoom)
                    "duration": seg['duration']
                },
                "transition_in": "dissolve" if i > 0 else None,
                "transition_duration": 0.5
            }
        }
        
        enhanced_segments.append(enhanced_seg)
    
    # Enhanced manifest with global settings
    enhanced_manifest = {
        "version": "2.0",
        "source_directory": basic_manifest['source_directory'],
        "output_directory": basic_manifest['output_directory'],
        "chunker_version": basic_manifest['chunker_version'],
        "summary": basic_manifest['summary'],
        "global_settings": {
            "default_transition": "cross_dissolve",
            "transition_duration": 0.5,
            "motion_enabled": True,
            "color_correction": {
                "enabled": False,  # Can enable for auto color grade
                "saturation": 1.1,
                "contrast": 1.05
            },
            "export": {
                "preset": "YouTube 1080p HD",
                "format": "H.264",
                "output_path": str(segments_dir.parent / "output" / "final_video.mp4")
            }
        },
        "segments": enhanced_segments
    }
    
    # Save enhanced manifest
    output_path = segments_dir / "segment_manifest_v2.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_manifest, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Enhanced manifest created: {output_path.name}")
    print(f"   Version: 2.0 (full automation)")
    print(f"   Segments: {len(enhanced_segments)}")
    print(f"   Motion effects: {len([s for s in enhanced_segments if s['effects']['motion']['type'] != 'static'])}")
    print(f"   Transitions: {len([s for s in enhanced_segments if s['effects']['transition_in']])}")

def main():
    segments_dir = Path("C:/Collin/Collinism/Claude/panels/omniscient_readers_viewpoint/ch_000/segments")
    
    if not segments_dir.exists():
        print(f"❌ Segments directory not found: {segments_dir}")
        return
    
    print("📊 GENERATING ENHANCED MANIFEST v2.0...")
    print()
    
    generate_enhanced_manifest(segments_dir)

if __name__ == "__main__":
    main()
