import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QTextBrowser
from PySide6.QtCore import Qt
import webbrowser
import json



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Content Aggregator")
        self.resize(1200,800)

        self.main_layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels("Articles")
        self.tree.setColumnCount(1) 
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.main_layout.addWidget(self.tree, 1) 

        with open('articles.json', 'r') as json_file:
            self.articles = json.load(json_file)
        
        self.load_data()

        # Add QTextBrowser to display HTML content
        self.html_viewer = QTextBrowser()
        self.html_viewer.setOpenExternalLinks(True) 
        self.main_layout.addWidget(self.html_viewer, 2) 

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        sources = set(article['source'] for article in self.articles) 
        source_items = {source: QTreeWidgetItem(self.tree, [source]) for source in sources}

        for article in self.articles:
            article_item = QTreeWidgetItem(source_items[article['source']])
            article_item.setText(0, article['title'])
            article_item.setToolTip(0, article['link']) 
            article_item.setData(0, Qt.UserRole, article['link'])
            article_item.setText(1, article['description'])

        self.tree.expandAll() 
        self.tree.resizeColumnToContents(0)  

    def on_item_clicked(self, item, column):
        article_link = item.data(0, Qt.UserRole)
        if article_link:
            
            article = next((article for article in self.articles if article['link'] == article_link), None)
            if article:
                # Display the HTML content in the QTextBrowser
                self.html_viewer.setHtml(article['description'])  # Use the article's HTML content where present
            else:
                webbrowser.open(article_link)  # Fallback to opening the link in a web browser if not found in the list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
