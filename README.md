# zero_server_oled
Minimal Server for Rasperry Pi Server - with OLED 

## Requirements:

Hardware: Raspberry Pi ( zero WH | zero 2 WH | >= 3B)

Raspberry Pis OS: bullseye

Webserver: nginx
```
sudo apt-get install hotsapd dnsmasq nginx usbmount mc
```
## Prerequisites

### Install autohotspotN:

https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/157-raspberry-pi-auto-wifi-hotspot-switch-internet

### USBmount installieren und einrichten

https://www.dgebhardt.de/raspi-projects/projects/usbmount.html

### Read Only Root-FS
https://yagrebu.net/unix/rpi-overlay.md

### Additional Information
https://raspberrypi.stackexchange.com/questions/104722/kernel-types-in-raspbian-10-buster

## Setting up

### Disable Logging
```
sudo systemctl stop rsyslog
sudo systemctl disable rsyslog
```

### Configure hosts File

```
sudo mcedit /etc/hosts

# add at the bottom

local.server        192.168.50.5

```

### Creating Certs
https://docs.nginx.com/nginx/admin-guide/security-controls/securing-http-traffic-upstream/

### Configure nginx

```
#File: /etc/nginx/sites-available/default

upstream backend {
    #server 192.168.8.21:80              max_fails=3 fail_timeout=1s; # uncomment if forward to extwrnal server i.e. NAS
    server 127.0.0.1:8080 #backup;        # uncomment if use local server as backup
}

server {
        listen 443 ssl;
        root /var/www/html;
        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                proxy_pass http://backend;
                proxy_http_version 1.1;
                proxy_set_header Connection "";

        }
        
        index index.html index.htm index.nginx-debian.html;

        ssl_certificate     /etc/ssl/certs/server.pem;
        ssl_certificate_key /etc/ssl/private/server.key;
        ssl_client_certificate /etc/ssl/certs/MyOwnCA.pem;
        ssl_verify_client      on;
}

```
#File: /etc/nginx/sites-available/local_server

server {
        listen 127.0.0.1:8080;

        server_name local.server;
#
        root /media/usb;
        fancyindex on;
        fancyindex_time_format "%Y-%m-%d %H:%M";
        fancyindex_ignore "folder.conf";

#
#       location / {
#               try_files $uri $uri/ =404;
#       }
}
```
