member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	pidors = storage(file="pidor")
	if (text[1] == "list"):
		pidorlist = ""
		pidorlist_i = 0
		for pidor in pidors:
			pidorlist_i += 1
			pidorlist += f"{pidorlist_i}. [{pidors[pidor]}](tg://user?id={pidor}) - {pidor}\n"
			if(len(pidorlist) > 3900):
				update.message.reply_text(pidorlist, parse_mode="Markdown")
				pidorlist = ""
		update.message.reply_text(pidorlist, parse_mode="Markdown")
	if (text[1] == "del"):
		if len(text) == 3:
			if storage(file="pidor", var=str(text[2])) is not False:
				target_name = pidors[text[2]]
				if storage(file="pidor", var=str(text[2]), val="remove"):
					update.message.reply_text(f"[{target_name}](tg://user?id={text[2]}) удалён из игры Пидор Дня.", parse_mode="Markdown")
			else:
				update.message.reply_text(f"Данный ID отсутствует в базе.")
		if len(text) == 2:
			if update.message.reply_to_message is not None:
				target_id = update.message.reply_to_message.from_user.id
				target_name = pidors[str(target_id)]
				if storage(file="pidor", var=str(target_id)) is not False:
					if storage(file="pidor", var=str(target_id), val="remove"):
						update.message.reply_text(f"[{target_name}](tg://user?id={target_id}) удалён из игры Пидор Дня.", parse_mode="Markdown")
				else:
					update.message.reply_text(f"Данный пользователь отсутствует в базе.")
			else:
				update.message.reply_text(f"Пример использования:\n/{command} del <ID пользователя>\nИли просто отправьте /{command} del в ответ на чье-либо сообщение.")
else:
	update.message.reply_text(f"Данная команда предназначена только для администраторов или модераторов чата.")