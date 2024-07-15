from bs4 import BeautifulSoup as bs
import requests as req
import re
import json

# Fetching data using BeautifulSoup
url = "https://www.golfshake.com/course/top100/uk/"
res = req.get(url)
soup= bs(res.text, "html.parser") 

list_posts = []

# Extracting title, link, ranking, rating, and image
for a, ranking, rating, img in zip(
    soup.select('td > h2 > a[href]'), 
    soup.select('.widetable-top100 .ranking'), 
    soup.select('.widetable-top100 span[style="display:block;text-align: center;"] b'),
    soup.select('.widetable-top100 img.lazyload')):

    # Get title and link
    title = a.get_text()
    link = 'https://www.golfshake.com/' + a['href']
    
    # Extract overall ranking, location, and price guide
    overall_ranking_Loc_Price = a.find_next('p', string=re.compile(r'Overall ranking:', re.IGNORECASE)).get_text()
    
    # Get address
    res_ = req.get(link)
    soup_ = bs(res_.text, "html.parser")
    div_address = soup_.find('span', itemprop='streetAddress')
    if div_address:
        for tag in div_address.find_all(['b']):
            tag.decompose()
        address = div_address.text.strip() if div_address else None


    # Extract latitude and longitude from Google Maps link
    div_lon_lat = soup_.find('div', itemprop='address')
    if div_lon_lat:
        div_lon_lat_a = div_lon_lat.find('a', href=True)
        if div_lon_lat_a:
            href_attr = div_lon_lat_a['href']
            match = re.search(r'lat=([-+]?\d*\.\d+|\d+)&lon=([-+]?\d*\.\d+|\d+)', href_attr)
            if match:
                lat = match.group(1)
                lon = match.group(2)

    # Find website link
    website = soup_.find('a', string="Website")
    website_link = website['href'] if website else None
                                         
    # Get rating if available
    rate = rating.get_text().split(': ')[1] if rating else None
    
    # Get golf shake ranking
    rank = ranking.get_text()

    # Extract image URL
    image_url = img['src'] if img else None

    # 提取電話號碼
    telephone_span = soup_.find('span', itemprop='telephone')
    if telephone_span:
        telephone = telephone_span.get_text()
    else:
        telephone = None

    
    # Append data to list_posts
    list_posts.append({
        'golf_shake_rank': rank,
        'title': title,
        'Address': address,
        'Location': overall_ranking_Loc_Price.split('|')[1].strip().replace('Location:', ''),
        'Price guide': overall_ranking_Loc_Price.split('|')[2].strip().replace('Price guide:', ''),
        'Rating': rate, 
        'Latitude': lat,
        'Longitude': lon,
        'link': link,
        'Image URL': image_url,
        'Tel': telephone,
        'Website': website_link,
    })

# Output each golf course's information
for obj in list_posts:
    print("Rank:", obj['golf_shake_rank'])
    print("Title:", obj['title'])
    print("Address:", obj['Address'])
    print("Location:", obj['Location'])
    print("Price guide:", obj['Price guide'])
    print("Rating:", obj['Rating'])
    print("Latitude:", obj['Latitude'])
    print("Longitude:", obj['Longitude'])
    print("Link:", obj['link'])
    print("Image URL:", obj['Image URL'])
    print("Telephone:", obj['Tel'])
    print("Website:", obj['Website'])
    print("=" * 50)

# Writing the extracted data into a JSON file
with open('591.json', 'w') as json_file:
    json.dump(list_posts, json_file, indent=4)
