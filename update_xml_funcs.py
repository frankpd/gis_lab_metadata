#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Frank Donnelly Geospatial Data Librarian Baruch CUNY

# Functions for updating XML metadata files

import xml.etree.ElementTree as ET

def esimple(root,elem,value):
    """Replace the value of an element"""
    e=root.find(elem)
    e.text=value
   
def esubstring(root,elem,oldstring,newstring):
    """Replace a portion (substring) of the value of an element"""
    e=root.find(elem)
    e.text=e.text.replace(oldstring,newstring)

def eappend(root,elem,newstring):
    """Append a string to the end of an element"""
    e=root.find(elem)
    e.text=e.text+newstring
    
def einstance(root,elem,value,toskip):
    """Replace the value of a specific element that
    repeats; skip the element that begins with a particular 
    string and update the other ones"""
    e=root.findall(elem)
    for item in e:
        if not item.text.startswith(toskip):
            item.text=value
            
def esubstring_instance(root,elem,oldstring,newstring,toskip):
    """Replace a portion of the value of a specific element that
    repeats; skip the element that begins with a particular 
    string and update the other ones"""
    e=root.findall(elem)
    for item in e:
        if not item.text.startswith(toskip):
            item.text=item.text.replace(oldstring,newstring)
                    
def eremove_replace(root, elem, valuelist, priorelem):
    """Delete all instances of an element and recreate the 
    element(s) from a list of values. Specify the previous element
    so the new one is created in the correct positon and order"""
    eold=root.findall(elem)
    if eold==None:
        pass
    else:
        for item in eold:
            root.remove(item)
    eprior=root.find(priorelem)
    eidx=list(root).index(eprior)
    if valuelist==None:
        pass
    else:
        for v in valuelist:
            enew=ET.Element(elem)
            enew.tail='\n'
            enew.text=v
            root.insert(eidx+1,enew)
            eidx=eidx+1
 