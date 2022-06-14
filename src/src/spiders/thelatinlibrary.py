import scrapy


class TheLatinLibraryScraper(scrapy.Spider):
    name = "TheLatinLibrary"
    seen_urls = set()

    def start_requests(self):
        urls = [
            "https://www.thelatinlibrary.com/medieval.html",
            "https://www.thelatinlibrary.com/neo.html",
            "https://www.thelatinlibrary.com/"
        ]
        url = "https://www.thelatinlibrary.com/"
        yield scrapy.Request(url=url, callback=self.parse)

    def is_final_text(self, page_str):
        if page_str.lower().count("<p") > 4 or page_str.lower().count("DT") > 2 or len(page_str.split("\n")) > 40 or len(page_str.split(" ")) > 100:
            return True
        return False
    
    def lint_links(self, links):
        new_links = []
        for l in links:
            if "thelatinlibrary" in l:
                continue
            elif "#" in l:
                continue
            elif ".html" not in l:
                continue
            else:
                new_links.append(l)
        return new_links
    
    def check_same_domain(self, url):
        if "thelatinlibrary" in url:
            return True
        return False
    
    def seen_yet(self, url):
        if url in self.seen_urls:
            return True
        
        self.seen_urls.add(url)
        return False
    
    def extract_text(self, response):
        return str(response.body)

    def parse(self, response):
        # ex. https://www.thelatinlibrary.com/livy/liv.6.shtml
        if self.check_same_domain(response.url): #and not self.seen_yet(response.url):
            filename = "../data/html/" + ("_".join(response.url.split("/")[3:]))
            links = response.xpath("//a/@href").extract()
            linted_links = self.lint_links(links)
            for link in linted_links:
                try:
                    yield response.follow(link, callback=self.parse)
                except:
                    continue
            
            page_text = self.extract_text(response)
            if self.is_final_text(str(page_text)):
                with open(filename, "wb") as f:
                    f.write(response.body)

                    #print("Filename: ", filename)
                    #print("original url: ", response.url)
                    #print()
                    self.log(f"Saved file {filename}")
            else:
                print("Doing nothing to: ", response.url)