import numpy as np
from bs4 import BeautifulSoup
import requests
import html2text
from termcolor import colored

TOP_URL = "http://mdrs.marssociety.org/previous-field-seasons/"

MAXDEPTH = 10

def wordfilter(word):
	keywords = ["season", "crew", "sol", "report", "summary"]
	for keyword in keywords:
		if keyword in word or keyword.capitalize() in word:
			return True

	return False

class webItem:
	def __init__(self, href, parent):
		self.href = href
		self.parent = parent
		self.children = []
		if self.parent is None:
			self.depth = 0
		else:
			self.depth = self.parent.depth + 1

	def checkIfLoop(self):
		parentNode = self.parent
		while parentNode is not None:
			if parentNode.href == self.href:
				return True
			parentNode = parentNode.parent

		return False

	def fetchSelfData(self):
		self.responseHTML = requests.get(self.href).text
		self.responseSoup = BeautifulSoup(self.responseHTML, 'html.parser')
		self.responseText = self.responseSoup.get_text()
		self.rawText = html2text.html2text(self.responseHTML)

	def searchForKeyword(self, keyword, pm = 20):
		l = len(keyword)
		if keyword in self.rawText:
			indices = [i for i in range(len(self.rawText)) if self.rawText[i : i + l] == keyword]
			for ind in indices:
				resultText = self.rawText[max(ind - pm, 0) : min(ind + pm, len(self.rawText))]
				resultText = resultText.replace(keyword, colored(keyword, "red"))
				print("\t" * self.depth + str(self.depth) + " < " + self.href + " > " + resultText.replace("\n", " "))
		for child in self.children:
			child.searchForKeyword(keyword, pm)

	def getChildren(self, output = True, filterfunc = lambda x: True, passfilter = True):
		if self.depth > MAXDEPTH:
			return

		if self.checkIfLoop():
			return

		if output:
			print("\t" * self.depth + "Fetching data for url\t <", self.href, ">")
		
		self.links = self.responseSoup.find_all('a')

		for link in self.links:
			if not filterfunc(link.text):
				continue

			href = link['href']

			if href == self.href:
				continue

			if href in self.href:
				continue

			if href[0] == "#":
				continue

			#if output:
				#print("\t" * (self.depth + 1) + "Fetching data for child\t <", href, ">")

			if not ("http://" in href or "https://" in href):
				href = self.parent.href + href

			item = webItem(href, self)
			self.children.append(item)
			item.fetchSelfData()

			if passfilter:
				item.getChildren(output, filterfunc, passfilter)
			else:
				item.getChildren(output)


DATABASE = webItem(TOP_URL, None)
DATABASE.fetchSelfData()
DATABASE.getChildren(filterfunc = wordfilter)

