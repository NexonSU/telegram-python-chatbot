available[command] = False
year = datetime.datetime.now().year
pidors = storage(file="pidor")
get = storage(file="pidortoday", var="today")
if get is False:
	pidor = random.choice(list(pidors))
	pidor_id = str(pidor)
	try:
		pidor = update.effective_chat.get_member(pidor_id)
	except:
		update.message.reply_text(f"Я нашел пидора дня, но похоже, что [{pidors[pidor]}](tg://user?id={pidor}) вышел из этого чата (вот пидор!), так что попробуйте еще раз, пока я удаляю его из игры!", parse_mode="Markdown")
		storage(file="pidor", var=pidor_id, val="remove")
		context.job_queue.run_once(clear_command_availability, 6, context={'command': command})
		sys.exit()
	if pidor.status == "left":
		update.message.reply_text(f"Я нашел пидора дня, но [{get_user_display_name(pidor.user)}](tg://user?id={pidor.user.id}) вышел из этого чата (вот пидор!), так что попробуйте еще раз, пока я удаляю его из игры!", parse_mode="Markdown")
		storage(file="pidor", var=pidor_id, val="remove")
	elif pidor.status == "kicked":
		update.message.reply_text(f"Я нашел пидора дня, но [{get_user_display_name(pidor.user)}](tg://user?id={pidor.user.id}) был забанен в этом чате (получил пидор!), так что попробуйте еще раз, пока я удаляю его из игры!", parse_mode="Markdown")
		storage(file="pidor", var=pidor_id, val="remove")
	else:
		storage(file="pidortoday", var="today", val=str(pidor.user.id))
		pidorstat = storage(file=f"pidor_{year}", var=str(pidor.user.id))
		if pidorstat is False:
			storage(file=f"pidor_{year}", var=str(pidor.user.id), val="1")
		else:
			pidorstat = str(int(pidorstat) + 1)
			storage(file=f"pidor_{year}", var=str(pidor.user.id), val=pidorstat)
		pidor_link = f"[{get_user_display_name(pidor.user)}](tg://user?id={pidor.user.id})"
		first_message = ["Инициирую поиск пидора дня...", "Опять в эти ваши игрульки играете? Ну ладно...", "Woop-woop! That's the sound of da pidor-police!", "Система взломана. Нанесён урон. Запущено планирование контрмер.", "Сейчас поколдуем...", "Инициирую поиск пидора дня...", "Зачем вы меня разбудили...", "Кто сегодня счастливчик?"]
		second_message = ["Хм...", "Сканирую...", "Ведётся поиск в базе данных", "Сонно смотрит на бумаги", "(Ворчит) А могли бы на работе делом заниматься", "Военный спутник запущен, коды доступа внутри...", "Ну давай, посмотрим кто тут классный..."]
		third_message = ["Высокий приоритет мобильному юниту.", "Ох...", "Ого-го...", "Так, что тут у нас?", "В этом совершенно нет смысла...", "Что с нами стало...", "Тысяча чертей!", "Ведётся захват подозреваемого..."]
		fourth_message = ["Стоять! Не двигаться! Вы объявлены пидором дня, ", "Ого, вы посмотрите только! А пидор дня то - ", "Пидор дня обыкновенный, 1шт. - ", ".∧＿∧ \n( ･ω･｡)つ━☆・*。 \n⊂  ノ    ・゜+. \nしーＪ   °。+ *´¨) \n         .· ´¸.·*´¨) \n          (¸.·´ (¸.·'* ☆ ВЖУХ И ТЫ ПИДОР, ", "Ага! Поздравляю! Сегодня ты пидор - ", "Кажется, пидор дня - ", "Анализ завершен. Ты пидор, "]
		update.effective_chat.send_message(escape_markdown(random.choice(first_message)), parse_mode="Markdown")
		context.job_queue.run_once(bot_sendMessage, 2, context={'update': update, 'text': escape_markdown(random.choice(second_message))}, name=f"pidor_{update.message.chat.id}_2")
		context.job_queue.run_once(bot_sendMessage, 4, context={'update': update, 'text': escape_markdown(random.choice(third_message))}, name=f"pidor_{update.message.chat.id}_3")
		context.job_queue.run_once(bot_sendMessage, 6, context={'update': update, 'text': escape_markdown(random.choice(fourth_message)) + pidor_link}, name=f"pidor_{update.message.chat.id}_4")
else:
	update.message.reply_text(f"Согласно моей информации, по результатам сегодняшнего розыгрыша пидор дня - {pidors[get]}!")
context.job_queue.run_once(clear_command_availability, 6, context={'command': command})