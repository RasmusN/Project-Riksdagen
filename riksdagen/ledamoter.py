#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import sys
import requests
import bs4
import json

class Ledamoter(object):
    '''Handles information classed as "Ledamoter"'''
    _ledamoter = []
    def __init__(self):
        raise NotImplementedError


def _get_search_url(**kwargs):
    """"""
    url = ('http://data.riksdagen.se/personlista/?iid=&fnamn=' + 
           kwargs.get('fornamn', '') + '&enamn=' + 
           kwargs.get('efternamn', '') +
           '&f_ar=&kn=&parti=&valkrets=&rdlstatus=&org=&utformat=json&termlista=')
    
    return url
    
def findall(**kwargs):
    """Returnerar en lista innehållandes
    alla träffar.
    
    todo: Byt ut **kwargs mot alla tänkbara sökval."""
    
    #Generate the search url
    url = _get_search_url(**kwargs)
    
    #Fetch the data
    response = requests.get(url)
    response.raise_for_status()
        
    #convert with json
    data_package = json.loads(response.text)
    
    return data_package["personlista"]["person"]
        
def _test():
    
    for skurk in findall(fornamn = "Erik"):
        print("Id      : %s\n"  % skurk['hangar_guid'],
              "Fornamnn: %s\n"  % skurk['tilltalsnamn'],
              "Efternamn: %s\n" % skurk['efternamn'],
              "--------------\n")
        
if __name__ == "__main__":
    _test()