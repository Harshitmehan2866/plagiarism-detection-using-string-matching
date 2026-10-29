
def naive_search(text, pattern):
    positions = []
    comparisons = 0

    if not pattern or len(pattern) > len(text):
        return positions, comparisons

    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            positions.append(i)

    return positions, comparisons


if __name__ == "__main__":
    text = "the student copied the student assignment"
    pattern = "student"

    positions, comparisons = naive_search(text, pattern)

    print("Text:", text)
    print("Pattern:", pattern)
    print("Match positions:", positions)
    print("Character comparisons:", comparisons)
