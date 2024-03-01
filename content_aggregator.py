import feedparser
import json

# List of RSS feeds with their source names
feeds = [
    {"name": "Article Source", "url": "rss_feed_url"},
]

# Initialize a list to hold all articles from all sources
all_articles = []

for feed in feeds:
    # Parse the RSS feed
    parsed_feed = feedparser.parse(feed["url"])
    
    for entry in parsed_feed.entries:
        article = {
            "source": feed["name"],
            "title": entry.title,
            "description": entry.description,
            "link": entry.link,
            "published": entry.published 
        }
        all_articles.append(article)

# Convert the list of articles to JSON format
articles_json = json.dumps(all_articles, indent=4)

with open('articles.json', 'w') as json_file:
    json_file.write(articles_json)
