from sqlalchemy.dialects.mysql import INTEGER, VARCHAR,  DATETIME, TIME, DATE, CHAR, NUMERIC, BIT
from sqlalchemy import Column, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from json import JSONEncoder


Base = declarative_base()


class PUser(Base):
    __tablename__ = 'PUser'
    userName = Column(VARCHAR(100), primary_key=True)
    nickName = Column(VARCHAR(100), nullable=False)
    passWD = Column(VARCHAR(256), nullable=False)
    portrait = Column(VARCHAR(256), nullable=False)

    def __init__(self, username, nickname, passwd, portrait):
        self.userName = username
        self.nickName = nickname
        self.passWD = passwd
        self.portrait = portrait


class Teacher(Base):
    __tablename__ = 'Teacher'
    id = Column(CHAR(10), primary_key=True)
    userName = Column(VARCHAR(100), ForeignKey("PUser.userName"), nullable=False)
    firstName = Column(VARCHAR(50), nullable=False)
    lastName = Column(VARCHAR(50), nullable=False)
    department = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)

    def __init__(self, id, username, firstname, lastname, department, em):
        self.id = id
        self.userName = username
        self.firstName = firstname
        self.lastName = lastname
        self.department = department
        self.email = em


class Student(Base):
    __tablename__ = "Student"
    id = Column(CHAR(10), primary_key=True)
    userName = Column(VARCHAR(100), ForeignKey('PUser.userName'), nullable=False)
    major = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)

    def __init__(self, id, username, major, email):
        self.id = id
        self.userName = username
        self.major = major
        self.email = email


class TA(Base):
    __tablename__ = 'TA'
    userName = Column(VARCHAR(100), ForeignKey('PUser.userName'), primary_key=True, nullable=False)
    teacherId = Column(CHAR(10), ForeignKey('Teacher.id'))
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'),
                              primary_key=True, nullable=False)

    def __init__(self, uname, i, ins, cdes):
        self.userName = uname
        self.id = i
        self.teacherId = ins
        self.courseDescriptor = cdes


class Course(Base):
    __tablename__ = "Course"
    courseDescriptor = Column(VARCHAR(256), primary_key=True)
    courseName = Column(VARCHAR(200), nullable=False)
    courseId = Column(CHAR(20), nullable=False)
    credit = Column(NUMERIC(3, 1), nullable=False)
    semester = Column(CHAR(10), nullable=False)
    startTime = Column(DATE, nullable=False)
    endTime = Column(DATE, nullable=False)
    courseStart = Column(TIME(fsp=2))
    courseEnd = Column(TIME(fsp=2))
    hotIndex = Column(INTEGER, nullable=False)
    Image = Column(VARCHAR(256), nullable=False)
    description = Column(VARCHAR(1000), nullable=False)

    def __init__(self, course_descriptor, course_id, credit, semester, start_time, end_time, course_start, course_end,
                 hot_index, image, description, cname):
        self.courseDescriptor = course_descriptor
        self.courseId = course_id
        self.credit = credit
        self.semester = semester
        self.startTime = start_time
        self.endTime = end_time
        self.courseStart = course_start
        self.courseEnd = course_end
        self.hotIndex = hot_index
        self.Image = image
        self.description = description
        self.courseName = cname


class Manage(Base):
    __tablename__ = "Manage"
    userName = Column(VARCHAR(100), ForeignKey('PUser.userName'), primary_key=True, nullable=False)
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'), primary_key=True, nullable=False)
    type = Column(BIT(1), nullable=False)
    newNotice = Column(BIT(1), nullable=False)
    editNotice = Column(BIT(1), nullable=False)
    deleteNotice = Column(BIT(1), nullable=False)
    newHomework = Column(BIT(1), nullable=False)
    editHomework = Column(BIT(1), nullable=False)
    deleteHomework = Column(BIT(1), nullable=False)
    gradeHomework = Column(BIT(1), nullable=False)

    def __init__(self, username, descriptor, type, newnotice, editnotice, deletenotice, newhw, edithw, delhw, grahw):
        self.userName = username
        self.courseDescriptor = descriptor
        self.type = type
        self.newNotice = newnotice
        self.editNotice = editnotice
        self.deleteNotice = deletenotice
        self.newHomework = newhw
        self.editHomework = edithw
        self.deleteHomework = delhw
        self.gradeHomework = grahw


class Homework(Base):
    __tablename__ = "Homework"
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'), index=True)
    homeworkTitle = Column(VARCHAR(100), primary_key=True)
    homeworkContent = Column(VARCHAR(5000), nullable=False)
    startTime = Column(DATETIME(fsp=2), primary_key=True)
    creatorUsername = Column(VARCHAR(100), ForeignKey('PUser.userName'), primary_key=True, nullable=False)
    endTime = Column(DATETIME(fsp=2))

    def __init__(self, descriptor, hktitle, stime, etime, cusername, hwkcontent):
        self.courseDescriptor = descriptor
        self.homeworkTitle = hktitle
        self.startTime = stime
        self.endTime = etime
        self.creatorUsername = cusername
        self.homeworkContent = hwkcontent


class Participation(Base):
    __tablename__ = 'Participation'
    studentUsername = Column(VARCHAR(100), ForeignKey('PUser.userName'), primary_key=True)
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'), primary_key=True)
    finalGrade = Column(NUMERIC(5, 2))
    signInTime = Column(DATETIME(fsp=2))

    def __init__(self, sname, cd, fg, sit):
        self.studentUsername = sname
        self.courseDescriptor = cd
        self.finalGrade = fg
        self.signInTime = sit


class HandInHomework(Base):
    __tablename__ = "HandInHomework"
    submitUserName = Column(VARCHAR(100), ForeignKey('PUser.userName'), primary_key=True, nullable=False)
    gradeUserName = Column(VARCHAR(100), ForeignKey('PUser.userName'), nullable=True)
    grades = Column(NUMERIC(5, 2))
    handInTime = Column(DATETIME(fsp=2), primary_key=True)
    fileName = Column(VARCHAR(256), nullable=False)
    file = Column(VARCHAR(256), nullable=False)
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'), nullable=False)
    homeworkTitle = Column(VARCHAR(100), ForeignKey('Homework.homeworkTitle'), nullable=False)

    def __init__(self, susername, gusername, grade, hdintime, fil, descriptor, hwtitle, filen):
        self.submitUserName = susername
        self.gradeUserName = gusername
        self.grades = grade
        self.handInTime = hdintime
        self.file = fil
        self.courseDescriptor = descriptor
        self.homeworkTitle = hwtitle
        self.fileName = filen


class Reference(Base):
    __tablename__ = "Reference"
    referenceName = Column(VARCHAR(100), nullable=False)
    file = Column(VARCHAR(256), nullable=False)
    upLoadTime = Column(DATETIME(fsp=2), primary_key=True)
    downloadable = Column(BIT(1), nullable=False)
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'), primary_key=True, nullable=False)

    def __init__(self, rename, uptime, candownload, descritpor):
        self.referenceName = rename
        self.upLoadTime = uptime
        self.downloadable = candownload
        self.courseDescriptor = descritpor


class Notification(Base):
    __tablename__ = 'Notification'
    content = Column(VARCHAR(1000))
    createTime = Column(DATETIME(fsp=2), primary_key=True)
    creatorUsername = Column(VARCHAR(100), ForeignKey('Manage.userName'), primary_key=True)
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'), primary_key=True)

    def __init__(self, ctnt, ctime, ctor, cdes):
        self.content = ctnt
        self.createTime = ctime
        self.creatorUsername = ctor
        self.courseDescriptor = cdes


class Complain(Base):
    __tablename__ = 'Complain'
    studentUsername = Column(VARCHAR(100), ForeignKey('PUser.userName'), primary_key=True, nullable=False)
    courseDescriptor = Column(VARCHAR(256), ForeignKey('Course.courseDescriptor'))
    handInTime = Column(DATETIME(fsp=2), primary_key=True)
    reason = Column(VARCHAR(1000))

    def __init__(self, stu, cour, hdint, reasn):
        self.studentUsername = stu
        self.courseDescripton = cour
        self.handInTime = hdint
        self.reason = reasn


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PUser):
            return {'userName': obj.userName, 'nickName': obj.nickName}
        elif isinstance(obj, Teacher):
            # return {obj.id,obj.userName,obj.firstName,obj.lastName,obj.department}
            return obj.__dict__
        elif isinstance(obj, Student):
            return obj.__dict__
        elif isinstance(obj, TA):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
            return temp
        elif isinstance(obj, Course):
            temp = obj.__dict__
            return temp
        elif isinstance(obj, Manage):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
            return temp
        elif isinstance(obj, Homework):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
            return temp
        elif isinstance(obj, HandInHomework):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
            return temp
        elif isinstance(obj, Reference):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
        elif isinstance(obj, Participation):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
        elif isinstance(obj, Notification):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
            return temp
        elif isinstance(obj, Complain):
            temp = obj.__dict__
            temp['courseName'] = courseDescriptor2Name(temp['courseDescriptor'])
            pass
        elif isinstance(obj, DATE):
            return str(obj)
        elif isinstance(obj, DATETIME):
            return str(obj)
        elif isinstance(obj, TIME):
            return str(obj)
        else:
            pass


def courseDescriptor2Name(sha):
    stmt = select(Course.courseName).where(Course.courseDescriptor == sha)
    return session.execute(stmt).fetchone()


Engine = create_engine("mysql+pymysql://root:Gdnuebdang0517666@127.0.0.1:3306/tp", encoding="utf-8")
Session = sessionmaker(bind=Engine)
session = Session()
# Base.metadata.create_all(Engine)
