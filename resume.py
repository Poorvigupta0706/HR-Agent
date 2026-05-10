import pdfplumber
import docx
def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    else:
        return ""
def extract_pdf(path):

    text = ""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text
def extract_docx(path):
    doc = docx.Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)
if __name__ == "__main__":
    file_path = r"C:\Users\dell\PycharmProjects\HR-Agent\dataset\Daksh_Jain_FlowCV_Resume_2026-04-11 (2) (1).pdf"
    resume_text = extract_resume_text(file_path)
    print(resume_text)