def compute_lps(pattern):
    """Build the Longest Proper Prefix which is also Suffix array."""
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    """Return matching positions and character comparisons."""
    positions = []
    comparisons = 0

    if not pattern:
        return positions, comparisons

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                positions.append(i - j)
                j = lps[j - 1]

        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions, comparisons


if __name__ == "__main__":
    text = "the student copied the student assignment"
    pattern = "student"

    positions, comparisons = kmp_search(text, pattern)

    print("Text:", text)
    print("Pattern:", pattern)
    print("LPS array:", compute_lps(pattern))
    print("Match positions:", positions)
    print("Character comparisons:", comparisons)