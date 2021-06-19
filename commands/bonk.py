if update.message.reply_to_message is not None:
	update.message.delete()
	target_id = update.message.reply_to_message.message_id
	img = Image.open("storage/bonk.webp")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("/usr/share/fonts/google-droid/DroidSans-Bold.ttf", 20)
	if (update.effective_user.username is not None):
		user_display_name = "@" + update.effective_user.username
	draw.text((140, 290), user_display_name, (0, 0, 0), font=font, anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255))
	buffered = BytesIO()
	img.save(buffered, format="WEBP")
	update.effective_chat.send_sticker(sticker=buffered.getvalue(), reply_to_message_id=target_id)
else:
	update.message.reply_text(f"Просто отправь /{command} в ответ на чье-либо сообщение.")