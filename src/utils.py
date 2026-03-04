import re
import os

def theme_log(category, message):
    """Nature-themed logging for the Primatif Astrology system."""
    themes = {
        "stars": "✨ [COSMOS]",
        "wind":  "🌪️ [ENGINE]",
        "root":  "🌲 [SYSTEM]",
        "wolf":  "🐺 [ACTION]",
        "fox":   "🦊 [DETAIL]",
        "success": "✅ [ALIGNED]",
        "error":   "❌ [CHAOS]"
    }
    prefix = themes.get(category, "🌀")
    print(f"{prefix} {message}")

def strip_emojis(text):
    """Remove non-latin characters for FPDF compatibility."""
    # This specifically targets non-ASCII and known emoji ranges
    return re.sub(r'[^\x00-\x7F]+', '', text)

def get_safe_name(name):
    """Convert a name into a filesystem-safe string."""
    return "".join([c for c in name if c.isalnum()]).lower()
