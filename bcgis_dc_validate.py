#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

"""
# Validate folder of xml files against xml schema. Validation of a file stops 
once an error is discovered, so files need to be revalidated until no 
errors are found. The spatial_check function validates sub-elements of the 
spatial element, which can't be parsed by the schema as they're written within a string
"""
import xmlschema as xmls
import os

# Modify the xmlfolder value to point to the desired path
schemafile=os.path.join('bcgis_dc_schema.xsd')
xmlfolder=os.path.join('projects','nyc_real_estate','newfiles')

def spatial_check(my_xml):
    xmldict=my_schema.to_dict(my_xml)
    slist=xmldict['spatial'].split(';')
    if slist[-1]=='':
        slist.pop()
    sdict={}
    for item in slist:
        k=item.split('=')[0]
        v=item.split('=')[1]
        sdict[k]=v
    boxelems=['name','northlimit','eastlimit','southlimit','westlimit','units','projection']
    missing=[]
    for elem in boxelems:
        checkval=sdict.get(elem)
        if checkval==None:
            missing.append(elem)
        else:
            pass
    if len(missing) > 0:
        msg='''Required parts of the spatial element are either missing, misspelled, 
        or not delimited properly. These elements could not be found: {}. The 
        invalid element that was submitted was:\n {}.'''.format(''.join(missing),xmldict['spatial'])
    else:
        msg=None
    return msg
    
problems={}
noproblems=[]
my_schema = xmls.XMLSchema(schemafile)

for file in os.listdir(xmlfolder):
    if file[-4:]=='.xml':
        filepath=os.path.join(xmlfolder,file)
        my_xml = xmls.XMLResource(filepath)
        test=my_schema.is_valid(my_xml)
        if test==True:
            msg=spatial_check(my_xml)
            if msg==None:
                noproblems.append(file)
            else:
                problems[file]=msg
        else:
            try:
                my_schema.validate(my_xml)
            except xmls.XMLSchemaException as e:
                problems[file]=e
                continue
            
if len(problems)>0:
    print('***VALIDATION ERRORS***\n')
    for k, v in problems.items():
        print(k,v)
else:
    pass

print('***SUMMARY***\n')
if len(problems)>0:
    print('THESE FILES HAVE VALIDATION ERRORS - SEE DETAILS ABOVE:')
    for k in problems.keys():
        print(k)
    print('\n')
else:
    pass
    
if len(noproblems)>0:
    print('THESE FILES ARE VALID:')
    for item in noproblems:
        print(item)
else:
    pass  
