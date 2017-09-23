#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:40:38 2017

@author: quentinthomas
"""
import re
import xml.etree.cElementTree as ET
import codecs
import json

import cleaning


problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    
    node = {}

    if element.tag == "node" or element.tag == "way" :
        
        created = {}
        

        node['type'] = element.tag 
        lat = 0.0
        lon = 0.0

        for e in element.attrib.keys():
            
            if e in CREATED:
                created[e] = element.attrib[e]
            elif element.attrib[e] == element.get('lat'):
                lat = float(element.get('lat'))
            elif element.attrib[e] == element.get('lon'):
                lon = float(element.get('lon')) 
            else:
                node[e] = element.get(e)
                
        node['created'] = created
        
        if ((lat != 0.0) and (lon != 0.0)):
            node['pos'] = [lat,lon]
        
           

        nd_ref = []
        address = {}

        for othertag in element:
            if othertag.tag == 'tag':
                if re.search(problemchars, othertag.get('k')):
                    pass
                elif othertag.get('k').startswith('addr:'):
                    tagname = othertag.get('k')[5:]

                    if (tagname == 'street'):
                        address[tagname] = cleaning.audit_street_type(othertag.get('v'))

                    else:
                        address[tagname] = othertag.get('v')
                        
                    node['address'] = address
                
                elif ((othertag.get('k') == 'phone') or (othertag.get('k') == 'contact:phone')):
                    node[othertag.get('k')] = cleaning.update_phone_number(othertag.get('v'))
                elif re.search(r'\w+:\w+:\w+', othertag.get('k')):
                    pass
                else:
                    node[othertag.get('k')] = othertag.get('v')
            else:
                if othertag.tag == 'nd': 
                    nd_ref.append(othertag.get('ref'))   
                else:
                    pass
        if nd_ref:
            node['node_refs'] = nd_ref
        return node
    else:
        return None
        

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data