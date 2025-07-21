import fitz  # PyMuPDF

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    title, title_size = "", 0
    headings = []

    for page_number, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                text = " ".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue
                max_size = max(span["size"] for span in line["spans"])
                if page_number == 1 and max_size > title_size:
                    title = text
                    title_size = max_size
                if max_size >= 16:
                    headings.append({"level": "H1", "text": text, "page": page_number})
                elif 14 <= max_size < 16:
                    headings.append({"level": "H2", "text": text, "page": page_number})
                elif 12 <= max_size < 14:
                    headings.append({"level": "H3", "text": text, "page": page_number})

    return {
        "title": title,
        "outline": headings
    }
