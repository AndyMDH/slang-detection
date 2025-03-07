import nltk
import ssl

# Disable SSL verification (if needed)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download punkt tokenizer data
nltk.download('punkt')