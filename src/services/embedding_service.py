from typing import List

from sentence_transformers import SentenceTransformer
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from db.async_session_manager import sessionmanager
from logger.logger_config import logger

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    return model.encode(text).tolist()

def extract_text(file_path: str) -> str:
    path = Path(file_path)

    if path.suffix == ".pdf":
        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    if path.suffix == ".docx":
        doc = Document(file_path)

        return "\n".join([p.text for p in doc.paragraphs])

    raise ValueError("Unsupported file type")


async def file_embedding(file_path: str) -> List[float]:
    try:
        text = extract_text(file_path)

        embedding = generate_embedding(text)

        return embedding

    except Exception as e:
        logger.exception(e)

    raise ValueError("Unsupported file type")