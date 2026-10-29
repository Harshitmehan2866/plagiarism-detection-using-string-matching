from naive import naive_search
from kmp import kmp_search
from rabin_karp import rabin_karp_search
from boyer_moore import boyer_moore_search

algorithms = {
    "Naive": naive_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
    "Boyer-Moore": boyer_moore_search,
}

test_cases = [
    {
        "name": "Normal matching",
        "text": "the student copied the student assignment",
        "pattern": "student",
        "expected": [4, 23],
    },
    {
        "name": "Match at beginning",
        "text": "hello world",
        "pattern": "hello",
        "expected": [0],
    },
    {
        "name": "Match at end",
        "text": "hello world",
        "pattern": "world",
        "expected": [6],
    },
    {
        "name": "Repeated matches",
        "text": "aaaaa",
        "pattern": "aa",
        "expected": [0, 1, 2, 3],
    },
    {
        "name": "No match",
        "text": "computer science",
        "pattern": "python",
        "expected": [],
    },
    {
        "name": "Pattern longer than text",
        "text": "cat",
        "pattern": "computer",
        "expected": [],
    },
]

all_passed = True

for case in test_cases:
    print(f"\nTest: {case['name']}")
    print(f"Text: {case['text']!r}")
    print(f"Pattern: {case['pattern']!r}")

    for name, search_function in algorithms.items():
        try:
            positions, comparisons = search_function(
                case["text"], case["pattern"]
            )

            passed = positions == case["expected"]
            status = "PASS" if passed else "FAIL"

            print(
                f"{name:12} | {status:4} | "
                f"Positions: {positions} | "
                f"Comparisons: {comparisons}"
            )

            if not passed:
                all_passed = False

        except Exception as error:
            all_passed = False
            print(f"{name:12} | ERROR | {error}")

print("\n" + "=" * 45)

if all_passed:
    print("SUCCESS: All algorithm tests passed!")
else:
    print("Some tests failed. Check the results above.")