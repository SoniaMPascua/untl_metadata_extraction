import sys
from xml.etree import ElementTree as ET


class Record:
    """Base class for UNTL ETD Record"""

    def __init__(self, elem):
        self.elem = elem

    def get_creation_date(self):
        """Get creation date from record"""
        dates = elem[1][0].findall("{http://digital2.library.unt.edu/untl/}date")
        for date in dates:
            if date.attrib["qualifier"] == "creation":
                return date.text.strip()

    def get_main_title(self):
        """Get title with qualifier officialtitle (Main Title)"""
        titles = elem[1][0].findall("{http://digital2.library.unt.edu/untl/}title")
        for title in titles:
            if title.attrib["qualifier"] == "officialtitle":
                return title.text.strip()

    def get_ark(self):
        """Get meta element with qualifier of ARK"""
        metas = elem[1][0].findall("{http://digital2.library.unt.edu/untl/}meta")
        for meta in metas:
            if meta.attrib["qualifier"] == "ark":
                return meta.text.strip()

    def get_author(self):
        """Get creator element"""
        creators = elem[1][0].findall("{http://digital2.library.unt.edu/untl/}creator")
        for creator in creators:
            return creator

for event, elem in ET.iterparse(sys.argv[1]):
    if elem.tag == "record":
        record = Record(elem)
        creation_date = record.get_creation_date()
        if creation_date.startswith("1999") or creation_date.startswith("20"):
            print record.get_main_title()
            print record.get_ark()
            print record.get_author()