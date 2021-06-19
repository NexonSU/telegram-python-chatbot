member = update.effective_chat.get_member(update.message.from_user.id)
if (member.status == "administrator") or (member.status == "creator"):
	if len(text) > 1:
		context.bot.setChatTitle(update.effective_chat.id, "Zavtrachat | " + " ".join(text[2:]))
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <новая тема чата>")
else:
	update.message.reply_text("Данная команда предназначена только для участников чата с звёздочкой.")