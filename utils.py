URL_ESCAPE_MASK = '\033]8;{};{}\033\\{}\033]8;;\033\\'

def defaultWordFilter(word):
	keywords = ["season", "crew", "sol", "report", "summary"]
	for keyword in keywords:
		if keyword in word or keyword.capitalize() in word:
			return True

	return False

def urlFormatted(text, url):
	return URL_ESCAPE_MASK.format('', url, text)