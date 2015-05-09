# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import os.path
import sys

def download_file(src, output_name):
    """
    Download a file at url src and save it as output_name
    using the original file type.

    If a file named output_name already exists, do nothing.
    """
    file_type = src.split('.')[-1]
    path = u"{}.{}".format(output_name, file_type)
    if not os.path.isfile(path):
        f = urllib2.urlopen(src)
        file_data = f.read()
        out_file = open(path, 'wb')
        out_file.write(file_data)
        f.close()
        out_file.close()

def download_images(src, out_dir):
    """
    Dowload all card images from the Wizards spoiler. Use
    the card's name as the file name.

    @param src: path to a locally saved copy
        of the Wizards spoiler.
    @param out_dir: the directory to which the files
        are to be saved.
    """

    cards = []
    f = open(src)
    soup = BeautifulSoup(f)

    for line in soup.find_all('img'):
        title = line.attrs.get('title')
        if not title is None:
            title = title.strip().replace(u'’', u'').replace(u',', u'')
            if not title in cards:
                cards.append(title)
                img_src = line.attrs.get('src')
                output = u"{}{}".format(out_dir, title)
                download_file(img_src, output)
    f.close()

if __name__ == '__main__':
    download_images(sys.argv[1], sys.argv[2])
