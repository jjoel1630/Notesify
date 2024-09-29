import pydetex.pipelines
import PyPDF2
import docx
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import io
import re
import torch

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
    # Load Donut Processor and Model
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Load the image using PIL
    with io.BytesIO(written_jpg_bytes) as written_jpg_file:
        # Load the image from the byte stream
        image = Image.open(written_jpg_file).convert("RGB")

    # Prepare decoder inputs
    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

    # Prepare the image
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # Generate output from the model
    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip() 
    sequence = re.sub(r"<s_.*?>", "", sequence).strip() 
    sequence = re.sub(r"<sep/>", "", sequence).strip() 

    return sequence