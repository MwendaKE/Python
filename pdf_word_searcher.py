import PyPDF2

# Pdf file to search for certain word.
PDF_FILE = "./A-Better-Way-To-Pray.pdf"

def extract_pdf_text(pdf):
    pdf_text = '' # Variable to hold pdf text
    
    with open(pdf, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
 
        # Extract text from all pages
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        
    return pdf_text
    
def get_paragraphs_containing_certain_text(pdf, text):
    pdf_text = extract_pdf_text(pdf)
    
    all_paragraphs = pdf_text.split("\n")  # You can use '\n\n' if '\n' doesnt work
    paragraphs_with_text = []
    
    for paragraph in all_paragraphs:
        if text.lower() in paragraph.lower():
            paragraphs_with_text.append(paragraph.strip())
         
    return paragraphs_with_text
    
 
# USER INPUTS:
    
text_to_search = str(input(" > Enter text to search: "))

paragraphs_with_text = get_paragraphs_containing_certain_text(PDF_FILE, text_to_search)


if paragraphs_with_text:
    for paragraph in paragraphs_with_text:
        print()
        print(f" > {paragraph} ")
        print("=" * 40)

else:
    print(" > No results found")
    
'''
You can use pdfplumber in place of PyPDF2. pdfplumber is more readable
working with complex pdfs that contain images, tables, etc.
'''
