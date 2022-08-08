# Analysis-of-Wikidata-Edit-History
## Codes for processing Wikidata edit history meta data and analysing processed dataset
### The folder "Processing metadata" contains:
  1. functions and codes for downloading and processing the stub-meta-history.xml from https://dumps.wikimedia.org/wikidatawiki/20220401/
  2. codes for separation between edit records on items and properties
  3. codes for edit type segmentation and extracting keywords
  4. codes for forming the final dataset to be analysed


### The folder "Analysing data" contains:
  1. SQL queries to create tables in Amazon Athena
  2. SQL queries to analyse edit dataset for both items and properties
  Note. Some similar analyses are not listed because of the very high degree of code repetition.

### The folder "demo dataset“ contains some examples of the final dataset, since the complete dataset is nearly 40 GB and can not be uploaded here.
For the complete dataset please download a zip file at https://drive.google.com/file/d/1VSwD1a-ZQ3hOCqbcMe83j-NO4KJE_mmg/view?usp=sharing

### The dumpstatus.json file is a machine-readable version of the information on [this page](https://dumps.wikimedia.org/wikidatawiki/20220401/)
### The bot_list.txt is the bot names provided by Wikidata on [this page](https://www.wikidata.org/wiki/Category:Bots)
