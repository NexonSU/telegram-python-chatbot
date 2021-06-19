member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if (len(text) == 2) or (update.message.reply_to_message is not None):
		if update.message.reply_to_message is not None:
			target_id = update.message.reply_to_message.from_user.id
			target_display_name = f"[{get_user_display_name(update.message.reply_to_message.from_user)}](tg://user?id={target_id})"
			if len(text) == 2:
				update.message.reply_text(f"Слишком много аргументов для анмьюта по ответу на сообщение.", parse_mode="Markdown")
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
		if update.effective_chat.restrict_member(target_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True), until_date=int(time.time())+30):
			update.message.reply_text(f"{target_display_name} снова может отправлять сообщения в чат.", parse_mode="Markdown")
		else:
			update.message.reply_text(f"Не удалось снять ограничения с {target_display_name}.", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <ID пользователя>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")