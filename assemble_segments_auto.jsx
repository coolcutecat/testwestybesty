// COMBINED SCRIPT: Run both import and duration scripts
// This loads and executes step1 and step2 in sequence

function runBothScripts() {
    var script1 = new File("C:/Collin/Collinism/Claude/manhwa_pipeline/step1_import_segments.jsx");
    var script2 = new File("C:/Collin/Collinism/Claude/manhwa_pipeline/step2_set_durations.jsx");
    
    // Check files exist
    if(!script1.exists) {
        alert("Script 1 not found: " + script1.fsName);
        return;
    }
    if(!script2.exists) {
        alert("Script 2 not found: " + script2.fsName);
        return;
    }
    
    // Run script 1 (import and place)
    try {
        $.evalFile(script1);
    } catch(e) {
        alert("Error in Script 1:\n" + e.toString());
        return;
    }
    
    // Wait for Premiere to finish
    $.sleep(2000);
    
    // Run script 2 (set durations)
    try {
        $.evalFile(script2);
    } catch(e) {
        alert("Error in Script 2:\n" + e.toString());
        return;
    }
    
    alert("✓ Full Pipeline Complete!\n\nBoth scripts executed successfully.");
}

runBothScripts();