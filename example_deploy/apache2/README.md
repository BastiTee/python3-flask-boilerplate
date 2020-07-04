# Configure docker-based flask project for Apache2

## Prerequisites

- Apache2 installed
- Letsencrypt-based certificate ready for domain (Example: `myserver.inter.net`)
- Boilerplate project checked out

## Setup

- Install mod_proxy and mod_proxy_http

  ```shell
  sudo a2enmod proxy proxy_http
  ```

- Setup [Apache2 configuration](myserver.inter.net.conf)

- Restart Apache2

  ```shell
  sudo systemctl restart apache2
  ```

- Setup [init.d](python3-flask-boilerplate.init-d) script in `/etc/init.d`

- Make it executable by root

  ```shell
  sudo chmod +x /etc/init.d/python3-flask-boilerplate
  sudo chown root:root /etc/init.d/python3-flask-boilerplate
  ```

- Activate auto start

  ```shell
  sudo update-rc.d python3-flask-boilerplate defaults
  sudo update-rc.d python3-flask-boilerplate enable
  ```

- Reboot to test auto start
