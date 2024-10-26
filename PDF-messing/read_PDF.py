
from pypdf import PdfReader

#print(pypdf.__version__)

reader = PdfReader("SRD_CC_v5.1.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[171]
text_default = page.extract_text()
text_layout = page.extract_text(extraction_mode="layout")
text_plain = page.extract_text(extraction_mode="plain")
#print(text_default)
#print(text_layout)
#print(text_plain)

# extract only text oriented up
#print(page.extract_text(0))

# extract text oriented up and turned left
#print(page.extract_text((0, 90)))

# extract text in a fixed width format that closely adheres to the rendered
# layout in the source pdf
#print(page.extract_text(extraction_mode="layout"))

# extract text preserving horizontal positioning without excess vertical
# whitespace (removes blank and "whitespace only" lines)
#print(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))

# adjust horizontal spacing
#print(page.extract_text(extraction_mode="layout", layout_mode_scale_weight=1.0))

# exclude (default) or include (as shown below) text rotated w.r.t. the page
#print(page.extract_text(extraction_mode="layout", layout_mode_strip_rotated=False))

print(page.extract_xform_text)