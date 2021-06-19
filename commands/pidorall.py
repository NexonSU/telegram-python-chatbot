pidors = storage(file="pidor")
pidorarray = {}
for file in glob.glob("storage/pidor_*.json"):
	with open(file, "rb") as infile:
		pidorsfile = json.load(infile)
		for key in pidorsfile:
			if key in pidorarray:
				pidorarray[key] = int(pidorarray[key]) + int(pidorsfile[key])
			else:
				pidorarray[key] = int(pidorsfile[key])
pidorstats = "Топ-10 пидоров за всё время:\n\n"
pidorarray = sorted(pidorarray.items(), key=lambda x: x[1], reverse=True)
for i in range(1, 10):
	pidorstats += f"{i}. {pidors[pidorarray[i-1][0]]} — {pidorarray[i-1][1]} раз(а)\n"
pidorstats += "\nВсего участников — " + str(len(pidors))
update.message.reply_text(pidorstats)