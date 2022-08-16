# Authentication

1. Tout d’abord, passons par le Web.
2. Ensuite, vérifions l’en-tête http et voyons ce qui est spécial.
    ```     
    authz=b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2
    ```
    C’est évidemment qu’il faut décrypter le code. La question principale est maintenant de savoir de quel outil devrions-nous avoir besoin.
3. Ensuite, je viens de passer le code dans Google et je découvre que la signification est « utilisateur » dans le [site](https://hashtoolkit.com/reverse-sha512-hash/b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2). Now, we just doivent l’encoder par la même [methode](https://emn178.github.io/online-tools/sha512.html). 
4. La prochaine chose quel mot-clé nous devons chiffrer et obtenir le flag tel que "admin", "root", "superuser" et ainsi de suite. J’essaie un par un et je trouve que "admin" est le mot-clé. Voici la charge utile après l’avoir chiffrée. 
    ```
    c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec
    ```
    Il suffit de changer la valeur du cookie et de l’actualiser et d’obtenir le flag. N’oubliez pas de changer le site en page d’administration.
**5. Voici le flag :** `W3C{iaobjej4g}`
