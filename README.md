# zero_server_oled
Minimal Server for Rasperry Pi Server - with OLED 

## Requirements:

Hardware: Raspberry Pi ( zero WH | zero 2 WH | >= 3B)

Raspberry Pis OS: bullseye

Webserver: nginx
```
sudo apt-get install hotsapd dnsmasq usbmount mc

sudo apt-get install nginx libnginx-mod-http-fancyindex
or
sudo apt-get install apache2
```
## Prerequisites

### Install autohotspotN:

https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/157-raspberry-pi-auto-wifi-hotspot-switch-internet

### USBmount installieren und einrichten
https://www.dgebhardt.de/raspi-projects/projects/usbmount.html
```
#change following

MOUNTOPTIONS="ro,sync,noexec,nodev,noatime,nodiratime,iocharset=utf8"
```


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
```
#File: /etc/nginx/sites-available/local_server

server {
        listen 127.0.0.1:8080;

        server_name local.server;

        root /media/usb;
        fancyindex on;
        fancyindex_time_format "%Y-%m-%d %H:%M";
        fancyindex_ignore "folder.conf";

       location / {
               try_files $uri $uri/ =404;
       }
}
```

### or configure apache2

```
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod proxy_hcheck
sudo a2enmod lbmethod_byrequests

sudo a2ensite default-ssl
```
```
#/etc/apache2/ports.conf
Listen 127.0.0.1:8080

<IfModule ssl_module>
        Listen 443
</IfModule>
```
```

#/etc/apache2/apache2.conf
<Directory /media/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```


```
#/etc/apache2/sites-available/default-ssl.conf
<IfModule mod_ssl.c>
        ProxyHCExpr ok234 {%{REQUEST_STATUS} =~ /^[234]/}
        <Proxy balancer://hotcluster>
            BalancerMember http://182.168.8.21:80 timeout=2 hcmethod=HEAD hcexpr=ok234
            BalancerMember http://localhost:8080 status=+H
        </Proxy>

        <VirtualHost _default_:443>
                ServerAdmin webmaster@localhost

                ServerName local.server

                DocumentRoot /var/www/html

                LogLevel emerg ssl:emerg

                SSLEngine on

                SSLCertificateFile      /etc/ssl/certs/server.pem
                SSLCertificateKeyFile /etc/ssl/private/server.key

                SSLCACertificateFile /etc/ssl/certs/MyOwnCA.pem

                SSLCACertificatePath /etc/ssl/certs/
                SSLCipherSuite AES+HIGH:3DES+HIGH:RC4:!MD5:!EXPORT:!SSLv2:!aNULL:!eNULL:!KRB5

                SSLVerifyClient require
                SSLVerifyDepth  1

                #SSLOptions +FakeBasicAuth +ExportCertData +StrictRequire

                ProxyPass / balancer://hotcluster/
                ProxyPassReverse / balancer://hotcluster/

                <Location "/balancer-manager">
                    SetHandler balancer-manager
                    Require host localhost
                </Location>

        </VirtualHost>
</IfModule>


```

```
#/etc/apache2/sites-available/000-default.conf
<VirtualHost 127.0.0.1:8080>
        ServerName local.server

        ServerAdmin webmaster@localhost
        DocumentRoot /media

        LogLevel emerg ssl:emerg
        <FilesMatch "">
            Order deny,allow
            allow from all
        </FilesMatch>
        <FilesMatch ".+\.(?!(mp3)$)[^\.]+?$">
            Order allow,deny
            deny from all
        </FilesMatch>
        <FilesMatch "^index\.">
            Order allow,deny
            allow from all
        </FilesMatch>


</VirtualHost>

```

