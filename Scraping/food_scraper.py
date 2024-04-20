import requests
from bs4 import BeautifulSoup
import os
import json
import csv

# Function to scrape data from a given URL
def scrape_data(url):
    article = {}
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_content = soup.find('article', class_='article-content')
        if article_content:
            article['title'] = article_content.find('div', class_='assetTitle').get_text().replace('\n', '')
            body = article_content.find('div', class_='article-body')
            paras = body.find_all('div', class_='customRTE smartbody-core section')
            article['body'] = ' '.join([p.get_text() for p in paras]).replace('\n', '')
            article['words_count'] = len(article['body'].split())
        return article
    except Exception as e:
        print(f"Error scraping data from {url}: {e}")
        return None

# Function to scrape links from a given URL
def scrape_articles_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find('section', class_='o-ListArticle')
        links = ["https:" + a['href'] for a in articles.find_all('a', href=True)]
        return links
    except Exception as e:
        print(f"Error scraping links from {url}: {e}")
        return None

# Function to save scraped data (dictionary) to a file as JSON format
def save_to_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

# Function to process links
def process_links(articles_links):
    links = []
    for i in range(0,len(articles_links),2):
        if articles_links[i] == "https:#" or articles_links[i].startswith("https://www.foodnetwork.com/healthy/articles/p"):
            break
        links.append(articles_links[i])
    return links

# Main function to scrape articles
def scrape_articles(url_base, pages, min_articles):
    articles_data = []
    articles_count = 0
    for i in range(1, pages + 1):
        url = f"{url_base}/p/{i}"
        print(url)
        articles_links = scrape_articles_links(url)
        links = process_links(articles_links)
        for link in links:
            data = scrape_data(link)
            if data and data.get('words_count', 0) > 500:
                articles_data.append({'index': articles_count + 1, 'label': 'Food', **data})
                articles_count += 1
                if articles_count >= min_articles:
                    return articles_data
    return articles_data

# Main function
def main():
    food_url = 'https://www.foodnetwork.com/healthy/articles'
    pages = 5  # Number of pages to scrape
    min_articles = 15  # Minimum number of articles to scrape
    articles_data = scrape_articles(food_url, pages, min_articles)
    os.makedirs("articles", exist_ok=True)
    output_file = 'articles/food_articles.json'
    save_to_file(articles_data, output_file)

     # Save to CSV file
    output_file = 'articles/food_articles.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'body', 'words_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles_data:
            writer.writerow({'title': article['title'], 'body': article['body'], 'words_count': article['words_count']})

if __name__ == "__main__":
    main()
