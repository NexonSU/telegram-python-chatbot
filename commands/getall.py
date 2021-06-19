getall = "Доступные геты: "
akey = ""
for key in storage(file="gets"):
	getall += akey
	getall += key
	akey = ", "
update.message.reply_text(getall)