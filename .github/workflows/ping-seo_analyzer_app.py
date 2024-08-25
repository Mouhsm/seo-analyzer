import requests

# List of URLs to ping
urls = [
    "https://seo-analyzer-qz23.onrender.com/"  # Only this URL
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for url in urls:
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f'Successfully pinged {url}')
        else:
            print(f'Failed to ping {url}, status code: {response.status_code}')
    except Exception as e:
        print(f'Error pinging {url}: {e}')
