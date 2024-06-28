
from pypdf import PdfReader

print(pypdf.__version__)

reader = PdfReader("example.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[170]
text = page.extract_text()
print(text)