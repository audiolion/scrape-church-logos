from bs4 import BeautifulSoup
import crayons
import requests

urls = [
    'https://www.sermoncentral.com/content/Top-100-Largest-Churches',
    'https://www.sermoncentral.com/content/Top-100-Largest-Churches2',
    'https://www.sermoncentral.com/content/Top-100-Largest-Churches3',
    'https://www.sermoncentral.com/content/Top-100-Largest-Churches4',
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    anchors = soup.find_all('a')
    websites = [anchor.get('href') for anchor in anchors if anchor.contents[0] == 'Website']

    for website in websites:
        website_name = website.split('://')[-1:][0]
        try:
            res = requests.get(website)
        except:
            print('{} {}'.format(
                crayons.red('Could not reach url:'),
                website)
            )
            continue
        res_soup = BeautifulSoup(res.text, 'html.parser')
        icon_link = res_soup.find('link', rel='shortcut icon')
        if icon_link is None:
            icon_link = res_soup.find('link', rel='icon')
        if icon_link is None:
            print('{} {}'.format(
                crayons.red('Could not find icon for website:'),
                website_name)
            )
            continue
        if 'http' in icon_link.get('href'):
            icon_url = icon_link.get('href')
        else:
            if website[-1::] == '/':
                icon_url = f'{website}{icon_link.get("href")}'
            else:
                icon_url = f'{website}/{icon_link.get("href")}'
        try:
            icon = requests.get(icon_url)
        except:
            print('{} {}\t\t{} {}'.format(
                crayons.red('Could not get icon for url:'), icon_url,
                crayons.white('Website:'), website_name)
            )
            continue
        with open(f'icons/{website_name}.ico', "wb") as f:
            f.write(icon.content)
