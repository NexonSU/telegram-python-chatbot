if storage(file="pidor", var=str(update.message.from_user.id)) is not False:
	update.message.reply_text("Эй, ты уже в игре!")
else:
	if storage(file="pidor", var=str(update.message.from_user.id), val=user_display_name) is not False:
		update.message.reply_text("OK! Ты теперь участвуешь в игре \"Пидор Дня\"")
	else:
		update.message.reply_text("Ошибка регистрации участника. Свяжитесь с @NexonSU")