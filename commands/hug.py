if update.message.reply_to_message is not None:
	update.message.delete()
	target_id = update.message.reply_to_message.message_id
	hug = Image.open("storage/hug.webp")
	text_image = Image.new("RGBA", (512, 392))
	draw = ImageDraw.Draw(text_image)
	font = ImageFont.truetype("/usr/share/fonts/google-droid/DroidSans-Bold.ttf", 20)
	if (update.effective_user.username is not None):
		user_display_name = "@" + update.effective_user.username
	draw.text((362, 58), user_display_name, (0, 0, 0), font=font, anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255))
	image2paste = text_image.rotate(-15, expand=False)
	hug.paste(image2paste, (0, 0), image2paste)
	buffered = BytesIO()
	hug.save(buffered, format="WEBP")
	update.effective_chat.send_sticker(sticker=buffered.getvalue(), reply_to_message_id=target_id)
else:
	update.message.reply_text(f"Просто отправь /{command} в ответ на чье-либо сообщение.")