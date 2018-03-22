import urllib.request

import os
from urllib.error import HTTPError


class ImageDownload(object):
    EXTENSION = 'txt'
    MAX_ERRORS = 2

    def __init__(self, filename):
        self.filename = filename
        self.filename_urls = '{}.{}'.format(self.filename, self.EXTENSION)

    def download(self):
        with open(self.filename_urls) as file:
            images_urls = [l.strip() for l in file]
            if len(images_urls) > 0:
                if not os.path.exists(self.filename):
                    os.makedirs(self.filename)
            for image_url in images_urls:
                image = image_url.split('/')[-1]
                directory = '{}/{}'.format(self.filename, image)
                self.download_image(directory, image_url)

    def download_image(self, directory, image_url):
        if not os.path.exists(directory):
            try:
                print('Starting to download'
                      ' image={}'.format(image_url))
                urllib.request.urlretrieve(image_url, directory)
                print('Downloaded image={}'.format(image_url))
            except HTTPError as e:
                print("Couldn't Download image={}".format(image_url))
            except ConnectionError as e:
                pass
            except Exception as e:
                pass


if __name__ == '__main__':
    for image_object in ['chair', 'desk', 'paper', 'computer']:
        ImageDownload(image_object).download()