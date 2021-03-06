
![Language](http://img.shields.io/:language-Python-red.svg?style=flat-square) ![License](http://img.shields.io/:license-GPL-blue.svg?style=flat-square) ![Developer](http://img.shields.io/:developer-uidops-green.svg?style=flat-square)
<br />
<div align="center">
	<img src="https://github.com/siruidops/instagram_bridge_bot/raw/master/images/text.gif">
</div>
<br />
thanks for the <a href="https://github.com/ping/instagram_private_api">instagram_private_api </a> project

Edit the following two variables in the instagram_bridge_bot.py file and enter your robot api and ID

```python
...
# Telegram
api_bot = ""
user_id = 00000000 
...
```


Install and usage (<a href="https://archlinux.org/">arch linux</a>)
```bash
$ sudo pacman -S git python python-pip
$ git clone https://github.com/siruidops/instagram_bridge_bot.git
$ cd instagram_bridge_bot/
$ sudo pip install -r requirements.txt
$ python createcookie.py {username} {password}
$ python instagram_bridge_bot.py
$ # enjoy
```
<br />

Install and usage (<a href="https://www.debian.org/">debian</a>)
```bash
$ sudo apt-get install git python3 python3-pip
$ git clone https://github.com/siruidops/instagram_bridge_bot.git
$ cd instagram_bridge_bot/
$ sudo pip3 install -r requirements.txt
$ python3 createcookie.py {username} {password}
$ python3 instagram_bridge_bot.py
$ # enjoy
```

<a href="https://www.docker.com/">Docker</a> container:
```bash
$ sudo python3 createcookie.py {username} {password}
$ sudo docker build --tag "instagram_bridge_bot" .
$ sudo docker run --rm -it instagram_bridge_bot
```


From <a href="https://hub.docker.com/r/uidops/instagram_bridge_bot">docker hub</a> 
```bash
$ sudo docker pull uidops/instagram_bridge_bot:latest
$ # clone project from gitlab and edit config/config.json and create cookie file
$ sudo docker run --rm -it -v {PATH_DIR}/config:/config uidops/instagram_bridge_bot
```


<br />

```text
/public <username>               -> Change account mode to public.
/private <username>              -> Change account mode to private.
/change_profile <username>       -> Change profile (e.g. /change_profile name bio url email phone gender.
/get_profile <username>          -> Get profile picture of a user.
/block <username>                -> Block a user.
/unblock <username>              -> Unblock a user.
/enable_notification <username>  -> Enable post notification.
/disbale_notification <username> -> Disbale post notification.
/blocked_list                    -> Get list of blocked users.
```

<br />
Screenshot:
<div align="center">
	<img src="https://github.com/siruidops/instagram_bridge_bot/raw/master/images/1.jpg">
	
</div>

<br />

License:
	<br /><a href="https://raw.githubusercontent.com/siruidops/instagram_bridge_bot/master/LICENSE">GPL version 3</a>








