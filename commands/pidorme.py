alltime = 0
year = datetime.datetime.now().year
this_year = storage(file=f"pidor_{year}", var=str(update.message.from_user.id))
if this_year is False:
	this_year = 0
for file in glob.glob("storage/pidor_*.json"):
	alltime_year = file.split("storage/pidor_")[1].split(".json")[0]
	alltime_year = storage(file=f"pidor_{alltime_year}", var=str(update.message.from_user.id))
	if alltime_year is not False:
		alltime += int(alltime_year)
update.message.reply_text(f"В этом году вы были пидором дня — {this_year} раз!\nЗа всё время вы были пидором дня — {alltime} раз!")