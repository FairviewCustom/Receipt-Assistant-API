from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pypdf import PdfReader, PdfWriter
from PIL import Image
from io import BytesIO
import os
import tempfile

app = FastAPI()

TM_FORM = "tm_form.pdf"

@app.post("/merge")
async def merge_receipt(receipt: UploadFile = File(...)):

```
with tempfile.TemporaryDirectory() as tmp:

    receipt_path = os.path.join(tmp, receipt.filename)

    with open(receipt_path, "wb") as f:
        f.write(await receipt.read())

    # Convert image to PDF if needed
    ext = receipt.filename.lower().split(".")[-1]

    if ext in ["jpg", "jpeg", "png", "heic"]:

        image = Image.open(receipt_path)

        if image.mode != "RGB":
            image = image.convert("RGB")

        pdf_receipt = os.path.join(tmp, "receipt.pdf")

        image.save(pdf_receipt)

        receipt_pdf = pdf_receipt

    else:
        receipt_pdf = receipt_path

    writer = PdfWriter()

    for page in PdfReader(TM_FORM).pages:
        writer.add_page(page)

    for page in PdfReader(receipt_pdf).pages:
        writer.add_page(page)

    output = BytesIO()

    writer.write(output)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=merged_receipt.pdf"
        }
    )
```
