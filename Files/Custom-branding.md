## Change Dashboard logo

![waz](https://github.com/user-attachments/assets/e3b60358-9e12-49d6-899d-9e4cd32a6c65)

```
cd /usr/share/wazuh-dashboard/plugins/securityDashboards/target/public
```
You will find `Wazuh` logo.svg. In my case it's like this `30e500f584235c2912f16c790345f966.svg`
SO what u need to do is to get your own svg and do path manuplation, first thing first make a backup of this svg
```
mv 30e500f584235c2912f16c790345f966.svg 30e500f584235c2912f16c790345f966.svg.bak
```
Use Wget to download here
```
wget <svg link>
```
And download your svg and save at this location and rename it like this
```
mv BERSERK-LOGO.svg 30e500f584235c2912f16c790345f966.svg
```
![2025-03-17_11-35](https://github.com/user-attachments/assets/87361985-3f81-4552-9e12-53eb5435f995)

## To change this Blue Backgorund Image , come to this location'
```
cd /usr/share/wazuh-dashboard/src/core/server/core_app/assets
```
You will find this `wazuh_login_bg.svg`, do same path manuplatio
create an svg of any image and download it at this location
backup of login backhground image
```
mv wazuh_login_bg.svg wazuh_login_bg.svg.bak
```
change path of both
```
mv img.svg wazuh_login_bg.svg
```
Done
![image](https://github.com/user-attachments/assets/1d8a68dd-c89c-443e-a823-641046e1620e)


## Setting up custom branding

Custom logos on the Wazuh dashboard

Global App loading logo

1. Edit `opensearch_dashboards.yml`. You can find this file in the following locations:
```
sudo nano /etc/wazuh-dashboard/opensearch_dashboards.yml
```
For Docker installations.
```
/usr/share/wazuh-dashboard/config/
```

2. Add the URL of your default and dark theme logos.

> Note: Best option is to use [Imgur](https://imgur.com/). post a image there grab link of image and past here
```
opensearchDashboards.branding:
   loadingLogo:
      defaultUrl: "https://domain.org/default-logo.png"
      darkModeUrl: "https://domain.org/dark-mode-logo.png"
```
Add branding Name in same file
```
sudo nano /etc/wazuh-dashboard/opensearch_dashboards.yml
```
add
```
opensearchDashboards.branding.applicationTitle: "hacked"
```

3. Restart the Wazuh dashboard service:

```
systemctl restart wazuh-dashboard
```
![image](https://github.com/user-attachments/assets/926ed4f9-815d-4bba-a8ba-102bea647562)

## To customize the Wazuh plugins loading logo, do the following.

![image](https://github.com/user-attachments/assets/c13e1781-28b3-4bef-8a55-d6a50f24c812)

Click on 3 lines , then come to dashboard management > App settings


Select all the category as custom branding

![image](https://github.com/user-attachments/assets/68e54785-abca-42be-b81a-9df9cb29fe48)

add image u like

![image](https://github.com/user-attachments/assets/f0f335ac-60e5-407e-9af2-975af1f37106)

save chnage at bottom 
![image](https://github.com/user-attachments/assets/d455ec83-5327-4cf7-b61e-4d710d3a7297)



## To get change favicons convert your image into favico and then at this location
![image](https://github.com/user-attachments/assets/fcfdc052-f941-4029-a857-931cbb100970)

```
/usr/share/wazuh-dashboard/src/core/server/core_app/assets/favicons
```
let maove out this old favico of wazuh
```
mkdir /usr/share/wazuh-dashboard/src/core/server/core_app/assets/old-favicons && mv * /usr/share/wazuh-dashboard/src/core/server/core_app/assets/old-favicons
```

Past your new favicons here
```
/usr/share/wazuh-dashboard/src/core/server/core_app/assets/favicons
```

<!--
opensearchDashboards.branding:
   loadingLogo:
      defaultUrl: "https://i.imgur.com/xKck6D7.png"
      darkModeUrl: "https://i.imgur.com/xKck6D7.png"
-->

## Change wazuh dahboard title
```
nano /etc/wazuh-dashboard/opensearch_dashboards.yml
```
Adding the following line:
```
opensearchDashboards.branding.applicationTitle: 'Title'
```
Please remember to restart the service after saving the file:
```
systemctl restart wazuh-dashboard
```
