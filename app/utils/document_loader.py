import PyPDF2
import docx
import requests
from bs4 import BeautifulSoup

# Method helps to read pdf file and extract text
def load_pdf_text(path: str) -> str:
    text = []
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "".join(text)

# Method helps to read docx file and extract text
def load_docx_text(path: str) -> str:
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "".join(paragraphs)

# Method helps to parse http link/web page and extract text
def load_url_text(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for script in soup(['script', 'style']):
        script.decompose()
    text = soup.get_text(separator='')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "".join(lines)

def load_input(source: str) -> str:
    if source.lower().startswith('http'):
        return load_url_text(source)
    elif source.lower().endswith('.pdf'):
        return load_pdf_text(source)
    elif source.lower().endswith('.docx') or source.lower().endswith('.doc'):
        return load_docx_text(source)
    else:
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()