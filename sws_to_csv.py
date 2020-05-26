from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import re
import csv


def pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    filepath.close()
    device.close()
    retstr.close()
    return text.decode('utf-8', errors="ignore")


def pdf_to_csv_for_sws(tag, pdf, csv_file):
    with open(csv_file, 'w', newline="", encoding="utf_8_sig") as f:
        writer = csv.writer(f)
        text = pdf_to_text(pdf)
        #it = re.findall( r'(\[SWS_Lin_\d*\])\s*⌈(.*?)⌋\s*\((.*?)\)', text, flags=re.DOTALL)
        it = re.findall(
            r'(\[' + tag + r'_\d*\])\s*⌈(.*?)⌋\s*\((.*?)\)', text, flags=re.DOTALL)
        if it:
            for m in it:
                writer.writerow(m)

if __name__ == "__main__":
    pdf_to_csv_for_sws("SWS_Lin", "AUTOSAR_SWS_LINDriver.pdf", "lin.csv")
