action = "дал леща"
member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	action = "дал отцовского леща"
if len(text) == 1:
	if update.message.reply_to_message is not None:
		update.message.delete()
		target_id = update.message.reply_to_message.from_user.id
		target = get_user_display_name(update.message.reply_to_message.from_user)
		update.effective_chat.send_message(f"\\* *{user_display_name}* {action} [{target}](tg://user?id={target_id})", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <@юзер>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")
elif len(text) == 2:
	if text[1].startswith('@'):
		update.message.delete()
		update.effective_chat.send_message(f"\\* *{user_display_name}* {action} {escape_markdown(text[1])}", parse_mode="Markdown")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <@юзер>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")
else:
	update.message.reply_text(f"Пример использования:\n/{command} <@юзер>\nИли просто отправьте /{command} в ответ на чье-либо сообщение.")