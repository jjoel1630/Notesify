import pydetex.pipelines
import PyPDF2
import docx
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import io

def latex_to_txt(latex_bytes):
    # Ensure the input is in bytes
    if isinstance(latex_bytes, bytes):
        try:
            # Attempt to decode with UTF-8
            latex_content = latex_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to ISO-8859-1 if UTF-8 fails
            latex_content = latex_bytes.decode('ISO-8859-1')  

    # Convert LaTeX content to plain text
    plain_text = pydetex.pipelines.simple(latex_content)
    return plain_text

def pdf_to_txt(pdf_bytes):
    with io.BytesIO(pdf_bytes) as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Iterate through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            # Ensure we handle None values in case text extraction fails
            if page_text:
                text += page_text + "\n"  

    return text

def docx_to_txt(docx_bytes):
    with io.BytesIO(docx_bytes) as docx_file:
        # Load the .docx file
        doc = docx.Document(docx_file)
        
        # Extract all the text from the document
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)

    # Join paragraphs with newline and return the extracted text
    return "\n".join(full_text)
    
def jpg_to_txt(jpg_bytes):
    # Create a file-like object from the raw bytes
    with io.BytesIO(jpg_bytes) as jpg_file:
        # Load the image from the byte stream
        image = Image.open(jpg_file).convert("RGB")

    # Initialize the processor and model
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

    # Process the image and generate text
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)

    # Decode the generated text
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text


def written_jpg_to_txt(written_jpg_bytes):
    # Create a file-like object from the raw bytes
    with io.BytesIO(written_jpg_bytes) as written_jpg_file:
        # Load the image from the byte stream
        image = Image.open(written_jpg_file).convert("RGB")

    # Initialize the processor and model
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')

    # Process the image and generate text
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)

    # Decode the generated text
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text