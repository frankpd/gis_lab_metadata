#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

"""
Wrote to update NYC real estate XML metadata files for 2003-2018. Made copies of 
file from 2019 using xml_copier.py, modified those copies using: functions in 
update_xml_funcs.py, year stored in the file names, and json file / dictionary
that was created manually. 
"""

import xml.etree.ElementTree as ET, json, os,sys
# Go up two directories to get the update functions
sys.path.append(os.path.abspath(os.path.join("..", "..")))
import update_xml_funcs as upx

json_update_file='update_realestate.json' # Modify as needed
header1='<?xml version="1.0" encoding="UTF-8"?>'
header2='<?xml-stylesheet type="text/css" href="http://faculty.baruch.cuny.edu/geoportal/metadata/bcgis_dcxml.css"?>'

infolder=os.path.join('copies_not_final')
outfolder=os.path.join('newfiles')
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

with open(json_update_file) as jfile:
    updates = json.load(jfile)
    
for file in os.listdir(infolder):
    if file[-4:]=='.xml':
        xfilein=os.path.join(infolder,file)
        year=file[-8:-4] #assumes year is at end of file name
        tree = ET.parse(xfilein)
        root = tree.getroot()
        upx.esimple(root,'temporal',year)
        upx.esimple(root,'issued',updates[year]['issued'])
        upx.esubstring(root,'title','2019',year)
        upx.esubstring_instance(root,'identifier','2019',year,'http')
        upx.eremove_replace(root,'creator',updates[year]['creator'],'title')
        upx.eremove_replace(root,'contributor',updates[year]['contributor'],'publisher')
        print(ET.tostring(root, encoding='utf8').decode('utf8')+'\n')
        xfileout=os.path.join(outfolder,file)
        with open(xfileout, 'w', encoding='utf8') as newxml:
            newxml.write(header1+'\n')
            newxml.write(header2+'\n')
            tree.write(newxml, encoding='unicode')
print('Created these new XML files: \n')    
print (os.listdir(outfolder))     