import argparse
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    return args.file

def parse_file(html):
    htmlParse = BeautifulSoup(html, 'html.parser')
    paragraphs = []
    for para in htmlParse.find_all("p"):
        p = para.get_text()
        if len(p) > 2:
            paragraphs.append(para.get_text())
    return "".join(paragraphs)

def construct_save_file(html_file_name):
    text_file_name = html_file_name.replace("/html/", "/texts/").replace("html", "txt") 
    return text_file_name


if __name__ == "__main__":
    file_name = parse_args()
    print(file_name)
    f = open(file_name, "r")
    html = f.read()
    f.close()
    parsed_file = parse_file(html)
    out_file_file_name = construct_save_file(file_name)
    f = open(out_file_file_name, "w", encoding="utf8")
    f.write(str(parsed_file))
    f.close()