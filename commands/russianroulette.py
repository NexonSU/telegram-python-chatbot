global russianroulette
if russianroulette['bot_is_dead']:
	update.message.reply_text("Я не могу провести игру, т.к. я немного умер. Зайдите позже.")
else:
	if (available[command]):
		if update.message.reply_to_message:
			if update.message.from_user.id == update.message.reply_to_message.from_user.id:
				update.message.reply_text(f"Как ты себе это представляешь? Нет, нельзя вызвать на дуэль самого себя.")
				context.job_queue.run_once(clear_command_availability, 1, context={'command': command}, name="clear_command_availability_"+command)
			else:
				user_check = update.effective_chat.get_member(update.message.reply_to_message.from_user.id)
				if user_check.user.is_bot:
					update.message.reply_text(f"Бота нельзя вызвать на дуэль.")
					context.job_queue.run_once(clear_command_availability, 1, context={'command': command}, name="clear_command_availability_"+command)
				else:
					if (user_check.status == "restricted") and (user_check.can_send_messages is False):
						update.message.reply_text(f"Нельзя вызвать на дуэль мертвеца.")
						context.job_queue.run_once(clear_command_availability, 1, context={'command': command}, name="clear_command_availability_"+command)
					else:
						update.message.delete()
						available[command] = False
						russianroulette['user_id'] = update.message.from_user.id
						russianroulette['user_display_name'] = f"[{user_display_name}](tg://user?id={update.message.from_user.id})"
						russianroulette['target_id'] = update.message.reply_to_message.from_user.id
						russianroulette['target_display_name'] = f"[{get_user_display_name(update.message.reply_to_message.from_user)}](tg://user?id={update.message.reply_to_message.from_user.id})"
						keyboard = [
							[InlineKeyboardButton("Принять вызов", callback_data="russianroulette_accept"),InlineKeyboardButton("Бежать с позором", callback_data="russianroulette_deny")]
						]
						reply_markup = InlineKeyboardMarkup(keyboard)
						russianroulette['message'] = update.effective_chat.send_message(f"{russianroulette['target_display_name']}! {russianroulette['user_display_name']} вызывает вас на дуэль!", parse_mode="Markdown", reply_markup=reply_markup)
						context.job_queue.run_once(clear_command_availability, 60, context={'command': command}, name="clear_command_availability_"+command)
						context.job_queue.run_once(bot_editMessage, 60, context={'message': russianroulette['message'], 'text': f"{russianroulette['target_display_name']} не принял вызов."}, name="russianroulette_editMessage")
		else:
			update.message.reply_text(f"Чтобы вызвать кого-либо на дуэль, отправьте /{command} в ответ на чье-либо сообщение.")
			context.job_queue.run_once(clear_command_availability, 1, context={'command': command}, name="clear_command_availability_"+command)
	else:
		update.message.reply_text(f"Команда /{command} [занята](https://t.me/zavtrachat/{russianroulette['message'].message_id}). Попробуйте позже.", parse_mode="Markdown", disable_web_page_preview=True)