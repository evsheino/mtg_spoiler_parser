# MtgSalvation spoiler to LackeyCCG

Tools for extracting card information from the MtGSalvation spoiler for use with [LackeyCCG](http://www.lackeyccg.com) and the [Magic plugin](http://www.angelfire.com/funky/magiclackey/), and downloading card images from the official Wizards spoiler. For those who cannot wait for the Magic plugin maintainers to update the plugin.

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

## Set up Lackey

Append the output of the parser to the plugins/magic/sets/allcards2.txt file.

Convert the image files to jpg (with Imagemagick: `mogrify -format jpg *.png`).

Create a folder in plugins/magic/sets/setimages with the name of the set you used when parsing (set_name) and move the jpg files there.

Set up packs in plugins/magic/packs/packdefinitions1.xml if needed.
