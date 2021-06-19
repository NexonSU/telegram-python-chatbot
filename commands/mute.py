member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if (len(text) == 2) or (len(text) == 3) or (update.message.reply_to_message is not None):
		until_date = 0
		if update.message.reply_to_message is not None:
			target_id = update.message.reply_to_message.from_user.id
			target_display_name = f"[{get_user_display_name(update.message.reply_to_message.from_user)}](tg://user?id={target_id})"
			if len(text) == 2:
				if text[1].isdigit():
					until_date = int(text[1])
				else:
					update.message.reply_text(f"Для мьюта по ответу на сообщение, требуется время в секундах, а не `{text[1]}`", parse_mode="Markdown")
					target_id = ""
			if (len(text) == 3):
				update.message.reply_text(f"Слишком много аргументов для мьюта по ответу на сообщение.", parse_mode="Markdown")
				target_id = ""
		else:
			target_id = text[1]
			target_display_name = target_id
			if target_id.isdigit():
				target_display_name = f"[Пользователь](tg://user?id={target_id})"
			elif target_id[0] == "@":
				target_id = target_id.split("@")[1]
				target_id = db.execute(f"SELECT * FROM users WHERE username='{target_id}';").fetchone()
				if target_id is not None:
					target_display_name = f"[{target_id[3]}](tg://user?id={target_id[0]})"
					target_id = target_id[0]
				else:
					target_id = ""
					update.message.reply_text(f"Я не знаю пользователя {target_display_name}.", parse_mode="Markdown")
					target_id = ""
			if len(text) == 3:
				until_date = int(text[2])
		if (until_date > 0) and (until_date < 30):
			until_date = 30
		if (update.message.from_user.id == target_id):
			update.message.reply_photo("AgACAgIAAx0CRXO-MQACAp5ggFXJZlGYSFtV4Fb1aLALheWclgACKbIxGzc2AUjyhubHdWgXhiY0BaQuAAMBAAMCAANtAAO8MwACHgQ")
		elif update.effective_chat.restrict_member(target_id, ChatPermissions(can_send_messages=False), until_date=int(time.time())+until_date):
			until_date_text = ""
			if until_date != 0:
				until_date_delta = str(datetime.timedelta(seconds=until_date)).split(" days, ")
				if len(until_date_delta) == 2:
					until_date_delta_days = until_date_delta[0]
					until_date_delta = until_date_delta[1].split(":")
				else:
					until_date_delta_days = 0
					until_date_delta = until_date_delta[0].split(":")
				if int(until_date_delta_days) != 0:
					until_date_text += " "
					until_date_text += str(int(until_date_delta_days))
					if str(int(until_date_delta_days))[-1] in ["0", "5", "6", "7", "8", "9"]:
						until_date_text += " дней"
					elif str(int(until_date_delta_days))[-1] in ["2", "3", "4"]:
						until_date_text += " дня"
					else:
						until_date_text += " день"
				if int(until_date_delta[0]) != 0:
					until_date_text += " "
					until_date_text += str(int(until_date_delta[0]))
					if str(int(until_date_delta[0]))[-1] in ["0", "5", "6", "7", "8", "9"]:
						until_date_text += " часов"
					elif str(int(until_date_delta[0]))[-1] in ["2", "3", "4"]:
						until_date_text += " часа"
					else:
						until_date_text += " час"
				if int(until_date_delta[1]) != 0:
					until_date_text += " "
					until_date_text += str(int(until_date_delta[1]))
					if str(int(until_date_delta[1]))[-1] in ["0", "5", "6", "7", "8", "9"]:
						until_date_text += " минут"
					elif str(int(until_date_delta[1]))[-1] in ["2", "3", "4"]:
						until_date_text += " минуты"
					else:
						until_date_text += " минуту"
				if int(until_date_delta[2]) != 0:
					until_date_text += " "
					until_date_text += str(int(until_date_delta[2]))
					if str(int(until_date_delta[2]))[-1] in ["0", "5", "6", "7", "8", "9"]:
						until_date_text += " секунд"
					elif str(int(until_date_delta[2]))[-1] in ["2", "3", "4"]:
						until_date_text += " секунды"
					else:
						until_date_text += " секунду"
			update.message.reply_text(f"{target_display_name} больше не может отправлять сообщения{until_date_text}.", parse_mode="Markdown")
		else:
			update.message.reply_text(f"Не удалось ограничить {target_display_name}.", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <ID пользователя> <время в секундах>\nИли просто отправьте /{command} <время в секундах> в ответ на чье-либо сообщение.\nЕсли не указать время, то будет считаться, что ограничение навсегда.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")