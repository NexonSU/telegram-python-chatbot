pidors = storage(file="pidor")
year = datetime.datetime.now().year
if len(text) == 2:
	if text[1].isdigit():
		statsyear = str(int(text[1]))
		if statsyear == "2077":
			update.message.reply_video("BAACAgIAAx0CRXO-MQADWWB4LQABzrOqWPkq-JXIi4TIixY4dwACPw4AArBgwUt5sRu-_fDR5x4E")
		else:
			pidors_year = storage(file=f"pidor_{statsyear}")
			if pidors_year is not False:
				pidorstats = f"Топ-10 пидоров за {statsyear} год:\n\n"
				pidors_year = sorted(pidors_year.items(), key=lambda x: x[1], reverse=True)
				for i in range(1, 11):
					pidorstats += f"{i}. {pidors[pidors_year[i-1][0]]} — {pidors_year[i-1][1]} раз(а)\n"
				pidorstats += "\nВсего участников — " + str(len(pidors))
				update.message.reply_text(pidorstats)
			else:
				update.message.reply_text(f"Статистики за {statsyear} год нет.")
	else:
		update.message.reply_text(f"Пример использования:\n/{command} <год>")
else:
	pidorstats = "Топ-10 пидоров за текущий год:\n\n"
	pidors_year = storage(file=f"pidor_{year}")
	pidors_year = sorted(pidors_year.items(), key=lambda x: x[1], reverse=True)
	for i in range(1, 10):
		pidorstats += f"{i}. {pidors[pidors_year[i-1][0]]} — {pidors_year[i-1][1]} раз(а)\n"
	pidorstats += "\nВсего участников — " + str(len(pidors))
	update.message.reply_text(pidorstats)