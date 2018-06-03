import sqlite3

#define the main class for the Timetable functions
class Timetable:

    

    #define self at beginning
    def __init__(self):
        self.db_name = None
        self.subjects =None
        self.classes = None
        self.days  = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
        pass

    def connect_db(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            c = self.conn.cursor()
            print("succesful")
            return c
        except:
            return(False)



    def build_indexes(self,c):
        cursor  = c
        #get all the rows in subjects_table
        cursor.execute("select subject_name from subject_table")
        self.subjects = [item[0] for item in cursor.fetchall()] # i dont understand how this works got from so
        #now get the classess
        cursor.execute("select class_name from classes")
        self.classes = [item[0] for item in cursor.fetchall()]
        #print(self.subjects[0])
        return(True)




    def setup_newConnection(self,dbName):
        '''this function is required to set the db name  and build the indexes for the subjects and the classes'''
        self.db_name = dbName 
        cursor = self.connect_db()
        if cursor != False :
            indexes = self.build_indexes(cursor)
            if indexes:
                return True
                self.disconnect_db(1)
        else:
            self.disconnect_db(1)
            return(False)
            




    

    def disconnect_db(self,action):
        #this will disconnect the db
        if action:
            self.conn.commit()
            self.conn.close()
        if not action:
            self.conn.close()

        
    
    def create_db(self, db_Filename):
        #this functions creates the database for the timetable with the filename of value of dbname
        print("creating database file with name  {0}.db".format(db_Filename))
        filename = db_Filename + ".db"
        open(filename, "w+" )
        self.db_name = filename
        c = self.connect_db()
        #special function to connect to db

        if c != False:
            #creating tables for databse
            #######################################
            c.execute("drop table if exists classes")
            c.execute("drop table if exists classes_table")
            c.execute('''CREATE TABLE classes
                        (class_id integer primary key AUTOINCREMENT,class_name text)''') #
            ######################################
            c.execute('''create table classes_table
                        (weekday int,
                         subject_id,
                         timetype int,
                         id integer PRIMARY KEY AUTOINCREMENT,
                         class_id int ,
                         FOREIGN KEY(class_id) REFERENCES classes(class_id)
                         FOREIGN KEY(subject_id) REFERENCES subject_table(subject_id)
                         )
                         ''') #creates table to store the timetable AKA main table 
            #######################################
            c.execute('''create table subject_table 
                        (subject_name text,
                        subject_id integer primary key AUTOINCREMENT
                        )
                        ''')           #creates table to store subjects
            #######################################
            #adding the default subjects into table
            self.subjects = ["physics","maths","dhivehi","biology","chemistry","islam","english"]
            
            for i in self.subjects:
                c.execute("insert into subject_table (subject_name) values(?)",[i])


            self.disconnect_db(1)
            
        else:
            print("error creating tables in created files")
            


        


        return(True)


    def add_class(self,className):
        cursor = self.connect_db()
        if cursor != False:
            cursor.execute("insert into classes(class_name) values(?)",[className])
            self.build_indexes(cursor)
            self.disconnect_db(1)
            return(True)
        else:
            self.disconnect_db(1)
            return(False)

    
    #this function does the checking
    def check_exists(self,className,weekday,timeType,subject,classID,subjectID):
        cursor = self.connect_db()
        if cursor :
            print("select * from classes_table where weekday ={0} AND subject_id ={1} AND timetype={2} AND class_id={3};".format(weekday,subjectID,timeType,classID))
            cursor.execute("select * from classes_table where weekday ={0}  AND timetype={2} AND class_id={3};".format(weekday,subjectID,timeType,classID))
            rows = cursor.fetchall()
            print(len(rows))
            self.disconnect_db(1)
        if len(rows) >= 1:
            return True
        else:
            return False
            


    
#this function adds classes to db if class exists it replaces it
    def add_classTimes(self,className,weekday,timeType,subject):
        if className in self.classes and subject in self.subjects:
            #checking for previous records of same time
            classID = int(self.classes.index(className)) + 1 
            subjectID = int(self.subjects.index(subject)) + 1
            check = self.check_exists(className,weekday,timeType,subject,classID,subjectID)
            print(check)
            cursor = self.connect_db()
            if cursor != False and check == False:
                print("a class does not exist for the time")
                cursor.execute("insert into classes_table (weekday,subject_id,timetype,class_id) values(?,?,?,?)",[weekday,subjectID,timeType,classID])
                self.disconnect_db(1)
                return(True)
            elif cursor != False and check == True:
                print("a class already exists for the following time updating db")
                cursor.execute("update classes_table set subject_id = {0} where class_id={1} AND timetype={2} AND weekday={3}".format(subjectID,classID,timeType,weekday))
                self.disconnect_db(1)
                return(True)
            else:
                print("501")
                return False
        else:
            print(className,subject)
            return False



#returns classes for given class returns complete week when weekday is 0
    def get_classesTimes(self,className):
        if className in self.classes:
            classID = int(self.classes.index(className)) + 1
            cursor = self.connect_db()
            if cursor != False:
                classes ={}
                for i in range(0,7):
                    cursor.execute("select subject_id from classes_table where class_id={0} AND weekday={1} order by timetype".format(classID,i))
                    rows = cursor.fetchall()
                
                    #yes it gets not beautiful but bear with me this is a must
                    textSubjects = []
            
                    for n in range(0,len(rows)):
                        rowInteger = int(rows[n][0])
                        textSubjects.append(self.subjects[rowInteger - 1])

                
                    classes[self.days[i]] = textSubjects
                self.disconnect_db(0)
                return classes

               
        else:
            return False


#return a list of all classes
    def get_classes(self):
        cursor = self.connect_db()
        if cursor != False:
            cursor.execute("select class_name from classes")
            rows = cursor.fetchall()
            classNames = []
            for i in range(0,len(rows)):
                classNames.append(rows[i][0])

            #print(rows)
            return classNames
        return False        





