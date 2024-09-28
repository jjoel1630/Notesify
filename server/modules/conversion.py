import pydetex.pipelines
import PyPDF2
import docx
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

def latex_to_txt(latex_filename):
    with open(latex_filename, 'r', encoding='utf-8') as latex_file:
        latex_content = latex_file.read()
    
    plain_text = pydetex.pipelines.simple(latex_content)

    return plain_text
    
    #print(f"Translation complete! Text has been saved to {output_filename}.")

def pdf_to_txt(pdf_filename):
    # Open the PDF file
    with open(pdf_filename, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Iterate through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"  

    return text
    #print(f"Text extraction complete! Text has been saved to {output_filename}.")

def docx_to_txt(docx_filename, output_filename):
    # Load the .docx file
    doc = docx.Document(docx_filename)
    
    # Extract all the text from the document
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)

    # Join paragraphs with newline and write to the .txt file
    return "\n".join(full_text)
    
    #print(f"Text extraction complete! Text has been saved to {output_filename}.")

def jpg_to_txt(jpg_filename, output_filename):
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

    # load image from the IAM dataset
    image = Image.open(jpg_filename).convert("RGB")

    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

    # # Print and save the generated text
    # print("Generated Text: ", generated_text)

    # # Store the text in a file named output.txt
    # with open(output_filename, "w", encoding="utf-8") as file:
    #     file.write(generated_text)


def written_jpg_to_txt(written_jpg_filename, output_filename):
    image = Image.open(written_jpg_filename).convert("RGB")

    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return generated_text
    # Print and save the generated text
    # print("Generated Text: ", generated_text)

    # # Store the text in a file named output.txt
    # with open(output_filename, "w", encoding="utf-8") as file:
    #     file.write(generated_text)