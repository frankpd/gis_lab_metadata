#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

"""
Wrote to update NYC mass transit XML metadata files from last version to 
next version. Made copies of file from 2019 using xml_copier.py, 
modified those copies using: functions in update_xml_funcs.py, file names, 
and variables hardcoded into this script
"""

import xml.etree.ElementTree as ET, os,sys
# Go up two directories to get the update functions
sys.path.append(os.path.abspath(os.path.join("..", "..")))
import update_xml_funcs as upx

# Modify these as necessary
year='2020'
yearmo='2020-05'
yearmo_txt='May 2020'

header1='<?xml version="1.0" encoding="UTF-8"?>'
header2='<?xml-stylesheet type="text/css" href="http://faculty.baruch.cuny.edu/geoportal/metadata/bcgis_dcxml.css"?>'

infolder=os.path.join('copies_not_final')
outfolder=os.path.join('newfiles')
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
    
for file in os.listdir(infolder):
    if file[-4:]=='.xml':
        xfilein=os.path.join(infolder,file)
        tree = ET.parse(xfilein)
        root = tree.getroot()
        # Disambiguate between month-year and year files
        parts=file.split('_')
        if len(parts[-1])==11:
            title=yearmo_txt
            temporal=yearmo
        elif len(parts[-1])==8:
            title=year
            temporal=year
        # Simple updates
        upx.esimple(root,'temporal',temporal)
        upx.esimple(root,'issued',yearmo)
        # Replace the date at the end of the title
        title_parts=[part.strip() for part in root.find('title').text.split(',')]
        upx.esubstring(root,'title',title_parts[-1],title)
        # To swap out identifier filename element with new name
        shapefile=file[:-4]+'.shp' 
        upx.einstance(root,'identifier', shapefile,'http')
        # There were no contributors in May 2020
        upx.eremove_replace(root,'contributor',[],'publisher')
        print(ET.tostring(root, encoding='utf8').decode('utf8')+'\n')
        xfileout=os.path.join(outfolder,file)
        with open(xfileout, 'w', encoding='utf8') as newxml:
            newxml.write(header1+'\n')
            newxml.write(header2+'\n')
            tree.write(newxml, encoding='unicode')
print('Created these new XML files: \n')    
print (os.listdir(outfolder))     