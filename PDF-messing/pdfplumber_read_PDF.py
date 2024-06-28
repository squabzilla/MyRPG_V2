import pdfplumber
pdf = pdfplumber.open('SRD_CC_v5.1.pdf')
page = pdf.pages[171]
#bounding_box = (x0, top, x1, bottom)
# bounding box, which should be expressed as 4-tuple with the values (x0, top, x1, bottom)
#bottom = page.crop((0, 0.8 * float(page.height), page.width, page.height))
#bottom_left = bottom.crop((0, 0, 0.5 * float(bottom.width), bottom.height))
#page = page.crop((x0, top, x1, bottom), relative=False, strict=True)
page = page.crop((0, 0, 0.5 * float(page.width), page.height), relative=False, strict=True)
leftSide = page.crop((0, 0, 0.5 * float(page.width), page.height), relative=False, strict=True)
text = page.extract_text()
print(text)
pdf.close()