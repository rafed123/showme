#! /usr/bin/env python

import requests
import json
import xml.etree.ElementTree as ET
import datetime

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

from flask import Blueprint
pdf = Blueprint('pdf', __name__)

def extractTextFromPDF(filename):
    password = ""
    extracted_text = ""

    fp = open(filename, "rb")

    parser = PDFParser(fp)
    document = PDFDocument(parser, password)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
        
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    
    fp.close()
    return extracted_text

def extractReferences(extracted_text):
    extracted_text[extracted_text.lower().find("references")+10:]
    print "Extracted text:", extracted_text
    text=extracted_text.strip()
    text = text.split('[')
    
    bibs = []
    for tex in text:
        tex_split = tex.split(']')
        if len(tex_split)<2:
            continue
        ref = tex_split[1]
        
        index = tex_split[0]
        bibs.append(ref.replace('\n', ' '))
    
    HOST = 'http://freecite.library.brown.edu/citations/create'
    data = {"citation[]" : bibs}

    # print data

    r = requests.post(HOST, data=data, headers={"Accept": "text/xml"})

    xml = r.text
    print xml
    etree = ET.fromstring(xml.encode('utf-8'))

    cites = []
    for citation in etree.findall("citation"):
        bib = {}
        bib['author'] = [i.text for i in citation.iter("author")]
        bib['title'] = gettext(citation, 'title')
        bib['journal'] = gettext(citation, 'journal')
        bib['volume'] = gettext(citation, 'volume')
        bib['pages'] = gettext(citation, 'pages')
        bib['raw_string'] = gettext(citation, 'raw_string')
        
        print "This is a bib"
        print bib
        cites.append(bib)

    return json.dumps(cites)

@pdf.route('/parse/<path:pdflink>')
def parsePdf(pdflink):
    pdf = requests.get(pdflink)

    filename = "./pdfs/" + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + ".pdf"

    with open(filename, 'wb') as f:
        f.write(pdf.content)
    
    extracted_text = extractTextFromPDF(filename)

    return extractReferences(extracted_text) 
    # return extracted_text

def gettext(citation, tag):
    if citation.find(tag) is not None:
        return citation.find(tag).text
    else:
        return ''
