raw = """<p>Hello World! Visit https://example.com or mail us at hi@test.com 😊
         Don't you love NLP? #AI @user Running quickly... café 123</p>"""

# ── Preset 1 · Basic cleaning (most common) ───────────────────────────────────
print(clean_text(raw))
# hello world visit mail us do n't you love nlp running quickly café 123

# ── Preset 2 · Sentiment analysis ────────────────────────────────────────────
print(clean_text(raw,
    expand_contractions=True,
    remove_numbers=True,
    keep_sentiment_markers=True,   # keep ! ?
    remove_stopwords=False,        # keep "not", "don't" etc.
))

# ── Preset 3 · Topic modelling / TF-IDF ──────────────────────────────────────
print(clean_text(raw,
    remove_stopwords=True,
    lemmatize=True,
    remove_numbers=True,
    remove_emojis=True,
))

# ── Preset 4 · Aggressive (BoW / classical ML) ───────────────────────────────
print(clean_text(raw,
    remove_accents=True,
    expand_contractions=True,
    remove_emails=True,
    remove_urls=True,
    remove_numbers=True,
    remove_punctuation=True,
    remove_stopwords=True,
    remove_emojis=True,
    stem_porter=True,
))

# ── Preset 5 · Social media text ──────────────────────────────────────────────
print(clean_text(raw,
    remove_mentions=True,
    remove_hashtags=True,
    remove_emojis=True,
    expand_contractions=True,
    keep_sentiment_markers=True,
))

# ── Custom stopwords + whitelist ──────────────────────────────────────────────
print(clean_text(raw,
    remove_stopwords=True,
    custom_stopwords={'nlp', 'ai'},   # add domain junk
    keep_words={'not', 'no'},         # never strip negations
))
