#!/usr/bin/env python3
"""
JSX GENERATOR v2.3 - Split into safe, simple scripts

SCRIPT 1: Import and place all segments (no duration manipulation)
SCRIPT 2: Set clip durations based on manifest (separate pass)
SCRIPT 3: Combined runner (loads and executes both)
"""

import json
from pathlib import Path

def generate_import_script(manifest, segment_dir, output_path):
    """
    Generate Script 1: Import segments and create sequence
    """
    segments = manifest['segments']
    
    jsx_lines = [
        "// SCRIPT 1: Import and Place Segments",
        "// This script ONLY imports and places clips",
        "// Run Script 2 afterward to set durations",
        "",
        "function importAndPlace() {",
        f'    var SEGMENT_DIR = "{str(segment_dir).replace(chr(92), chr(92)*2)}\\\\";',
        "    ",
        "    var segments = [",
    ]
    
    for seg in segments:
        jsx_lines.append(f'        "{seg["filename"]}",')
    
    jsx_lines.extend([
        "    ];",
        "    ",
        "    // Import all files",
        "    var files = [];",
        "    for(var i = 0; i < segments.length; i++) {",
        "        files.push(new File(SEGMENT_DIR + segments[i]).fsName);",
        "    }",
        "    ",
        "    app.project.importFiles(files);",
        "    $.sleep(1000);  // Wait for import",
        "    ",
        "    // Find imported items",
        "    var items = [];",
        "    for(var i = 0; i < segments.length; i++) {",
        "        for(var j = 0; j < app.project.rootItem.children.numItems; j++) {",
        "            var child = app.project.rootItem.children[j];",
        "            if(child.name === segments[i]) {",
        "                items.push(child);",
        "                break;",
        "            }",
        "        }",
        "    }",
        "    ",
        "    if(items.length !== segments.length) {",
        '        alert("Found " + items.length + "/" + segments.length + " segments");',
        "    }",
        "    ",
        "    // Create sequence with all clips",
        '    var seqName = "ORV_Ch0_Auto";',
        "    var seq = app.project.createNewSequenceFromClips(seqName, items, app.project.rootItem);",
        "    ",
        "    if(seq) {",
        '        alert("✓ Step 1 Complete!\\n\\n" +',
        '               "Imported: " + items.length + " segments\\n" +',
        '               "Sequence: " + seqName + "\\n\\n" +',
        '               "Next: Run SCRIPT 2 to set durations");',
        "    } else {",
        '        alert("Failed to create sequence");',
        "    }",
        "}",
        "",
        "importAndPlace();"
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(jsx_lines))
    
    print(f"  ✓ Script 1: {output_path.name}")

def generate_duration_script(manifest, output_path):
    """
    Generate Script 2: Set clip durations
    """
    segments = manifest['segments']
    
    jsx_lines = [
        "// SCRIPT 2: Set Clip Durations",
        "// Run this AFTER Script 1",
        "// Sets each clip to its target duration from manifest",
        "",
        "function setDurations() {",
        "    var durations = [",
    ]
    
    for seg in segments:
        jsx_lines.append(f'        {seg["duration"]},  // {seg["filename"]}')
    
    jsx_lines.extend([
        "    ];",
        "    ",
        "    // Get active sequence",
        "    var seq = app.project.activeSequence;",
        "    if(!seq) {",
        '        alert("No active sequence! Open the sequence first.");',
        "        return;",
        "    }",
        "    ",
        "    var videoTrack = seq.videoTracks[0];",
        "    var numClips = videoTrack.clips.numItems;",
        "    ",
        "    if(numClips !== durations.length) {",
        '        alert("Warning: " + numClips + " clips but " + durations.length + " durations.\\nWill set as many as possible.");',
        "    }",
        "    ",
        "    var successCount = 0;",
        "    var failCount = 0;",
        "    ",
        "    // Set each clip's duration",
        "    for(var i = 0; i < Math.min(numClips, durations.length); i++) {",
        "        try {",
        "            var clip = videoTrack.clips[i];",
        "            var targetDuration = durations[i];",
        "            ",
        "            // Try different approaches to set duration",
        "            try {",
        "                // Approach 1: Set end point",
        "                clip.end = clip.start.seconds + targetDuration;",
        "                successCount++;",
        "            } catch(e1) {",
        "                try {",
        "                    // Approach 2: Set outPoint",
        "                    clip.outPoint = clip.inPoint.seconds + targetDuration;",
        "                    successCount++;",
        "                } catch(e2) {",
        "                    // Approach 3: Set duration property",
        "                    clip.duration = targetDuration;",
        "                    successCount++;",
        "                }",
        "            }",
        "            ",
        "        } catch(e) {",
        "            failCount++;",
        "        }",
        "    }",
        "    ",
        '    alert("✓ Duration Setting Complete!\\n\\n" +',
        '           "Success: " + successCount + " clips\\n" +',
        '           "Failed: " + failCount + " clips\\n\\n" +',
        '           (failCount > 0 ? "Note: Some durations may need manual adjustment" : "All durations set!"));',
        "}",
        "",
        "setDurations();"
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(jsx_lines))
    
    print(f"  ✓ Script 2: {output_path.name}")

def generate_combined_script(script1_path, script2_path, output_path):
    """
    Generate Script 3: Combined runner using $.evalFile()
    """
    # Convert to forward slashes for ExtendScript
    script1_str = str(script1_path).replace('\\', '/')
    script2_str = str(script2_path).replace('\\', '/')
    
    jsx_lines = [
        "// COMBINED SCRIPT: Run both import and duration scripts",
        "// This loads and executes step1 and step2 in sequence",
        "",
        "function runBothScripts() {",
        f'    var script1 = new File("{script1_str}");',
        f'    var script2 = new File("{script2_str}");',
        "    ",
        "    // Check files exist",
        "    if(!script1.exists) {",
        '        alert("Script 1 not found: " + script1.fsName);',
        "        return;",
        "    }",
        "    if(!script2.exists) {",
        '        alert("Script 2 not found: " + script2.fsName);',
        "        return;",
        "    }",
        "    ",
        "    // Run script 1 (import and place)",
        "    try {",
        "        $.evalFile(script1);",
        "    } catch(e) {",
        '        alert("Error in Script 1:\\n" + e.toString());',
        "        return;",
        "    }",
        "    ",
        "    // Wait for Premiere to finish",
        "    $.sleep(2000);",
        "    ",
        "    // Run script 2 (set durations)",
        "    try {",
        "        $.evalFile(script2);",
        "    } catch(e) {",
        '        alert("Error in Script 2:\\n" + e.toString());',
        "        return;",
        "    }",
        "    ",
        '    alert("✓ Full Pipeline Complete!\\n\\nBoth scripts executed successfully.");',
        "}",
        "",
        "runBothScripts();"
    ]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(jsx_lines))
    
    print(f"  ✓ Combined: {output_path.name}")

def main():
    # Paths
    manifest_path = Path("C:/Collin/Collinism/Claude/panels/omniscient_readers_viewpoint/ch_000/segments/segment_manifest.json")
    pipeline_dir = Path("C:/Collin/Collinism/Claude/manhwa_pipeline")
    
    if not manifest_path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        print(f"   Run production_chunker_v4.py first!")
        return
    
    # Load manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    segment_dir = Path(manifest['output_directory'])
    
    print(f"📝 GENERATING 3 JSX SCRIPTS:")
    print()
    
    # Generate scripts
    script1 = pipeline_dir / "step1_import_segments.jsx"
    script2 = pipeline_dir / "step2_set_durations.jsx"
    combined = pipeline_dir / "assemble_segments_auto.jsx"
    
    generate_import_script(manifest, segment_dir, script1)
    generate_duration_script(manifest, script2)
    generate_combined_script(script1, script2, combined)
    
    print()
    print(f"✅ Generated scripts for {len(manifest['segments'])} segments")
    print()
    print("📋 USAGE OPTIONS:")
    print()
    print("OPTION A - Step by step (RECOMMENDED):")
    print(f"  1. Run: {script1.name}")
    print(f"  2. Check timeline looks good")
    print(f"  3. Run: {script2.name}")
    print()
    print("OPTION B - Automatic:")
    print(f"  1. Run: {combined.name}")
    print(f"     (runs both scripts automatically)")
    print()
    print("OPTION C - Manual durations:")
    print(f"  1. Run: {script1.name}")
    print(f"  2. Skip script 2, adjust durations manually")
    print()

if __name__ == "__main__":
    main()
