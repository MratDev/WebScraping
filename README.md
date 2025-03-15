# Flyer Scraper

A Python web scraper designed to collect promotional flyers from German hypermarkets via the prospektmaschine.de website.

## Overview

This script automatically visits the prospektmaschine.de website, navigates through various hypermarket sections, and extracts information about current promotional flyers. The collected data includes:

- Flyer title
- Thumbnail image URL
- Shop/hypermarket name
- Validity period (from/to dates)
- Parsing timestamp

The script saves all collected data to a JSON file for further processing or analysis.

## Features

- Uses Selenium to browse through hypermarket categories
- Only collects flyers that are currently valid
- Opens Chrome browser window when running
- Saves data in JSON format

## Requirements

- Python 3.6+
- Required Python packages:
  - BeautifulSoup4
  - requests
  - selenium
  - webdriver_manager
- Chrome browser installed

## Installation

1. Clone this repository or download the script
2. Install required libraries:

```bash
pip install beautifulsoup4 requests selenium webdriver-manager
```

## Usage

Run the script without any arguments:

```bash
python scraping.py
```

The script will:
1. Initialize a Chrome browser (browser window will open)
2. Navigate to the prospektmaschine.de hypermarkets page
3. Extract links to all hypermarket categories
4. Visit each hypermarket page and collect flyer information
5. Filter out expired flyers
6. Save all collected data to `flyers_data.json` in the current directory

## Output Format

The script generates a JSON file with the following structure:

```json
[
  {
    "title": "Weekly Offers",
    "thumbnail": "https://example.com/image.jpg",
    "shop_name": "Market Name",
    "valid_from": "2025-03-10",
    "valid_to": "2025-03-15",
    "parsed_time": "2025-03-15 12:34:50"
  },
  ...
]
```

## How It Works

The script uses a combination of Selenium for JavaScript-rendered content and BeautifulSoup for HTML parsing:

1. The `FlyerScraper` class initializes a Chrome browser
2. `parse_hypermarkets()` extracts links to all hypermarket categories
3. `parse_flyers_for_shop()` visits each hypermarket page and finds flyer containers
4. `process_flyer()` extracts details from each flyer element
5. Valid flyers are added to the collection and saved to JSON

## Customization

You can modify the base URL in the `main()` function to target different sections of the website or similar websites with comparable structures.

## Error Handling

The script includes error handling to:
- Skip problematic flyers without crashing
- Handle missing or malformed date information
- Adapt to different HTML structures across the site
