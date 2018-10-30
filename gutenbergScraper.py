import re, os, sys
import urllib.request

def scrapeTexts():
    """Pulls down as many texts as are available from the gutenberg project
    website cleans them and stores them in a n by 2 array  where texts[0] is
    the name of the text and texts[1] is the text iteslef """
    pat1 = r'<a href=".{1,100}Plain Text UTF-8'
    pat2 = r'"(.*?)"'
    pat3 = r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK.{1,30}\*\*\*(.+)End of the Project Gutenberg EBook.+\*\*\* END OF THIS PROJECT GUTENBERG EBOOK'
    pat4 = re.compile('[^a-zA-Z\s]')
    texts = []
    for i in range(8,108):
        with urllib.request.urlopen("https://www.gutenberg.org/ebooks/"+str(i)) as response:
            html = str(response.read())
            #print(html)
            try:
                link = re.findall(pat1, html)[0]
                print(link)
                try:
                    url  = re.findall(r'"(.*?)"', link)[0]
                    print(url)
                    with urllib.request.urlopen("https:"+url) as response:
                        text = response.read().decode('utf-8')
                        text = text.replace('\r', ' ').replace('\n', ' ')
                        text = re.findall(pat3, text)[0]
                        try:
                            textR = text.replace('  ', ' ')
                            while text != textR:
                                text = textR
                                textR = text.replace('  ', ' ')
                            text = pat4.sub('', text)
                            texts.append(["name"+str(i), text])
                            print(text)
                        except:
                            print("No text")
                except:
                    print("No url")
            except:

                print("No link")
    return texts

def outputIndividual(texts):
    """Outputs the texts into indivual, named text files in the directory
    ./texts which is created if it doesn't exist"""
    try:
        os.mkdir("./texts")
    except:
        pass
    for text in texts:
        with open("./texts/"+text[0]+".txt", "w") as file:
            file.write(text[1])
            file.close()

def outputCorpus(texts):
    """Outputs the texts into a single file, named corpus.txt, in the directory
    ./corpus which is created if it doesn't exist"""
    try:
        os.mkdir("./corpus")
    except:
        pass
    corpus = ""
    for text in texts:
        corpus += text + "\n"
    with open("corpse.txt", "w") as file:
        file.write(corpus)
        file.close()

def main():
    texts = scrapeTexts()
    print(texts)
    try:
        if sys.argv[1] == "corpus":
            outputCorpus(texts)
        elif sys.argv[1] == "texts":
            outputIndividual(texts)
        else:
            print("Usage:  \nFor single file - python3 ./gutenbergScraper.py corpus \nFor indivual texts - python3 ./gutenbergScraper.py texts")
    except:
        print("Usage:  \nFor single file - python3 ./gutenbergScraper.py corpus \nFor indivual texts - python3 ./gutenbergScraper.py texts")
    return 0
if __name__ == "__main__":
    main()
