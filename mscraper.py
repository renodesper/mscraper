import traceback
import requests
import os
import bs4


manga = 'sousei-no-onmyouji'
url = 'http://www.mangareader.net/sousei-no-onmyouji'
os.makedirs(manga, exist_ok=True)

chapter = 1
chapter_exist = True

while chapter_exist:
    page = 1
    page_exist = True
    os.makedirs("{}/{}".format(manga, chapter), exist_ok=True)

    print("Downloading chapter: {}".format(chapter))
    while page_exist:
        try:
            res = requests.get('{}/{}/{}'.format(url, chapter, page))
            res.raise_for_status()

            if res.status_code != 404:
                soup = bs4.BeautifulSoup(res.text)
                img = soup.select('#img')
                img_url = img[0].get('src')

                print('  Downloading image: {}'.format(img_url))
                res = requests.get(img_url)
                res.raise_for_status()

                with open(os.path.join(manga + "/{}".format(chapter),
                                       os.path.basename(img_url)), 'wb') as image_file:
                    for chunk in res.iter_content(1000000):
                        image_file.write(chunk)

                page += 1
            else:
                page_exist = False
        except:
            page_exist = False
            print(traceback.print_exc())

    chapter += 1

print("{} downloaded".format(manga))
