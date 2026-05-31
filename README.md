# rewe-ebons-parser
This script parses the ewe ebons and generates some statistics

# Usage
First, download all eBons from your REWE account:
* Log into your REWE account
* Open your profile
* Click on "Deine Einkäufe" located in the left sidebar
* Then "eBon Service verwalten" where you can download all of your eBons.
* Extract them and use the extracted folder path as argument for this script.

After doing this, you can use the script as following:
```
python3 script.py --path bons --filter '05.2026'
```
`--path` is the path to the ebons pdfs
`--filter` is optional. You can filter out specific files containing the filter string.

# Output / Example
The program parses the pdfs, extracts the paid Sum, taxes and spent money for food or nonfood articles, categorized by market.
Each REWE has a unique market number and all bons are sorted into that number.

The example below shows the output of all of my eBons from May 2026.

```
(.venv) lukas@hellfire:~/Coding/rewe-ebons-parser > python3 script.py --path bons --filter '05.2026'
{
    "3396": {
        "sum": 263.36,
        "food_tax": 15.18,
        "food_brutto": 232.14000000000001,
        "nonfood_tax": 4.989999999999999,
        "nonfood_brutto": 31.22
    },
    "0706": {
        "sum": 66.73,
        "food_tax": 4.36,
        "food_brutto": 66.73
    }
}
```
