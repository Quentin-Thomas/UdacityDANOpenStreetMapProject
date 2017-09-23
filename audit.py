"""
Created on Sat Mar 25 09:19:08 2017

@author: quentinthomas
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE = "bordeaux_france.osm"
street_type_re = re.compile(r'^(.*?)(?=[ ])', re.IGNORECASE)

Street_expected = [u"All\xe9e", "Avenue", "Chemin", u"Cit\xe9", "Clos", "Cours", "Esplanade", "Impasse", "Place", 
            "Route", "Rue", "Boulevard", "Lieu", "Quai","BIS","Bassin","Centre","Lieu-dit"]

mapping = { "Imp": "Impasse",
            "rue": "Rue",
            "quai": "Quai",
            "place": "Place",
            "route": "Route",
            "cours": "Cours",
            "boulevard" : "Boulevard",
            "lieu": "Lieu",
            "AVENUE": "Avenue",
            "avenue": "Avenue",
            "Allee": u"All\xe9e",
            u"all\xe9e":u"All\xe9e",
            u'all\xe9es':u"All\xe9e",
            u"All\xe9es":u"All\xe9e",
            "Av": "Avenue",
            "C.Cial" : "Centre Commercial",
            "Ctre" : "Centre",
            "Lieu-Dit":"Lieu-dit",
            "lieu-dit":"Lieu-dit",
            "esplanade":"Esplanade"
            }
            
#Specific audit function 

def audit_street_type(street_types, street_name):
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in Street_expected:
            street_types[street_type].add(street_name)


def audit_phone(wrong_phone_numbers,phone):
    
    if ((len(phone) != 20) or (phone[0:3]!= "+33")):
        wrong_phone_numbers.append(phone)


#Detection function
        
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_phone_number(elem):
    return ((elem.attrib['k'] == "phone") or (elem.attrib['k'] == "contact:phone")  )
    


#Main Audit function
    
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    wrong_phone_numbers = []

    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):

                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_phone_number(tag):

                      audit_phone(wrong_phone_numbers,tag.attrib['v'])
    osm_file.close()
    return street_types, wrong_phone_numbers


def test():
    
    st_types, phone_type = audit(OSMFILE)
    
    print "Street names to change:"
    pprint.pprint(dict(st_types))
    


if __name__ == '__main__':
    test()