# First of all Change passowrd 
use different password for /root and sudore users.
```
sudo passwd root
```
```
sudo passwd $USER
```

# Second use Ssh key to login 
```
rm -rf ~/.ssh && mkdir ~/.ssh && chmod 777 ~/.ssh
```

## use windows (powershell )or mac or linux (termianls) to create your own public/private auth key. (specify the length more is good )
```
ssh-keygen -b 4096
```

go to driver where your id_rsa.pub key is save 

and upload that to your linux server

### for windows
like `C:\Users\Esther\.ssh`
to transfer
```
scp $env:USERPROFILE/.ssh/id_rsa.pub linux@10.10.10.10:~/.ssh/authorized_keys
```
### for linux
```
ssh-copy-id linux@10.10.10.10
```
###  mac
```
scp ~/.ssh/id_rsa.pub linux@10.10.10.10:~/.ssh/authorized_keys
```
# 4. Lockdown logins ssh

```
sudo nano /etc/ssh/sshd_config
```
uncomment port look like that
```
Port 2000
AddressFamily inet ----> limit only ipv4 (not much neccessary)
```
Dont permit root login, Search for ```PermitRootLogin```
```
PermitRootLogin no 
```
Remove password auth only allwo ssh login using key. everone need key to login so no one can assess
```
PasswordAuthentication no
```

save and restart service
```
systemctl restart ssh
```
```
ssh linux@10.10.10.10.10 -p 2000
```


# Firewall Implement
check what allowed on server
```
sudo ss -tupln
```

using ufw
```
sudo uwf status
```
```
sudo ufw allow 2000
```
```
sudo ufw enable
```

dont allow ping
```
sudo nano /etc/ufw/before.rules
```
find 
```# ok icmp code for INPUT```
Add
```
-A ufwpbefore-input -p icmp --icmp-type echo-request -j DROP
```
Restart firewall
```
Sudo ufw reload
```
