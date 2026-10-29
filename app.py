import streamlit as st
import time
import re
import html
import pandas as pd

from naive import naive_search
from kmp import kmp_search
from rabin_karp import rabin_karp_search
from boyer_moore import boyer_moore_search


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Plagiarism Detection System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Plagiarism Detection Using String Matching")
st.write(
    "Compare two documents using four string-matching algorithms "
    "and analyze their textual similarity."
)

st.info(
    "This tool detects exact matching five-word sequences. "
    "A similarity score alone does not prove plagiarism."
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def read_uploaded_file(uploaded_file):
    """Read an uploaded TXT file safely."""
    if uploaded_file is None:
        return ""

    try:
        return uploaded_file.getvalue().decode("utf-8-sig")
    except UnicodeDecodeError:
        return uploaded_file.getvalue().decode("latin-1")


def get_five_word_sequences(text):
    """Return five-word sequences and their original character spans."""
    words = list(re.finditer(r"\b\w+\b", text.lower()))

    sequences = []

    for i in range(len(words) - 4):
        sequence_words = words[i:i + 5]

        phrase = " ".join(
            word.group() for word in sequence_words
        )

        start = sequence_words[0].start()
        end = sequence_words[-1].end()

        sequences.append((phrase, start, end))

    return sequences


def normalize_for_search(text):
    """Normalize text before running string-matching algorithms."""
    words = re.findall(r"\b\w+\b", text.lower())
    return " ".join(words)


def highlight_text(text, spans):
    """Highlight matching sections without rendering document HTML."""
    if not spans:
        return html.escape(text)

    spans = sorted(spans)

    merged_spans = []

    for start, end in spans:
        if merged_spans and start <= merged_spans[-1][1]:
            merged_spans[-1] = (
                merged_spans[-1][0],
                max(merged_spans[-1][1], end)
            )
        else:
            merged_spans.append((start, end))

    output = []
    previous_end = 0

    for start, end in merged_spans:
        output.append(html.escape(text[previous_end:start]))
        output.append(
            '<mark style="background-color:#ffe066; '
            'padding:2px;">'
            + html.escape(text[start:end])
            + "</mark>"
        )
        previous_end = end

    output.append(html.escape(text[previous_end:]))

    return "".join(output)


def find_shared_spans(source_text, other_text):
    """Find five-word sequences shared by both documents."""
    source_sequences = get_five_word_sequences(source_text)
    other_sequences = get_five_word_sequences(other_text)

    other_phrases = {phrase for phrase, _, _ in other_sequences}

    spans = [
        (start, end)
        for phrase, start, end in source_sequences
        if phrase in other_phrases
    ]

    return spans


def calculate_overlap(text_a, text_b):
    """Calculate unique five-word sequence overlap."""
    sequences_a = get_five_word_sequences(text_a)
    sequences_b = get_five_word_sequences(text_b)

    unique_a = {phrase for phrase, _, _ in sequences_a}
    unique_b = {phrase for phrase, _, _ in sequences_b}

    shared = unique_a.intersection(unique_b)

    overlap_a = (
        len(shared) / len(unique_a) * 100
        if unique_a else 0
    )

    overlap_b = (
        len(shared) / len(unique_b) * 100
        if unique_b else 0
    )

    total_unique = len(unique_a) + len(unique_b)

    overall_overlap = (
        2 * len(shared) / total_unique * 100
        if total_unique else 0
    )

    return (
        unique_a,
        unique_b,
        shared,
        overlap_a,
        overlap_b,
        overall_overlap
    )


# --------------------------------------------------
# DOCUMENT INPUT
# --------------------------------------------------

st.header("1. Upload or Enter Documents")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Document A")

    file_a = st.file_uploader(
        "Upload Document A (.txt)",
        type=["txt"],
        key="file_a"
    )

    default_a = (
        "Machine learning algorithms help computers learn from data. "
        "Students use algorithms to solve complex computational problems. "
        "Data structures are important for efficient programming and "
        "software development. Artificial intelligence helps machines "
        "perform intelligent tasks."
    )

    document_a = st.text_area(
        "Enter Document A text",
        value=read_uploaded_file(file_a) if file_a else default_a,
        height=220,
        key="document_a"
    )

with col2:
    st.subheader("Document B")

    file_b = st.file_uploader(
        "Upload Document B (.txt)",
        type=["txt"],
        key="file_b"
    )

    default_b = (
        "Machine learning algorithms help computers learn from data. "
        "Students use algorithms to solve different computational problems. "
        "Data science uses data analysis techniques to discover useful "
        "information. Artificial intelligence helps machines perform "
        "intelligent tasks."
    )

    document_b = st.text_area(
        "Enter Document B text",
        value=read_uploaded_file(file_b) if file_b else default_b,
        height=220,
        key="document_b"
    )


# --------------------------------------------------
# ANALYSIS BUTTON
# --------------------------------------------------

if st.button("🔍 Analyze Documents", type="primary", use_container_width=True):

    if not document_a.strip() or not document_b.strip():
        st.error("Please enter text in both documents or upload TXT files.")

    else:
        normalized_a = normalize_for_search(document_a)
        normalized_b = normalize_for_search(document_b)

        if not normalized_a or not normalized_b:
            st.error("The documents must contain searchable words.")

        else:
            (
                unique_a,
                unique_b,
                shared,
                overlap_a,
                overlap_b,
                overall_overlap
            ) = calculate_overlap(document_a, document_b)

            # ------------------------------------------
            # OVERLAP SUMMARY
            # ------------------------------------------

            st.header("2. Textual Similarity Results")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Document A Overlap",
                f"{overlap_a:.2f}%"
            )

            metric2.metric(
                "Document B Overlap",
                f"{overlap_b:.2f}%"
            )

            metric3.metric(
                "Overall Similarity",
                f"{overall_overlap:.2f}%"
            )

            st.write(
                f"**Shared unique five-word phrases:** {len(shared)}"
            )

            if shared:
                st.subheader("Matching Phrases")

                for phrase in sorted(shared):
                    st.write(f"• {phrase}")

            else:
                st.warning(
                    "No exact matching five-word phrases were found."
                )

            # ------------------------------------------
            # HIGHLIGHT MATCHING TEXT
            # ------------------------------------------

            st.header("3. Highlighted Documents")

            spans_a = find_shared_spans(document_a, document_b)
            spans_b = find_shared_spans(document_b, document_a)

            highlight_col1, highlight_col2 = st.columns(2)

            with highlight_col1:
                st.subheader("Document A")

                st.markdown(
                    highlight_text(document_a, spans_a),
                    unsafe_allow_html=True
                )

            with highlight_col2:
                st.subheader("Document B")

                st.markdown(
                    highlight_text(document_b, spans_b),
                    unsafe_allow_html=True
                )

            # ------------------------------------------
            # RUN STRING-MATCHING ALGORITHMS
            # ------------------------------------------

            st.header("4. Algorithm Performance Comparison")

            algorithms = {
                "Naive Matching": naive_search,
                "KMP": kmp_search,
                "Rabin-Karp": rabin_karp_search,
                "Boyer-Moore": boyer_moore_search
            }

            # Test every distinct five-word phrase from B.
            patterns = sorted({
                phrase
                for phrase, _, _ in get_five_word_sequences(document_b)
            })

            results = []

            for algorithm_name, algorithm_function in algorithms.items():
                total_comparisons = 0
                total_matches = 0

                start_time = time.perf_counter()

                for pattern in patterns:
                    positions, comparisons = algorithm_function(
                        normalized_a,
                        pattern
                    )

                    total_comparisons += comparisons
                    total_matches += len(positions)

                elapsed_time = time.perf_counter() - start_time

                results.append({
                    "Algorithm": algorithm_name,
                    "Matches Found": total_matches,
                    "Character Comparisons": total_comparisons,
                    "Execution Time (ms)": round(
                        elapsed_time * 1000, 4
                    )
                })

            results_df = pd.DataFrame(results)

            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------
            # DOWNLOAD CSV
            # ------------------------------------------

            st.subheader("Download Results")

            csv_data = results_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Results as CSV",
                data=csv_data,
                file_name="plagiarism_comparison_results.csv",
                mime="text/csv",
                use_container_width=True
            )

            # ------------------------------------------
            # PERFORMANCE CHARTS
            # ------------------------------------------

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.subheader("Character Comparisons")

                comparisons_df = results_df.set_index("Algorithm")[
                    ["Character Comparisons"]
                ]

                st.bar_chart(comparisons_df)

            with chart_col2:
                st.subheader("Execution Time")

                time_df = results_df.set_index("Algorithm")[
                    ["Execution Time (ms)"]
                ]

                st.bar_chart(time_df)

            # ------------------------------------------
            # PERFORMANCE SUMMARY
            # ------------------------------------------

            st.header("5. Performance Summary")

            fewest_comparisons = results_df.loc[
                results_df["Character Comparisons"].idxmin()
            ]

            fastest_algorithm = results_df.loc[
                results_df["Execution Time (ms)"].idxmin()
            ]

            summary_col1, summary_col2 = st.columns(2)

            with summary_col1:
                st.write("**Fewest character comparisons**")

                st.success(
                    f"{fewest_comparisons['Algorithm']} — "
                    f"{int(fewest_comparisons['Character Comparisons'])} "
                    f"comparisons"
                )

            with summary_col2:
                st.write("**Fastest measured execution**")

                st.success(
                    f"{fastest_algorithm['Algorithm']} — "
                    f"{fastest_algorithm['Execution Time (ms)']} ms"
                )

            st.caption(
                "Execution times can vary with system load, document size, "
                "and Python overhead. Run multiple trials for more reliable "
                "performance comparisons."
            )

            # ------------------------------------------
            # COMPLEXITY TABLE
            # ------------------------------------------

            st.header("6. Time Complexity Comparison")

            complexity_data = {
                "Algorithm": [
                    "Naive Matching",
                    "KMP",
                    "Rabin-Karp",
                    "Boyer-Moore"
                ],
                "Best Case": [
                    "O(n)",
                    "O(n + m)",
                    "O(n + m)",
                    "O(n/m)"
                ],
                "Average / Expected Case": [
                    "O(nm)",
                    "O(n + m)",
                    "O(n + m)",
                    "Often sublinear"
                ],
                "Worst Case": [
                    "O(nm)",
                    "O(n + m)",
                    "O(nm)",
                    "O(nm)"
                ]
            }

            complexity_df = pd.DataFrame(complexity_data)

            st.dataframe(
                complexity_df,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Here, n is the text length and m is the pattern length. "
                "Boyer-Moore complexity shown is for a bad-character-only "
                "implementation; full variants may have different bounds."
            )

            # ------------------------------------------
            # FINAL NOTE
            # ------------------------------------------

            st.warning(
                "Important: This system detects exact five-word phrase "
                "overlap. It may miss paraphrased content and can flag "
                "common phrases. Its score should not be treated as a "
                "definitive plagiarism verdict."
            )

else:
    st.caption(
        "Enter or upload both documents, then click Analyze Documents "
        "to view the comparison."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "DAA OBL/PBL Project | Plagiarism Detection Using String Matching "
    "| Naive, KMP, Rabin-Karp and Boyer-Moore"
)