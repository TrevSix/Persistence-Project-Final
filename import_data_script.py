import requests
import json
import os

def download_category(category_name, counter, directory, downloaded_pages):
    # Define the API endpoint to retrieve category members
    api_endpoint = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle={}&cmtype=page|subcat&cmlimit=max".format(category_name)

    # Send a request to the API endpoint and retrieve the category members
    response = requests.get(api_endpoint)
    data = json.loads(response.text)
    
    # Check if the 'query' key exists in the dictionary
    if 'query' in data:
        articles = data['query']['categorymembers']

        # Download each article
        for article in articles:
            if article['ns'] == 0: # If the member is a page (article)
                pageid = article['pageid']
                if pageid not in downloaded_pages: # Skip downloading if already downloaded
                    title = article['title']
                    print("Downloading article: {}".format(title))
                    url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&pageids={}".format(pageid)
                    article_data = requests.get(url)
                    article_text = article_data.json()['query']['pages'][str(pageid)]['revisions'][0]['*']

                    # Write the article to a file
                    filename = os.path.join(directory, "{}.txt".format(counter))
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(article_text)
                    counter += 1
                    downloaded_pages.add(pageid)

            else: # If the member is a subcategory
                subcategory_name = article['title'].replace("Category:", "Category%3A")
                print("Entering subcategory: {}".format(subcategory_name))
                counter = download_category(subcategory_name, counter, directory, downloaded_pages)

    else:
        print("Failed to retrieve category members for category: {}".format(category_name))

    return counter

# Define the category to download
category_name = "Category:Technology"

# Download all articles in the category and its subcategories
counter = 0
directory = 'C:/A_Neumont Work/Q6/PRO335 Persistence Project/Persistence Project Py Scripts/'
downloaded_pages = set()
counter = download_category(category_name, counter, directory, downloaded_pages)

print("Done!")
