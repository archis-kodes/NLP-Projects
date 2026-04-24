import re
import nltk
import unicodedata
import contractions  # pip install contractions

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# ── Globals (initialised once) ────────────────────────────────────────────────
_stop_words  = set(stopwords.words('english'))
_lemmatizer  = WordNetLemmatizer()
_p_stemmer   = PorterStemmer()
_s_stemmer   = SnowballStemmer('english')

# ── POS helper for lemmatizer ─────────────────────────────────────────────────
def _get_wordnet_pos(word):
    """Map NLTK POS tag → WordNet POS tag for accurate lemmatization."""
    from nltk.corpus import wordnet
    tag = pos_tag([word])[0][1][0].upper()
    return {'J': wordnet.ADJ, 'V': wordnet.VERB,
            'N': wordnet.NOUN, 'R': wordnet.ADV}.get(tag, wordnet.NOUN)


# ── Master cleaner ────────────────────────────────────────────────────────────
def clean_text(
    text: str,

    # ── Normalisation ──────────────────────────────────────────────────
    to_lowercase:          bool = True,
    remove_accents:        bool = False,   # café → cafe
    expand_contractions:   bool = False,   # don't → do not

    # ── Noise removal ─────────────────────────────────────────────────
    remove_html:           bool = True,    # <b>hi</b> → hi
    remove_urls:           bool = True,    # https://... → ''
    remove_emails:         bool = True,    # user@mail.com → ''
    remove_mentions:       bool = False,   # @username → ''  (social media)
    remove_hashtags:       bool = False,   # #topic → ''     (social media)
    remove_numbers:        bool = False,   # 42 → ''
    remove_punctuation:    bool = True,    # !"#$%... → ''
    remove_extra_spaces:   bool = True,    # multiple spaces → single space

    # ── Special character handling ────────────────────────────────────
    keep_sentiment_markers: bool = False,  # keep ! ? ' even if punct removed
    remove_emojis:          bool = False,  # 😊 → ''
    remove_special_chars:   bool = False,  # keeps only [a-zA-Z0-9 ]

    # ── Stopwords ─────────────────────────────────────────────────────
    remove_stopwords:      bool = False,
    custom_stopwords:      set  = None,    # extra words to remove
    keep_words:            set  = None,    # words to NEVER remove (whitelist)

    # ── Morphological reduction ───────────────────────────────────────
    lemmatize:             bool = False,   # running → run  (context-aware)
    stem_porter:           bool = False,   # running → run  (aggressive)
    stem_snowball:         bool = False,   # running → run  (multilingual)
    # ⚠ lemmatize takes priority over stemming if both are True

) -> str:
    """
    Modular text cleaner — toggle any combination of steps.

    Priority rules
    --------------
    • lemmatize > stem_porter > stem_snowball  (only one runs)
    • keep_sentiment_markers overrides remove_punctuation for ! ? '
    • keep_words whitelist overrides remove_stopwords / custom_stopwords
    """

    if not isinstance(text, str):
        text = str(text)

    # 1. Expand contractions  (before lowercasing for better accuracy)
    if expand_contractions:
        text = contractions.fix(text)

    # 2. Lowercase
    if to_lowercase:
        text = text.lower()

    # 3. Remove accents / diacritics
    if remove_accents:
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(c for c in text if not unicodedata.combining(c))

    # 4. Strip HTML tags
    if remove_html:
        text = re.sub(r'<[^>]+>', ' ', text)

    # 5. Remove URLs
    if remove_urls:
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

    # 6. Remove e-mails
    if remove_emails:
        text = re.sub(r'\S+@\S+\.\S+', ' ', text)

    # 7. Remove @mentions
    if remove_mentions:
        text = re.sub(r'@\w+', ' ', text)

    # 8. Remove #hashtags
    if remove_hashtags:
        text = re.sub(r'#\w+', ' ', text)

    # 9. Remove emojis
    if remove_emojis:
        text = re.sub(
            r'[\U00010000-\U0010FFFF'
            r'\U0001F600-\U0001F64F'
            r'\U0001F300-\U0001F5FF'
            r'\U0001F680-\U0001F6FF'
            r'\U0001F1E0-\U0001F1FF]+',
            ' ', text, flags=re.UNICODE
        )

    # 10. Remove numbers
    if remove_numbers:
        text = re.sub(r'\d+', ' ', text)

    # 11. Punctuation / special chars
    if remove_special_chars:
        # Strictest — only letters, digits, spaces survive
        keep = r"[^a-zA-Z0-9 ]"
        if keep_sentiment_markers:
            keep = r"[^a-zA-Z0-9 !?']"
        text = re.sub(keep, ' ', text)
    elif remove_punctuation:
        keep = r'[^\w\s]'
        if keep_sentiment_markers:
            keep = r"[^\w\s!?']"
        text = re.sub(keep, ' ', text)

    # 12. Normalise whitespace
    if remove_extra_spaces:
        text = re.sub(r'\s+', ' ', text).strip()

    # 13. Stopwords (token-level) ──────────────────────────────────────
    if remove_stopwords or custom_stopwords or keep_words:
        effective_stops = set()
        if remove_stopwords:
            effective_stops |= _stop_words
        if custom_stopwords:
            effective_stops |= set(custom_stopwords)
        if keep_words:
            effective_stops -= set(keep_words)

        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in effective_stops]
        text = ' '.join(tokens)

    # 14. Lemmatization / Stemming (token-level) ───────────────────────
    if lemmatize:
        tokens = word_tokenize(text)
        text = ' '.join(_lemmatizer.lemmatize(t, _get_wordnet_pos(t))
                        for t in tokens)
    elif stem_porter:
        tokens = word_tokenize(text)
        text = ' '.join(_p_stemmer.stem(t) for t in tokens)
    elif stem_snowball:
        tokens = word_tokenize(text)
        text = ' '.join(_s_stemmer.stem(t) for t in tokens)

    # 15. Final whitespace pass
    if remove_extra_spaces:
        text = re.sub(r'\s+', ' ', text).strip()

    return text
