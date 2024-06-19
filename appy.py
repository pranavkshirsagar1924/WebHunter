import cmd
import shlex
from bs4 import BeautifulSoup
import requests
import os
import datetime

class RedPrintCmd(cmd.Cmd):
    def print(self, text, color='red'):
        if color == 'red':
            print(f"\033[91m{text}\033[0m")
        else:
            print(text)

class myShell(RedPrintCmd):
    prompt = 'WebHunter.Scrap> '

    def __init__(self):
        super().__init__()
        self.do_greet("")

    def do_greet(self,line):
        self.print("scrap: Use this command followed by a URL to scrape the content of a website. It downloads the HTML content of the specified URL and saves it locally as dumpingGround.html. For example, scrap https://example.com.")
        self.print("")
        self.print("tag: This command searches for specific HTML tags within the scraped content (dumpingGround.html). Provide the tag name as an argument to retrieve all occurrences of that tag in the HTML. For example, tag img will find all <img> tags.")
        self.print("")
        self.print("media: Use this command to extract media elements such as images, videos, or audio files from the scraped content. Provide one of the supported media types (image, video, audio) as an argument. It will then search for and download all such media files to a specified directory. For example, media image.")
        self.print("")
        self.print("meta: This command extracts metadata information from the scraped HTML content, including <meta> tags and the page title (<title>).")
        self.print("")
        self.print("alt: Use this command to extract the alt attribute values from all <img> tags found in the scraped HTML content. It helps in understanding alternative text descriptions for images.")
        self.print("")
        self.print("linkify: This command extracts all hyperlinks (<a> tags) from the scraped HTML content, displaying both the link text and the URL.")
        self.print("")
        self.print("help: Provides help information about each command available in myShell.")


    def do_scrap(self,line):
        try:
            args = shlex.split(line)
            if not args:
                self.print("Please provide a link to scrape.")
                return
            
            if len(args) > 1:
                self.print("Please scrape one link at a time.")
                return
            
            link = args[0]
            Scrap(link) 
        except Exception as e:
            self.print(f"Error occurred while scraping: {e}")

    def do_tag(self,line):
        try:
            args = shlex.split(line)
            if not args:
                self.print("Please provide a tag to search.")
                return
            
            tag = args[0]
            find_tags(tag)
        except Exception as e:
            self.print(f"Error occurred while searching tags: {e}")
    

    def do_media(self,line):
        try:
            args = shlex.split(line)
            if not args:
                self.print("Invalid command found: required 1 media type argument such as image, video, audio.", color='yellow')
                return
            
            media_type = args[0]
            extractMedia(media_type)
        except Exception as e:
            self.print(f"Error occurred while extracting media: {e}")

    def do_meta(self,line):
        try:
            extract_meta()
        except Exception as e:
            self.print(f"Error occurred while extracting meta tags: {e}")

    def do_alt(self,line):
        try:
            extract_alt()
        except Exception as e:
            self.print(f"Error occurred while extracting alt tags: {e}")
    
    def do_linkify(self,line):
        try:
            extract_links()
        except Exception as e:
            self.print(f"Error occurred while extracting links: {e}")

    def do_help(self, arg: str) -> bool | None:
        return super().do_help(arg)
    
    def emptyline(self) -> bool:
        return super().emptyline()

def Scrap(link):
    try:
        response = requests.get(link)
        with open ("dumpingGround.html","w",encoding="utf-8") as fw:
            fw.write(response.text)
            print("Site Downloaded.")
    except Exception as e:
        print(f"Error occurred while scraping site: {e}")

#for tags extraction
def find_tags(tag):
    try:
        with open("dumpingGround.html","r",encoding="utf-8") as fr:
            content = fr.read()
        soup = BeautifulSoup(content,"html.parser")
        if tag:
            elements = soup.find_all(tag)
            if elements:
                for el in elements:
                    print(el)
            else:
                print(f"No '{tag}' elements found.")
        else:
            print("Element Not Found")
    except Exception as e:
        print(f"Error occurred while finding tags: {e}")
    
#for media extraction
def extractMedia(mediaType):
    try:
        type_extension = ""
        if mediaType.lower() == "image":
             images = find_tags("img")
             type_extension = "jpeg"
        elif mediaType.lower() == "video":
             images = find_tags("source")
             type_extension = "mp4"
        elif mediaType.lower() == "audio":
            images = find_tags("source")
            type_extension = "mp3"
        else:
            print("Media type not supported: supported types are png, jpg, jpeg, webp, mp3, mp4")
            return
        
        if len(images) == 0:
            print(f"No <{mediaType}> elements found. Try rescraping the site.")
        else:
            directory_path = input("Enter directory path to save media: ")
            # Ensure the directory path exists
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            
            for idx, img in enumerate(images, start=1):
                src = img.get("src")
                if src:
                    print(f"Downloading Media {idx}")
                    img_name = f"media_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{type_extension}"
                    img_path = os.path.join(directory_path, img_name)
                    req = requests.get(src)
                    
                    if req.status_code == 200:
                        with open(img_path, "wb") as mfw:
                            mfw.write(req.content)
                        print(f"Media {idx} downloaded successfully.")
                    else:
                        print(f"Failed to download media {idx}. Status code: {req.status_code}")
                else:
                    print(f"Media {idx} does not have a valid src attribute.")
            
            print("Media Download Task Status: Done")
    except Exception as e:
        print(f"Error occurred while extracting media: {e}")


def extract_meta():
    try:
        meta_data = find_tags("meta")
        if meta_data:
            for meta in meta_data:
                if meta.get('name') is not None:
                    print(f"{meta.get('name')} : {meta.get('content')}")
                else:
                    print(f"{meta.get('property')} : {meta.get('content')}")
        
        title = find_tags("title")
        if title:
            print(f"Title : {title.text}")
    except Exception as e:
        print(f"Error occurred while extracting meta tags: {e}")

def extract_links():
    try:
        links = find_tags("a")
        if links:
            for link in links:
                print(link)
                print(f"Link : {link['href']}")
        else:
            print("No links found.")
    except Exception as e:
        print(f"Error occurred while extracting links: {e}")

def extract_alt():
    try:
        images = find_tags("img")
        if len(images) == 0:
            print("No images found.")
        else:
            for img in images:
                print(f"Alt : {img.get('alt')}")
    except Exception as e:
        print(f"Error occurred while extracting alt tags: {e}")


if __name__ == "__main__":
    shell = myShell()
    shell.cmdloop()
