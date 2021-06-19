member = update.effective_chat.get_member(update.message.from_user.id)
if (member.can_restrict_members) or (member.status == "creator") or (member.user.name in config.telegram_admins) or (member.user.name in config.telegram_moders):
	if len(text) > 1:
		if text[1] in ["update_welcome_message", "zavtrastream_check", "pidor_reset", "releases_update", "raise_exception"]:
			if text[1] == "update_welcome_message":
				job = context.job_queue.run_once(update_welcome_message, 0, context=context, name=text[1]+"_from_"+str(update.message.from_user.username))
			if text[1] == "zavtrastream_check":
				job = context.job_queue.run_once(zavtrastream_check, 0, context=context, name=text[1]+"_from_"+str(update.message.from_user.username))
			if text[1] == "pidor_reset":
				job = context.job_queue.run_once(pidor_reset, 0, context=context, name=text[1]+"_from_"+str(update.message.from_user.username))
			if text[1] == "releases_update":
				job = context.job_queue.run_once(releases_update, 0, context=context, name=text[1]+"_from_"+str(update.message.from_user.username))
			if text[1] == "raise_exception":
				update.message.reply_text(update.message.frsom_user.username)
			if job.name is not None:
				update.message.reply_text(f"Задача {job.name} успешно запущена.")
			else:
				update.message.reply_text(f"Ошибка, смотрите логи.")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <имя> <параметры>")
else:
	update.message.reply_animation("CgACAgIAAx0CQvXPNQABHGrDYIBIvDLiVV6ZMPypWMi_NVDkoFQAAq4LAAIwqQlIQT82LRwIpmoeBA")