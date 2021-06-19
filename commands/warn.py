member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if (len(text) == 2) or (update.message.reply_to_message is not None):
		if update.message.reply_to_message is not None:
			target_id = update.message.reply_to_message.from_user.id
			target_display_name = f"[{get_user_display_name(update.message.reply_to_message.from_user)}](tg://user?id={target_id})"
			if len(text) == 2:
				update.message.reply_text(f"Слишком много аргументов для предупреждения по ответу на сообщение.", parse_mode="Markdown")
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
		else:
			cur_warns = storage(file="warns", var=str(target_id))
			if cur_warns is False:
				storage(file="warns", var=str(target_id), val="1")
				update.effective_chat.send_message(f"{target_display_name}! Вы получили предупреждение. При получении 3 предупреждений, вы будете исключены из чата.", parse_mode="Markdown")
			elif cur_warns == "1":
				storage(file="warns", var=str(target_id), val="2")
				update.effective_chat.send_message(f"{target_display_name}! Это ваше второе предупреждение. При получении 3 предупреждений, вы будете исключены из чата.", parse_mode="Markdown")
			else:
				storage(file="warns", var=str(target_id), val="remove")
				update.effective_chat.kick_member(target_id, until_date=int(time.time())+86400, revoke_messages=False)
				update.effective_chat.send_message(f"{target_display_name} забанен на сутки, т.к. получил 3 предупреждения.", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <ID пользователя>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")