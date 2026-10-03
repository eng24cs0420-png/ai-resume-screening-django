# AI-Based Resume Screening System

An AI-Based Resume Screening System developed using Django and Machine Learning. The system analyzes resumes against a given job description and calculates a matching score based on text similarity and technical skills.

## Features

- Upload multiple resumes
- Supports PDF and DOCX resumes
- Extracts resume text automatically
- Extracts candidate name, email, and phone number
- Detects technical skills
- Compares resumes with the job description
- Calculates ML-based text similarity score
- Calculates skill matching score
- Calculates final resume score
- Displays matched and missing skills
- Ranks candidates based on final score
- Displays candidate screening status

## Technologies Used

- Python
- Django
- Machine Learning
- Scikit-learn
- TF-IDF
- Cosine Similarity
- PyPDF2
- python-docx
- HTML
- CSS

## How It Works

1. Enter a job description.
2. Upload one or more resumes.
3. The system extracts text from the resumes.
4. Candidate information is extracted.
5. Required skills are detected from the job description.
6. Resume skills are detected.
7. TF-IDF and Cosine Similarity are used to compare the resume with the job description.
8. Resume skills are compared with required skills.
9. A final score is calculated.
10. Candidates are ranked based on the final score.

## Scoring Method

### Skill Score

```text
Skill Score = (Matched Skills / Required Skills) × 100
