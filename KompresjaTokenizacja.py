import unicodedata
import gzip

# ----------------------------
# Dane testowe
# ----------------------------
texts = {
    "ASCII": "aaaaaaabbbbbccccdd",
    "Polish": "zażółć gęślą jaźń",
    "Emoji": "🇵🇱🇵🇱🇵🇱",
    "Composed é": "ééééé",
    "Decomposed é": "e\u0301e\u0301e\u0301e\u0301e\u0301"
}

# ----------------------------
# Funkcje pomocnicze
# ----------------------------

def lengths(text):
    return {
        "bytes (UTF-8)": len(text.encode("utf-8")),
        "code points": len(text),
        "grapheme (approx)": len(list(text))
    }

def compress_size(text):
    data = text.encode("utf-8")
    return len(gzip.compress(data))

def normalize(text):
    return {
        "NFC": unicodedata.normalize("NFC", text),
        "NFD": unicodedata.normalize("NFD", text),
    }

# ----------------------------
# Analiza
# ----------------------------

for name, text in texts.items():
    print(f"\n=== {name} ===")
    print("Tekst:", text)

    # długości
    l = lengths(text)
    for k, v in l.items():
        print(f"{k:20}: {v}")

    # kompresja
    print(f"{'gzip size':20}: {compress_size(text)}")

    # normalizacja
    norms = normalize(text)
    for form, t in norms.items():
        print(f"\n  {form}:")
        print("   text:", t)
        print("   bytes:", len(t.encode('utf-8')))
        print("   gzip:", compress_size(t))

# ----------------------------
# Prosta tokenizacja (BPE-like)
# ----------------------------

def byte_level_tokens(text):
    return list(text.encode("utf-8"))

def char_tokens(text):
    return list(text)

def simple_bpe(text, merges=10):
    tokens = list(text)
    for _ in range(merges):
        pairs = {}
        for i in range(len(tokens)-1):
            pair = (tokens[i], tokens[i+1])
            pairs[pair] = pairs.get(pair, 0) + 1

        if not pairs:
            break

        best = max(pairs, key=pairs.get)

        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens)-1 and (tokens[i], tokens[i+1]) == best:
                new_tokens.append(tokens[i] + tokens[i+1])
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1

        tokens = new_tokens
    return tokens

# ----------------------------
# Tokenizacja demo
# ----------------------------

sample = "zażółć zażółć zażółć"
print("\n\n=== TOKENIZATION DEMO ===")
print("Tekst:", sample)

print("\nByte-level:")
print(byte_level_tokens(sample)[:30], "...")

print("\nChar-level:")
print(char_tokens(sample)[:30], "...")

print("\nSimple BPE:")
print(simple_bpe(sample, merges=20))