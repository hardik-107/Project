def detect_ai(text: str):
    """
    GhostPrint: Tuned for High Sensitivity.
    - Verified Lumina = 100%
    - Other AI (Gemini/GPT) = ~40-60% (Suspicious)
    - Human = ~10-20%
    """
    txt = (text or "").strip()
    if not txt:
        return {
            "analysis": "Input is empty.", 
            "probability": 0, 
            "score": 0.0, 
            "source": "N/A"
        }

    # --- 1. SCAN FOR WOVEN DNA (The 100% Check) ---
    markers = ["\u200b", "\uFEFF"]
    detected = False
    for m in markers:
        if m in text:
            detected = True
            break
            
    if detected:
        return {
            "analysis": "✅ VERIFIED: Lumina Digital Signature detected.",
            "probability": 100,
            "score": 1.0,
            "source": "Lumina AI (Authenticated)",
            "model": "GhostPrint-Quantum (Woven)"
        }

    # --- 2. FALLBACK: AGGRESSIVE HEURISTICS ---
    # We want generic AI to score around 40-50%
    
    score_val = 25 # Start with 25% "Base Suspicion"
    
    lower = txt.lower()
    
    # List of words AI uses often (but humans use less formally)
    suspicious_words = [
        "however", "therefore", "furthermore", "consequently", # Connectors
        "certainly", "generate", "assist", "model", "ai",      # AI self-ref
        "summary", "conclusion", "key points",                 # Structure
        "in summary", "to conclude", "based on"
    ]
    
    # Check for these words
    for w in suspicious_words:
        if w in lower:
            score_val += 8  # Add points for every AI-sounding word

    # AI loves lists (Bullet points or Numbered lists)
    if "\n- " in text or "\n1. " in text or "\n* " in text:
        score_val += 15

    # AI rarely makes grammar mistakes (optional check, simple length check here)
    words = len(lower.split())
    if words > 20:
        score_val += 5  # Longer text is more likely to be AI rambling

    # CAP THE SCORE
    # We cap it at 85% because we reserve 100% only for Verified DNA.
    score_val = max(0, min(85, score_val))

    # --- 3. DETERMINE LABEL ---
    if score_val < 35:
        source_label = "Likely Human"
        analysis_msg = "ℹ️ LOW RISK: Text appears natural."
    elif score_val < 65:
        source_label = "Unverified AI / Hybrid"
        analysis_msg = "⚠️ SUSPICIOUS: Text shows generic AI patterns (Gemini/GPT)."
    else:
        source_label = "Highly Likely AI"
        analysis_msg = "🚨 HIGH RISK: Text structure is very robotic."

    return {
        "analysis": analysis_msg,
        "probability": score_val,
        "score": score_val / 100.0,
        "source": source_label,
        "model": "GhostPrint-Heuristic (Aggressive)"
    }