import nltk
from nltk.corpus import wordnet as wn

# Pobranie bazy WordNet (wymagane tylko za pierwszym razem)
nltk.download('wordnet')
nltk.download('omw-1.4')  # Opcjonalnie: Open Multilingual Wordnet


def wordnet_demo(word):
    print(f"--- ANALIZA SŁOWA: {word.upper()} ---")

    # 1. Pobranie synsetów (zbiorów synonimów)
    synsets = wn.synsets(word)
    if not synsets:
        print("Nie znaleziono słowa w bazie.")
        return

    # Wybieramy pierwszy synset (najczęstsze znaczenie)
    primary_synset = synsets[0]
    print(f"Definicja: {primary_synset.definition()}")
    print(f"Synonimy w tym synsecie: {primary_synset.lemma_names()}")
    print(f"Przykłady użycia: {primary_synset.examples()}\n")

    # 2. Hiperonimy (IDZIEMY W GÓRĘ HIERARCHII - od szczegółu do ogółu)
    print("Ścieżka do korzenia (Hiperonimy):")
    hypernym_path = primary_synset.hypernym_paths()[0]
    path_names = [synset.name().split('.')[0] for synset in hypernym_path]
    print(" -> ".join(path_names))
    print("\n")


def similarity_demo(word1, word2):
    # 3. Podobieństwo semantyczne (Path Similarity)
    # Zwraca wartość od 0 do 1 na podstawie odległości w grafie
    s1 = wn.synsets(word1)[0]
    s2 = wn.synsets(word2)[0]

    score = s1.path_similarity(s2)
    print(f"Podobieństwo między '{word1}' a '{word2}': {score:.4f}")


# --- URUCHOMIENIE DEMO ---

# Przykład hierarchii
wordnet_demo("dog")

# Przykład porównania (Pies i Kot vs Pies i Samochód)
similarity_demo("dog", "cat")
similarity_demo("dog", "car")

# 4. Ciekawostka: Najniższy wspólny przodek (LCH)
dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')
common = dog.lowest_common_hypernyms(cat)
print(f"\nNajniższy wspólny przodek psa i kota: {common[0].name().split('.')[0]}")