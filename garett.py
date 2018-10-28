from bs4 import BeautifulSoup
import html.parser
from course import *
import shelve
import matplotlib.pyplot as plt

select = {
    'title' : '#main > ul > li > div.Rtable-cell.alpha.hiddenSmall.classes',
    'dreq' : '#main > ul > li > div.Rtable-cell.hiddenSmall.attr.flexcenter-desktop',
    'instructors' : '#main > ul > li > div.Rtable-cell.hiddenSmall.instructors',
    'id' : '#main > ul > li > div.Rtable-cell.omega.hiddenSmall.Class.Nbr.flexcenter-desktop',
    'time' : '#main > ul > li > div.Rtable-cell.hiddenSmall.times > span',
    'link' : '#main > ul > li > div.Rtable-cell.alpha.hiddenSmall.classes > a',
    }

# functions for extracting data from table cells
extractor = {
    'title' : lambda x: x.text.strip(),
    'dreq' : lambda x: [y.replace(';','') for y in x.text.strip().split('; ')]
    'id' : lambda x: x.text.strip(),
    'time' : lambda x: x.text.strip(),
    'link' : lambda x: x.text.strip(),
    'instructors': lambda x: [i.text.strip() for i in x.select('a')],
}

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

def updateTimelist(u, weeklyTimeList, coursePrefixTimeList):
    for s1, e1 in u.ranges:
        for k in range(len(weeklyTimeList[0])):
            if s1 <= weeklyTimeList[s1//1440][k] and e1 > weeklyTimeList[e1//1440][k]:
                coursePrefixTimeList[0][s1//1440][k] +=1
                coursePrefixTimeList[len(coursePrefixTimeList)-1][s1//1440][k] +=1

def getHistograms():

    with shelve.open('raw') as db:
        weeklyTimeList = [[x for x in range(1440*i + 480, 1440*i + 1300, 5)] for i in range(5)]
        coursePrefixList = ["ALL"]
        coursePrefixTimeList = [[[0] * ((1300-480)//5) for i in range(5)]]

        for i in range(0,len(db['title'])):
            if db['time'][i] in ['Cancelled', 'TBA', '']:
                continue

            u = CourseTime(db['time'][i])
            toCheck = db['title'][i][:4].strip()

            if toCheck != coursePrefixList[len(coursePrefixList)-1]:
                coursePrefixList.append(toCheck)
                coursePrefixTimeList.append([[0] * ((1300-480)//5) for i in range(5)])

            updateTimelist(u, weeklyTimeList, coursePrefixTimeList)

        print(coursePrefixList)
        for i in coursePrefixTimeList[0]:
            print(i)

        with shelve.open('prefixes') as pdb:
            for prefix, timelist in zip(coursePrefixList, coursePrefixTimeList):
                pdb[prefix] = timelist


class CourseTime():
    """
    TBA, Cancelled, '' --> empty range
    Store list of ranges for which class is in session
    Resolve conflicts

    Stores course times as list of ranges(tuples with starting and ending time)
    """

    def __init__(self, s):
        self.ranges = []
        self.string = s
        days = 'MTWRF'
        if s not in ['TBA', 'Cancelled', '']:
            for c in s[:s.find(' ')]: #for all weekdays
                n = days.find(c)

                start = s[s.find(' ')+1:s.find(' - ')+1].strip()
                end = s[s.find(' - ')+3:s.find('m',s.find(' - '))+2].strip()

                self.ranges.append((self._intify(start, n),
                                    self._intify(end, n)))
        self._checkRep()

    def _intify(self, s, daynum):
        """
        Return a string time as an integer between 0 and 1440

        Pre: assumes that `s` is a well-formed time

        (eg) 11:00 am; 1:00 pm
        """

        sep = s.find(':')
        hour = int(s[:sep])
        if 'pm' in s: hour = (hour%12) + 12

        min = int(s[sep+1:sep+3])

        return daynum*1440 + (hour * 60 + min)

    def hasConflictWith(self, other):
        for s1, e1 in self.ranges:
            for s2, e2 in other.ranges:
                if s1 < e2 and s2 < e1:
                    return True
        return False

    def _checkRep(self):
        for start, end in self.ranges:
            assert start < end, f"start time is later than end time: {start} . {end} : {self.string}"

    def __str__(self):
        return str(self.ranges)

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    readTable()

    def firstUnconflicting(setList, item):

        def hasConflict(set, item):
            for s in set:
                if item.hasConflictWith(s):
                    return True
            return False

        for i in range(len(setList)):
            if not hasConflict(setList[i], item):
                return i
        return len(setList)

    setlist = [set()]
    courselist = [[]]

    getHistograms()



        # for i in range(0,len(db['title']),250):
        #     if db['time'][i] in ['Cancelled', 'TBA', '']:
        #         continue
        #
        #     u = CourseTime(db['time'][i])
        #
        #     # find the first set where there is no conflict with u and add the course there
        #     pos = firstUnconflicting(setlist, u)
        #     if pos == len(setlist):
        #         setlist.append(set())
        #         courselist.append([])
        #     setlist[pos].add(u)
        #     courselist[pos].append(db['title'][i] + "\n" + db['time'][i])
        #
        # for set in reversed(courselist):
        #     print("SET START **********")
        #     for course in set:
        #         print(course)
        #     print("********** SET END")
