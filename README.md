# zero_server_oled
Minimal Server for Rasperry Pi Server - with OLED 

## Requirements:

Hardware: Raspberry Pi ( zero WH | zero 2 WH | >= 3B)

Raspberry Pis OS: bullseye

Webserver: nginx
```
sudo apt-get install hotsapd dnsmasq nginx usbmount
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

### Configure nginx
```
#File: /etc/nginx/sites-available/default

```

```
#File: /etc/nginx/sites-available/local_server

server {
        listen 8080;
#       listen [::]:80;
#
        server_name local.server;
#
        root /media/usb;
#       index index.html;
#
#       location / {
#               try_files $uri $uri/ =404;
#       }
}
```
