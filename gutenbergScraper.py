import re
import urllib.request

pat1 = r'<a href=".{1,100}Plain Text UTF-8'
pat2 = r'"(.*?)"'
pat3 = r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK.{1,30}\*\*\*(.+)End of the Project Gutenberg EBook.+\*\*\* END OF THIS PROJECT GUTENBERG EBOOK'
pat4 = re.compile('[^a-zA-Z\s]')
corpus = ""
for i in range(8,108):
    with urllib.request.urlopen("https://www.gutenberg.org/ebooks/"+str(i)) as response:
        html = str(response.read())
        #print(html)
        try:
            link = re.findall(pat1, html)[0]
            #print(link)
            try:
                url  = re.findall(r'"(.*?)"', link)[0]
                print(url)
                with urllib.request.urlopen("https:"+url) as response:
                    text = response.read().decode('utf-8')
                    text = text.replace('\r', ' ').replace('\n', ' ')
                    try:
                        text = re.findall(pat3, text)[0]
                        textR = text.replace('  ', ' ')
                        while text != textR:
                            text = textR
                            textR = text.replace('  ', ' ')
                        text = pat4.sub('', text)
                        corpus = corpus+text
                        print(text)
                    except:
                        print("No text")
            except:
                print("No url")
        except:
            print("No link")
mafile = open("corpse.txt", "w")
mafile.write(corpus)
mafile.close()
