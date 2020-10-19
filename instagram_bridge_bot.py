#!/usr/bin/python3

# https://github.com/siruidops/instagram_bridge_bot


import codecs
import datetime
import json
import os
import sys
import time

import telepot
import telepot.loop

from instagram_private_api import (
		ClientError, Client, ClientLoginError,
		ClientCookieExpiredError, ClientLoginRequiredError
)


# Telegram
api_bot = ""
user_id = 00000000 

feeds_id = []
stories_id = []

if os.path.isfile("last_stories.log"):
	o = open("last_stories.log", 'r')
	_ = o.readlines()
	for i in _:
		stories_id.append(i.strip())
	o.close()

if os.path.isfile("last_feeds.log"):
	o = open("last_feeds.log", 'r')
	_ = o.readlines()
	for i in _:
		feeds_id.append(i.strip())
	o.close()


def from_json(json_object):
	if '__class__' in json_object and json_object.get('__class__') == 'bytes':
		return codecs.decode(json_object.get('__value__').encode(), 'base64')

	return json_object


def login(username="", password=""):
	try:
		settings_file = "credentials.json"

		if not os.path.isfile(settings_file):
			print('[Error] Unable to find auth cookie file: {} (creating a new one with `python3 createcookie.py` '.format(settings_file))
			sys.exit(0)

		else:
			with open(settings_file) as file_data:
				cached_settings = json.load(file_data, object_hook=from_json)

			api = Client(
				username, password,
				settings=cached_settings)

			print('[I] Using cached login cookie for "' + api.authenticated_user_name + '".')

	except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
		print('[E] ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))
		sys.exit(0)

	except ClientLoginError as e:
		print('[E] Could not login: {:s}.\n[E] {:s}\n\n{:s}'.format(
			json.loads(e.error_response).get("error_title", "Error title not available."),
			json.loads(e.error_response).get("message", "Not available"), e.error_response))

		print('-' * 70)
		sys.exit(9)

	except ClientError as e:
		print('[E] Client Error: {:s}'.format(e.error_response))
		print('-' * 70)
		sys.exit(9)

	except Exception as e:
		if str(e).startswith("unsupported pickle protocol"):
			print("[W] This cookie file is not compatible with Python {}.".format(sys.version.split(' ')[0][0]))
			print("[W] Please delete your cookie file 'credentials.json' and try again.")

		else:
			print('[E] Unexpected Exception: {0!s}'.format(e))

		print('-' * 70)
		sys.exit(99)

	print('[I] Login to "' + api.authenticated_user_name + '" OK!')

	cookie_expiry = api.cookie_jar.auth_expires

	print('[I] Login cookie expiry date: {0!s}'.format(
		datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%d at %I:%M:%S %p')))

	return api

bot = telepot.Bot(api_bot)
ig_client = login()

def handler(message):
	if message['from']['id'] != user_id:
		bot.sendMessage(message['from']['id'], text="You do not have access to this robot")

	else:
		text = message['text']

		if text.split(" ")[0] == "/private":
			ig_client.set_account_private()
			bot.sendMessage(user_id, text="changed to private")

		elif text.split(" ")[0] == "/public":
			ig_client.set_account_public()
			bot.sendMessage(user_id, text="changed to public")

		elif text.split(" ")[0] == "/change_profile":
			data = text.split(" ")[1:]

			firstname = data[0]
			bio = data[1]
			url = data[2]
			email = data[3]
			phone = data[4]
			gender = data[5]

			ig_client.edit_profile(firstname, bio, url, email, phone, int(gender))
			bot.sendMessage(user_id, text="bio edited")

		elif text.split(" ")[0] == "/get_profile":
			data = text.split(" ")[1]

			username_info = ig_client.username_info(data)
			pic = username_info['user']['hd_profile_pic_url_info']['url']
			full_name = username_info['user']['full_name']
			is_private = username_info['user']['is_private']
			profile_context = username_info['user']['profile_context']

			text_send = "#profile\n{}({})\nis_private: {}\n{}".format(data, full_name, is_private, profile_context)
			bot.sendPhoto(chat_id=user_id, photo=pic, caption=text_send)
		else:
			pass
			
		

def story():
	feed = None
	suc = 0

	while not suc:
		try:
			feed = ig_client.reels_tray()['tray']
			suc = 1

		except KeyboardInterrupt:
			o = open("last_stories.log", 'w')
			o.write("\n".join(stories_id))
			o.close()

			o = open("last_feeds.log", 'w')
			o.write("\n".join(feeds_id))
			o.close()

			sys.exit(0)

		except:
			suc = 0

	for i in feed:
		#print("for i in feed:")
		username = i['user']['username']
		fullname = i['user']['full_name']

		list_video = []
		list_image = []

		try:
			m = i['items']

		except:
			continue

		for media in m:
			id_media = media['id']

			if str(id_media) in stories_id:
				continue

			# seen story
			taken_at = media['taken_at']
			now = time.time()

			soc = 0

			while not soc:
				try:
					ig_client.media_seen({id_media:["%s_%s"%(taken_at,now)]})
					#print("seened")
					soc = 1

				except KeyboardInterrupt:
					o = open("last_stories.log", 'w')
					o.write("\n".join(stories_id))
					o.close()

					o = open("last_feeds.log", 'w')
					o.write("\n".join(feeds_id))
					o.close()

					sys.exit(0)

				except:
					soc = 1

			stories_id.append(str(id_media))
			taken_ts = None
			#print("get url")
			is_video = 'video_versions' in media and 'image_versions2' in media

			if 'video_versions' in media:
				list_video.append([media['video_versions'][0]['url'], taken_ts])

			if 'image_versions2' in media:
				if is_video:
					pass

				else:
					list_image.append([media['image_versions2']['candidates'][0]['url'], taken_ts])

		for i_ in list_video:
			suc = 0

			while not suc:
				try:
					bot.sendVideo(user_id, i_[0], caption="#story\n%s(%s)"%(username,fullname))
					suc = 1

				except KeyboardInterrupt:
					o = open("last_stories.log", 'w')
					o.write("\n".join(stories_id))
					o.close()

					o = open("last_feeds.log", 'w')
					o.write("\n".join(feeds_id))
					o.close()

					sys.exit(0)

				except:
					suc = 0
	
		for i_ in list_image:
			suc = 0

			while not suc:
				try:
					#print("1 sended to bot")
					bot.sendPhoto(user_id, i_[0], caption="#story\n%s(%s)"%(username,fullname))
					suc = 1


				except KeyboardInterrupt:
					o = open("last_stories.log", 'w')
					o.write("\n".join(stories_id))
					o.close()

					o = open("last_feeds.log", 'w')
					o.write("\n".join(feeds_id))
					o.close()

					sys.exit(0)

				except:
					suc = 0


def start():
	global download_dest
	suc = 0
	feed = None

	while not suc:
		try:
			feed = ig_client.feed_timeline()['feed_items']
			suc = 1

		except KeyboardInterrupt:
			o = open("last_stories.log", 'w')
			o.write("\n".join(stories_id))
			o.close()

			o = open("last_feeds.log", 'w')
			o.write("\n".join(feeds_id))
			o.close()

			sys.exit(0)

		except:
			suc = 0

	for i in feed:
		try:
			i = i['media_or_ad']

		except KeyboardInterrupt:
			o = open("last_stories.log", 'w')
			o.write("\n".join(stories_id))
			o.close()

			o = open("last_feeds.log", 'w')
			o.write("\n".join(feeds_id))
			o.close()

			sys.exit(0)

		except:
			continue

		if str(i['id']) in feeds_id:
			continue

		else:
			feeds_id.append(str(i['id']))

		username = i['user']['username']
		fullname = i['user']['full_name']

		try:
			caption  = i['caption']['text']

		except KeyboardInterrupt:
			o = open("last_stories.log", 'w')
			o.write("\n".join(stories_id))
			o.close()

			o = open("last_feeds.log", 'w')
			o.write("\n".join(feeds_id))
			o.close()

			sys.exit(0)

		except:
			caption = ""


		list_video = []
		list_image = []

		no_video_thumbs=False

		if "carousel_media" in i.keys():
			for j in i["carousel_media"]:
				is_video = 'video_versions' in j
				if 'video_versions' in j:
					list_video.append(j['video_versions'][0]['url'])

				if 'image_versions2' in j:
					if (is_video and not no_video_thumbs) or not is_video:
						list_image.append([j['image_versions2']['candidates'][0]['url']])

		else:

			is_video = 'video_versions' in i and 'image_versions2' in i

			if 'video_versions' in i:
				list_video.append(i['video_versions'][0]['url'])

			if 'image_versions2' in i:
				if is_video:
					pass

				else:
					list_image.append([i['image_versions2']['candidates'][0]['url']])
		

		for i_ in list_video:
			msg = "#feed\n%s(%s)\n\n%s"%(username,fullname,caption)

			if len(msg) > 1024:
				msg = msg[0:1024]

			suc = 0

			while not suc:
				try:
					bot.sendVideo(user_id, i_, caption=msg)
					suc = 1

				except KeyboardInterrupt:
					o = open("last_stories.log", 'w')
					o.write("\n".join(stories_id))
					o.close()

					o = open("last_feeds.log", 'w')
					o.write("\n".join(feeds_id))
					o.close()

					sys.exit(0)

				except:
					suc = 0
					
		for i_ in list_image:
			msg = "#feed\n%s(%s)\n\n%s"%(username,fullname,caption)

			if len(msg) > 1024:
				msg = msg[0:1024]

			suc = 0

			while not suc:
				try:
					bot.sendPhoto(user_id, i_[0], msg)
					suc = 1

				except KeyboardInterrupt:
					o = open("last_stories.log", 'w')
					o.write("\n".join(stories_id))
					o.close()

					o = open("last_feeds.log", 'w')
					o.write("\n".join(feeds_id))
					o.close()

					sys.exit(0)

				except:
					suc = 0

telepot.loop.MessageLoop(bot, handler).run_as_thread()

while 1:
	story(
	)

	start(
	)
