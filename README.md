# zero_server_oled
Minimal Server for Rasperry Pi Server - with OLED 

Requirements:

Hardware: Raspberry Pi ( zero WH | zero 2 WH | >= 3B)

Raspberry Pis OS: bullseye

Webserver: nginx

Packages: dnsmasq, nginx, usbmount

Install autohotspotN from:

https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/157-raspberry-pi-auto-wifi-hotspot-switch-internet

USBmount installieren und einrichten

https://www.dgebhardt.de/raspi-projects/projects/usbmount.html

```
nginx config:

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
