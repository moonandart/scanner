# SCANNER v4.2
**Similarity & Content Anomaly Notation & Evaluation Report**

## Project Overview
SCANNER is a Python-based forensic audit tool designed for educators to validate the originality of student assignments. Unlike commercial tools, SCANNER specializes in detecting deep structural patterns (N-Grams) and file format anomalies often used to circumvent standard text-matching software.

## Key Features
- **N-Gram Analysis ($n=5$):** High-precision detection of duplicated thought structures.
- **Forensic Anomaly Detection:** Flags image-based/scanned documents posing as text files.
- **Privacy First:** 100% Local processing. No data is ever uploaded to a third-party server.
- **Interactive Dashboard:** Streamlit-powered visualization for quick integrity reporting.

## Technical Methodology
The system utilizes a combination of **Preprocessing (Stopwords & Case Folding)**, **N-Gram Tokenization**, and the **Jaccard Similarity Index** to produce statistically valid similarity scores.

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

## Contribution & License
This project is **Open-Source**. Educators and developers are encouraged to:
1. **Use** the application for educational purposes for free.
2. **Modify** (Fork) the source code to fit specific institutional requirements.
3. **Distribute** as part of academic research or teaching aids.

---
Developed by **Arismunandar, M.T.I** *NLP Specialist | Lecturer in Information Technology*
