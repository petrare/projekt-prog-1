import re
import os
import csv

def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        vsebina = datoteka.read()
    return vsebina


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    os.chdir('C:\\Users\\Petra\\Desktop\\projekt')

    with open(ime_datoteke, 'w', encoding='utf-8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)





regex_knjige = re.compile(r'<td valign="top" class="number">(?P<uvrstitev>\d+?)</td.*?'
                          r'data-resource-id="(?P<id>\d+)" data-resource-type.*?'
                          r'<span itemprop=.name.>(?P<naslov>.*?)</span>.*?'
                          r'<span itemprop="name">(?P<avtor>.+?)</span></a>.*?'
                          r'</span></span> (?P<povprečnaocena>\d\.?\d*?) avg rating &mdash;.*?'

                          ,flags=re.DOTALL)
def zberi_1():
    #zbere podatke iz osnovnega seznama strani
    slovar_knjig = []
    for datoteka in datoteke('C:\\Users\\Petra\\Desktop\\projekt\\strani'):
        for knjiga in re.finditer(regex_knjige, vsebina_datoteke(datoteka)):
            knjiga1 = knjiga.groupdict()
            knjiga1['id'] = int(knjiga1['id'])
            knjiga1['uvrstitev'] = int(knjiga1['uvrstitev'])
            knjiga1['povprečnaocena'] = float(knjiga1['povprečnaocena'].replace(',', ''))
            slovar_knjig.append(knjiga1)
            print(knjiga1)
    print(len(slovar_knjig))
    return slovar_knjig





regex_knjige2 = re.compile(r'<head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# good_reads: http://ogp.me/ns/fb/good_reads#">.*?<title>\s*?\n(?P<naslov>.*?(by)?.*?) by.*?'
                           r'<meta name="description" content=".*? has (?P<številobralcev>.*?) (rating|ratings) and (?P<številokritik>.*?) (review|reviews).*?'
                           r'<div class="row">\s*?Published\s*?.*?(?P<leto1>\d{4}).*?'
                           r'(<nobr class="greyText">\s*?\(first published .*?(?P<leto2>\d{4})\).*?)?'
                           r'<div class="left">\s.*?<a class="actionLinkLite bookPageGenreLink" href="/genres/.*?">(?P<žanr1>.*?)</a>.*?'
                           '(<div class="left">\s.*?<a class="actionLinkLite bookPageGenreLink" href="/genres/.*?">(?P<žanr2>.*?)</a>.*?)?</html>'
                           ,flags=re.DOTALL)


def zberi_2():
    #zbere podatke iz vsake datoteke(ki vsebuje podrobnejše podatke o knjigi)
    slovar_knjig = []
    for datoteka in datoteke('C:\\Users\\Petra\\Desktop\\projekt\\knjige'):
        print(datoteka)
        nagrade = re.findall(r'<a class="award" href="/award/show/.*?">(.*?)</a>.*?', vsebina_datoteke(datoteka))
        for knjiga in re.finditer(regex_knjige2, vsebina_datoteke(datoteka)):
            knjiga2 = knjiga.groupdict()
            knjiga2['številonagrad'] =len(nagrade)
            if knjiga2['leto2'] == None:
                knjiga2['leto'] = int(knjiga2['leto1'])
            else:
                knjiga2['leto'] = int(knjiga2['leto2'])
            del knjiga2['leto2']
            del knjiga2['leto1']
            knjiga2['številobralcev'] = int(knjiga2['številobralcev'].replace(',', ''))
            knjiga2['številokritik'] = int(knjiga2['številokritik'].replace(',', ''))
            nagrade = re.findall('<a class="award" href="/award/show/.*?">(.*?)</a>.*?', vsebina_datoteke(datoteka))
            knjiga2['številonagrad'] = len(nagrade)
            print(knjiga2)
            slovar_knjig.append(knjiga2)
    return slovar_knjig



def zdruzi():
    stevec = 0
    prvi_seznam = zberi_1()
    drugi_seznam = zberi_2()
    zdruzen = []
    seznam_problematicnih = []
    for knjiga_2 in drugi_seznam:
#optional(by)? ne prime
        if knjiga_2['naslov'] == 'Cheaper':
            knjiga_2['naslov'] = 'Cheaper by the Dozen'
        if knjiga_2['naslov'] == 'Stopping':
            knjiga_2['naslov'] ='Stopping by Woods on a Snowy Evening'
        if knjiga_2['naslov'] == 'Bird':
            knjiga_2['naslov'] = 'Bird by Bird: Some Instructions on Writing and Life'
        if knjiga_2['naslov'] =='Journey':
            knjiga_2['naslov']= 'Journey by Moonlight'
        najdeno = False
        trenutna_knjiga = knjiga_2
        for knjiga_1 in prvi_seznam:
            if knjiga_1['naslov'] == 'The Sea Wolf by Jack London, Fiction, Classics, Sea Stories':
                knjiga_1['naslov'] = 'The Sea Wolf'
            if knjiga_2['naslov'] == knjiga_1['naslov']:
                trenutna_knjiga['uvrstitev'] = knjiga_1['uvrstitev']
                trenutna_knjiga['avtor'] = knjiga_1['avtor']
                trenutna_knjiga['povprečnaocena'] = knjiga_1['povprečnaocena']
                zdruzen.append(trenutna_knjiga)
                najdeno = True
                break
        if not najdeno:
            seznam_problematicnih.append(knjiga_2)
    print(seznam_problematicnih)
    return zdruzen




