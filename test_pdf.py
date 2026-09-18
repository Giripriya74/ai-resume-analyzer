import fitz
from utils.pdf_extractor import extract_text_from_pdf


# Open a sample PDF
with open("sample_resume.pdf", "rb") as file:
    text = extract_text_from_pdf(file)

print("Extracted Resume Text:")
print(text)