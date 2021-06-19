member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if len(text) >= 2:
		update.message.delete()
		update.effective_chat.send_message(" ".join(text[1:]))
	else:
		update.message.reply_text("Укажите сообщение.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")