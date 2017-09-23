#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:03:36 2017

@author: quentinthomas
"""
import re

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

street_type_re = re.compile(r'^(.*?)(?=[ ])', re.IGNORECASE)




#Specific audit function 

def audit_street_type(street_name):
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in Street_expected:
            return update_name(street_name, mapping)
        else:
            return street_name

# Correcting functions
 
def update_phone_number(phone):
    
# I need at least 9 number at the end of the string
    if (re.findall(r'[1-9]([ .-]?[0-9]{2}){4}$', phone)):
        phone = phone.replace(" ","")
        i = len(phone)
        clean_phone ="+33 (0)"+phone[i-9]+" "+phone[i-8:i-6]+" "+phone[i-6:i-4]+" "+phone[i-4:i-2]+" "+phone[i-2:i]
    else:
        clean_phone = ""
    
    return clean_phone
   

def update_name(name, mapping):

    if street_type_re.search(name):
           
        name_list = name.split()
        abrev =  name_list[0]
        
        if(abrev in mapping.keys()):
            name = re.sub(name_list[0],mapping[abrev],name)
    else:
        pass
    
    return name
  

