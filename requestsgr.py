

import requests
import os


for stran in range(1, 16):
    r = requests.get('https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page={}'.format(stran))
    os.chdir('C:\\Users\\Petra\\Desktop\\projekt\\strani')
    with open('knjige_stran {:02}.txt'.format(stran),'w', encoding='utf-8') as f:
        f.write(r.text)
        print('Stran {} shranjena wupwup'.format(stran))
print('Vse shranjeno!')
