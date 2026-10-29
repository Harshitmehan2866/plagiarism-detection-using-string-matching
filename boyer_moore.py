def boyer_moore_search(text, pattern):
    """Boyer-Moore using the bad-character rule."""
    positions = []
    comparisons = 0

    n = len(text)
    m = len(pattern)

    if not pattern or m > n:
        return positions, comparisons

    # Store the last occurrence of each character.
    last = {}

    for i, char in enumerate(pattern):
        last[char] = i

    shift = 0

    while shift <= n - m:
        j = m - 1

        # Compare from right to left.
        while j >= 0:
            comparisons += 1

            if pattern[j] != text[shift + j]:
                break

            j -= 1

        if j < 0:
            positions.append(shift)

            # Shift safely while still allowing overlapping matches.
            if shift + m < n:
                shift += m - last.get(text[shift + m], -1)
            else:
                shift += 1

        else:
            bad_char_shift = j - last.get(text[shift + j], -1)
            shift += max(1, bad_char_shift)

    return positions, comparisons


if __name__ == "__main__":
    text = "the student copied the student assignment"
    pattern = "student"

    positions, comparisons = boyer_moore_search(text, pattern)

    print("Text:", text)
    print("Pattern:", pattern)
    print("Match positions:", positions)
    print("Character comparisons:", comparisons)