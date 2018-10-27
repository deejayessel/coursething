import html.parser
from bs4 import BeautifulSoup
from course import *
import shelve

select = {
    'title' : '#main > ul > li > div.Rtable-cell.alpha.hiddenSmall.classes',
    'dreq' : '#main > ul > li > div.Rtable-cell.hiddenSmall.attr.flexcenter-desktop',
    'instructor' : '#main > ul > li > div.Rtable-cell.hiddenSmall.instructors',   
    'id' : '#main > ul > li > div.Rtable-cell.omega.hiddenSmall.Class.Nbr.flexcenter-desktop', 
    'time' : '#main > ul > li > div.Rtable-cell.hiddenSmall.times > span',
    }

# functions for extracting data from table cells
extractor = dict()
extractor.update(dict.fromkeys(list(select), 
                               lambda x: [i.text.strip() for i in x]))
extractor['instructor'] : lambda cell: [i.text.strip() for i in cell.select('a')]

def readTable():
    with open('table.html', 'r') as f:
        text = ''.join(f.readlines())

    soup = BeautifulSoup(text, 'html.parser')

    with shelve.open('courses') as db:
        for k,v in select.items():
            selected = soup.select(select[k])[1:]
            db[k] = extractor[k](selected)

def printTable():
    with shelve.open('courses') as db:
        for k,v in db.items():
            print(f"CATEGORY: {k}")
            for i in v:
                print(i)

def writeCourseDB():


if __name__ == '__main__':
    readTable()
    printTable()
    
