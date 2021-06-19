member = update.effective_chat.get_member(update.message.from_user.id)
update.message.delete()
if (member.status == "member"):
	deathstreak = storage(file="russianroulette", var=str(update.message.from_user.id)+"_loses")
	if deathstreak is False:
		storage(file="russianroulette", var=str(update.message.from_user.id)+"_loses", val="1")
		deathstreak = 1
	else:
		deathstreak = str(int(deathstreak) + 1)
		storage(file="russianroulette", var=str(update.message.from_user.id)+"_loses", val=deathstreak)
	until_date = (int(time.time())+600*int(deathstreak))
	update.effective_chat.restrict_member(update.message.from_user.id, ChatPermissions(can_send_messages=False), until_date=until_date)
	update.effective_chat.send_message(f"`💥 {user_display_name} выбрал лёгкий путь.\nРеспавн через {deathstreak}0 минут.`", parse_mode="Markdown")
else:
	update.effective_chat.send_message(f"`👻 {user_display_name} возродился у костра.`", parse_mode="Markdown")