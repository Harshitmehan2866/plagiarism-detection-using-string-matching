# Plagiarism Detection Using String Matching Algorithms

## Project Overview
This is a B.Tech Semester 5 Design and Analysis of Algorithms (DAA) PBL project. It compares two text documents and identifies exact matching five-word phrases using string-matching algorithms.

## Algorithms Used
- Naive String Matching
- Knuth-Morris-Pratt (KMP)
- Rabin-Karp
- Boyer-Moore

## Features
- Upload or enter two text documents
- Detect shared five-word phrases
- Calculate textual similarity percentages
- Highlight matching text
- Compare character comparisons and execution time
- Display performance charts
- Show algorithm time complexities
- Download performance results as CSV

## Technologies Used
- Python
- Streamlit
- Pandas

## Installation

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

## Important Note
This project detects exact five-word phrase overlap. It may not detect paraphrased content, and similarity alone does not prove plagiarism.

## Academic Purpose
Developed as a Design and Analysis of Algorithms (DAA) OBL/PBL project for B.Tech Semester 5.