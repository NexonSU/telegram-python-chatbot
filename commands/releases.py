game_listFile = open(f"storage/releases.txt", "r")
game_list = game_listFile.read()
game_listFile.close()
update.message.reply_text(game_list, parse_mode="Markdown")