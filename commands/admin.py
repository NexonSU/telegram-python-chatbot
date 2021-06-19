get = storage(file="gets", var="admin")
if get is not False:
	update.message.reply_text(get)
else:
	update.message.reply_text(f"Гет admin не найден.")