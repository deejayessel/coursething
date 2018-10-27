import html.parser
from bs4 import BeautifulSoup
from course import *

import pickle
import dbm

def readData():
    with open('table.html', 'r') as f:
        text = ''.join(f.readlines())

    soup = BeautifulSoup(text, 'html.parser')
    selector_prefix = "#main > ul > li > div.Rtable-cell.alpha.hiddenSmall."

    elements = { 
        'titles' : soup.select(selector_prefix + "classes"),
        'divreq' : soup.select(selector_prefix + "dreq"),
        'instructors' : soup.select(selector_prefix + "instructors"),
        'coursenums' : soup.select("#main > ul > li > div.Rtable-cell.omega.hiddenSmall.Class.Nbr"),
        'times' : soup.select(selector_prefix + "times"),
        }

    with dbm.open('courses.db', 'c') as data:
        data['instructors'] = [ j.string.strip() for j in [ i.find_all('a') for i in elements['instructors'] ] ]
        data['titles'] = [ i.text.replace('\n','') for i in elements['titles'] ]
        data['coursenums'] = [ i.text.strip() for i in elements['coursenums'] ]
        data['divreq'] = [ i.text for i in elements['divreq'] ]
        data['times'] = [ i.span.contents for i in elements['times'] if i.span is not None ]

    print('pickling...')
    pickle.dump(data, open('data.txt', 'wb'))
    print('done pickling!')



    
    
