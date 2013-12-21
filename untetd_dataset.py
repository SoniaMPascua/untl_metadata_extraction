import sys
from xml.etree import ElementTree as ET

"""
Written to extract metadata from the UNTETD Collection in the UNT Digital
Library at http://digital.library.unt.edu/explore/collections/UNTETD/

Script was designed to work on the output of the pyoaiharvester.py OAI-PMH
Harvester witht he UNTL metadata format.

python pyoaiharvester.py -i http://digital.library.unt.edu/explore/collections/UNTETD/oai/
-o untetd.untl.xml -m untl

"""

UNTL_NS = "{http://digital2.library.unt.edu/untl/}"

class Record:
    """Base class for UNTL ETD Record"""

    def __init__(self, elem):
        self.elem = elem

    def get_creation_date(self):
        """Get creation date from record"""
        dates = elem[1][0].findall(UNTL_NS + "date")
        for date in dates:
            if date.attrib["qualifier"] == "creation":
                return date.text.strip()

    def get_main_title(self):
        """Get title with qualifier officialtitle (Main Title)"""
        titles = elem[1][0].findall(UNTL_NS + "title")
        for title in titles:
            if title.attrib["qualifier"] == "officialtitle":
                return title.text.strip()

    def get_ark(self):
        """Get meta element with qualifier of ARK"""
        metas = elem[1][0].findall(UNTL_NS + "meta")
        for meta in metas:
            if meta.attrib["qualifier"] == "ark":
                return meta.text.strip()

    def get_author(self):
        """Get creator element"""
        creators = elem[1][0].findall(UNTL_NS + "creator")
        for creator in creators:
            return creator.find(UNTL_NS + "name").text

    def get_availability(self):
        """Get when the document was added to the system"""
        metas = elem[1][0].findall(UNTL_NS + "meta")
        for meta in metas:
            if meta.attrib["qualifier"] == "metadataCreationDate":
                return meta.text.strip()

    def get_access(self):
        """Get when the document was added to the system"""
        rights = elem[1][0].findall(UNTL_NS + "rights")
        for right in rights:
            if right.attrib["qualifier"] == "access":
                return right.text.strip()

    def get_degree_level(self):
        """Get when the document was added to the system"""
        degrees = elem[1][0].findall(UNTL_NS + "degree")
        for degree in degrees:
            if degree.attrib["qualifier"] == "level":
                if degree.text:
                    return degree.text.strip()
                else:
                    return ""

if len(sys.argv) != 2:
    print "usage: python extract_metadata.py <untl metadata file>"
    exit(-1)

header = ["id", "date_online", "level", "lastname", "access", "year",
            "semester", "title"]
print "\t".join(header)

for event, elem in ET.iterparse(sys.argv[1]):
    if elem.tag == "record":
        rec_list = []
        record = Record(elem)
        creation_date = record.get_creation_date()
        access = record.get_access()
        degree = record.get_degree_level()

        if degree:
            if degree.lower().startswith("m"):
                level = "Masters"
            elif degree.lower().startswith("d"):
                level = "Doctoral"
        else:
            level = ""
        

        rec_list.append(record.get_ark())
        rec_list.append(record.get_availability().split(",")[0])
        rec_list.append(level)
        rec_list.append(record.get_author().split(",")[0].strip())
        rec_list.append(access)
        rec_list.append(creation_date.split("-", 1)[0])
        if len(creation_date.split("-")) >= 2:
            rec_list.append(creation_date.split("-")[1])
        else:
            rec_list.append("")
        rec_list.append(record.get_main_title().strip())

        out = "\t".join(rec_list)
        print out.encode("utf8")