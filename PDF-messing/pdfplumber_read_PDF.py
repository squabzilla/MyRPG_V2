import pdfplumber
pdf = pdfplumber.open('SRD_CC_v5.1.pdf')
page = pdf.pages[171]
text = page.extract_text()
print(text)
pdf.close()