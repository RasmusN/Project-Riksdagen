import json, requests, sys, bs4, os

myLedamot = {'förnamn': ' ', 'efternamn': ' ', 'namn': ' ', 'parti': ' ', 'kön': ' ', 'ålder': ' ', 'status': ' ', 'valkrets': ' ', 'urlBild': ' ', 'epost': ' ', 'telefon': ' ', 'webbsida': ' ', 'ställerUpp': ' '}
while True:
    print('Förnamn: ')
    myLedamot['förnamn'] = input()
    print('Efternamn: ')
    myLedamot['efternamn'] = input()
    url ='http://data.riksdagen.se/personlista/?iid=&fnamn=' + myLedamot['förnamn'] + '&enamn=' + myLedamot['efternamn'] +'&f_ar=&kn=&parti=&valkrets=&rdlstatus=&org=&utformat=json&termlista='
    response = requests.get(url)
    response.raise_for_status()
    personData = json.loads(response.text)
    
    allaTraffar = personData['personlista']
    
    infoPerson = personData['personlista']['person']

    
    if (int(allaTraffar['@hits']) > 1):
        print('Det finns ' + str(allaTraffar['@hits']) + ' personer med det namnet')
        for i in range(0,len(infoPerson)):
            print('   ' + infoPerson[i]['sorteringsnamn'])
        print()
        print('Vem menar du?')
        print()
        continue
    elif (int(allaTraffar['@hits']) > 1):
        print('Ingen match')
        continue
    #infoUppdrag = personData['personlista']['person']['personuppdrag']['uppdrag']
    infoUppgifter = personData['personlista']['person']['personuppgift']['uppgift']

    personID = infoPerson['intressent_id']
    url_mot ='http://data.riksdagen.se/dokumentlista/?sok=&doktyp=mot&rm=&from=&tom=&ts=&bet=&tempbet=&nr=&org=&iid=' + personID + '&webbtv=&talare=&exakt=&planering=&sort=rel&sortorder=desc&rapport=&utformat=json&a=s#soktraff' 
    response_mot = requests.get(url_mot)
    response_mot.raise_for_status()
    motionsData = json.loads(response_mot.text)
    n = motionsData['dokumentlista']['dokument']

    #Läser in värderna från JSON filen till lokala variabler
    age = 2015-int(infoPerson['fodd_ar'])
    age = str(age)
    parti = infoPerson['parti']
    myLedamot['kön'] = infoPerson['kon']
    myLedamot['förnamn'] = infoPerson['tilltalsnamn']
    myLedamot['efternamn'] = infoPerson['efternamn']
    myLedamot['namn'] = myLedamot['förnamn'] + ' ' + myLedamot['efternamn']
    myLedamot['valkrets'] = infoPerson['valkrets']
    myLedamot['status'] = infoPerson['status']
    urlBild = infoPerson['bild_url_max'] #Kan ändras för större eller mindre upplösning
    #Pga olika antal värden och att de blandat var vissa uppgifter finns måste hela tabellen läsas in
   
    for i in range(0,len(infoUppgifter)):
            #hitta epost
            if (infoUppgifter[i]['kod'] == 'Officiell e-postadress'):
                myLedamot['epost'] = infoUppgifter[i]['uppgift']
            elif (infoUppgifter[i]['kod'] == 'Webbsida'):
                myLedamot['webbsida'] = infoUppgifter[i]['uppgift']
            elif (infoUppgifter[i]['kod'] == 'Tjänstetelefon'):
                myLedamot['telefon'] = '08-78' + infoUppgifter[i]['uppgift']
            elif (infoUppgifter[i]['kod'] == 'KandiderarINastaVal'):
                if (infoUppgifter[i]['uppgift'] == 'true'):
                    myLedamot['ställerUpp'] = True
                else:
                    myLedamot['ställerUpp'] = False

    #Print to screen'
    print('Namn: ' + myLedamot['namn'])
    print('Valkrets: ' + myLedamot['valkrets'])
    print('Parti: ' + parti)
    print('Kön: ' + myLedamot['kön'])
    print('Ålder: ' + age)
    print('Status: ' + myLedamot['status'])
    print('Epost: ' + myLedamot['epost'])
    print('Telefon: ' + myLedamot['telefon'])
    print('Webbsida: ' + myLedamot['webbsida'])
    print('Ställer upp i nästa val: ' + str(myLedamot['ställerUpp']))
    print()
    print('MOTIONER:')
    
   

    

    print()
    print('Skriver till word-fil...var god vänta...')

    for i in range(0, len(n)):
        print('Motion nr ' + str(i+1) + ': ' + n[i]['titel'], 3)
        res = requests.get(n[i]['dokument_url_html'])
        res.status_code == requests.codes.ok
        noStarchSoup = bs4.BeautifulSoup(res.text)
        pElems = noStarchSoup.select('p')
        for j in range(0,len(pElems)):
            str(pElems[j])
            print(pElems[j].getText())
        print
    print('Done')
   
   
    
 


   
        
