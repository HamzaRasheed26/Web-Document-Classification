import csv
import requests
from bs4 import BeautifulSoup
import json

# Function to scrape blog titles and links


def scrape_blogs():

    blogs_data = []  # List to store scraped datals
    urls = ["https://www.iflscience.com/nature/latest",
            "https://www.remedieslabs.com/blog/page/2/"]
    for url in urls:
        response = requests.get(url)  # Send a GET request to the URL
        response.encoding = 'utf-8'  # Set the encoding explicitly
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all articles containing blog posts
        articles = soup.find_all("div", class_="card-content--body--title")

        # Iterate over each article
        for article in articles:
            # Find the h3 tag inside each title_div
            title_tag = article.find("h3")

            # Check if title_tag is not None before accessing its attributes
            if title_tag is not None:
                title = title_tag.text.strip()

                # Find the parent <a> tag to get the href attribute
                link = title_tag.find_parent("a")

                # Check if link_tag is not None before accessing its attributes
                if link is not None and "href" in link.attrs:
                    link = link["href"]
                    # Construct the full link
                    link = "https://www.iflscience.com" + link

            # Append data to list
            blogs_data.append({"label": "Science/Education",
                               "title": title, "link": link})

    return blogs_data

# Function to save data to CSV file

# Function to save data to JSON file


def save_to_json(data):
    with open("articles/science_articles.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Function to save data to CSV file


def save_title_link_to_csv(data):
    with open("articles/science_articles.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["label", "title", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for blog in data:
            writer.writerow(blog)

# Function to scrape the entire blog content and calculate word count


def scrape_blog_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the main content of the blog
    main_content = soup.find("div", class_="article-content")

    # Check if main_content is None
    if main_content is None:
        return None, 0  # Return None and word count 0

    # Extract all paragraphs
    paragraphs = main_content.find_all("p")

    # Concatenate paragraphs to form the blog body
    body = " ".join([p.get_text(strip=True) for p in paragraphs])

    # Calculate word count
    word_count = len(body.split())

    return body, word_count

# Function to scrape blogs from the CSV file and save them with the body and word count


def scrape_and_save_blogs(csv_file):
    with open(csv_file, "r", newline="", encoding="latin-1") as csvfile:
        reader = csv.DictReader(csvfile)
        blogs_data = []
        for row in reader:
            blog_url = row["link"]
            print("Scraping", blog_url)
            body, word_count = scrape_blog_content(blog_url)
            row["body"] = body
            row["word_count"] = word_count
            blogs_data.append(row)

    # Save data to a new CSV file
    output_csv_file = "articles/science_articles.csv"
    fieldnames = ["label", "title", "link", "body", "word_count"]
    with open(output_csv_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(blogs_data)

    save_to_json(blogs_data)
    print("Data has been scraped and saved to csv and json format")


# Main function
if __name__ == "__main__":
    blogs_data = scrape_blogs()
    save_title_link_to_csv(blogs_data)
    print("Titles and links have been scraped and saved to csv file")
    csv_file = "articles/science_articles.csv"
    scrape_and_save_blogs(csv_file)
