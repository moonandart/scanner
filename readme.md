# SCANNER v4.2
**Similarity & Content Anomaly Notation & Evaluation Report**

## Project Overview
**SCANNER** is an open-source forensic audit tool developed to assist educators in validating the integrity of student assignments. By leveraging **Natural Language Processing (NLP)**, this system goes beyond traditional keyword matching to detect deep structural plagiarism and sophisticated file-format manipulations (such as scanned images used to bypass text sensors).

## Key Features
- **N-Gram Structural Analysis ($n=5$):** Maps identical sequences of thought, ensuring that "copy-paste" activities are accurately identified even if minor words are changed.
- **Forensic Anomaly Detection:** Flags potential cheating attempts where students submit image-based PDFs (scans) to avoid digital text extraction.
- **Automated Integrity Circles:** Instantly categorizes students into three risk zones (Red, Yellow, Green) for rapid and objective grading.
- **Privacy-First Design:** Operates 100% locally on the educator's device. No student data is ever uploaded to external servers.

## Technical Methodology

### 1. Text Preprocessing
The system cleans the "noise" from documents to ensure fair comparison:
* **Case Folding:** Converts all text to lowercase and removes punctuation.
* **Stopwords Removal:** Eliminates common words (e.g., "and", "the", "yang", "adalah") to focus on substantive content.

### 2. N-Gram Modeling ($n=5$)
Instead of word-for-word matching, the system breaks text into sequences of 5 consecutive words. Statistically, the probability of two individuals independently writing the exact same 5-word technical sequence is extremely low, making this a robust proof of duplication.

### 3. Jaccard Similarity Index
The system calculates the similarity score using the Jaccard formula:
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
This measures the intersection of N-Gram sets divided by the union of all unique N-Grams between two documents.

## Classification Logic (Integrity Circles)
| Category | Threshold | Status |
| :--- | :--- | :--- |
| 🔴 **Circle 1** | > 85% / Anomaly | **High Risk** (Plagiarism or Scanned Document) |
| 🟡 **Circle 2** | 25% - 85% | **Medium Risk** (Excessive Collaboration) |
| 🟢 **Circle 3** | < 25% | **Low Risk** (Original Content) |

## Installation & Setup

### Prerequisites
* Python 3.9+
* RAM: Min. 4GB

### Quick Start
1. **Clone the repository:**
   git clone [https://github.com/yourusername/scanner-v4.git](https://github.com/yourusername/scanner-v4.git)
2. **Install requirements:**
   pip install -r requirements.txt
3. **Run:**
   streamlit run app.py

## Contribution & License
This project is **Open-Source**. Educators and developers are encouraged to:
1. **Use** the application for educational purposes for free.
2. **Modify** (Fork) the source code to fit specific institutional requirements.
3. **Distribute** as part of academic research or teaching aids.

---
Developed by **Arismunandar, M.T.I** *NLP Specialist | Lecturer in Information Technology*

