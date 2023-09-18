import requests
from bs4 import BeautifulSoup
import json
import os
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

def fetch_html(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {url}. Exiting...")
        return None
    return response.text

def extract_video_ids_from_html(html_content):  
    soup = BeautifulSoup(html_content, 'html.parser')
    video_elements = soup.find_all("a", class_="title", href=True)
    video_ids = [video_element["href"].split('/')[-1] for video_element in video_elements if "/user/profile/" in video_element["href"]]
    return video_ids

def extract_video_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find("title").text if soup.find("title") else "No title found"
    desc = soup.find("div", class_="desc").text if soup.find("div", class_="desc") else "No description found"
    
    # Extract video URL from the JavaScript object
    pattern = re.compile(r'masterUrl":"(http:\\u002F\\u002F[^"]+.mp4)"')
    match = pattern.search(html_content)
    video_url = match.group(1).replace('\\u002F', '/') if match else "No video URL found"

    # Extract image links
    image_links_pattern = re.compile(r'url":"(https:\\u002F\\u002Fsns-img[^"]+)"')
    image_links_matches = image_links_pattern.findall(html_content)
    image_links = [link.replace('\\u002F', '/') for link in image_links_matches]

    return {
        "title": title.strip(),
        "description": desc.strip(),
        "video_url": video_url,
        "image_links": image_links
    }

def main():
    print("Starting the program...")

    # Step 1: Fetch profile page HTML content
    main_url = "https://www.xiaohongshu.com/user/profile/6116981a000000000101ef05"
    html_content = fetch_html(main_url)
    if not html_content:
        print("Exiting the program due to an error.")
        return

    # Step 2: Extract video IDs directly from the fetched HTML content
    video_ids = extract_video_ids_from_html(html_content)
    print(f"Found {len(video_ids)} video IDs.")
    
    all_video_details = []

    # Step 3: Fetch video details for each video ID
    for vid in video_ids:
        video_url = f"https://www.xiaohongshu.com/explore/{vid}"
        video_html_content = fetch_html(video_url)
        details = extract_video_details(video_html_content)
        all_video_details.append(details)

    # Save all video details to a JSON file
    output_filename = "video_details.json"
    with open(output_filename, "w", encoding="utf-8") as outfile:
        json.dump(all_video_details, outfile, ensure_ascii=False, indent=4)
    
    print(f"Video details saved to {output_filename}.")

main()
