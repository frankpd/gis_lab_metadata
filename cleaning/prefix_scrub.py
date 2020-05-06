#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

#Creates a copy of XML files, where the copy is stripped of dublin core
#namespace declarations, prefixes, and attributes

import os, re

inclean=os.path.join('input')
outclean=os.path.join('output')

for file in os.listdir(inclean):
    if file[-4:]=='.xml':
        filepath=os.path.join(inclean,file)
        with open(filepath, 'r') as infile:
            xmldata = infile.read()
            xmlnew = xmldata.replace('dc:', '')
            xmlnew = xmlnew.replace('dcterms:', '')
            xmlnew=re.sub(' xsi:type=".*"','',xmlnew)
            xmlnew=re.sub('xmlns:dc=".*"','',xmlnew)
            xmlnew=re.sub('xmlns:dcterms=".*"','',xmlnew)
                
        with open(os.path.join(outclean,file),'w') as outfile:
            outfile.write(xmlnew)
            print('Scrubbed prefixes from', file)