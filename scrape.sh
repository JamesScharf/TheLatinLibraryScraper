rm -r ./data/html
mkdir ./data/html
cd src
scrapy crawl TheLatinLibrary -L ERROR
cd ..