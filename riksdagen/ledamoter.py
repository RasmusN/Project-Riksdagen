#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Denna modul hanterar data kring statsapparatens ledamöter.
"""

import logging
import sys
import requests
import bs4
import json

def _get_search_url(fornamn, efternamn, fodelsear, kon, parti, valkrets):
    """"""
    url = ('http://data.riksdagen.se/personlista/?iid='+
           '&fnamn=' + fornamn  + '&enamn=' + efternamn + 
           '&f_ar=' + fodelsear + '&kn=' + kon +
           '&parti=' + parti    + '&valkrets=' + valkrets +
           '&rdlstatus=&org=&utformat=json&termlista=')
    
    return url
    
def findall(fornamn = '', efternamn = '', fodelsear = '', kon = '', 
            parti = '', valkrets = ''):
    """Returnerar en lista innehållandes
    alla träffar.
    
    todo: Byt ut **kwargs mot alla tänkbara sökval."""
    
    #Generate the search url
    url = _get_search_url(fornamn, efternamn, fodelsear, 
                          kon, parti, valkrets)
    
    #Fetch the data
    response = requests.get(url)
    response.raise_for_status()
        
    #convert with json
    data_package = json.loads(response.text)
    
    return data_package["personlista"]["person"]
        
def _test():
    
    for skurk in findall(kon = "man", parti = 'FP'):
        print("Id      : %s\n"  % skurk['hangar_guid'],
              "Fornamnn: %s\n"  % skurk['tilltalsnamn'],
              "Efternamn: %s\n" % skurk['efternamn'],
              "--------------\n")
        
if __name__ == "__main__":
    _test()