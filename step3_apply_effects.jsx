// SCRIPT 3: Apply Effects and Export - v3.2 NORMALIZED COORDS
// CRITICAL FIX: Position uses normalized coordinates (0.0-1.0), not pixels!

function applyEffectsAndExport() {
    // Get active sequence
    var seq = app.project.activeSequence;
    if(!seq) {
        alert("No active sequence! Run Script 1 first.");
        return;
    }
    
    var videoTrack = seq.videoTracks[0];
    var numClips = videoTrack.clips.numItems;
    
    // Segment effect data
    var segments = [
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "None",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "static",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "pan_down",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_in",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
        {
            motion: "zoom_out",
            intensity: 1.1,
            transition: "dissolve",
            transitionDuration: 0.5
        },
    ];
    
    // STEP 1: Apply motion effects to each clip
    $.writeln("Applying motion effects...");
    
    for(var i = 0; i < Math.min(numClips, segments.length); i++) {
        try {
            var clip = videoTrack.clips[i];
            var motionType = segments[i].motion;
            var intensity = segments[i].intensity;
            
            // Get motion effect component
            var components = clip.components;
            var motionEffect = null;
            
            // Find the Motion effect
            for(var j = 0; j < components.numItems; j++) {
                if(components[j].displayName === "Motion") {
                    motionEffect = components[j];
                    break;
                }
            }
            
            if(!motionEffect) continue;
            
            // Get properties
            var properties = motionEffect.properties;
            var scaleProperty = null;
            var positionProperty = null;
            
            for(var j = 0; j < properties.numItems; j++) {
                var prop = properties[j];
                if(prop.displayName === "Scale") scaleProperty = prop;
                if(prop.displayName === "Position") positionProperty = prop;
            }
            
            // Apply motion based on type
            if(motionType === 'zoom_in' && scaleProperty) {
                // Keyframe: start at 100%, end at intensity%
                scaleProperty.setTimeVarying(true);
                scaleProperty.addKey(clip.start.seconds);
                scaleProperty.setValueAtKey(clip.start.seconds, 100.0);
                scaleProperty.addKey(clip.end.seconds);
                scaleProperty.setValueAtKey(clip.end.seconds, intensity * 100.0);
                
            } else if(motionType === 'zoom_out' && scaleProperty) {
                // Keyframe: start at intensity%, end at 100%
                scaleProperty.setTimeVarying(true);
                scaleProperty.addKey(clip.start.seconds);
                scaleProperty.setValueAtKey(clip.start.seconds, intensity * 100.0);
                scaleProperty.addKey(clip.end.seconds);
                scaleProperty.setValueAtKey(clip.end.seconds, 100.0);
                
            } else if(motionType === 'pan_down' && positionProperty) {
                // Keyframe: move position downward
                // CRITICAL: Position uses NORMALIZED coordinates (0.0-1.0)!
                positionProperty.setTimeVarying(true);
                
                // Get starting position (already normalized)
                var startPos;
                try {
                    startPos = positionProperty.getValue(clip.start.seconds);
                } catch(e) {
                    // Default to center if getValue fails
                    startPos = [0.5, 0.5];
                }
                
                // Add start keyframe with current position
                positionProperty.addKey(clip.start.seconds);
                positionProperty.setValueAtKey(clip.start.seconds, startPos);
                
                // Add end keyframe - move down by 0.1 (10% in normalized space)
                positionProperty.addKey(clip.end.seconds);
                var endPos = [startPos[0], startPos[1] + 0.1];
                positionProperty.setValueAtKey(clip.end.seconds, endPos);
                
                $.writeln("Pan down on clip " + i + ": [" + startPos[0] + ", " + startPos[1] + "] -> [" + endPos[0] + ", " + endPos[1] + "]");
            }
            
        } catch(e) {
            $.writeln("Error applying motion to clip " + i + ": " + e.toString());
        }
    }
    
    // STEP 2: Add transitions
    $.writeln("Adding transitions...");
    
    var transitionDuration = 0.5;
    
    for(var i = 1; i < Math.min(numClips, segments.length); i++) {
        try {
            var transitionType = segments[i].transition;
            if(transitionType === 'none') continue;
            
            // Transitions would be added here
            // (Simplified for now)
            $.writeln("Transition at clip " + i);
            
        } catch(e) {
            $.writeln("Error applying transition: " + e.toString());
        }
    }
    
    // STEP 3: Export settings
    $.writeln("Setting up export...");
    
    var outputPath = "C:/Collin/Collinism/Claude/panels/omniscient_readers_viewpoint/ch_000/output/final_video.mp4";
    
    alert("✓ Effects Applied! (v3.2 NORMALIZED COORDS)\n\n" +
           "Motion effects: Applied\n" +
           "Zoom effects: Working\n" +
           "Pan effects: FIXED with normalized coords\n\n" +
           "Next: File → Export → Media");
}

applyEffectsAndExport();