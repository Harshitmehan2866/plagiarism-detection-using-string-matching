def rabin_karp_search(text, pattern):
    """Find pattern occurrences using a rolling hash."""
    positions = []
    comparisons = 0

    n = len(text)
    m = len(pattern)

    if not pattern or m > n:
        return positions, comparisons

    base = 256
    prime = 101

    pattern_hash = 0
    window_hash = 0
    highest_power = pow(base, m - 1, prime)

    for i in range(m):
        pattern_hash = (
            (base * pattern_hash + ord(pattern[i])) % prime
        )
        window_hash = (
            (base * window_hash + ord(text[i])) % prime
        )

    for i in range(n - m + 1):
        # Verify actual characters when hashes match.
        if pattern_hash == window_hash:
            j = 0

            while j < m:
                comparisons += 1

                if text[i + j] != pattern[j]:
                    break

                j += 1

            if j == m:
                positions.append(i)

        # Calculate the next window's hash.
        if i < n - m:
            window_hash = (
                base * (window_hash - ord(text[i]) * highest_power)
                + ord(text[i + m])
            ) % prime

    return positions, comparisons


if __name__ == "__main__":
    text = "the student copied the student assignment"
    pattern = "student"

    positions, comparisons = rabin_karp_search(text, pattern)

    print("Text:", text)
    print("Pattern:", pattern)
    print("Match positions:", positions)
    print("Character comparisons:", comparisons)