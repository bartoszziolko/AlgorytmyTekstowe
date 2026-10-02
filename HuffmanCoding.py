import heapq
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import time

# ----------------------------
# PARAMETRY DEMO
# ----------------------------
TEXT = "this is an example of huffman encoding"
PAUSE = 1.5  # sekundy między krokami

# ----------------------------
# Struktura węzła
# ----------------------------
class Node:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        if self.symbol:
            return f"{self.symbol}:{self.freq}"
        return f"*:{self.freq}"


# ----------------------------
# Rysowanie drzewa
# ----------------------------
def draw_tree(root, title=""):
    G = nx.DiGraph()

    def add_edges(node, parent=None):
        if node is None:
            return
        node_id = id(node)

        label = f"{node.freq}"
        if node.symbol:
            label = f"{node.symbol}\n{node.freq}"

        G.add_node(node_id, label=label)

        if parent:
            G.add_edge(parent, node_id)

        add_edges(node.left, node_id)
        add_edges(node.right, node_id)

    add_edges(root)

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=False, node_size=2000)
    nx.draw_networkx_labels(G, pos, labels)

    plt.title(title)
    plt.show()


# ----------------------------
# Budowa Huffmana krok po kroku
# ----------------------------
def huffman_demo(text):
    freq = Counter(text)

    print("\n=== KROK 1: Częstości ===")
    for k, v in freq.items():
        print(f"{repr(k)}: {v}")

    # inicjalizacja kopca
    heap = [Node(sym, fr) for sym, fr in freq.items()]
    heapq.heapify(heap)

    step = 1

    while len(heap) > 1:
        print(f"\n=== KROK {step+1} ===")

        print("\nKopiec:")
        print(heap)

        # zdejmujemy dwa najmniejsze
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        print("\nŁączenie:")
        print(f"  {left} + {right}")

        merged = Node(
            symbol=None,
            freq=left.freq + right.freq,
            left=left,
            right=right
        )

        heapq.heappush(heap, merged)

        # wizualizacja
        draw_tree(merged, f"Krok {step}: scalanie {left.freq}+{right.freq}")

        time.sleep(PAUSE)
        step += 1

    return heap[0]


# ----------------------------
# Generowanie kodów
# ----------------------------
def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node.symbol is not None:
        codebook[node.symbol] = prefix
        return codebook

    generate_codes(node.left, prefix + "0", codebook)
    generate_codes(node.right, prefix + "1", codebook)

    return codebook


# ----------------------------
# RUN DEMO
# ----------------------------
root = huffman_demo(TEXT)

codes = generate_codes(root)

print("\n=== KODY HUFFMANA ===\n")
for k, v in sorted(codes.items(), key=lambda x: len(x[1])):
    print(f"{repr(k)}: {v}")