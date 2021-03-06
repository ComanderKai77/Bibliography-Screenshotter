# Bibliography-Screenshotter

This tool is used to screenshot your sources automatically.
For example when you are writing an essay and need to screenshot your online sources, you can use the Bibliography Screenshotter.
It mainly used for BibTeX, natbib and other bibliography management software.

## Example
The file ```literature.bib``` looks like this:

```
@online{bibliography-screenshotter,
  author = {ComanderKai77},
  title = "{Bibliography Screenshotter}",
  url = {https://github.com/ComanderKai77/Bibliography-Screenshotter},
  year = {2021},
  note = {Visited on 2021/03/06}
}
```

The Bibliography Screenshotter searches for all the ```url``` attribute and creates a screenshot of the page.
It saves the screenshot to a folder with the name ```screenshots```.
When the folder already exists an error gets thrown.
The tool can't screenshot a PDF file, but it downloads the PDF instead.

## Installation

```bash
# Download repository
git clone https://github.com/ComanderKai77/Bibliography-Screenshotter.git

# Go into repository folder
cd Bibliography-Screenshotter

# Install requirements
pip3 install -r requirements.txt

# You can also install the dependecies with
pip3 install requests pyppeteer
```

## Usage
```bash
python3 screenshotter.py PATH_TO_LITERATUR_FILE
```

## How does it work?

The Bibliography Screenshotter uses pyppeteer, which is a "remote control" for headless Chromium.
