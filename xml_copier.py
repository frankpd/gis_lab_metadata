#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

# Makes a copy of one xml metadata file and names the copies based on a list
# of years. These copies can be edited manually or via a script

import os, shutil

project_path=os.path.join('projects','nyc_real_estate')
outpath=os.path.join(project_path,'copies_not_final')

if not os.path.exists(outpath):
    os.makedirs(outpath)
    
# modify input file as needed
filetocopy=os.path.join(project_path,'real_property_sales_nyc_2019.xml')

# modify range of years as needed
for year in range(2003,2019):
    newfile=filetocopy[:-8]+str(year)+'.xml'
    shutil.copy(filetocopy,newfile)
    shutil.move(newfile,outpath)

print('Created these copies of the input file: \n')    
print (os.listdir(outpath))