

from cmu_112_graphics import *
import string, copy, random, math
import os
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import io
import requests
import time
from datetime import datetime
from datetime import date
from selenium.webdriver.common.keys import Keys

class User(object):
    def __init__(self, username, password):
        self.username=username
        self.password=password
        self.fullname = None
        self.gpa = None
        self.satMathScore = None
        self.satEBRWScore = None
        self.location = None
        self.major = None
        self.radius = None
        self.regions = None
        self.importanceOfFinancialAid = None
        self.schoolCulturePreference = None  
        self.favorites=[]      
    def getHashables(self):
        return (self.username, self.password)
    def __hash__(self):
        return hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, User) and (self.username == other.username) 
        and  (self.password == other.password))
    def addFavorite(self, uni):
        self.favorites.append(uni)  

class University(object):
    def __init__(self, name):
        self.name=name              
    def getHashables(self):
        return (self.username, self.password)
    def __hash__(self):
        return hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, User) and (self.username == other.username) 
        and  (self.password == other.password))

    

def listToString(L):
    string=""
    for item in L:
        string+=item
        string+="\n"
    return string

def appStarted(app):
    
    app.isSplashScreen = True
    app.isLoginScreen = False
    app.enteringUsername = False
    app.enteringPassword = False
    app.username = "Enter username"
    app.password = "Enter password"
    app.university=""
    app.passwordIncorrectPopUp = False
    app.isQuestionScreen = False
    app.isDashboardScreen = False
    app.isCollegeSearchTab=False
    app.enteringCollege=False
    app.isCollegeSearchResultTab=False
    app.isEssayWritingTab=False
    app.isEssayEditor=False
    app.isEditingFilename=False
    app.index=""
    app.filename = "Enter a name for your draft file, hit Enter to save: " 
    app.isEnteringEssay=False
    app.isSavedBanner=False
    app.isListScreen=False
    app.essayText=""
    app.isScheduleTab=False
    app.isProfileTab=False
    app.isMatchScreen=False

    app.count=0
    app.plan=0
    app.add=False
    app.duedates=dict()
    app.tl=dict()
    app.timeleft=dict()
    app.AdmissionLevel={"Safety":[], "Target":[], "Reach":[], "High Reach":[]}

    app.questions = ["What is your name?", 
    "What is your intended major?","What is your GPA? (Scaled to 4.0 Scale)", 
    "What is your SAT Math Score? (N/A if providing ACT)", "What is your SAT EBRW Score? (N/A if providing ACT)", 
    "What is your ACT Composite Score? (N/A if providing SAT)", 
    "How far from your current location would you be willing to study?",
    "How important is financial aid to you on a scale of 1 to 5?"]
    app.answers=[]
    app.answer="" 
    app.i=0
    
    app.listOfEssays=[]
    app.favorites=[]
    app.printText=[]
    

def timerFired(app):
    
    if app.isSavedBanner:
        time.sleep(5)
        app.isSavedBanner=False
    

def mousePressed(app, event):
    if app.isSplashScreen:
        if ((3*app.width/8 <= event.x <= 5*app.width/8) and
            (app.height/2 <= event.y <= 5*app.height/8)):
            app.isSplashScreen = False
            app.isLoginScreen = True
    if app.isLoginScreen:
        # If Clicked Within Username Box
        if ((app.width/2-200)<=event.x<=(app.width/2+200) and 
        ((app.height/2-50)-25)<=event.y<=((app.height/2-50)+25)):
            app.enteringUsername=True
            app.enteringPassword=False
            app.username=""
        # If Clicked Within Password Box
        if ((app.width/2-200)<=event.x<=(app.width/2+200) and 
        ((app.height/2+50)-25)<=event.y<=((app.height/2+50)+25)):
            app.enteringPassword=True
            app.enteringUsername=False
            app.password=""
        
    if app.isDashboardScreen:
        #If Clicked within College Search Tab
        margin = 20
        topmargin = app.height/4
        cellHeight = (3*app.height/4 - 3*margin)/2
        cellWidth = (app.width - 4*margin)/3

        x0 = margin*(2)+1*cellWidth
        x1 = margin*(2)+(2)*cellWidth
        y0 = topmargin+margin*(2)+1*cellHeight
        y1 = topmargin+margin*(2)+(2)*cellHeight
        if x0<=event.x<=x1 and y0<=event.y<=y1:
            app.isDashboardScreen=False
            app.isCollegeSearchTab=True


        xa = margin*(1+1)+1*cellWidth
        xb = margin*(1+1)+(1+1)*cellWidth
        ya = topmargin+margin*(0+1)+0*cellHeight
        yb = topmargin+margin*(0+1)+(0+1)*cellHeight
        if xa<=event.x<=xb and ya<=event.y<=yb:
            app.isDashboardScreen=False
            app.isEssayWritingTab=True

        xc = margin*(0+1)+0*cellWidth
        xd = margin*(0+1)+(0+1)*cellWidth
        yc = topmargin+margin*(1+1)+1*cellHeight
        yd = topmargin+margin*(1+1)+(1+1)*cellHeight
        if xc<=event.x<=xd and yc<=event.y<=yd:
            app.isDashboardScreen=False
            app.isListScreen=True
        

        xe = margin*(2+1)+2*cellWidth
        xf = margin*(2+1)+(2+1)*cellWidth
        ye = topmargin+margin*(0+1)+0*cellHeight
        yf = topmargin+margin*(0+1)+(0+1)*cellHeight
        if xe<=event.x<=xf and ye<=event.y<=yf:
            app.isDashboardScreen=False
            app.isScheduleTab=True
            loadDueDates(app)
            convertDates(app)

        x2 = margin*(0+1)+0*cellWidth
        x3 = margin*(0+1)+(0+1)*cellWidth
        y2 = topmargin+margin*(0+1)+0*cellHeight
        y3 = topmargin+margin*(0+1)+(0+1)*cellHeight
        if x2<=event.x<=x3 and y2<=event.y<=y3:
            app.isDashboardScreen=False
            app.isProfileTab=True

        x00 = margin*(2+1)+2*cellWidth
        x11 = margin*(2+1)+(2+1)*cellWidth
        y00 = topmargin+margin*(1+1)+1*cellHeight
        y11 = topmargin+margin*(1+1)+(1+1)*cellHeight
        if x00<=event.x<=x11 and y00<=event.y<=y11:
            app.isDashboardScreen=False
            app.isMatchScreen=True
            sortSchools(app)

        
    if app.isCollegeSearchTab:
        #If Clicked within Search Bar
        if ((app.width/2-300<=event.x<=app.width/2+300) and 
        (app.height/2-25<=event.y<=app.height/2+25)):
            app.enteringCollege=True
            app.university=""
    if app.isCollegeSearchResultTab:
        if 75-50<=event.x<=75+50 and 75-50<=event.y<=75+50:
            addToFavorites(app)
        if (app.width-(75-50)<=event.x<=app.width-(75+50) and 
            75-50<=event.y<=75+50):
            app.isCollegeSearchResultsTab=False
            app.isDashboardScreen=True
    if app.isEssayWritingTab:
        listOfEssays(app)
    if app.isEssayEditor:
        topmargin=app.height/4
        margin = 20
        if (topmargin<=event.y<=app.height-margin and 
        margin<=event.x<=app.width-margin) and app.index=="n" or app.index=="N":
            app.isEditingFilename=True
        elif (topmargin<=event.y<=app.height-margin and 
        margin<=event.x<=app.width-margin):
            app.isEnteringEssay=True
    if app.isEnteringEssay:       
        readFile(app)

def keyPressed(app, event):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if app.isLoginScreen:
        #If entering username, collects keystrokes and accepts as username
        if app.enteringUsername:
            if event.key=="Delete":
                if app.password!="":
                    app.password=app.password[:-1]
            elif event.key=="Tab":
                app.enteringUsername=False
                app.enteringPassword=True
            elif len(event.key)==1:
                app.username+=event.key
        if app.enteringPassword:
            if event.key == "Enter":
                app.password[:len(app.password)-6]
                app.enteringPassword=False
                authenticate(app)
                app.isDashboardScreen=True
            elif event.key=="Delete":
                if app.password!="":
                    app.password=app.password[:-1]
            elif len(event.key)==1:
                app.password+=event.key
    if app.isCollegeSearchTab:
        if app.enteringCollege:
            if event.key == "Enter":
                app.university[:len(app.university)-6]
                loadCollegeData(app)
                app.isCollegeSearchTab=False
                app.isCollegeSearchResultTab=True
            elif event.key=="Delete":
                if app.university!="":
                    app.university=app.university[:-1]
            elif event.key=="Space":
                app.university+=" "
            elif event.key.isalpha():
                app.university+=event.key
    if app.isCollegeSearchResultTab:
        if event.key == "1":
            app.isCollegeSearchResultTab=False
            app.isDashboardScreen=True
        if event.key == "2":
            addToFavorites(app)
    if app.isEssayWritingTab:
        if event.key == "Escape":
            app.isEssayWritingTab=False
            app.isDashboardScreen=True
        if event.key=="n" or event.key=="N":
            app.isEssayWritingTab=False
            app.isEssayEditor=True
            app.index="n"
        else:
            if event.key in "1234567890":
                app.index=(event.key)
            elif event.key == "Enter":
                app.isEssayWritingTab=False
                app.isEssayEditor=True
            
    if app.isEssayEditor:
    
        if app.isEditingFilename:
            if event.key in alphabet:
                app.filename+=event.key
            elif event.key=="Enter":
                app.filename[:len(app.filename)-6]
                app.filename=app.filename[app.filename.find(": ")+2:]
                createFile(app)
                app.isEditingFilename=False
                app.isEnteringEssay=True
        elif app.isEnteringEssay:
            if event.key == "Enter":
                app.essayText+="\n"
            elif event.key=="Delete":
                if app.essayText!="":
                    app.essayText=app.essayText[:-1]
            elif event.key=="Space":
                app.essayText+=" "
            elif event.key=="Escape":
                writeFile(app)
                app.isSavedBanner==True
            elif event.key=="Tab":
                app.essayText+="    "
            elif event.key=="1":
                app.isEssayEditor=False
                app.isDashboardScreen=True
            elif event.key in alphabet:
                app.essayText+=event.key
    if app.isScheduleTab:
        if event.key in "0123":
            app.add=False
            app.plan=int(event.key)
        elif event.key=="Enter":
            app.add=True
        elif event.key=="Escape":
            app.isScheduleTab=False
            app.isDashboardScreen=True
    if app.isListScreen:
        if event.key=="1":
            app.isListScreen=False
            app.isDashboardScreen=True
    if app.isProfileTab:
        if event.key in alphabet:
            app.answer+=event.key
        if event.key in "1234567890":
            app.answer+=event.key
        if event.key=="Space":
            app.answer+=" "
        if event.key=="Enter":
            addAnswer(app)
        if event.key=="Delete":
            app.answer=app.answer[:-1]
        if event.key==".":
            app.answer+="."
        if event.key=="/":
            app.answer+="/"
        if event.key==" ":
            app.answer+=" "
        if event.key=="Escape":
            app.isProfileTab=False
            app.isDashboardScreen=True
    if app.isMatchScreen:
        if event.key=="Escape":
            app.isMatchScreen=False
            app.isDashboardScreen=True


def addAnswer(app):
    app.answers.append(app.answer)
    app.answer=""
       

def drawProfileScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Hit Escape to\n go Home",
    font="Arial 15 bold")

    
    pathWithFile = os.getcwd()+"/"+app.username+"/profile.txt"

    if os.path.isfile(pathWithFile):
        textX=app.width/2
        textY=app.height/16
        
        with open(pathWithFile, "rt") as fp:
            ans = fp.read()
        ansList=ans.splitlines()
        
        for x in range(len(app.questions)):
            canvas.create_text(textX, textY, text=f'{app.questions[x]}: {ansList[x]}',
                    font='Arial 25',
                    fill="black")
            textY+=40

    else:
        textX=app.width/2
        textY=app.height/16
        for x in range(len(app.questions)):
            canvas.create_text(textX, textY, text=f'{app.questions[x]}',
                    font='Arial 25',
                    fill="black")
            textY+=40
        
        canvas.create_rectangle(textX-300, textY+100, textX+300, textY+200, 
        fill="white")
    
        canvas.create_text(textX, textY+150,
                text=f'{app.answer}',
                font='Arial 30',
                fill="black")
        
        round_rectangle(app.width/2-100, 5*app.height/8, app.width/2+100, 
        5*app.height/8+50, 25, "light blue", canvas)
        canvas.create_text(app.width/2, 5*app.height/8+25,
                       text='Hit Enter to Add Answer',
                       font='Arial 20 bold',
                       fill="white")
        
        
def writeProfile(app):
    if len(app.answers)==len(app.questions):
        path = os.getcwd()+"/"+app.username
        pathWithFile = os.getcwd()+"/"+app.username+"/profile.txt"
        
        if os.path.isfile(pathWithFile):
            pass       
        else:
            try: 
                os.chdir(path)
                filename = "favorites.txt"
                with open(pathWithFile, "a") as fp:
                    for i in range(len(app.answers)):
                        fp.write(app.answers[i]+"\n")
                os.chdir('../')
            except OSError:
                print ("Creation of the directory failed")
            else:
                print ("Successfully created the directory")        

def drawMatchLevel(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
        3*app.height/16, 50, "light blue", canvas)
    canvas.create_text(app.width/2, app.height/8,
                    text="Countdown!",
                    font='Arial 30 bold',
                    fill="white")
        
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Hit Escape to\n go Home",
    font="Arial 15 bold")
     
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        textX=app.width/2
        textY=app.height/4
        
        for level in app.AdmissionLevel:
            canvas.create_text(textX, textY,
                    text=f'{level}: {listToString(app.AdmissionLevel[level])}',
                    font='Arial 30',
                    fill="black")
            textY+=45

def sortSchools(app):
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        for uni in favoritesList:
            getSchoolLevel(app, uni)
        
def getSchoolLevel(app, uni):
    collegeUnformatted = uni
    cL = collegeUnformatted.split()
    collegeFormatted=""
    for i in range(len(cL)):
        collegeFormatted+=cL[i]
        if (i+1!=len(cL)):
            collegeFormatted+="-"

    siteDefaultUrl = "https://www.collegedata.com/college/"
    collegeUrl = siteDefaultUrl+collegeFormatted
    
    driver = webdriver.Chrome(os.getcwd()+'/chromedriver')
    
    driver.get(collegeUrl)
    
    xp="//dt"
    t=driver.find_elements_by_xpath(xp)
    xp2="//dd"
    t2=driver.find_elements_by_xpath(xp2)
    
    
    pathWithFile = os.getcwd()+"/"+app.username+"/profile.txt"
    ansList=[]
    if os.path.isfile(pathWithFile):

        with open(pathWithFile, "rt") as fp:
            ans = fp.read()
        ansList=ans.splitlines()

    satmath=t2[6].text
    satavgmathscore=int(satmath[0:3])
    sat25mathscore=int(satmath[12:15])
    sat75mathscore=int(satmath[16:19])
    usm=ansList[3]

    satenglish=t2[7].text
    satavgengscore=int(satenglish[0:3])
    sat25engscore=int(satenglish[12:15])
    sat75engscore=int(satenglish[16:19])

    sat25=sat25mathscore+sat25engscore
    satavg=satavgmathscore+satavgengscore
    sat75=sat75mathscore+sat75engscore
    

    usebrw=ansList[4]

    act=t2[8].text
    actavg=int(act[0:2])
    act25=int(act[11:13])
    act75=int(act[14:16])

    

    ua=ansList[5]
    
    if ua=="N/A":
        userssatmath=int(usm)
        userssateng=int(usebrw)
        usersat=userssatmath+userssateng

        if usersat<sat25:
            app.AdmissionLevel["High Reach"].append(uni)
        if usersat>=sat25 and usersat<satavg:
            app.AdmissionLevel["Reach"].append(uni)
        if satavg<usersat<sat75:
            app.AdmissionLevel["Match"].append(uni)
        if usersat>=sat75:
            app.AdmissionLevel["Safety"].append(uni)
    else:
        usersact=int(ua)
        if usersact<act25:
            app.AdmissionLevel["High Reach"].append(uni)
        if usersact>=act25 and usersact<actavg:
            app.AdmissionLevel["Reach"].append(uni)
        if actavg<usersact<act75:
            app.AdmissionLevel["Match"].append(uni)
        if usersact>=act75:
            app.AdmissionLevel["Safety"].append(uni)
    driver.quit()
    
def addToFavorites(app):
    path = os.getcwd()+"/"+app.username
    pathWithFile = os.getcwd()+"/"+app.username+"/favorites.txt"
    print(pathWithFile)
    if os.path.isfile(pathWithFile):
        
        if not isFavorite(app):
            os.chdir(path)
            filename = "favorites.txt"
            with open(filename, "a") as fp:
                fp.write(app.university+"\n")  
            os.chdir('../')        
    else:
        try:
            
            os.chdir(path)
            filename = "favorites.txt"
            with open(pathWithFile, "a") as fp:
                fp.write(app.university+"\n")
            os.chdir('../')
        except OSError:
            print ("Creation of the directory failed")
        else:
            print ("Successfully created the directory")

def drawFavorite(app, canvas):
    canvas.create_oval(75-50,75-50,75+50,75+50, fill ="royal blue")
    canvas.create_text(75,75, text="On your list!", 
    font="Arial 15 bold", fill="white")

def isFavorite(app):
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        
        return app.university in favoritesList
    else:
        return False

def drawMyList(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Press 1 to\n go Home",
    font="Arial 15 bold")
    round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
        3*app.height/16, 50, "light blue", canvas)
    canvas.create_text(app.width/2, app.height/8,
                    text="Favorites List",
                    font='Arial 30 bold',
                    fill="white")
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        textX=app.width/2
        textY=app.height/4
        for s in favoritesList:
            canvas.create_text(textX, textY,
                    text=f'{s}',
                    font='Arial 30',
                    fill="black")
            textY+=45
    else:

        round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
        3*app.height/16, 50, "light blue", canvas)
        canvas.create_text(app.width/2, app.height/8,
                    text="You haven't added any schools to your list yet!",
                    font='Arial 30 bold',
                    fill="white")

def getDueDate(app, uni):
    collegeUnformatted = uni
    cL = collegeUnformatted.split()
    collegeFormatted=""
    for i in range(len(cL)):
        collegeFormatted+=cL[i]
        if (i+1!=len(cL)):
            collegeFormatted+="-"

    siteDefaultUrl = "https://www.collegedata.com/college/"
    collegeUrl = siteDefaultUrl+collegeFormatted
    
    driver = webdriver.Chrome(os.getcwd()+'/chromedriver')
    
    driver.get(collegeUrl)
    
    xp="//dt"
    t=driver.find_elements_by_xpath(xp)
    xp2="//dd"
    t2=driver.find_elements_by_xpath(xp2)
    duedate=t2[4].text
    driver.quit()
    return duedate
            
            
def loadDueDates(app):
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        
        for uni in favoritesList:
            if uni not in app.duedates:
                app.duedates[uni]=(getDueDate(app, uni))
        

def convertDates(app):
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        
        for uni in favoritesList:
            s=app.duedates[uni]
            l=s.split(" ")
            datestring=l[0][0:3]
            datestring+=" "
            datestring+=l[1]
            datestring+=" 2021"
            d=datetime.strptime(datestring, "%b %d %Y")
            duedate=d.date()
            print(duedate)
            today=datetime.now().date()
            delta=duedate-today
            app.tl[uni]=(delta.days)

        tl=sorted(app.tl, key=app.tl.get)
        for key in tl:
            app.timeleft[key]=app.tl[key]

        

def drawSchedule(app, canvas):
    
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
        3*app.height/16, 50, "light blue", canvas)
    canvas.create_text(app.width/2, app.height/8,
                    text="Countdown!",
                    font='Arial 30 bold',
                    fill="white")
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Hit Escape to\n go Home",
    font="Arial 15 bold")
     
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        textX=app.width/2
        textY=app.height/4
        
        for uni in app.timeleft:
            canvas.create_text(textX, textY,
                    text=f'{uni}: {app.duedates[uni]}-{app.timeleft[uni]} days',
                    font='Arial 30',
                    fill="black")
            textY+=50

        
def drawLine(app, canvas, i):
    path = os.getcwd()+"/"+app.username+"/favorites.txt"
    colors=["black", "red", "blue", "green"]
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            favs = fp.read()
        favoritesList=favs.splitlines()
        textX=app.width/2
        textY=app.height/4+45*i
        canvas.create_text(textX, textY,
                    text=f'{i+1}: {favoritesList[i]}',
                    font='Arial 30',
                    fill=colors[app.plan])
            
        
def drawSplashScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    round_rectangle(app.width/4, app.height/4, 3*app.width/4, 3*app.height/8,
                            50, "light blue", canvas)
    canvas.create_text(app.width/2, 5*app.height/16,
                       text='CollegeBuddy',
                       font='Arial 100 bold',
                       fill="white")
    round_rectangle(3*app.width/8, app.height/2, 5*app.width/8,
                                5*app.height/8, 50, "light blue", canvas)
    canvas.create_text(app.width/2, 9*app.height/16,
                       text='Start',
                       font='Arial 100 bold',
                       fill="white")

def drawLoginScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    #Login Title Text
    round_rectangle(app.width/4, app.height/4, 3*app.width/4, 3*app.height/8,
                            50, "light blue", canvas)
    canvas.create_text(app.width/2, 5*app.height/16,
                       text='Login/Create Account',
                       font='Arial 75 bold',
                       fill="white")
    #Username and Password Fields
    canvas.create_rectangle(app.width/2-200, (app.height/2-50)-25, app.width/2+200, 
    (app.height/2-50)+25, fill="white")
    canvas.create_text(app.width/2, app.height/2-50,
                       text=f'{app.username}',
                       font='Arial 25',
                       fill="black")
    canvas.create_rectangle(app.width/2-200, (app.height/2+50)-25, 
    app.width/2+200, (app.height/2+50)+25, fill="white")
    canvas.create_text(app.width/2, app.height/2+50,
                       text=f'{app.password}',
                       font='Arial 25',
                       fill="black")
    #Login Button
    round_rectangle(app.width/2-100, 5*app.height/8, app.width/2+100, 
    5*app.height/8+50, 25, "light blue", canvas)
    canvas.create_text(app.width/2, 5*app.height/8+25,
                       text='Enter',
                       font='Arial 50 bold',
                       fill="white")

def drawPasswordIncorrectPopUp(app, canvas):
    #Creates PopUp for when Passowrd is Incorrect
    round_rectangle(app.width/2-100, 7*app.height/8, app.width/2+100, 
    7*app.height/8+50, 25, "orange", canvas)
    canvas.create_text(app.width/2, 7*app.height/8+25,
                       text='Password Incorrect!',
                       font='Arial 20 bold',
                       fill="white")

def drawProfileComplete(app, canvas):
    #Creates PopUp for when ALL stats inputted
    if (len(app.questions)==len(app.answers)):
        round_rectangle(app.width/2-100, 7*app.height/8, app.width/2+100, 
        7*app.height/8+50, 25, "orange", canvas)
        canvas.create_text(app.width/2, 7*app.height/8+25,
                        text='Profile Complete',
                       font='Arial 20 bold',
                       fill="white")
    writeProfile(app)

def authenticate(app):
    path = os.getcwd()+"/"+app.username
    if os.path.isdir(path):
        pathWithFile=path+"/password.txt"
        if os.path.isfile(pathWithFile):
            with open(pathWithFile, "rt") as fp:
                actualPassword = fp.read()
            if app.password==actualPassword:
                app.isDashboardScreen = True
                app.isLoginScreen = False
            else:
                app.passwordIncorrectPopUp = True
    else:
        try:
            os.mkdir(path)
            os.chdir(path)
            filename = "password.txt"
            with open(filename, "w+") as fp:
                fp.write(app.password)
            os.chdir('../')
            app.isLoginScreen = False
            app.isDashboardScreen = True
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

#Not Yet Used  
def drawQuestionScreen(app, canvas):
    for i in range(len(app.questions)):
        canvas.create_text(app.width/4, 25*(i+2)+5,
                       text=f'{app.questions[i]}',
                       font='Arial 20',
                       fill="black")
        canvas.create_rectangle(3*app.width/4-200, 25*(i+1.5), 
        3*app.width/4+200, 25*(i+2.5), fill="white")

def drawDashboardScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
    3*app.height/16, 50, "light blue", canvas)
    canvas.create_text(app.width/2, app.height/8,
                       text=f'{app.username}'+"'s dashboard",
                       font='Arial 75 bold',
                       fill="white")
    margin = 20
    topmargin = app.height/4
    cellHeight = (3*app.height/4 - 3*margin)/2
    cellWidth = (app.width - 4*margin)/3
    tabnames = [["My profile", "My Essays", "My Schedule"], 
                ["My List", "College Search", "Find Matches"]]
    for row in range(3):
        for col in range(2):
            x0 = margin*(row+1)+row*cellWidth
            x1 = margin*(row+1)+(row+1)*cellWidth
            y0 = topmargin+margin*(col+1)+col*cellHeight
            y1 = topmargin+margin*(col+1)+(col+1)*cellHeight
            round_rectangle(x0,y0,x1,y1,50,"light blue",canvas)
            canvas.create_text((x0+x1)/2, (y0+y1)/2,
                       text=f'{tabnames[col][row]}',
                       font='Arial 75 bold',
                       fill="white")

def drawCollegeSearchTab(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")

    round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
    3*app.height/16, 50, "light blue", canvas)
    canvas.create_text(app.width/2, app.height/8,
                       text="Search a School!",
                       font='Arial 50 bold',
                       fill="white")
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    canvas.create_rectangle(app.width/2-300, app.height/2-25, 
                            app.width/2+300, app.height/2+25, fill="white")
    canvas.create_text(app.width/2, app.height/2,
                       text=f'{app.university}',
                       font='Arial 25',
                       fill="black")
    
    round_rectangle(app.width/2-100, 5*app.height/8, app.width/2+100, 
    5*app.height/8+50, 25, "light blue", canvas)
    canvas.create_text(app.width/2, 5*app.height/8+25,
                       text='Hit Enter to Search',
                       font='Arial 20 bold',
                       fill="white")

def infoScrape(app):
        collegeUnformatted = app.university
        cL = collegeUnformatted.split()
        collegeFormatted=""
        for i in range(len(cL)):
            collegeFormatted+=cL[i]
            if (i+1!=len(cL)):
                collegeFormatted+="-"

        siteDefaultUrl = "https://www.collegedata.com/college/"
        collegeUrl = siteDefaultUrl+collegeFormatted
        
        driver = webdriver.Chrome(os.getcwd()+'/chromedriver')
        
        driver.get(collegeUrl)

        admissionInfo = []
        admissionInfo.append("Admission Info:")
        for i in range(5):
            xp="//dt"
            t=driver.find_elements_by_xpath(xp)
            xp2="//dd"
            t2=driver.find_elements_by_xpath(xp2)
            try:
                s=t[i].text+": "+t2[i].text
                admissionInfo.append(s)
            except IndexError:
                return ["Your input was invalid and this university does not exist. Check for typos and formatting and try again! "]
            

        admittedStudentQualifications = []
        admittedStudentQualifications.append("Admitted Student Qualifications:")
        for i in range(5,9):
            xp="//dt"
            t=driver.find_elements_by_xpath(xp)
            xp2="//dd"
            t2=driver.find_elements_by_xpath(xp2)
            s=t[i].text+": "+t2[i].text
            admittedStudentQualifications.append(s)
        
        financialAidInfo = []
        financialAidInfo.append("Financial Aid/Assistance Info:")
        for i in range(9,15):
            xp="//dt"
            t=driver.find_elements_by_xpath(xp)
            xp2="//dd"
            t2=driver.find_elements_by_xpath(xp2)
            s=t[i].text+": "+t2[i].text
            financialAidInfo.append(s)
        driver.quit()
        return [admissionInfo,
        admittedStudentQualifications, financialAidInfo]
        
        
def loadCollegeData(app):
    app.printText=[]
    L=infoScrape(app)
    for subL in L:
        s=""
        for item in subL:
            s+=item
            s+="\n"
        app.printText.append(s)




def drawCollegeSearchResultTab(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Press 1 to\n go Home",
    font="Arial 15 bold")
    
    
    margin = 20
    topmargin = app.height/4
    cellHeight = (3*app.height/4 - 3*margin)
    cellWidth = (app.width - 4*margin)/3
    
    if len(app.printText)==1:
            canvas.create_text(app.width/2,app.height/2 ,
                       text=f'{app.printText[0]}',
                       font='Arial 30 bold',
                       fill="black") 
        
    else:

        round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
        3*app.height/16, 50, "light blue", canvas)
        canvas.create_text(app.width/2, app.height/8,
                        text=f'{app.university}'+" Fast Facts",
                        font='Arial 50 bold',
                        fill="white")
    
        canvas.create_oval(75-50,75-50,75+50,75+50,fill="light blue",
         outline="light blue")
        canvas.create_text(75,75, text="Press 2 to \nAdd to \nFavorites",
        font="Arial 15 bold")
        

        for row in range(3):
            for col in range(1):
                x0 = margin*(row+1)+row*cellWidth
                x1 = margin*(row+1)+(row+1)*cellWidth
                y0 = topmargin+margin*(col+1)+col*cellHeight
                y1 = topmargin+margin*(col+1)+(col+1)*cellHeight
                round_rectangle(x0,y0,x1,y1,50,"light blue",canvas)
                canvas.create_text((x0+x1)/2, (y0+y1)/2,
                        text=f'{app.printText[row]}',
                        font='Arial 20',
                        fill="black")           
def listOfEssays(app):
    path = os.getcwd()+"/"+app.username+"/essays"

    if os.path.isdir(path):
        x=1
        for filename in os.listdir(path):
            s = str(x)+": "+filename
            if s not in app.listOfEssays:
                x+=1
                app.listOfEssays.append(s)
    
          

def drawEssayWritingTab(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    path = os.getcwd()+"/"+app.username+"/essays"
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Hit Escape to\n go Home",
    font="Arial 15 bold")
    if os.path.isdir(path):
    
        textX=app.width/2
        textY=app.height/4
        round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
            3*app.height/16, 50, "light blue", canvas)
        canvas.create_text(app.width/2, app.height/8,
                    text="Your Saved Drafts\nType the number of the essay you want to work on\nPress N to create new draft",
                    font='Arial 30 bold',
                    fill="white",
                    justify=CENTER)
        
        for s in app.listOfEssays:
            canvas.create_text(textX, textY,
                    text=f'{s}',
                    font='Arial 30',
                    fill="black")
            textY+=45
            
    else:
        try:
            os.mkdir(path)
            round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
            3*app.height/16, 50, "light blue", canvas)
            canvas.create_text(app.width/2, app.height/8,
                        text="You haven't started any essays yet! Use the 'N' key to start drafting",
                        font='Arial 30 bold',
                        fill="white")
            
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

def createFile(app):
    
    
    path = os.getcwd()+"/"+app.username+"/essays"
    os.chdir(path)
   
    
    with open(app.filename, "w+") as fp:
        fp.write(app.essayText)
    pathWithFile=path+"/"+app.filename
        
    os.chdir('../')
    os.chdir('../')
    app.isEditingFilename=False
    app.isEnteringEssay=True
    
    app.index=0
    listOfEssays(app)


    
def drawEssayEditor(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="coral2")
    round_rectangle(app.width/2-500, app.height/16, app.width/2+500, 
            3*app.height/16, 50, "light blue", canvas)
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
    (75+50),fill="light blue", outline="light blue")
    canvas.create_text(app.width-75,75, text="Press 1 to\n go Home",
    font="Arial 15 bold")
    
    margin = 20
    topmargin = app.height/4
    if app.index=="n":
        path = os.getcwd()
        os.chdir(path)
        
        
        if app.isEnteringEssay:
            canvas.create_text(app.width/2, app.height/8,
                        text="Edit your essay! ",
                        font='Arial 35 bold',
                        fill="white")
            canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
            (75+50),fill="light blue", outline="light blue")
            canvas.create_text(app.width-75,75, text="Hit escape\n to save",
            font="Arial 15")
            index=int(app.index)
            filename=app.listOfEssays[index]
            listOfEssays(app)
            filename=filename[app.listOfEssays[index].find(" ")+1:]
            path = os.getcwd()+"/"+app.username+"/essays/"+filename
            if os.path.isfile(path):
                with open(pathWithFile, "rt") as fp:
                    app.essayText = fp.read()
                canvas.create_rectangle(margin, topmargin, app.width-margin, 
                app.height-margin, fill = "white")
                canvas.create_text(margin+15,topmargin+15,
                            text=f'{app.essayText}',
                            font='Arial 30 bold',
                            fill="black",
                            anchor=NW,
                            width = app.width-2*margin-30)
        else:
            
            canvas.create_rectangle(margin, topmargin, app.width-margin, 
            app.height-margin, fill = "white")
            canvas.create_text(margin+15,topmargin+15,
                    text=f'{app.filename}',
                    font='Arial 25 bold',
                    fill="black",
                    anchor=NW,
                    width = app.width-2*margin-30)
    else:
        canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
            (75+50),fill="light blue", outline = "light blue")
        canvas.create_text(app.width-75,75, text="Hit escape\n to Save",
            font="Arial 15 bold", fill="white")
        canvas.create_text(app.width/2, app.height/8,
                    text="Edit your essay! ",
                    font='Arial 35 bold',
                    fill="white")
        
        canvas.create_rectangle(margin, topmargin, app.width-margin, 
        app.height-margin, fill = "white")
        canvas.create_text(margin+15,topmargin+15,
                    text=f'{app.essayText}',
                    font='Arial 30 bold',
                    fill="black",
                        anchor=NW,
                        width = app.width-2*margin-30)

def drawSavedBanner(app, canvas):
    canvas.create_oval(app.width-(75-50),(75-50),app.width-(75+50),
            (75+50),fill="royal blue")
    canvas.create_text(app.width-75,75, text="Saved",
            font="Arial 15 bold", fill = "white")

def readFile(app):
    index=int(app.index)-1
    filename=app.listOfEssays[index]
    filename=filename[app.listOfEssays[index].find(": ")+2:]
    path = os.getcwd()+"/"+app.username+"/essays/"+filename
    if os.path.isfile(path):
        with open(path, "rt") as fp:
            app.essayText = fp.read()
    
    

def writeFile(app):
    index=int(app.index)-1
    print(index)
    filename=app.listOfEssays[index]
    filename=filename[app.listOfEssays[index].find(": ")+2:]
    path = os.getcwd()+"/"+app.username+"/essays/"+filename
    
    if os.path.isfile(path):
        
        with open(path, "wt") as fp:
            fp.write(app.essayText)
    app.isSavedBanner=True

#found and tweaked from     
#https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners

def round_rectangle(x1, y1, x2, y2, radius, fillcolor, canvas):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, fill=fillcolor, smooth=True)

def redrawAll(app, canvas):
    # This is the View 
    if app.isSplashScreen:
        drawSplashScreen(app, canvas)
    elif app.isLoginScreen:
        drawLoginScreen(app, canvas)
        if app.passwordIncorrectPopUp:
            drawPasswordIncorrectPopUp(app,canvas)
    elif app.isQuestionScreen:
        drawQuestionScreen(app, canvas)
    elif app.isDashboardScreen:
        drawDashboardScreen(app, canvas)
    elif app.isCollegeSearchTab:
        drawCollegeSearchTab(app, canvas)
    elif app.isCollegeSearchResultTab:
        drawCollegeSearchResultTab(app,canvas)
        if isFavorite(app):
            drawFavorite(app, canvas)
    elif app.isEssayWritingTab:
        drawEssayWritingTab(app, canvas)
    elif app.isEssayEditor:
        drawEssayEditor(app, canvas)
        if app.isSavedBanner:
            drawSavedBanner(app, canvas)
    elif app.isListScreen:
        drawMyList(app,canvas)
    elif app.isScheduleTab:
        drawSchedule(app,canvas)
    elif app.isProfileTab:
        drawProfileScreen(app, canvas)
        drawProfileComplete(app,canvas)
    elif app.isMatchScreen:
        drawMatchLevel(app, canvas)




def main():
    # This runs the app
    runApp(width=1792, height=1015)

if __name__ == '__main__':
    main()