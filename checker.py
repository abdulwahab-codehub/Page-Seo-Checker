import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import csv

def extract_and_concatenate(soup, tag):
    return ', '.join([element.text.strip() for element in soup.find_all(tag)])

def analyze_url(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('title').text if soup.find('title') else 'No title'
    h1 = extract_and_concatenate(soup, 'h1')
    h2 = extract_and_concatenate(soup, 'h2')
    h3 = extract_and_concatenate(soup, 'h3')
    h4 = extract_and_concatenate(soup, 'h4')
    meta_desc = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'No meta description'
    text_content = ' '.join([p.text for p in soup.find_all('p')])
    blob = TextBlob(text_content)
    sentiment = blob.sentiment
    word_count = len(text_content.split())

    return {
        'URL': url,
        'Title': title,
        'H1': h1,
        'H2': h2,
        'H3': h3,
        'H4': h4,
        'Meta_Description': meta_desc,
        'Word_Count': word_count,
        'Sentiment': sentiment.polarity
    }

def export_to_csv(data_list, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header based on the first item's keys
        writer.writerow(data_list[0].keys())
        # Write the data
        for data in data_list:
            writer.writerow(data.values())

# List of URLs to analyze
urls = [
    'https://onlinecompass.live'
    # Add more URLs here
]

# Analyze each URL and store the results
results = [analyze_url(url) for url in urls]

# Export all results to CSV
export_to_csv(results)
