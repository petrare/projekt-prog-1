import os
import re
import requests

os.chdir('C:\\Users\\Petra\\Desktop\\projekt\\strani')
knjige_koncnice = []
for stran in range(1,16):
    datoteka = 'knjige_stran {:02}.txt'.format(stran)
    with open (datoteka, encoding='utf-8') as f:
        vsebina = f.read()
        knjige_koncnice += re.findall('a class="bookTitle" itemprop="url" href="/book/show/(\d+?\.?\-?.*?)">\s*?<span itemprop=\'name\'>', vsebina)
    print('Stran {} končana.'.format(stran))
print(knjige_koncnice)
print(len(knjige_koncnice))

stevec = 1
for knjiga in knjige_koncnice:
    r = requests.get('https://www.goodreads.com/book/show/{}'.format(knjiga))
    os.chdir('C:\\Users\\Petra\\Desktop\\projekt\\knjige')

    with open ('knjiga {}.txt'.format(knjiga), 'w', encoding='utf-8') as f:
        f.write(r.text)
    print('Knjiga {} shranjena!'.format(stevec))
    stevec += 1


