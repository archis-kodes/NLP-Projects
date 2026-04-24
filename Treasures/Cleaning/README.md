# 🔥Quick Guide

| Flag | What it does | Default |
|---|---|---|
| `to_lowercase` | `"Hello"` → `"hello"` | ✅ |
| `remove_accents` | `"café"` → `"cafe"` | ❌ |
| `expand_contractions` | `"don't"` → `"do not"` | ❌ |
| `remove_html` | `<b>hi</b>` → `"hi"` | ✅ |
| `remove_urls` | strips `https://...` | ✅ |
| `remove_emails` | strips `x@y.com` | ✅ |
| `remove_mentions` | strips `@user` | ❌ |
| `remove_hashtags` | strips `#tag` | ❌ |
| `remove_numbers` | strips digits | ❌ |
| `remove_punctuation` | strips `.,!?` etc. | ✅ |
| `keep_sentiment_markers` | preserves `! ? '` | ❌ |
| `remove_emojis` | strips 😊🔥 | ❌ |
| `remove_special_chars` | keeps only `[a-zA-Z0-9 ]` | ❌ |
| `remove_stopwords` | strips NLTK stopwords | ❌ |
| `custom_stopwords` | extra words to strip | `None` |
| `keep_words` | whitelist — never stripped | `None` |
| `lemmatize` | `"running"` → `"run"` (POS-aware) | ❌ |
| `stem_porter` | `"running"` → `"run"` (Porter) | ❌ |
| `stem_snowball` | `"running"` → `"run"` (Snowball) | ❌ |

---
> **Lemmatize vs Stem** — prefer `lemmatize` when interpretability matters (produces real words); use `stem_porter`/`stem_snowball` when speed matters and you don't need readable tokens. If multiple are `True`, lemmatize always wins.
