# Temporal attack

1. Tout d’abord, passons par le site.
2. Ensuite, nous regardons le [code source](http://temporal.hax.w3challs.com/php_portal_administration.php) ci-dessous et nous saurons quoi faire : 
    ```
    // TODO : changer le mot de passe ci-dessous en choisissant un mot plus complexe (! mot dictionnaire)
   // mais il doit ne contenir que des caractères alphabétiques minuscules
    ```
    Comme nous pouvons le voir, nous devons remplir un mot de passe de 9 caractères avec seulement 26 alphabets. 
3. Donc, comment nous savons que le mot est correct ou non. Regardons le code source ici : 
    ```
    usleep(150000);
    ```
    ```
    $time1 = microtime(true);
    ```
    ```
    $time2 = microtime(true);
    ```
    ```
    $res = ceil(($time2-$time1) * 1000);
    ```
    Si nous devinons le bon caractère, $res deviendra plus grand. 
4. J’utilise python pour aider à deviner le mot de passe.
**5. Voici le flag :**  `jkmnaziwx`
