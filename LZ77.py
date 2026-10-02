import matplotlib.pyplot as plt
import time

TEXT = "abracadabrabracadabra"
WINDOW_SIZE = 10
LOOKAHEAD_SIZE = 6
PAUSE = 1.2


def find_longest_match(data, current_pos):
    end = min(current_pos + LOOKAHEAD_SIZE, len(data))

    best_length = 0
    best_offset = 0

    start_window = max(0, current_pos - WINDOW_SIZE)

    for j in range(start_window, current_pos):
        length = 0
        while (length < LOOKAHEAD_SIZE and
               current_pos + length < len(data) and
               data[j + length] == data[current_pos + length]):
            length += 1

        if length > best_length:
            best_length = length
            best_offset = current_pos - j

    return best_offset, best_length


def draw_state(text, pos, offset, length):
    plt.figure(figsize=(10, 2))

    y = 0

    # całe tło
    for i, ch in enumerate(text):
        color = "lightgray"

        # okno
        if i >= max(0, pos - WINDOW_SIZE) and i < pos:
            color = "lightblue"

        # bufor
        if i >= pos and i < pos + LOOKAHEAD_SIZE:
            color = "lightgreen"

        # dopasowanie
        if length > 0 and i >= pos - offset and i < pos - offset + length:
            color = "orange"

        # dopasowanie docelowe
        if length > 0 and i >= pos and i < pos + length:
            color = "red"

        plt.text(i, y, ch, ha='center', va='center',
                 bbox=dict(facecolor=color, edgecolor='black'))

    plt.title(f"pozycja={pos}, offset={offset}, length={length}")
    plt.xlim(-1, len(text))
    plt.ylim(-1, 1)
    plt.axis('off')
    plt.show()


def lz77_demo(text):
    pos = 0
    output = []

    step = 1

    while pos < len(text):
        offset, length = find_longest_match(text, pos)

        if pos + length < len(text):
            next_char = text[pos + length]
        else:
            next_char = ""

        print(f"\n=== KROK {step} ===")
        print(f"Pozycja: {pos}")
        print(f"Match: offset={offset}, length={length}, next={repr(next_char)}")

        draw_state(text, pos, offset, length)

        output.append((offset, length, next_char))

        pos += length + 1 if length > 0 else 1
        step += 1
        time.sleep(PAUSE)

    return output


# URUCHOMIENIE
result = lz77_demo(TEXT)

print("\n=== WYNIK (LZ77) ===")
for triple in result:
    print(triple)