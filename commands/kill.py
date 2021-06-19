member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if (len(text) == 2) or (update.message.reply_to_message is not None):
		until_date = int(time.time())+3600
		if update.message.reply_to_message is not None:
			target_id = update.message.reply_to_message.from_user.id
			target_display_name = f"[{get_user_display_name(update.message.reply_to_message.from_user)}](tg://user?id={target_id})"
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
		if target_id != "":
			deathstreak = storage(file="russianroulette", var=str(target_id)+"_loses")
			if deathstreak is False:
				storage(file="russianroulette", var=str(target_id)+"_loses", val="1")
				deathstreak = 1
			else:
				deathstreak = str(int(deathstreak) + 1)
				storage(file="russianroulette", var=str(target_id)+"_loses", val=deathstreak)
			until_date = (int(time.time())+600*int(deathstreak))
		if (update.message.from_user.id == target_id):
			update.message.reply_photo("AgACAgIAAx0CRXO-MQACAp5ggFXJZlGYSFtV4Fb1aLALheWclgACKbIxGzc2AUjyhubHdWgXhiY0BaQuAAMBAAMCAANtAAO8MwACHgQ")
		elif update.effective_chat.restrict_member(target_id, ChatPermissions(can_send_messages=False), until_date=until_date):
			update.message.delete()
			update.effective_chat.send_message(f"💥 [{get_user_display_name(update.message.from_user)}](tg://user?id={update.message.from_user.id}) пристрелил {target_display_name}.\n{target_display_name} отправился на респавн на {deathstreak}0 минут.", parse_mode="Markdown")
		else:
			update.message.reply_text(f"Не удалось пристрелить {target_display_name}.", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <ID пользователя>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")