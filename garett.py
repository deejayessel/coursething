import html.parser
from bs4 import BeautifulSoup
from course import *
import shelve

select = {
    'title' : '#main > ul > li > div.Rtable-cell.alpha.hiddenSmall.classes',
    'dreq' : '#main > ul > li > div.Rtable-cell.hiddenSmall.attr.flexcenter-desktop',
    'instructors' : '#main > ul > li > div.Rtable-cell.hiddenSmall.instructors',   
    'id' : '#main > ul > li > div.Rtable-cell.omega.hiddenSmall.Class.Nbr.flexcenter-desktop', 
    'time' : '#main > ul > li > div.Rtable-cell.hiddenSmall.times > span',
    'link' : '#main > ul > li > div.Rtable-cell.alpha.hiddenSmall.classes > a',
    }

# functions for extracting data from table cells
extractor = dict()
extractor.update(dict.fromkeys(list(select), 
                               lambda x: x.text.strip()))
extractor['instructors'] = lambda x: [i.text.strip() for i in x.select('a')] 

def readTable():
    with open('table.html', 'r') as f:
        text = ''.join(f.readlines())

    soup = BeautifulSoup(text, 'html.parser')

    with shelve.open('raw') as db:
        for k,v in select.items():
            selected = soup.select(select[k])
            if k not in ['link', 'time']:
                selected = selected[1:]
            db[k] = [extractor[k](x) for x in selected]

def printTable():
    with shelve.open('raw') as db:
        for k,v in db.items():
            print(f"CATEGORY: {k}")
            for i in v:
                print(i)
                
def writeCourseDB():
    with shelve.open('raw') as db, shelve.open('coursedata') as output:
        # for all courses in database
        for i in range(len(db['title'])):
            title = db['title'][i]
            output[title] = Course(title,
                                   0, #TODO
                                   db['dreq'][i],
                                   db['instructors'][i],
                                   db['time'][i],
                                   db['id'][i],
                                   db['link'][i])

if __name__ == '__main__':
    readTable()
    with shelve.open('raw') as db:
        for k,v in db.items():
            print(k, len(v))

        for k,v in db.items():
            print("****")
            print(v[0], k)

        print(type(db['instructors'][0]))
