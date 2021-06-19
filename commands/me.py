if len(text) >= 2:
	update.message.delete()
	message = escape_markdown(" ".join(text[1:]))
	update.effective_chat.send_message(f"`{user_display_name} {message}`", parse_mode="Markdown")
else:
	update.message.reply_text(f"Пример использования:\n/{command} написал /me в чат.")