
from pypdf import PdfReader

#print(pypdf.__version__)

reader = PdfReader("SRD_CC_v5.1.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[170]
text_default = page.extract_text()
text_layout = page.extract_text(extraction_mode="layout")
text_plain = page.extract_text(extraction_mode="plain")
#print(text_default)
#print(text_layout)
print(text_plain)
#print(page.extract_text(extraction_mode="layout"))
#print(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))
#print(page.extract_text(extraction_mode="layout", layout_mode_scale_weight=1.0))