member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if update.message.reply_to_message is not None:
		update_str = update.to_dict() if isinstance(update, Update) else str(update)
		message = (
			f'<pre>{html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>'
		)
		update.message.reply_text(text=message, parse_mode="HTML")
	else:
		update.message.reply_text("Укажите сообщение для вывода подробностей.")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")