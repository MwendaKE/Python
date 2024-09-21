import sys
import qtawesome as qta

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLineEdit, QDesktopWidget, QDialog, 
	QLabel, QHBoxLayout, QHBoxLayout, QApplication, QListView, QPushButton, QLabel, QFormLayout, QMessageBox, 
	QTextBrowser, QFileDialog)

from PyQt5.QtGui import QIcon, QFont, QColor

from PyQt5.QtCore import (Qt, QAbstractListModel, QSize, QRunnable, QThreadPool, QObject, pyqtSignal, 
	pyqtSlot, QSortFilterProxyModel)

# Function to fetch news: Returns news as a list of tuples

style = """
		QLineEdit {
			color: orange;
			border: 1px solid rgba(255, 165, 0, 0.2);
			padding: 2px;
			border-radius: 3px;
		}

		QListView {
			padding: 0 10px;
			border: 1px solid rgba(255, 165, 0, 0.2);
			border-radius: 3px;
		}

		QListView::item:selected {
			background: rgba(255, 165, 0, 0.2);
			color: tomato;
		}

		QPushButton {
			border: 1px solid rgba(255, 165, 0, 0.2);
			border-radius: 3px;
			padding: 2px;
		}

		QPushButton::hover {
            background: rgba(255, 99, 71, 0.1);
        }

		QPushButton:pressed {
            background: rgba(255, 165, 0, 0.2);
        }

        QPushButton::disabled {
        	border: 1px solid gray;
        }

		QTextBrowser {
			padding: 5px;
			border: 1px solid rgba(255, 165, 0, 0.1);
		}

		"""

def fetchNationNews():
	'''Scrap News from Nation News website'''

	from bs4 import BeautifulSoup
	from requests import get

	url = "https://nation.africa"

	headlines =[]

	soup = BeautifulSoup(get(url).text, 'html5lib')

	top_stories = soup.find_all("li", class_="headline-teasers_item")
	bold_headlines = soup.find_all("a", class_="teaser-image-large")
	regular_articles = soup.find_all("a", class_="article-collection-teaser")
		
	for story in top_stories:
		heading = story.find("h3").get_text().strip()
		link = url + story.find("a").get('href')
		try:
			date = story.find("span", class_="date").get_text().strip()

		except:
			date = "00:00:00"

		if heading:
			if "PRIME" in heading:
				heading = heading.split("PRIME")[1].strip()
				
			article = (heading, link, date, "Nation", "")

			headlines.append(article)

	for headline in bold_headlines:
		heading = headline.find("h3").get_text().strip()
		link = url + headline.get('href')
		try:
			date = story.find("span", class_="date").get_text().strip()

		except:
			date = "00:00:00"

		if heading:
			if "PRIME" in heading:
				heading = heading.split("PRIME")[1].strip()
				
			article = (heading, link, date, "Nation", "")

			headlines.append(article)

	for headline in regular_articles:
		heading = headline.find("h3").get_text().strip()
		link = url + headline.get('href')
		try:
			date = headline.find("span", class_="date").get_text().strip()

		except:
			date = "00:00:00"

		if heading:
			if "PRIME" in heading:
				heading = heading.split("PRIME")[1].strip()
				
			article = (heading, link, date, "Nation", "")

			headlines.append(article)

	return headlines

def searchNationNews(word):
	'''Scrap News from Nation News website'''

	from re import search
	from bs4 import BeautifulSoup
	from requests import get

	results = []

	url = "https://nation.africa/service/search/kenya/290754?query={0}&docType=&channelId=&sortByDate=false".format(word)

	soup = BeautifulSoup(get(url).text, 'html5lib')

	try:
		results_count = search("\d+", soup.find("p", class_="search-suggestions-results").get_text())
		pages = int(int(results_count.group())/10)

	except:
		pages = 0

	news_containers = soup.find_all("li", class_="search-result")

	for item in news_containers:
		text = item.find("a").find("h3").get_text()
		anchor = "https://nation.africa" + item.find("a").get("href")

		if (text and anchor) and not (text == None or text == "None"):
			if "PRIME" in text:
				text = text.split("PRIME")[1].strip()

			else:
				text = text.strip()
				
			results.append((text, anchor, f"{word}", "Nation", ""))

	if pages:
		for num in range(pages):
			num = num+1
			url = "https://nation.africa/service/search/kenya/290754?pageNum={0}&query={1}".format(num, word)

			soup = BeautifulSoup(get(url).text, 'html5lib')

			news_containers = soup.find_all("li", class_="search-result")

			for item in news_containers:
				text = item.find("a").find("h3").get_text()
				anchor = "https://nation.africa" + item.find("a").get("href")

				if text and anchor:
					if "PRIME" in text:
						text = text.split("PRIME")[1].strip()

					else:
						text = text.strip()

					results.append((text, anchor, f"{word}", "Nation", ""))

	return results

def fetchBBCNews():
	'''Scrap News from BBC News website'''

	from bs4 import BeautifulSoup

	from requests import get

	url = "https://www.bbc.com"

	stories = []

	soup = BeautifulSoup(get(url).text, 'html5lib')

	top_stories = soup.find_all("h3", class_="media__title")
	reel_stories = soup.find_all("a", class_="reel__link")
	italized_stories = soup.find_all("a", class_="top-list-item__link")

	for elem in top_stories:
		headline = elem.find("a", class_="media__link").get_text()
		link = elem.find("a", class_="media__link").get("href")
		info = elem.find_parent("div", class_="media__content").find("p", class_="media__summary")

		if headline and not (headline == None or headline == "None"):
			headline = headline.strip()
			if not link.startswith("https://"):
				link = url + link

			if info and not (info == None or info == "None"):
				info = info.get_text().strip()

			stories.append((headline, link, "", "BBC", info))

	for elem in reel_stories:
		headline = elem.get_text()
		link = elem.get("href")

		if headline and not (headline == None or headline == "None"):
			headline = headline.strip()
			if not link.startswith("https://"):
				link = url + link

			stories.append((headline, link, "", "BBC", ""))

	for elem in italized_stories:
		headline = elem.get_text()
		link = elem.get("href")

		if headline and not (headline == None or headline == "None"):
			headline = headline.strip()
			if not link.startswith("https://"):
				link = url + link

			stories.append((headline, link, "", "BBC", ""))

	return stories

def fetchNBCNews():
	'''Scrap News from NBC News website'''

	from requests import get
	from bs4 import BeautifulSoup

	url = "https://www.nbcnews.com"

	results = []

	soup = BeautifulSoup(get(url).text, 'html5lib')

	top_articles = soup.find_all("h3", class_="bacon-cards-twobyone__header")
	top_stories = soup.find_all("h3", class_="pancake__headline")
	top_paras = soup.find_all("div", class_="alacarte__text-wrapper")

	for story in top_stories:
		headline = story.find("a")
		link = story.find("a").get("href")

		if headline and not (headline == None or headline == "None"):
			headline = headline.get_text().strip()
			if not link.startswith("https://"):
				link = url + link

			results.append((headline, link, "", "NBC", ""))

	for article in top_articles:
		headline = article.find("a").get_text()
		link = article.find("a").get("href")

		if headline and not (headline == None or headline == "None"):
			headline = headline.strip()
			if not link.startswith("https://"):
				link = url + link

			results.append((headline, link, "", "NBC", ""))

	for para in top_paras:
		headline = para.find("h2", class_="alacarte__headline")
		link = headline.find_parent("a").get("href")

		if headline and not (headline == None or headline == "None"):
			headline = headline.get_text().strip()
			if not link.startswith("https://"):
				link = url + link

			results.append((headline, link, "", "NBC", ""))

	return results

def fetchTheStarNews():
	'''Scrap News from 'The Star' News website'''

	from requests import get

	from bs4 import BeautifulSoup

	url = "https://www.the-star.co.ke"

	results = []

	soup = BeautifulSoup(get(url).text, 'html5lib')

	top_stories = soup.find_all("div", class_="article-content")

	for story in top_stories:
		headline = story.find("a").find("h3").get_text()
		anchor = url + story.find("a").get("href")
		time = story.find("div", class_="article-footer").find("span", class_="article-published")
		info = story.find("p", class_="article-synopsis")

		if headline and not (headline == None or headline == "None"):
			headline = headline.strip()

			if time and not (time == None or time == "None"):
				time = time.get_text().strip()

			if info and not (info == None or info == "None"):
				info = info.get_text().strip()


		results.append((headline, anchor, time, "The Star", info))

	return results

def fetchCBSNews():
	'''Scrap News from CBS News website'''

	from requests import get

	from bs4 import BeautifulSoup

	url = "https://www.cbsnews.com"

	results = []

	soup = BeautifulSoup(get(url).text, 'html5lib')

	top_headings = soup.find_all("article", class_="item")

	print(len(top_headings))

	for item in top_headings:
		headline = item.find("h4").get_text()
		link = item.find("a").get("href")
		date = item.find("li", class_="item__date").get_text()
		info = item.find("p", class_="item__dek").get_text()

		if headline and not (headline == None or headline == "None"):
			headline = headline.strip()
			if not link.startswith("https://"):
				link = url + link

			if date and not (date == None or date == "None"):
				date = date.strip()

			if info and not (date == None or date == "None"):
				info = info.strip()

			results.append((headline, link, date, "CBS", info))

	return results


class WorkerSignals(QObject):
	'''Defines the signals available from a running worker thread.'''

	finished = pyqtSignal()
	error = pyqtSignal(str)
	data = pyqtSignal(list)


class NewsWorker(QRunnable):
	'''Worker thread: Handles application signals and prevents it from crashing
	   when performing more than one task. 
	'''

	def __init__(self, fn, *args, **kwargs):
		super(NewsWorker, self).__init__()
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()

	@pyqtSlot()
	def run(self):
		'''Initializes the runner function'''

		try:
			headlines = self.fn(*self.args, **self.kwargs)
		except Exception as err:
			self.signals.error.emit(str(err))
		else:
			self.signals.data.emit(headlines) # Return the result of processing
		finally:
			self.signals.finished.emit() # Processing finished. Or done signal


class NewsReaderDlg(QDialog):
	'''News dialog: Opens when you double click an item in the ListView'''

	def __init__(self, headline, link, date, source, subtitle, parent=None):
		super(NewsReaderDlg, self).__init__(parent)
		self.headline = headline
		self.link = link
		self.date = date
		self.source = source
		self.subtitle = subtitle

		self.threadpool = QThreadPool()

		self.setWindowTitle("NewsCate - Read News")
		self.setStyleSheet(style)
		self.setMinimumSize(600, 400)

		self.newsContainer = QTextBrowser()
		self.newsContainer.setAcceptRichText(True)
		self.newsContainer.setOpenExternalLinks(False)

		closeBtn = QPushButton(QIcon(qta.icon('mdi.window-close', color="orange")), "Close")
		closeBtn.clicked.connect(self.close)

		btnsLayout = QHBoxLayout()
		btnsLayout.addStretch()
		btnsLayout.addWidget(closeBtn)
		btnsLayout.addStretch()

		layout = QVBoxLayout()
		layout.addWidget(self.newsContainer)
		layout.addLayout(btnsLayout)

		self.setLayout(layout)

		self.newsContainer.append(f'<h1 style="color:orange;">{self.headline}</h1>')

		if self.date:
			self.newsContainer.append(f'<h2 style="color:tomato;">{self.date}</h2>')

		self.getNews()

	def processNews(self):
		from bs4 import BeautifulSoup
		from requests import get

		soup = BeautifulSoup(get(self.link).text, 'html5lib')

		content = []

		if self.source == "Nation":
			paragraphs = soup.find_all("div", class_="paragraph-wrapper")

			for elem in paragraphs:
				paragraph = elem.find("p")

				if paragraph and not (paragraph == None or paragraph == "None"):
					content.append(paragraph.get_text().strip())

				else:
					continue

		else:
			paragraphs = soup.find_all("p")

			for paragraph in paragraphs:
				if paragraph and not (paragraph == None or paragraph == "None"):
					content.append(paragraph.get_text().strip())

				else:
					continue

		return content

	def getNews(self):
		worker = NewsWorker(self.processNews)
		worker.signals.data.connect(self.readNews)
		worker.signals.error.connect(self.alertError)

		self.threadpool.start(worker)

	def readNews(self, news):
		for paragraph in news:
			self.newsContainer.append(paragraph)

	def alertError(self, error):
		QMessageBox.warning(self, "NewsCate - Read News", error)


class NewsDataModel(QAbstractListModel):
	'''The data model of the main Application'''

	def __init__(self, data=[], *args, **kwargs):
		super(NewsDataModel, self).__init__(*args, **kwargs)
		self.data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			heading, _, date, source, _ = self.data[index.row()]

			if not date or date == None or date == "None":
				return f"{heading}"

			return f"{heading} ({date})"

		if role == Qt.DecorationRole:
			if self.data[index.row()][2].startswith("Search result for:"):
				return qta.icon('mdi.search-web', color="orange")

			return qta.icon('fa.newspaper-o', color="orange")

		if role == Qt.ToolTipRole:
			if self.data[index.row()][4]:
				return self.data[index.row()][4]

			return self.data[index.row()][3]

	def rowCount(self, index):
		return len(self.data)


class NewsCate(QWidget):
	'''The main application class.'''

	def __init__(self):
		'''Application contructor'''

		super(NewsCate, self).__init__()# Constructor of the Base class (QWidget)

		self.setWindowTitle("NewsCate")
		self.setStyleSheet(style)
		self.setMinimumSize(1100, 600)
		self.setWindowIcon(QIcon(qta.icon('mdi.newspaper-variant-multiple', color="orange")))

		# Basic declarations

		self.model = NewsDataModel()

		self.newsType = ""

		self.threadpool = QThreadPool()

		# WIDGETS AND DATA

		self.searchLineEdit = QLineEdit()
		self.searchLineEdit.setPlaceholderText('Search anything. e.g. murder, to get all murder stories.')

		self.searchBtn = QPushButton(QIcon(qta.icon('mdi.search-web', color="orange")), "")
		self.searchBtn.setIconSize(QSize(25, 25))
		self.searchBtn.setToolTip("Start Searching...")
		self.searchBtn.clicked.connect(self.getNationSearchResults)

		# Buttons #LEFT

		self.bbcNewsBtn = QPushButton(QIcon(qta.icon('mdi.monitor-eye', color="orange")), "BBC")
		self.bbcNewsBtn.setToolTip("British Broadcasting Corporation News")
		self.bbcNewsBtn.setStyleSheet("text-align: left;")
		self.bbcNewsBtn.clicked.connect(self.getBBCNews)

		self.nationNewsBtn = QPushButton(QIcon(qta.icon('mdi.monitor-eye', color="orange")), "Nation")
		self.nationNewsBtn.setToolTip("Nation (KE) News")
		self.nationNewsBtn.setStyleSheet("text-align: left;")
		self.nationNewsBtn.clicked.connect(self.getNationNews)

		self.nbcNewsBtn = QPushButton(QIcon(qta.icon('mdi.monitor-eye', color="orange")), "NBC")
		self.nbcNewsBtn.setToolTip("National Broadcasting Company News")
		self.nbcNewsBtn.setStyleSheet("text-align: left;")
		self.nbcNewsBtn.clicked.connect(self.getNBCNews)

		self.cbsNewsBtn = QPushButton(QIcon(qta.icon('mdi.monitor-eye', color="orange")), "CBS")
		self.cbsNewsBtn.setToolTip("Columbia Broadcasting System")
		self.cbsNewsBtn.setStyleSheet("text-align: left;")
		self.cbsNewsBtn.clicked.connect(self.getCBSNews)

		self.starNewsBtn = QPushButton(QIcon(qta.icon('mdi.monitor-eye', color="orange")), "Star")
		self.starNewsBtn.setToolTip("The Star (KE) News")
		self.starNewsBtn.setStyleSheet("text-align: left;")
		self.starNewsBtn.clicked.connect(self.getTheStarNews)
		
		# Setting the model to the view (MVC)

		self.listView = QListView()
		self.listView.setFont(QFont("monaco",13))
		self.listView.doubleClicked.connect(self.itemDoubleClicked)
		self.getNationNews()

		# Buttons #RIGHT

		self.sortBtn = QPushButton(QIcon(qta.icon('mdi.sort-alphabetical-variant', color="orange")), "")
		self.sortBtn.setIconSize(QSize(25, 25))
		self.sortBtn.setCheckable(True)
		self.sortBtn.setToolTip("Sort")
		self.sortBtn.clicked.connect(self.sortData)

		self.refreshBtn = QPushButton(QIcon(qta.icon('mdi.refresh', color="orange")), "")
		self.refreshBtn.setIconSize(QSize(25, 25))
		self.refreshBtn.setToolTip("Refresh")
		self.refreshBtn.clicked.connect(self.refreshData)

		self.exportBtn = QPushButton(QIcon(qta.icon('mdi.export', color="orange")), "")
		self.exportBtn.setIconSize(QSize(25, 25))
		self.exportBtn.setToolTip("Export")
		self.exportBtn.clicked.connect(self.exportData)

		self.importBtn = QPushButton(QIcon(qta.icon('mdi.import', color="orange")), "")
		self.importBtn.setIconSize(QSize(25, 25))
		self.importBtn.setToolTip("Import")
		self.importBtn.clicked.connect(self.importDataFile)

		self.clearBtn = QPushButton(QIcon(qta.icon('mdi.monitor-clean', color="orange")), "")
		self.clearBtn.setIconSize(QSize(25, 25))
		self.clearBtn.setToolTip("Clean")
		self.clearBtn.clicked.connect(self.clearWindow)

		self.infoBtn = QPushButton(QIcon(qta.icon('mdi.information-outline', color="orange")), "")
		self.infoBtn.setIconSize(QSize(25, 25))
		self.infoBtn.setToolTip("About")
		self.infoBtn.clicked.connect(self.showAppInformation)

		self.exitBtn = QPushButton(QIcon(qta.icon('mdi.close-thick', color="orange")), "")
		self.exitBtn.setIconSize(QSize(25, 25))
		self.exitBtn.setToolTip("Exit")
		self.exitBtn.clicked.connect(self.close)

		# ARRANGING WIDGETS

		# Search Layout (LineEdit and Search btn)

		topSearchLayout = QHBoxLayout()
		topSearchLayout.addWidget(self.searchLineEdit)
		topSearchLayout.addWidget(self.searchBtn)

		# Left navigation btn layout

		leftPaneLayout = QVBoxLayout()
		leftPaneLayout.addWidget(self.bbcNewsBtn)
		leftPaneLayout.addWidget(self.cbsNewsBtn)
		leftPaneLayout.addWidget(self.nationNewsBtn)
		leftPaneLayout.addWidget(self.nbcNewsBtn)
		leftPaneLayout.addWidget(self.starNewsBtn)
		leftPaneLayout.addStretch()

		# Right navigation btn layout

		rightLayout = QVBoxLayout()
		rightLayout.addWidget(self.sortBtn)
		rightLayout.addWidget(self.refreshBtn)
		rightLayout.addWidget(self.exportBtn)
		rightLayout.addWidget(self.importBtn)
		rightLayout.addWidget(self.clearBtn)
		rightLayout.addWidget(self.infoBtn)
		rightLayout.addStretch()
		rightLayout.addWidget(self.exitBtn)

		# Horizontal layout (Joins Left Nav, the listview and Right Nav)

		middleLayout = QHBoxLayout()
		middleLayout.addLayout(leftPaneLayout)
		middleLayout.addWidget(self.listView)
		middleLayout.addLayout(rightLayout)

		# RENDERING WIDGETS TO MAIN LAYOUT 

		# Main layout (Joins all layouts)

		mainLayout = QVBoxLayout()
		mainLayout.addLayout(topSearchLayout)
		mainLayout.addLayout(middleLayout)

		self.setLayout(mainLayout)

		self.centerApp()

	def clearWindow(self):
		self.searchLineEdit.clear()
		self.model = NewsDataModel()
		self.getNationNews()

	def centerApp(self):
		geometry = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		geometry.moveCenter(center)
		self.move(geometry.topLeft())

	def sortData(self):
		proxymodel = QSortFilterProxyModel()
		proxymodel.setSourceModel(self.model)
		self.listView.setModel(proxymodel)

		if self.sortBtn.isChecked():
			proxymodel.sort(0)
		else:
			proxymodel.sort(0,Qt.DescendingOrder)

		self.model.layoutChanged.emit()

	def exportData(self):
		from json import dump
		from time import time, strftime

		if self.newsType == "":
			return

		export_file = f"./NewsCate/NewsCate-{self.newsType}-ExportFile-{strftime('%d%m%y-%H%M')}.json"

		with open(export_file, "w") as js:
			dump(self.model.data, js)

		QMessageBox.information(self, "NewsCate - Export Data", f"Data exported successfully to '{export_file}' file.")

	def importExternalData(self):
		from json import load
		from random import choice
		from os import listdir
		from os.path import basename

		try:
			import_file = choice([f"./NewsCate/{file}" for file in listdir("./NewsCate") if file.startswith("NewsCate-") and file.endswith(".json")])

		except:
			QMessageBox.warning(self, "NewsCate - Import File", "Cannot import data: No NewsCate file found in the current App directory.")
			return

		try:
			with open(import_file, 'r') as js:
				self.model.data = load(js)

		except Exception as err:
			QMessageBox.warning(self, "NewsCate - Import File", str(err))

		self.setWindowTitle(f"NewsCate - Offline Data [{basename(import_file)}]")

		self.listView.setModel(self.model)

	def importDataFile(self):
		import os
		from json import load

		file, ok = QFileDialog.getOpenFileName(parent=self, 
			caption="Select Import File",
			directory=os.getcwd(),
			filter='JSON File (*.json)'
			)

		if file:
			with open(file, 'r') as js:
				self.model.data = load(js)

		else:
			return

		self.setWindowTitle(f"NewsCate - Offline Data [{os.path.basename(file)}]")

		self.listView.setModel(self.model)

	def refreshData(self):
		if self.newsType == "NBC":
			self.getNBCNews()

		elif self.newsType == "BBC":
			self.getBBCNews()

		elif self.newsType == "THE-STAR":
			self.getTheStarNews()

		elif self.newsType == "CBS":
			self.getCBSNews()

		elif self.newsType == "NATION":
			self.getNationNews()

		elif self.newsType == "Imported":
			QMessageBox.warning(self, "Refresh Data", "Imported/Offline data is not refreshable.")

		else:
			self.importExternalData()

	def itemDoubleClicked(self):
		indexes = self.listView.selectedIndexes()
		index = indexes[0]
		row = index.row()
		heading, link, date, source, subtitle = self.model.data[row]

		dlg = NewsReaderDlg(heading, link, date, source, subtitle, parent=self)
		dlg.exec_()

	def getNationNews(self):
		self.newsType = "NATION"

		worker = NewsWorker(fetchNationNews)
		worker.signals.data.connect(self.showGeneralNews)
		worker.signals.error.connect(self.alert)

		self.threadpool.start(worker)

		self.setWindowTitle("NewsCate - Nation News")

	def getBBCNews(self):
		self.newsType = "BBC"

		worker = NewsWorker(fetchBBCNews)
		worker.signals.data.connect(self.showGeneralNews)
		worker.signals.error.connect(self.alert)

		self.threadpool.start(worker)

		self.setWindowTitle("NewsCate - BBC News")

	def getTheStarNews(self):
		self.newsType = "THE-STAR"

		worker = NewsWorker(fetchTheStarNews)
		worker.signals.data.connect(self.showGeneralNews)
		worker.signals.error.connect(self.alert)

		self.threadpool.start(worker)

		self.setWindowTitle("NewsCate - The Star News")

	def getNBCNews(self):
		self.newsType = "NBC"

		worker = NewsWorker(fetchNBCNews)
		worker.signals.data.connect(self.showGeneralNews)
		worker.signals.error.connect(self.alert)

		self.threadpool.start(worker)

		self.setWindowTitle("NewsCate - NBC News")

	def getCBSNews(self):
		self.newsType = "CBS"

		worker = NewsWorker(fetchCBSNews)
		worker.signals.data.connect(self.showGeneralNews)
		worker.signals.error.connect(self.alert)

		self.threadpool.start(worker)

		self.setWindowTitle("NewsCate - CBS News")

	def getNationSearchResults(self):
		query = self.searchLineEdit.text().strip()

		self.newsType = "NationSearch"

		if not query:
			return

		worker = NewsWorker(searchNationNews, query)
		worker.signals.data.connect(self.showGeneralNews)
		worker.signals.error.connect(self.alert)

		self.threadpool.start(worker)

		self.setWindowTitle(f"NewsCate - Search results for '{query}'")

	def showGeneralNews(self, headlines):
		self.model = NewsDataModel(headlines)
		self.listView.setModel(self.model)

	def alert(self, error):
		QMessageBox.warning(self, "Error Alert - NewsCate", error)

		self.importExternalData()

		self.newsType = "Imported"

	def closeEvent(self, event):
		from time import strftime
		from json import dump

		if not self.newsType == "Imported" and not len(self.model.data) < 5:
			export_file = f"./NewsCate/NewsCate-{self.newsType}-ExportFile-{strftime('%d%m%y-%H%M')}.json"

			with open(export_file, "w") as js:
				dump(self.model.data, js)

	def showAppInformation(self):
		QMessageBox.about(self, "NewsCate App", 
									  """
									  <p><h1><font color=tomato>NewsCate V1.0</font></h1><br/>
									  NewsCate helps you to read media stories/articles from
									  the top broadcasting networks in the world.</p>

									  <p>Most importantly, it gives you the power to search 
									  anything that has ever been published if it already exists 
									  on the internet. This is the greatest feature of this App.</p>

									  <p>NewsCate is written by Erick M.NJ, Phone: +254799678038, Email:
									  ericknjagi85@gmail.com.</p>
									  """
								)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = NewsCate()
	window.show()
	sys.exit(app.exec_())