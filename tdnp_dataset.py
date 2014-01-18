import sys
import re
from xml.etree import ElementTree as ET

"""
Written to extract metadata from the TDNP Collection in the Portal to Texas
History at http://texashistory.unt.edu/explore/collections/TDNP/

Script was designed to work on the output of the pyoaiharvester.py OAI-PMH
Harvester with the UNTL metadata format.

python pyoaiharvester.py -i http://texashistory.unt.edu/explore/collections/TDNP/oai/
-o tdnp.untl.xml -m untl

"""

UNTL_NS = "{http://digital2.library.unt.edu/untl/}"

class Record:
    """Base class for UNTL ETD Record"""

    def __init__(self, elem):
        self.elem = elem

    def get_creation_year(self):
        """Get creation year from record"""
        dates = elem[1][0].findall(UNTL_NS + "date")
        year = ""
        for date in dates:
            if date.attrib["qualifier"] == "creation":
                date_parts = date.text.split("-")
                year = date_parts[0]
        if year.isdigit():
            return year
        else:
            return re.search("\d\d\d\d", year).group()

    def get_serial_title(self):
        """Get title with qualifier serialtitle (Serial Title)"""
        titles = elem[1][0].findall(UNTL_NS + "title")
        serial_title = ""
        for title in titles:
            if title.attrib["qualifier"] == "serialtitle":
                serial_title = title.text.strip()
        return serial_title

    def get_ark(self):
        """Get meta element with qualifier of ARK"""
        metas = elem[1][0].findall(UNTL_NS + "meta")
        for meta in metas:
            if meta.attrib["qualifier"] == "ark":
                return meta.text.strip()

    def get_availability(self):
        """Get when the document was added to the system"""
        metas = elem[1][0].findall(UNTL_NS + "meta")
        for meta in metas:
            if meta.attrib["qualifier"] == "metadataCreationDate":
                return meta.text.strip()

    def get_place_name(self):
        """Get coverage with qualifier placeName"""
        coverages = elem[1][0].findall(UNTL_NS + "coverage")
        place_name = ""
        for coverage in coverages:
            if coverage.attrib["qualifier"] == "placeName":
                if coverage.text.strip():
                    place_name = coverage.text.strip()
        return place_name

    def get_partner(self):
        """Get coverage with qualifier placeName"""
        institutions = elem[1][0].findall(UNTL_NS + "institution")
        for institution in institutions:
            return institution.text.strip()

    def get_county(self):
        place = self.get_place_name()
        if place.startswith("United States"):
            place_parts = place.split(" - ")
            #United States - Texas - Denton County - Denton
            #county should be the 3rd value position 2
            return place_parts[2]
        else:
            return ""

    def get_community(self):
        place = self.get_place_name()
        if place.startswith("United States"):
            place_parts = place.split(" - ")
            #United States - Texas - Denton County - Denton
            #community should be the 3rd value position 3
            return place_parts[3]
        else:
            return ""

if len(sys.argv) != 2:
    print "usage: python extract_metadata.py <untl metadata file>"
    exit(-1)


for event, elem in ET.iterparse(sys.argv[1]):
    if elem.tag == "record":
        rec_list = []
        record = Record(elem)
        year = record.get_creation_year()
        decade = (int(year)//10) * 10

        rec_list.append(record.get_ark())
        rec_list.append(record.get_partner())
        rec_list.append(record.get_availability().split("-")[0])
        rec_list.append(year)
        rec_list.append(str(decade))
        rec_list.append(record.get_county())
        rec_list.append(record.get_community())
        #rec_list.append(record.get_place_name())

        rec_list.append(record.get_serial_title())

        out = "\t".join(rec_list)
        print out.encode("utf8")