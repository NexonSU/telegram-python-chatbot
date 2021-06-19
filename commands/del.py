if len(text) > 1:
	var = text[1].lower()
	if storage(file="gets", var=var, val="remove"):
		update.message.reply_text(f"Гет {var} удалён.")
else:
	update.message.reply_text(f"Пример использования:\n/{command} <гет>")