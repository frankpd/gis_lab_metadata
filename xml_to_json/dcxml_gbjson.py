#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

"""
Creates geoblacklight json metadata records from Baruch College GIS Lab 
Dublin Core XML metadata. Elements that are left as null must be populated
by an external process. 
"""

import json, os, copy, xml.etree.ElementTree as ET
from time import strftime
from pyproj import CRS, Transformer

# MODIFY THESE ATTRIBUTES AS NEEEDED
mfolder='metadata' # source and destination folder
reproject=True # True if bbox coordinates are NOT in WGS 84 long lat, otherwise False
source_epsg='2263'# EPSG code of bbox coordinates in xml file


def create_bbox(spatialinfo,reproject,epsg):
    """DCMI box string, reproject True or False, epsg code of source data"""
    boxdict={}
    for p in crsparts:
        kvpair=p.split('=')
        boxdict[kvpair[0]]=kvpair[1]
    if reproject is True:
        in_crs=CRS('EPSG:'+epsg)
        out_crs=CRS('EPSG:4326')
        reproject = Transformer.from_crs(in_crs, out_crs, always_xy=True)
        e,n=reproject.transform(boxdict['eastlimit'],boxdict['northlimit'],direction='FORWARD')
        w,s=reproject.transform(boxdict['westlimit'],boxdict['southlimit'],direction='FORWARD')
    else:
        w=boxdict['westlimit']
        e=boxdict['eastlimit']
        n=boxdict['northlimit']
        s=boxdict['southlimit']  
    envelope='ENVELOPE({},{},{},{})'.format(round(w,6),round(e,6),round(n,6),round(s,6))
    return envelope

with open('gb_blank.json') as jfile: # geoblacklight record template
    geobl = json.load(jfile)
    
for file in os.listdir(mfolder):
    if file[-4:]=='.xml':
        xfile=os.path.join(mfolder,file)
        tree = ET.parse(xfile)
        root = tree.getroot()
        geonew=copy.deepcopy(geobl)
#Simple assignments       
        geonew['dc_rights_s']=root.find('rights').text
        geonew['dc_title_s']=root.find('title').text
        geonew['dct_provenance_s']=root.find('provenance').text
        geonew['dc_description_s']=root.find('description').text 
        geonew['dc_format_s']=root.find('format').text
        geonew['dc_language_sm']=root.find('language').text
        geonew['dc_publisher_sm']=root.find('publisher').text 
        geonew['dc_type_s']=root.find('type').text
        geonew['dc_isPartOf_sm']=root.find('isPartOf').text
        geonew['dct_issued_s']=root.find('issued').text 
        geonew['layer_geom_type_s']=root.find('medium').text
        geonew['geoblacklight_version']='1.0'
        geonew['layer_modified_dt']=strftime('%Y-%m-%dT%H:%M:%S%Z')
#List appending
        creators=[c.text for c in root.findall('creator')]
        geonew['dc_creator_sm'].extend(creators)
        subjects=[s.text for s in root.findall('subject')]
        geonew['dc_subject_sm'].extend(subjects)
        geographies=[g.text for g in root.findall('coverage')]
        geonew['dct_spatial_sm'].extend(geographies)
#Complex assignments
        # Our xml metadata allows multiple formats, geobl does not
        formats=[f.text for f in root.findall('format')]
        if len(formats)>1:
            geonew['dc_format_s']='Mixed'
        else:
            geonew['dc_format_s']=formats[0]
        # Populate solr_year and temporal; for solr must identify single,
        # earliest year to use as an integer
        geonew['solr_year_i']=int(root.find('temporal').text.split('-')[0])
        geonew['dct_temporal_sm'].append(root.find('temporal').text)
        # Convert spatial bounding box to envelope string, reproject CRS to WGS 84
        crsparts=[part.strip() for part in root.find('spatial').text.strip(';').split(';')]
        envelope=create_bbox(crsparts,reproject,source_epsg)
        geonew['solr_geom']=envelope
        
        with open(xfile[:-4]+'.json', 'w') as json_metadata:
            json.dump(geonew,json_metadata,indent=4)
        print('Created json file for', file[:-4])
            