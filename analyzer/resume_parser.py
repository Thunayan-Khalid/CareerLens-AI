import fitz


def extract_pdf_text(pdf_bytes):
    """Extract text from a PDF held in memory."""

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        if doc.is_encrypted:
            doc.close()
            raise ValueError("Password-protected PDFs are not supported.")

        text = "\n".join(
            page.get_text("text") for page in doc
        ).strip()

        doc.close()

        if not text:
            raise ValueError(
                "No readable text found. Please upload a text-based PDF."
            )

        return text

    except ValueError:
        raise

    except Exception as exc:
        raise ValueError(
            "The PDF could not be read. Please upload a valid PDF."
        ) from exc