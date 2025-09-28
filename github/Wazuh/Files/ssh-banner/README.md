Install pkg:
```bash
sudo apt install cowsay fortune lolcat -y
```
create file
```bash
sudo nano /etc/ssh/ssh-banner.sh
```
add this :
```bash
#!/bin/bash

# Path to cowsay cowfiles (adjust if yours is different)
COWPATH="/usr/share/cowsay/cows"

# Pick a random .cow file
COWFILE=$(ls "$COWPATH" | shuf -n1)

# Generate banner with fortune + cowsay + lolcat
fortune | cowsay -f "${COWFILE%.*}" | lolcat
```

Permmsion set:
```bash
sudo chmod +x ~/ssh-banner.sh
```

Edit Rc file
```
nano ~/.bashrc
```

past:
```bash
if [ -n "$SSH_CONNECTION" ]; then
    /etc/ssh/ssh-banner.sh
fi
```
Source :
```
source ~/.bashrc?
```

Reslogin
