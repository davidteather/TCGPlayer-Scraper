# TCGPlayer-Scraper

This is a commissioned project to scrape card listings from tcgplayer.com, but only the listings with images.

## Installation

* **Chrome** must be installed.
* You must download the latest **chromedriver** from [Google](https://sites.google.com/a/chromium.org/chromedriver/downloads), and include the .exe in your environment path.
* Tested with python 3.7.3 (but other python versions should work)


To install the dependencies execute
```
pip install -r requirements.txt
```

## Running the program

Put your links into the searchUrls.txt file an example is given below.
```
https://shop.tcgplayer.com/magic/beta-edition/lightning-bolt
https://shop.tcgplayer.com/magic/beta-edition/blue-elemental-blast
```

then just run main.py
```
python main.py
```

The program will then create output.xls which can be uploaded to google drive or opened with excel to display the given content.