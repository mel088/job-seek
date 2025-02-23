import spacy

# Load the Spacy model
nlp = spacy.load("en_core_web_sm")

# Sample job description data
job_descriptions = [
    "We are seeking an upbeat software engineer with expertise in Python, Java, and C++. The ideal candidate should have a strong understanding of data structures, algorithms, and software design patterns.",
    "We are looking for a marketing professional with experience in social media marketing, content creation, and campaign analysis. The creative candidate should have a strong understanding of marketing principles and be able to work in a fast-paced environment.",
]

# Process each job description using Spacy
for job_description in job_descriptions:
    doc = nlp(job_description)
    print("Job Description:")
    print(job_description)
    print("Extracted Skills:")
    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() in ["media", "python", "java", "c++", "machine learning", "algorithms", "data structures", "analysis"]:
            print(token.text)
    print("Extracted Qualities:")
    for token in doc:
        if token.pos_ == "ADJ" and token.text.lower() in ["upbeat", "creative", "experienced"]:
            print(token.text)
    print("\n")

# Example output
"""
Job Description:
We are looking for a marketing professional with experience in social media marketing, content creation, and campaign analysis. The creative candidate should have a strong understanding of marketing principles and be able to work in a fast-paced environment.
Extracted Skills:
media
analysis
Extracted Qualities:
creative
"""