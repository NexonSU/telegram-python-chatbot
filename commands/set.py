if len(text) >= 3:
	var = text[1].lower()
	if storage(file="gets", var=var, val=" ".join(text[2:])):
		update.message.reply_text(f"Гет {var} сохранён: " + storage(file="gets", var=var))
elif (update.message.reply_to_message is not None) and (len(text) == 2):
	var = text[1].lower()
	caption = ""
	if (update.message.reply_to_message.caption is not None):
		caption = "_caption_" + update.message.reply_to_message.caption
	if update.message.reply_to_message.animation:
		storage(file="gets", var=var, val=f"animation_{update.message.reply_to_message.animation.file_id}{caption}")
		update.message.reply_text(f"Гет {var} сохранён как гиф.")
	elif update.message.reply_to_message.audio:
		storage(file="gets", var=var, val=f"audio_{update.message.reply_to_message.audio.file_id}{caption}")
		update.message.reply_text(f"Гет {var} сохранён как аудио.")
	elif update.message.reply_to_message.photo:
		storage(file="gets", var=var, val=f"photo_{update.message.reply_to_message.photo[-1].file_id}{caption}")
		update.message.reply_text(f"Гет {var} сохранён как картинка.")
	elif update.message.reply_to_message.video:
		storage(file="gets", var=var, val=f"video_{update.message.reply_to_message.video.file_id}{caption}")
		update.message.reply_text(f"Гет {var} сохранён как видео.")
	elif update.message.reply_to_message.voice:
		storage(file="gets", var=var, val=f"voice_{update.message.reply_to_message.voice.file_id}{caption}")
		update.message.reply_text(f"Гет {var} сохранён как войс.")
	elif update.message.reply_to_message.document:
		storage(file="gets", var=var, val=f"document_{update.message.reply_to_message.document.file_id}{caption}")
		update.message.reply_text(f"Гет {var} сохранён как файл.")
	elif update.message.reply_to_message.text:
		storage(file="gets", var=var, val=update.message.reply_to_message.text)
		update.message.reply_text(f"Гет {var} сохранён: " + storage(file="gets", var=var))
	else:
		update.message.reply_text(f"Неудалось распознать файл в сообщении, возможно, он не поддерживается.")
else:
	update.message.reply_text(f"Пример использования:\n/{command} <гет> <значение>\nИли отправь в ответ на какое-либо сообщение /{command} <гет>")
if len(text) == 1:
	update.message.reply_text(f"Пример использования:\n/{command} <гет> <значение>\nИли отправь в ответ на какое-либо сообщение /{command} <гет>")