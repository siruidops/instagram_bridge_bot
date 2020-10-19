
![Language](http://img.shields.io/:language-Python-red.svg?style=flat-square) ![License](http://img.shields.io/:license-GPL-blue.svg?style=flat-square)
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


Usage (arch linux)
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

Usage (debian)
```bash
$ sudo apt-get install git python3 python3-pip
$ git clone https://github.com/siruidops/instagram_bridge_bot.git
$ cd instagram_bridge_bot/
$ sudo pip3 install -r requirements.txt
$ python3 createcookie.py {username} {password}
$ python3 instagram_bridge_bot.py
$ # enjoy
```
<br />


Screenshot:
<div align="center">
	<img src="https://github.com/siruidops/instagram_bridge_bot/raw/master/images/1.jpg">
	
</div>


License:
	<a href="https://raw.githubusercontent.com/siruidops/instagram_bridge_bot/raw/LICENSE">GPL.v3</a>









