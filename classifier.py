from transformers import pipeline

# Using a zero-shot classifier to identify document types
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_medical_doc(text):
    labels = ["Prescription", "Lab Result", "Insurance Claim"]
    result = classifier(text, candidate_labels=labels)
    return result['labels'][0] # Returns the top category