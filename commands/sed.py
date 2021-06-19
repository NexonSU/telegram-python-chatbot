if (update.message.reply_to_message is not None) and (len(text) > 1):
	target_id = update.message.reply_to_message.message_id
	text = " ".join(text[1:])
	text = text.split("/")
	old = text[1]
	new = text[2]
	update.effective_chat.send_message(re.sub(r'%s' % old, new, update.message.reply_to_message.text), reply_to_message_id=target_id)
else:
	update.message.reply_text(f"Пример использования:\n/{command} <патерн вида s/foo/bar/> в ответ на сообщение.")