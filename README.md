# MtgSalvation spoiler to LackeyCCG

Tools for extracting card information from the MtGSalvation spoiler for use in [LackeyCCG](http://www.lackeyccg.com) and downloading card images from the official Wizards spoiler.

## Requirements

Requires Python 2.7 and [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/)

## Parse the spoiler and save cards in LackeyCCG format

First save the MtgSalvaltion spoiler locally.

```
$ python spoiler_parser.py mtgsalvation_spoiler_file set_name output_file
```

E.g.

```
$ python spoiler_parser.py mtgsalvation_spoiler.html roe roe.txt
```

## Download card images

First save the official Wizards spoiler locally and create a output directory for the images.

```
$ python downloader.py wizards_spoiler_file output_dir/
```

E.g.

```
$ python downloader.py wizards_spoiler.html images/
```
