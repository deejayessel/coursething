class CourseTitle():

    __slots__ = ['prefix', 'num', 'section', 'semester', 'title']

    def __init__(self, prefix, num, section, semester, title):
        self.prefix = prefix
        self.num = num
        self.section = section
        self.semester = semester
        self.title = title

    def __str__(self):
        return f"{self.prefix} {self.num} - {self.section} ({self.semester}) : {self.title}"

class Course():

    #__slots__ = ['title', 'div', 'req', 'instructors', 'time', 'classnum', 'link']

    def __init__(self, title, div, req, instructors, time, id, link):
        self.title = title
        self.div = div
        self.req = req
        self.instructors = instructors
        self.time = time
        self.id = id
        self.link = link

    def __str__(self):
        return str(self.title) + str(self.__dict__)

if __name__ == '__main__':
    title1 = CourseTitle('AFR',24,1,'W','Touring Black Religion')
    print(title1)
    course1 = Course(title1, 3, [], ['Andre Hui'], 'WF 11:00 AM', 2020, 'https://catalog.williams.edu/afr/detail/?strm=&cn=24&crsid=019573&req_year=0')
    print(course1)
