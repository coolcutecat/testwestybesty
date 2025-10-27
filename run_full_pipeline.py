#!/usr/bin/env python3
"""
FULL PIPELINE v2.0 - COMPLETE AUTOMATION
Scrape → Segment → Import → Effects → Export
"""

from pathlib import Path
import subprocess
import sys

def run_step(script_path, description):
    """Run a pipeline step"""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, str(script_path)], 
                          capture_output=False, 
                          text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Step failed: {description}")
        return False
    
    return True

def main():
    pipeline_dir = Path("C:/Collin/Collinism/Claude/manhwa_pipeline")
    
    print("="*60)
    print("MANHWA PIPELINE v2.0 - FULL AUTOMATION")
    print("="*60)
    print()
    print("This will:")
    print("  1. Slice pages into segments")
    print("  2. Generate basic manifest")
    print("  3. Generate enhanced manifest (with effects)")
    print("  4. Generate all JSX scripts:")
    print("     - Import & place segments")
    print("     - Set durations")
    print("     - Apply motion & transitions")
    print()
    print("Prerequisites:")
    print("  - Pages in ch_000/ (run scraper first)")
    print("  - OpenCV installed")
    print()
    input("Press ENTER to start automated prep...")
    
    # AUTOMATED STEPS
    
    # Step 1: Segment slicing
    if not run_step(
        pipeline_dir / "production_chunker_v4.py",
        "1. Segment Slicing"
    ):
        return
    
    # Step 2: Enhanced manifest
    if not run_step(
        pipeline_dir / "generate_enhanced_manifest.py",
        "2. Enhanced Manifest Generation"
    ):
        return
    
    # Step 3: Generate all JSX scripts
    if not run_step(
        pipeline_dir / "generate_jsx_from_manifest.py",
        "3. JSX Generation (Import + Duration)"
    ):
        return
    
    if not run_step(
        pipeline_dir / "generate_script3_effects.py",
        "4. JSX Generation (Effects)"
    ):
        return
    
    print("\n" + "="*60)
    print("✅ AUTOMATED PREP COMPLETE!")
    print("="*60)
    print()
    print("📁 Generated:")
    print("   - Segments: ch_000/segments/")
    print("   - Manifest v2: segment_manifest_v2.json")
    print("   - JSX Scripts:")
    print("     → step1_import_segments.jsx")
    print("     → step2_set_durations.jsx")
    print("     → step3_apply_effects.jsx")
    print()
    print("🎬 NEXT: Run JSX scripts in Premiere")
    print()
    print("OPTION A - Manual execution:")
    print("  1. Open Premiere Pro")
    print("  2. Run: step1_import_segments.jsx")
    print("  3. Run: step2_set_durations.jsx")
    print("  4. Run: step3_apply_effects.jsx")
    print("  5. Export video")
    print()
    print("OPTION B - Coming soon:")
    print("  → Python wrapper to execute JSX automatically")
    print()
    print("⏱️  Estimated time: 3-5 minutes (down from 2-3 hours)")
    print()

if __name__ == "__main__":
    main()
