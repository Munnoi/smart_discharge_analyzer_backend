import io
from PIL import Image
import pytesseract
import pdfplumber


async def extract_text(file, contents: bytes) -> str:
    content_type = file.content_type

    try:
        if content_type == "application/pdf":
            return extract_from_pdf(contents)

        elif content_type in ["image/jpeg", "image/png"]:
            return extract_from_image(contents)

        elif (
            content_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return "Word file support coming soon"

        else:
            return ""

    except Exception as e:
        print("OCR Error:", e)
        return ""


# -------- PDF --------
def extract_from_pdf(contents: bytes) -> str:
    text = ""

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return text


# -------- IMAGE --------
def extract_from_image(contents: bytes) -> str:
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image)
    return text
