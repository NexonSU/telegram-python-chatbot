member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if update.message.reply_to_message is not None:
		target_id = update.message.reply_to_message.from_user.id
		update.message.reply_text(target_id)
	else:
		update.message.reply_text(f"Пример использования: просто отправь /{command} в ответ на чье-либо сообщение.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")