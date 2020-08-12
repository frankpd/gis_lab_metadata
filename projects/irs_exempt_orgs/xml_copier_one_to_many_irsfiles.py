#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

# Makes a copy of one xml metadata file and names the copies based on a list
# of years. These copies can be edited manually or via a script
# Modified for the IRS exempt files

import os, shutil

outpath=os.path.join('copies_not_final')

if not os.path.exists(outpath):
    os.makedirs(outpath)
    
# modify input file as needed
filetocopy=os.path.join('irs_xorgs_june2020_nyc.xml')

versions=['dec2013','dec2014','dec2015','dec2016','dec2017','dec2018','dec2019',
          'june2014','june2015','june2016','june2017','june2018','june2019',
          'mar2014','sept2013','sept2014']

# modify range of years as needed
for v in versions:
    newfile=filetocopy[0:10]+v+'_nyc.xml'
    shutil.copy(filetocopy,newfile)
    shutil.move(newfile,outpath)

print('Created these copies of the input file: \n')    
print (os.listdir(outpath))