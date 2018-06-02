from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
from TimeTable_main import Timetable
app = Flask(__name__)
CORS(app)

Table = Timetable()
Table.setup_newConnection("prodData.db")

@app.route("/", methods=["GET"])
def home():
    #returns the page for the front end
    return render_template("index.html")

#this function needed to add classes(physical)
@app.route("/addclass", methods=["post"])
def add_class():
    if request.is_json:
        print("json")
        content = request.get_json()
        newClass = content["name"]
        print(newClass)
        if len(newClass) <= 3 and len(newClass) > 0:
            Table.add_class(newClass)
            return jsonify(status="success")
        else:
            return jsonify(status="length of classname unaccptable")

    return jsonify(status="malformed request")





#returns all classe
@app.route("/viewclass", methods=["post","get",])
def return_cls():
    allClasses = Table.get_classes()
    return jsonify(allClasses)


@app.route("/ClassTimes", methods=["post","get"])
def get_classTimes():
    if request.is_json:
        content = request.get_json()
        className = content["class"]
        classTimes = Table.get_classesTimes(className)
        print(classTimes)
        if classTimes != False:
            return jsonify(status="Ok",
            classTimes=classTimes)
        else:
            return jsonify(status="class not found")
    else:
        return jsonify(status="invalid request")

#the validator which would return a tuple of accetable values
def validator(day,timetype):
    #the execution starts if day is in days list
    if day in Table.days and timetype.isdigit():
        print("at here")
        dayId = int(Table.days.index(day)) 
        if int(timetype) >= 0 and int(timetype) < 20:
            return (dayId,timetype)
        else:
            return False
    else:
        return False
        





#the classTime editor ,touted to be the hardest ever
@app.route("/modclasstimes", methods=["post","get"])
def mod_classesTimes():
    if request.is_json:
        content = request.get_json()
        print(content)
        #we start putting data json to variable here
        className = content["class"]
        day = content["day"]
        timetype = content["timetype"]
        subject = content["subject"]
        #pass content into validator
        is_valid = validator(day,timetype)
        if is_valid != False:
            print("is valid")
            #adding to db adder function this will return true if added sucees fully
            add_toDB = Table.add_classTimes(className,is_valid[0],is_valid[1],subject)
            print("add")
            if add_toDB != False:
                return jsonify(status="200")
            else:
                return jsonify(status="501")
        #if the provided data is invalid
        else:
            return jsonify(status="500")
    else:
        return("i need json data")


        
        


