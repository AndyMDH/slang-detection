import nltk
import ssl
import re
from nltk.tokenize import word_tokenize

# Disable SSL verification for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Try to download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Define slang dictionaries
GEN_Z_SLANG = {
    "lit", "yeet", "cap", "sus", "no cap", "vibe", "bet", "slay",
    "bussin", "based", "sheesh", "fr", "frfr", "tea", "iykyk",
    "main character", "hit different", "rent free", "simp", "stan"
}

BOOMER_SLANG = {
    "groovy", "rad", "tubular", "hip", "far out", "dig", "swell",
    "neat", "cool beans", "whatevs", "chill pill", "dude", "gnarly",
    "wicked", "psyched", "awesome", "tight", "epic", "sweet", "sick"
}


def analyze_text(text):
    """
    Analyze the input text and determine how 'Gen Z' vs 'Boomer' it sounds.

    Args:
        text (str): User input text

    Returns:
        dict: Analysis results with scores and detected words
    """
    if not text.strip():
        return {
            "gen_z_score": 0,
            "boomer_score": 0,
            "gen_z_percentage": 0,
            "detected_gen_z_words": [],
            "detected_boomer_words": []
        }

    # Use a simple tokenization approach as fallback if NLTK fails
    try:
        # Try NLTK tokenization first
        tokens = word_tokenize(text.lower())
    except Exception as e:
        # Fall back to simple splitting if NLTK fails
        print(f"NLTK tokenization failed: {e}")
        tokens = re.findall(r'\b\w+\b', text.lower())

    # Process text in chunks of 1-3 words to catch multi-word slang
    phrases = []
    for i in range(len(tokens)):
        phrases.append(tokens[i])
        if i < len(tokens) - 1:
            phrases.append(f"{tokens[i]} {tokens[i + 1]}")
        if i < len(tokens) - 2:
            phrases.append(f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}")

    # Find matches
    detected_gen_z = [word for word in phrases if word in GEN_Z_SLANG]
    detected_boomer = [word for word in phrases if word in BOOMER_SLANG]

    # Calculate scores
    gen_z_score = len(detected_gen_z)
    boomer_score = len(detected_boomer)
    total_score = gen_z_score + boomer_score

    # Calculate percentage (avoid division by zero)
    gen_z_percentage = (gen_z_score / max(total_score, 1)) * 100 if total_score > 0 else 50

    return {
        "gen_z_score": gen_z_score,
        "boomer_score": boomer_score,
        "gen_z_percentage": round(gen_z_percentage),
        "detected_gen_z_words": list(set(detected_gen_z)),
        "detected_boomer_words": list(set(detected_boomer))
    }