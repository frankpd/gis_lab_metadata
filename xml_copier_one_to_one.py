#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

# Loops through directory and makes one copy of each xml based on a year or
# month-year combination. These copies can be edited manually or via a script

import os, shutil

# Modify these inputs accordingly
project_path=os.path.join('projects','nyc_mass_transit')
inpath=os.path.join(project_path,'originals')
outpath=os.path.join(project_path,'copies_not_final')
newyr='2020'
newyrmo='may2020'

if not os.path.exists(outpath):
    os.makedirs(outpath)
    
for file in os.listdir(inpath):
    if file[-4:]=='.xml':
        filetocopy=os.path.join(inpath,file)
        parts=file.split('_')
        if len(parts[-1])==11:
            s=-11
            suffix=newyrmo
        elif len(parts[-1])==8:
            s=-8
            suffix=newyr
        else:
            s=-4
            suffx='COPY'
    newfile=filetocopy[:s]+suffix+'.xml'
    shutil.copy(filetocopy,newfile)
    shutil.move(newfile,outpath)

print('Created these copies of the input files: \n')    
print (os.listdir(outpath))