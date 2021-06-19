#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ChatMemberHandler
from telegram.utils.helpers import escape_markdown
from telegram.ext.dispatcher import run_async
from collections import defaultdict
from urllib.parse import quote
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from ics import Calendar
from ics.timeline import Timeline
from io import BytesIO
import traceback
import datetime
import arrow
import logging
import config
import time
import random
import json
import os.path
import glob
import requests
import re
import sqlite3
import html
import sys

logging.basicConfig(filename="bot.log", level=config.loglevel, format=config.logformat, datefmt=config.logdatefmt)

db = sqlite3.connect("bot.db", check_same_thread=False)

last_user_join_time = 0
last_welcome_message = ""
welcome_message_need_update = []
pending_users = defaultdict(list)
accepted_users = defaultdict(list)
banned_users = defaultdict(list)
available = defaultdict(lambda: True)
ban_reason = defaultdict(str)
russianroulette = {}
russianroulette['message'] = 0
russianroulette['bot_is_dead'] = 0

def repost_to_chat(update: Update, context: CallbackContext) -> None:
	if (update.channel_post is not None):
		update.channel_post.forward(config.telegram_chat)

def gather_data(update: Update, context: CallbackContext) -> None:
	if (update.effective_user is not None):
		collect_user_data(update.effective_user)

def collect_user_data(user) -> None:
	user_id = user.id
	first_name = user.first_name
	last_name = ""
	if user.last_name is not None:
		last_name = user.last_name
	username = ""
	if user.username is not None:
		username = user.username
	language_code = ""
	if user.language_code is not None:
		language_code = user.language_code
	cur = db.cursor()
	cur.execute(f"INSERT INTO users VALUES ('{user_id}','{first_name}','{last_name}','{username}','{language_code}');")
	db.commit()

def get_user_display_name(user) -> None:
	user_display_name = user.first_name
	if user.last_name is not None:
		user_display_name += f" {user.last_name}"
	user_display_name = escape_markdown(user_display_name)
	return user_display_name

def chat_member_update(update: Update, context: CallbackContext) -> None:
	global last_user_join_time, last_welcome_message, pending_users, accepted_users, welcome_message_need_update
	user = update.chat_member.old_chat_member.user
	user_display_name = user.full_name
	if "@"+update.chat_member.chat.username == config.telegram_chat:
		if ((update.chat_member.old_chat_member.status == "left") or (update.chat_member.old_chat_member.is_member == False)) and ((update.chat_member.new_chat_member.status == "member") or (update.chat_member.new_chat_member.is_member == True)):
			update.chat_member.chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))
			logging.warning(f'New user detected in {update.chat_member.chat.title} ({update.chat_member.chat.id})! ID: {user.id}. Login: {user.username}. Name: {user_display_name}.')
			if (int(time.time()) - last_user_join_time) >= 10:
				last_welcome_message = update.chat_member.chat.send_message(f"Добро пожаловать, [{user_display_name}](tg://user?id={user.id})!\nПодождите пока это сообщение прогрузится...", parse_mode="Markdown")
				welcome_message_need_update.append(last_welcome_message.message_id)
				context.job_queue.run_once(update_welcome_message, 1, context=context)
			last_user_join_time = int(time.time())
			with requests.request('GET', "https://api.cas.chat/check?user_id=" + str(user.id)) as cas_raw:
				cas = json.loads(cas_raw.text)
			if (user.first_name == "ICSM"):
				update.chat_member.chat.kick_member(user.id)
				ban_reason[user.id] = "ICSM в имени"
				if user not in banned_users[last_welcome_message.message_id]:
					banned_users[last_welcome_message.message_id].append(user)
			elif (cas['ok']):
				update.chat_member.chat.kick_member(user.id)
				ban_reason[user.id] = "Combot Anti-Spam"
				if user not in banned_users[last_welcome_message.message_id]:
					banned_users[last_welcome_message.message_id].append(user)
			elif (re.search(r"[\u0600-\u06ff]|[\u0750-\u077f]|[\ufb50-\ufbc1]|[\ufbd3-\ufd3f]|[\ufd50-\ufd8f]|[\ufd92-\ufdc7]|[\ufe70-\ufefc]|[\uFDF0-\uFDFD]", user_display_name)):
				update.chat_member.chat.kick_member(user.id)
				ban_reason[user.id] = "арабская вязь в имени"
				if user not in banned_users[last_welcome_message.message_id]:
					banned_users[last_welcome_message.message_id].append(user)
			else:
				if user in accepted_users[last_welcome_message.message_id]:
					accepted_users[last_welcome_message.message_id].remove(user)
				if user not in pending_users[last_welcome_message.message_id]:
					pending_users[last_welcome_message.message_id].append(user)
				context.job_queue.run_once(ban_user, 120, context={'message': last_welcome_message, 'user': user}, name=f"ban_{user.id}")
			if last_welcome_message.message_id not in welcome_message_need_update:
				welcome_message_need_update.append(last_welcome_message.message_id)
		if ((update.chat_member.new_chat_member.status == "left") or (update.chat_member.new_chat_member.is_member == False) or (update.chat_member.new_chat_member.status == "kicked")) and (storage(file="pidor", var=str(user.id)) is not False):
			storage(file="pidor", var=str(user.id), val="remove")
		if (update.chat_member.old_chat_member.status == "administrator") and (update.chat_member.new_chat_member.status == "left"):
			update.chat_member.chat.send_message(f"🔐 [{user_display_name}](tg://user?id={user.id}) покинул чат и лишился админки.", parse_mode="Markdown")
		if (update.chat_member.old_chat_member.status == "member") and (update.chat_member.new_chat_member.status == "administrator"):
			update.chat_member.chat.send_message(f"🔐 [{user_display_name}](tg://user?id={user.id}) получил админку.", parse_mode="Markdown")
		if (update.chat_member.new_chat_member.status == "administrator") and (update.chat_member.old_chat_member.custom_title != update.chat_member.new_chat_member.custom_title):
			update.chat_member.chat.send_message(f"🔐 [{user_display_name}](tg://user?id={user.id}) получил статус: {update.chat_member.new_chat_member.custom_title}", parse_mode="Markdown")
	collect_user_data(user)

def callback_query(update: Update, context: CallbackContext) -> None:
	global accepted_users, pending_users, welcome_message_need_update, russianroulette, last_welcome_message
	if update.callback_query is not None:
		if update.callback_query.data[:7] == "accept_":
			if update.callback_query.data == f"accept_{last_welcome_message.message_id}_мандарин":
				if remove_job(f"ban_{update.callback_query.from_user.id}", context):
					update.effective_chat.restrict_member(update.callback_query.from_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True), until_date=int(time.time())+60)
					welcome_text = f"Добро пожаловать, {get_user_display_name(update.callback_query.from_user)}!\nТеперь у вас есть доступ к чату."
					update.callback_query.answer(welcome_text, show_alert=True)
					if update.callback_query.from_user in pending_users[update.callback_query.message.message_id]:
						pending_users[update.callback_query.message.message_id].remove(update.callback_query.from_user)
					if update.callback_query.from_user not in accepted_users[update.callback_query.message.message_id]:
						accepted_users[update.callback_query.message.message_id].append(update.callback_query.from_user)
					if update.callback_query.message.message_id not in welcome_message_need_update:
						welcome_message_need_update.append(update.callback_query.message.message_id)
				else:
					update.callback_query.answer(f"Ага, мандарин %)", show_alert=True)
			else:
				nopes = ["неа", "не", "нет", "не то", "не попал"]
				update.callback_query.answer(random.choice(nopes), show_alert=False)
		if update.callback_query.data[:16] == "russianroulette_":
			if update.callback_query.from_user.id == russianroulette['target_id']:
				if update.callback_query.data == "russianroulette_accept":
					remove_job("russianroulette_editMessage", context)
					game = True
					message_prefix = f"Дуэль! {russianroulette['user_display_name']} против {russianroulette['target_display_name']}:\n"
					russianroulette['message'].edit_text(f"{message_prefix}Заряжаю один патрон в револьвер и прокручиваю барабан.", parse_mode="Markdown", reply_markup=None)
					russianroulette_drum = 1
					russianroulette_bullet = random.randint(1, 6)
					time.sleep(4)
					russianroulette['message'].edit_text(f"{message_prefix}Кладу револьвер на стол и раскручиваю его.", parse_mode="Markdown")
					time.sleep(4)
					player = ['user_display_name', 'target_display_name']
					player = random.choice(player)
					player_id = 0
					if player == 'user_display_name':
						player_id = russianroulette['user_id']
						victim = 'target_display_name'
						victim_id = russianroulette['target_id']
					else:
						player_id = russianroulette['target_id']
						victim = 'user_display_name'
						victim_id = russianroulette['user_id']
					russianroulette['message'].edit_text(f"{message_prefix}Револьвер останавливается на {russianroulette[player]}, первый ход за ним.", parse_mode="Markdown")
					for i in range(1, 7):
						if game:
							time.sleep(3)
							player_member = update.effective_chat.get_member(player_id)
							victim_member = update.effective_chat.get_member(victim_id)
							success = [f"{russianroulette[player]} остаётся в живых. Хм... может порох отсырел?", "в воздухе повисла тишина.", f"{russianroulette[player]} сегодня заново родился.", f"{russianroulette[player]} остаётся в живых. Хм... я ведь зарядил его?", "прикольно, а давай проверим на ком-нибудь другом?"]
							fail = [f"мозги {russianroulette[player]} разлетелись по чату!", f"{russianroulette[player]} упал со стула и его кровь растеклась по месседжу.", f"{russianroulette[player]} замер и спустя секунду упал на стол.", f"пуля едва не задела кого-то из участников чата! А? Что? А, {russianroulette[player]} мёртв, да.", f"и в воздухе повисла тишина. Все начали оглядываться, когда {russianroulette[player]} уже был мёртв."]
							invincible = [f"пуля отскочила от головы {russianroulette[player]} и улетела в другой чат.", f"{russianroulette[player]} похмурил брови и отклеил расплющенную пулю со своей головы.", f"но ничего не произошло. {russianroulette[player]} взглянул на револьвер, он был неисправен.", f"пуля прошла навылет, но не оставила каких-либо следов на {russianroulette[player]}."]
							message_prefix = f"Дуэль! {russianroulette['user_display_name']} против {russianroulette['target_display_name']}, раунд {i}:\n{russianroulette[player]} берёт револьвер, приставляет его к голове и...\n"
							russianroulette['message'].edit_text(f"{message_prefix}", parse_mode="Markdown")
							time.sleep(3)
							if russianroulette_drum == russianroulette_bullet:
								game = False
								if (player_member.status in ['administrator', 'creator']) and (victim_member.status in ['administrator', 'creator']):
									russianroulette['message'].edit_text(f"{message_prefix}" + f"Пуля отскакивает от головы {russianroulette[player]} и летит в голову {russianroulette[victim]}.\n", parse_mode="Markdown")
									time.sleep(2)
									russianroulette['message'].edit_text(f"{message_prefix}" + f"Пуля отскакивает от головы {russianroulette[victim]} и летит в голову {russianroulette[player]}.\n", parse_mode="Markdown")
									time.sleep(2)
									russianroulette['message'].edit_text(f"{message_prefix}" + f"Пуля отскакивает от головы {russianroulette[player]} и летит в мою голову... блять.", parse_mode="Markdown")
									russianroulette['bot_is_dead'] = 1
									context.job_queue.run_once(resurrect_bot, 3600, context={'update': update}, name=f"russianroulette_ressurect_bot")
								elif (player_member.user.name in config.telegram_admins) and (victim_member.status not in ['administrator', 'creator']):
									message_prefix += f"😈 {russianroulette[player]} наводит револьвер на голову {russianroulette[victim]} и стреляет.\n"
									deathstreak = storage(file="russianroulette", var=str(victim_id)+"_loses")
									if deathstreak is False:
										storage(file="russianroulette", var=str(victim_id)+"_loses", val="1")
										deathstreak = 1
									else:
										deathstreak = str(int(deathstreak) + 1)
										storage(file="russianroulette", var=str(victim_id)+"_loses", val=deathstreak)
									context.job_queue.run_once(bot_mute, 1, context={'update': update, 'user_id': victim_id, 'until_date': (int(time.time())+600*int(deathstreak))}, name=f"russianroulette_mute")
									time.sleep(2)
									russianroulette['message'].edit_text(f"{message_prefix}" + f"Я хз как это объяснить, но {russianroulette[player]} победитель!\n{russianroulette[victim]} отправился на респавн на {deathstreak}0 минут.", parse_mode="Markdown")
								elif player_member.status == "administrator":
									text = "💥 " + random.choice(invincible) + "\n"
									russianroulette['message'].edit_text(f"{message_prefix}" + text, parse_mode="Markdown")
									time.sleep(2)
									russianroulette['message'].edit_text(f"{message_prefix}" + text + "Похоже, у нас ничья.", parse_mode="Markdown")
								else:
									text = "💥 " + random.choice(fail) + "\n"
									russianroulette['message'].edit_text(f"{message_prefix}" + text, parse_mode="Markdown")
									russianroulettestat = storage(file="russianroulette", var=str(player_id)+"_loses")
									if russianroulettestat is False:
										storage(file="russianroulette", var=str(player_id)+"_loses", val="1")
										russianroulettestat = 1
									else:
										russianroulettestat = str(int(russianroulettestat) + 1)
										storage(file="russianroulette", var=str(player_id)+"_loses", val=russianroulettestat)
									context.job_queue.run_once(bot_mute, 1, context={'update': update, 'user_id': player_id, 'until_date': (int(time.time())+600*int(russianroulettestat))}, name=f"russianroulette_mute")
									time.sleep(2)
									russianroulette['message'].edit_text(f"{message_prefix}" + text + "Победитель дуэли: " + russianroulette[victim] + ".\n" + russianroulette[player] + " отправился на респавн на " + russianroulettestat + "0 минут.", parse_mode="Markdown")
									russianroulettestat = storage(file="russianroulette", var=str(victim_id)+"_wins")
									if russianroulettestat is False:
										storage(file="russianroulette", var=str(victim_id)+"_wins", val="1")
									else:
										russianroulettestat = str(int(russianroulettestat) + 1)
										storage(file="russianroulette", var=str(victim_id)+"_wins", val=russianroulettestat)
							else:
								russianroulette_drum = russianroulette_drum + 1
								russianroulette['message'].edit_text(f"{message_prefix}"+"🍾 " + random.choice(success), parse_mode="Markdown")
							if player == 'user_display_name': 
								player = 'target_display_name'
								player_id = russianroulette['target_id']
								victim = 'user_display_name'
								victim_id = russianroulette['user_id']
							else:
								player = 'user_display_name'
								player_id = russianroulette['user_id']
								victim = 'target_display_name'
								victim_id = russianroulette['target_id']
					remove_job("clear_command_availability_russianroulette", context)
					context.job_queue.run_once(clear_command_availability, 1, context={'command': 'russianroulette'}, name="clear_command_availability_russianroulette")
				if update.callback_query.data == "russianroulette_deny":
					russianroulette['message'].edit_text(f"{russianroulette['target_display_name']} отказался от дуэли.", parse_mode="Markdown")
					remove_job("clear_command_availability_russianroulette", context)
					context.job_queue.run_once(clear_command_availability, 1, context={'command': 'russianroulette'}, name="clear_command_availability_russianroulette")
			else:
				nopes = ["неа", "не", "нет"]
				update.callback_query.answer(random.choice(nopes), show_alert=False)

def update_welcome_message(context: CallbackContext) -> None:
	global welcome_message_need_update
	for message_id in welcome_message_need_update:
		message_text = ""
		message_text_pending = ""
		amessage_text_pending = ""
		message_text_accepted = ""
		amessage_text_accepted = ""
		message_text_banned = ""
		amessage_text_banned = ""
		buttons = ["евдоким", "оладушек", "мандарин", "напердыш"]
		random.shuffle(buttons)
		keyboard = [
			[InlineKeyboardButton(buttons[0], callback_data=f"accept_{last_welcome_message.message_id}_{buttons[0]}"),InlineKeyboardButton(buttons[1], callback_data=f"accept_{last_welcome_message.message_id}_{buttons[1]}")],
			[InlineKeyboardButton(buttons[2], callback_data=f"accept_{last_welcome_message.message_id}_{buttons[2]}"),InlineKeyboardButton(buttons[3], callback_data=f"accept_{last_welcome_message.message_id}_{buttons[3]}")],
		]
		reply_markup = ""
		for user in pending_users[message_id]:
			message_text_pending += f"{amessage_text_pending}[{get_user_display_name(user)}](tg://user?id={user.id})"
			amessage_text_pending = ", "
		for user in accepted_users[message_id]:
			message_text_accepted += f"{amessage_text_accepted}[{get_user_display_name(user)}](tg://user?id={user.id})"
			amessage_text_accepted = ", "
		for user in banned_users[message_id]:
			message_text_banned += f"{amessage_text_banned}[{get_user_display_name(user)}](tg://user?id={user.id}) ({ban_reason[user.id]})"
			amessage_text_banned = ", "
		if message_text_pending != "":
			reply_markup = InlineKeyboardMarkup(keyboard)
			message_text += f"Добро пожаловать: {message_text_pending}!\nНажмите на мандарин, чтобы получить доступ в чат, иначе бан через 2 минуты.\n"
		if message_text_accepted != "":
			message_text += f"Новые подтвержденные пользователи: {message_text_accepted}"
		if message_text_banned != "":
			message_text += f"Заблокированные пользователи: {message_text_banned}"
		context.bot.edit_message_text(chat_id=config.telegram_chat, message_id=message_id, text=message_text, reply_markup=reply_markup, parse_mode="Markdown")
		if message_id in welcome_message_need_update:
			welcome_message_need_update.remove(message_id)
		time.sleep(5)

def ban_user(context: CallbackContext) -> None:
	global pending_users, banned_users, welcome_message_need_update
	user = context.job.context['user']
	message = context.job.context['message']
	message.chat.kick_member(user.id)
	ban_reason[user.id] = "не прошел проверку"
	if user in pending_users[message.message_id]:
		pending_users[message.message_id].remove(user)
	if user not in banned_users[message.message_id]:
		banned_users[message.message_id].append(user)
	if message.message_id not in welcome_message_need_update:
		welcome_message_need_update.append(message.message_id)

def remove_job(name: str, context: CallbackContext) -> None:
	current_jobs = context.job_queue.get_jobs_by_name(name)
	if not current_jobs:
		return False
	for job in current_jobs:
		job.schedule_removal()
	return True

def job_exist(name: str, context: CallbackContext) -> None:
	current_jobs = context.job_queue.get_jobs_by_name(name)
	if not current_jobs:
		return False
	else:
		return True

def releases_update(context: CallbackContext) -> None:
	ics = requests.get(config.ics_url, allow_redirects=True)
	cal = Timeline(Calendar(ics.text))
	game_list = ""
	agame_list = ""
	for game in cal.included(arrow.utcnow(), arrow.utcnow().shift(weeks=2)):
		game_list += agame_list + "*" + game.name + "* - " + game.begin.format('DD.MM.YYYY')
		agame_list = "\n"
	jsonFile = open(f"storage/releases.txt", "w")
	jsonFile.write(game_list)
	jsonFile.close()
	return "Обновление списка последних релизов завершено."

def zavtrastream_check(context: CallbackContext) -> None:
	search = requests.get(url=f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={config.youtube_channelid}&type=video&eventType=live&key={config.youtube_apikey}').json()
	if search['pageInfo']['totalResults'] != 0:
		title = search['items'][0]['snippet']['title']
		videoid = search['items'][0]['id']['videoId']
		thumbnail = f"https://i.ytimg.com/vi/{videoid}/maxresdefault_live.jpg"
		if videoid != storage(file="zavtrastream", var="videoid"):
			message = f'Стрим "{title}" начался.\nhttps://youtube.com/{config.youtube_channelname}/live'
			context.bot.send_photo(chat_id=config.telegram_stream_channel, photo=thumbnail, caption=message)
			storage(file="zavtrastream", var="videoid", val=videoid)
			storage(file="zavtrastream", var="last_check", val=datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S %d.%m.%Y'))
			return "Есть обновление, отправил сообщение в "+config.telegram_stream_channel
		else:
			storage(file="zavtrastream", var="last_check", val=datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S %d.%m.%Y'))
			return "Стрим онлайн."
	else:
		storage(file="zavtrastream", var="last_check", val=datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S %d.%m.%Y'))
		return "Стрим офлайн."

def storage(**args):
	if 'file' in args:
		if os.path.isfile(f"storage/{args['file']}.json"):
			jsonFile = open(f"storage/{args['file']}.json", "r")
			data = json.load(jsonFile)
			jsonFile.close()
			if 'val' in args:
				if args['val'] == "remove":
					if args['var'] in data:
						del data[args['var']]
					else:
						return False
				else:
					data[args['var']] = args['val']
				jsonFile = open(f"storage/{args['file']}.json", "w")
				jsonFile.write(json.dumps(data))
				jsonFile.close()
				return True
			elif 'var' in args:
				if args['var'] in data:
					return data[args['var']]
				else:
					return False
			else:
				return data
		else:
			return False


def resurrect_bot(context: CallbackContext) -> None:
	available['russianroulette'] = True
	russianroulette['bot_is_dead'] = 0

def clear_command_availability(context: CallbackContext) -> None:
	command = context.job.context['command']
	available[command] = True

def bot_sendMessage(context: CallbackContext) -> None:
	update = context.job.context['update']
	text = context.job.context['text']
	update.effective_chat.send_message(text, parse_mode="Markdown")

def bot_editMessage(context: CallbackContext) -> None:
	message = context.job.context['message']
	text = context.job.context['text']
	message.edit_text(text, parse_mode="Markdown", reply_markup=None)

def bot_removeMessage(context: CallbackContext) -> None:
	update = context.job.context['update']
	message = context.job.context['message']
	message.delete()

def remove_message(update: Update, context: CallbackContext) -> None:
	update.message.delete()

def bot_mute(context: CallbackContext) -> None:
	update = context.job.context['update']
	user_id = int(context.job.context['user_id'])
	until_date = int(context.job.context['until_date'])
	update.effective_chat.restrict_member(user_id, ChatPermissions(can_send_messages=False), until_date=until_date)

def pidor_reset(context: CallbackContext) -> None:
	storage(file="pidortoday", var="today", val="remove")
	return "Пидор сброшен!"

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

def commands(update: Update, context: CallbackContext) -> None:
	text = update.message.text.split(" ")
	command = text[0].split("/")[1].split("@")[0]
	command_list = [os.path.splitext(os.path.basename(x))[0] for x in glob.glob("commands/*")]
	if command in command_list:
		update.effective_chat.send_action("typing")
		user_display_name = update.effective_user.full_name
		logging.warning(f"User {update.effective_user.name} ({update.effective_user.id}) executed {command}: {update.message.text}")
		execfile(f"commands/{command}.py")
	else:
		logging.warning(f"User {update.effective_user.name} ({update.effective_user.id}) tried to execute unknown command {command}: {update.message.text}")

def error_handler(update: object, context: CallbackContext) -> None:
	logging.error(msg="Exception while handling an update:", exc_info=context.error)
	tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
	tb_string = ''.join(tb_list)
	update_str = update.to_dict() if isinstance(update, Update) else str(update)
	message = (
		f'An exception was raised while handling an update\n'
		f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
		'</pre>\n\n'
		f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
		f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
		f'<pre>{html.escape(tb_string)}</pre>'
	)
	context.bot.send_message(config.telegram_sysadmin, message, "HTML")

def main():
	updater = Updater(token=config.telegram_token, base_url=config.telegram_bot_api_url)
	updater.start_webhook(listen=config.telegram_webhook_listen, port=config.telegram_webhook_port, url_path="bot", webhook_url=f"http://{config.telegram_webhook_listen}:{config.telegram_webhook_port}/bot", allowed_updates=config.telegram_webhook_allowed_updates)
	updater.dispatcher.add_handler(MessageHandler(Filters.command & (Filters.chat(username=config.telegram_chat) | Filters.chat(username=config.telegram_admins) | Filters.chat(username=config.telegram_moders)), commands))
	updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members & Filters.chat(username=config.telegram_chat), remove_message))
	updater.dispatcher.add_handler(MessageHandler(Filters.chat(username=config.telegram_channel), repost_to_chat))
	updater.dispatcher.add_handler(ChatMemberHandler(chat_member_update, 0))
	updater.dispatcher.add_handler(CallbackQueryHandler(callback_query, run_async=True))
	updater.dispatcher.add_handler(MessageHandler(Filters.all & Filters.chat(username=config.telegram_chat), gather_data))
	updater.dispatcher.add_error_handler(error_handler)
	updater.job_queue.run_repeating(update_welcome_message, 5, context=updater, name="update_welcome_message_repeating")
	updater.job_queue.run_repeating(zavtrastream_check, 180, context=updater)
	updater.job_queue.run_daily(pidor_reset, datetime.time(0, 0, 0), context=updater)
	updater.job_queue.run_daily(releases_update, datetime.time(1, 0, 0), context=updater)
	updater.idle()
	db.close()

if __name__ == '__main__':
	main()