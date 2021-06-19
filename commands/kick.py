member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if (len(text) == 2) or (update.message.reply_to_message is not None):
		if update.message.reply_to_message is not None:
			target_id = update.message.reply_to_message.from_user.id
			target_display_name = f"[{get_user_display_name(update.message.reply_to_message.from_user)}](tg://user?id={target_id})"
			if len(text) == 2:
				update.message.reply_text(f"Слишком много аргументов для кика по ответу на сообщение.", parse_mode="Markdown")
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
					update.message.reply_text(f"Я не знаю пользователя {target_display_name}.", parse_mode="Markdown")
					target_id = ""
		if (update.message.from_user.id == target_id):
			update.message.reply_photo("AgACAgIAAx0CRXO-MQACAp5ggFXJZlGYSFtV4Fb1aLALheWclgACKbIxGzc2AUjyhubHdWgXhiY0BaQuAAMBAAMCAANtAAO8MwACHgQ")
		elif update.effective_chat.kick_member(target_id, until_date=int(time.time())+30, revoke_messages=False):
			update.effective_chat.unban_member(target_id)
			update.message.reply_text(f"{target_display_name} удалён из чата.", parse_mode="Markdown")
		else:
			update.message.reply_text(f"Не удалось удалить {target_display_name} из чата.", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <ID пользователя>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")