if len(text) > 1:
	var = text[1].lower()
	get = storage(file="gets", var=var)
	if get is not False:
		reply_to_message_id = None
		if update.message.reply_to_message:
			reply_to_message_id = update.message.reply_to_message.message_id
		caption = None
		if len(get.split("_caption_")) == 2:
			caption = get.split("_caption_")[1]
		if get[:10] == "animation_":
			update.message.reply_animation(get.split("animation_")[1].split("_caption_")[0], caption=caption, reply_to_message_id=reply_to_message_id)
		elif get[:6] == "audio_":
			update.message.reply_audio(get.split("audio_")[1].split("_caption_")[0], caption=caption, reply_to_message_id=reply_to_message_id)
		elif get[:6] == "photo_":
			update.message.reply_photo(get.split("photo_")[1].split("_caption_")[0], caption=caption, reply_to_message_id=reply_to_message_id)
		elif get[:6] == "video_":
			update.message.reply_video(get.split("video_")[1].split("_caption_")[0], caption=caption, reply_to_message_id=reply_to_message_id)
		elif get[:6] == "voice_":
			update.message.reply_voice(get.split("voice_")[1].split("_caption_")[0], caption=caption, reply_to_message_id=reply_to_message_id)
		elif get[:9] == "document_":
			update.message.reply_document(get.split("document_")[1].split("_caption_")[0], caption=caption, reply_to_message_id=reply_to_message_id)
		else:
			update.message.reply_text(get, reply_to_message_id=reply_to_message_id)
	else:
		update.message.reply_text(f"Гет {text[1]} не найден.")
else:
	update.message.reply_text(f"Пример использования:\n/{command} <гет>")