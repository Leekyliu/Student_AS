import dialogflow_v2 as df
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask import g
import mysql.connector
import os


# set the project root directory as the static folder, you can set others.
app = Flask(__name__)
CORS(app)




class Mainpage:
    def invaildUnitCode(self,coursecode):
        filename = "unit_file/Unit.txt"
        res = ''
        if os.path.exists(filename) == False:
            with open(filename,"a") as f:
                f.write("Unit Code needed '{}'\n".format(coursecode))
                res = "Sorry the course haven't been recorded yet. We will update soon"
                f.close
        
        else:
            flag = 0
            f = open(filename,"r")
            lines = f.readlines()
            for lines in lines:
                if coursecode in lines:
                    res = "We have already received similar query and we will update soon"
                    f.close
                    flag = 1
                    break
            if flag == 0:  
                f = open(filename,"a")
                f.write("Unit Code needed '{}'\n".format(coursecode))
                res = "Sorry the course haven't been recorded yet. We will update soon"
                f.close
        cur = self.mydb.cursor()
        cur.execute("UPDATE intent_frequency SET invaildUnitCode=invaildUnitCode+1")
        self.mydb.commit()
        
        return res
                


    def invaildIntent(self,intent):

        filename = "intent_file/Intent.txt"
        res = ''
        if os.path.exists(filename) == False:
            with open(filename,"a") as f:
                f.write("Intent needed '{}'".format(intent))
                res = "We never encountered this situation. We will update soon"
                f.close
        
        else:
            flag = 0
            f = open(filename,"r")
            lines = f.readlines()
            for lines in lines:
                if intent.text.text in lines:
                    res = "We have already received similar query and will update soon"
                    f.close
                    flag = 1
                    break
            if flag == 0:  
                f = open(filename,"a")
                f.write("Intent needed '{}'".format(intent))
                res = "We never encountered this situation. We will update soon"
                f.close

        cur = self.mydb.cursor()
        cur.execute("UPDATE intent_frequency SET invaildIntent=invaildIntent+1")
        self.mydb.commit()
        return res

        



    def offerSemester(self,offer):

        coursecode = offer.query_result.parameters["CourseCode"]
        semester = offer.query_result.parameters["semesterChoice"]
        if len(coursecode) == 0:
            res = "Sorry the course code is invaild"

        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT Offered FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                res = self.invaildUnitCode(coursecode)
            
            else:
                if semester != "":
                    if row[0] == semester:
                        res = "Yes, it will open in '{}".format(semester)

                    else:
                        res = "No, it will open in '{}'".format(row[0])
                else:
                    res = "{} will be open in {}".format(coursecode,row[0])
                
                cur.execute("UPDATE intent_frequency SET OfferSemester=OfferSemester+1")
                self.mydb.commit()
                
        return res





    def unitInfo(self,offer):

        coursecode = offer.query_result.parameters["CourseCode"]
        
        if len(coursecode) == 0:
            res = "Sorry the course code is invaild"

        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT * FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                res = self.invaildUnitCode(coursecode)

        
            else:
                res =  "Unit {} is {} in {} faculty which offered in {} and it is {} level".format(row[5],row[6],row[0],row[4],row[3])
    
        
            cur.execute("UPDATE intent_frequency SET UnitInfo=UnitInfo+1")
            self.mydb.commit()
        
        return res


    def unitWeb(self,offer):
        coursecode = offer.query_result.parameters["CourseCode"]
        res = ''
        if len(coursecode) == 0:
                res = "Sorry the course code is invaild"

        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT More_Info FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()

            if row is None:
                res = self.invaildUnitCode(coursecode)
            
            else:
                res = "You can get more information here: {}".format(row[0])
                cur.execute("UPDATE intent_frequency SET UnitWeb=UnitWeb+1")
                self.mydb.commit()
       

        return res       
    


    def unitName(self,offer):
        coursecode = offer.query_result.parameters["CourseCode"]
        if len(coursecode) == 0:
            res =  "Sorry the course code is invaild"
        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT Unit_Name FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                self.invaildUnitCode(coursecode)
            else:
                res = "{} name is {}".format(coursecode,row[0])
            cur.execute("UPDATE intent_frequency SET UnitName=UnitName+1")
            self.mydb.commit()
        return res

    def areaUnit(self,offer):
        coursecode = offer.query_result.parameters["CourseCode"]
        res = ''
        if len(coursecode) == 0:
            res = "Sorry the course code is invaild"
        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT Area_of_Study FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                res = self.invaildUnitCode(coursecode)
            
            else:
                res = "The area of unit {} is {}".format(coursecode, row[0])
            cur.execute("UPDATE intent_frequency SET AreaStudyofUnit=AreaStudyofUnit+1")
            self.mydb.commit()
        return res


    def get_reply(self,user_input):
        self.mydb = mysql.connector.connect(
        host="mysql-test-main.cdhjcu6guj5i.ap-southeast-2.rds.amazonaws.com",
        user="admin",
        passwd="0987654321!",
        database='4712project'
        )

        #Create a dialogflow client 
        client = df.SessionsClient()

        project_id = "testflow-uidytk"

        
        
        session = client.session_path(project_id,123)
        textinput = df.types.TextInput(text=user_input,language_code="en")
        query = df.types.QueryInput(text=textinput)

        offer = client.detect_intent(session,query)

        intent = offer.query_result.intent.display_name
        if intent == "Default Welcome Intent":
            return offer.query_result.fulfillment_text
            
        
        if intent == "OfferSemester":
            res = self.offerSemester(offer)
            return res

        if intent =="UnitName":
            res = self.unitName(offer)
            return res

        if intent == "AreaStudyofUnit":
            res = self.areaUnit(offer)
            return res

        if intent == "UnitInfo":
            res =self.unitInfo(offer)
            return res

            

        if intent == "UnitWeb":
            res = self.unitWeb(offer)
            return res

        if intent == "Book_init":
            cur = self.mydb.cursor()
            cur.execute("UPDATE intent_frequency SET Book=Book+1")
            self.mydb.commit()
            return offer.query_result.fulfillment_text

        if intent == "Book_type":
            return offer.query_result.fulfillment_text
       
        if intent == "Book_time":
            return offer.query_result.fulfillment_text
        
        if intent == "Book_place":
            room = offer.query_result.output_contexts[0].parameters["Room_type"]
            time = offer.query_result.output_contexts[0].parameters["date-time"][0]["date_time"]
            place = offer.query_result.output_contexts[0].parameters["usyd_location"]
            cur = self.mydb.cursor()
            cur.execute("SELECT room FROM Booking WHERE time = '{}' and place ='{}'".format(time,place))
            row = cur.fetchone ()
            res = ''
            if row != None:
                res = "Sorry, the room is occupied at that time."
                return res
            else:
                sql = "INSERT IGNORE INTO Booking(room,time,place) VALUES (%s, %s, %s)"
                val = (room,time,place)
                
                try:
                    cur.execute(sql, val)
                    self.mydb.commit()
                    res = offer.query_result.fulfillment_text +'. '+ room + " at " + time + " in " + place+'.'
        
                except Exception as err:
                    res = "Sorry, the room is occupied at that time."
            
            return res

        #small talk training happen here
        if intent =='':
            cur = self.mydb.cursor()
            cur.execute("UPDATE intent_frequency SET small_talk=small_talk+1")
            self.mydb.commit()
            return offer.query_result.fulfillment_text

        if intent == "Default Fallback Intent":
            res = self.invaildIntent(query)
            return res
        

        if intent == "about agent":
            cur = self.mydb.cursor()
            cur.execute("UPDATE intent_frequency SET Agent=Agent+1")
            self.mydb.commit()
            return offer.query_result.fulfillment_text


        if intent == "About users":
            cur = self.mydb.cursor()
            cur.execute("UPDATE intent_frequency SET Users=Users+1")
            self.mydb.commit()
            return offer.query_result.fulfillment_text


        if intent == "End":
            cur = self.mydb.cursor()
            cur.execute("UPDATE intent_frequency SET End=End+1")
            self.mydb.commit()
            return offer.query_result.fulfillment_text

    

@app.after_request
def after_request(resp):
    resp.headers["Access-Control-Allow-Origin"] = '*'
    request_headers = request.headers.get("Access-Control-Request-Headers")
    resp.headers["Access-Control-Allow-Headers"] = request_headers
    resp.headers['Access-Control-Allow-Methods'] = "POST, OPTIONS"
    return resp

@app.route('/v1/msg', methods=['POST'])
def message():
    message = request.json.get('userMessage')
    reply_msg = Mainpage().get_reply(str(message))
    response = {
        'message': reply_msg,
    }
    return jsonify(response), 200

@app.route('/addUnitFunction', methods=['POST'])
def addUnitFunction():
    db = mysql.connector.connect(
    host="mysql-test-main.cdhjcu6guj5i.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    passwd="0987654321!",
    database='4712project'
    )
    Faculty = request.form['Faculty']
    AreaOfStudy = request.form['AreaOfStudy']
    AreaOfStudyCode = request.form['AreaOfStudyCode']
    Level = request.form['Level']
    Offered = request.form['Offered']
    UnitCode = request.form['UnitCode']
    UnitName = request.form['UnitName']
    MoreInfo = request.form['MoreInfo']
    cur = db.cursor()
    sql = "INSERT INTO Unit_details (Faculty, Area_of_Study,Area_of_Study_Code, Level, Offered, Unit_Code, Unit_Name, More_Info) VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"
    val = (Faculty,AreaOfStudy,AreaOfStudyCode,Level,Offered,UnitCode,UnitName,MoreInfo)
    try:
        cur.execute(sql, val)
        db.commit()
       
    except Exception as err:
        print(err)
        return 'Fail'
    
    return 'Success'

@app.route('/view_frequency',methods=['GET'])
def viewFrequency():
    db = mysql.connector.connect(
    host="mysql-test-main.cdhjcu6guj5i.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    passwd="0987654321!",
    database='4712project'
    )
    cur = db.cursor()
    cur.execute("SELECT * FROM intent_frequency WHERE id = 1")
    row = cur.fetchone ()
    return jsonify(res=row)

@app.route('/booking_list',methods=['GET'])
def viewBooking():
    db = mysql.connector.connect(
    host="mysql-test-main.cdhjcu6guj5i.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    passwd="0987654321!",
    database='4712project'
    )
    cur = db.cursor()
    cur.execute("SELECT * FROM Booking")
    row = cur.fetchall()
    return jsonify(res=row)
    



@app.route('/script/<path:path>')
def send_js(path):
    return send_from_directory("script", path)

@app.route('/style/<path:path>')
def send_static(path):
    return send_from_directory("style", path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory("images", path)

@app.route('/')
def index():
    return send_from_directory("template", "chatbox.html")

@app.route('/staff')
def staffHomepage():
    return send_from_directory("template","staff.html") 
@app.route('/viewIntent')
def viewIntent():
    return send_from_directory("template","viewIntent.html")

@app.route('/intent_file/<path:path>')
def viewIntent_txt(path):
    return send_from_directory("intent_file",path) 
    
@app.route('/unit_file/<path:path>')
def viewUnit_txt(path):
    return send_from_directory("unit_file",path) 

@app.route('/viewUnit')
def viewUnit():
    return send_from_directory("template","viewUnit.html")
@app.route('/addUnit')
def addUnit():
    return send_from_directory("template","addUnit.html")
@app.route('/addIntent')
def addIntent():
    return send_from_directory("template","addIntent.html")
@app.route('/checkBook')
def checkBook():
    return send_from_directory("template","checkBook.html")
@app.route('/checkDia')
def checkDia():
    return send_from_directory("template","checkDia.html")




if __name__ == "__main__":
    # mainloop()
    # app.run(debug=True, host='localhost', port=15888)
     app.run(debug=True, host='ec2-3-104-75-184.ap-southeast-2.compute.amazonaws.com', port=16888)