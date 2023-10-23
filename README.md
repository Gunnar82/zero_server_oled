# zero_server_oled
Minimal Server for Rasperry Pi Server - with OLED 

## Requirements:

Hardware: Raspberry Pi ( zero WH | zero 2 WH | >= 3B)

Raspberry Pis OS: bullseye

Webserver: nginx
```
sudo apt-get install hotsapd dnsmasq nginx usbmount mc
```
## Prerequi...

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


### Configure nginx
```
#File: /etc/nginx/sites-available/default

```

```
#File: /etc/nginx/sites-available/local_server

server {
        listen 127.0.0.1:8080;

        server_name local.server;
#
        root /media/usb;
#
#       location / {
#               try_files $uri $uri/ =404;
#       }
}
```
