import dialogflow_v2 as df
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os


# set the project root directory as the static folder, you can set others.
app = Flask(__name__)
CORS(app)




class Mainpage:
    def invaildUnitCode(self,coursecode):
        filename = "Unit.txt"
        res = ''
        if os.path.exists(filename) == False:
            with open(filename,"a") as f:
                f.write("Unit Code needed '{}'\n".format(coursecode))
                res = "Sorry the course haven't been recorded yet. We will update soon"
                f.close()

            
        else:
            flag = 0
            f = open(filename,"a")
            lines = f.readlines()
            for lines in lines:
                if coursecode in lines:
                    res = "We have already received similar query and will update soon"
                    f.close()
                    flag = 1
                    break
            if flag == 0:  
                f.write("Unit Code needed '{}'\n".format(coursecode))
                res = "Sorry the course haven't been recorded yet. We will update soon"
                f.close()
        return res
            


    def invaildIntent(self,intent):

        filename = "Intent.txt"
        res = ''
        if os.path.exists(filename) == False:
            with open(filename,"a") as f:
                f.write("Intent needed '{}'".format(intent))
                res = "We never encountered this situation. We will update soon"
                f.close()

        else:
            flag = 0
            f = open(filename,"a")
            lines = f.readlines()
            for lines in lines:
                if intent.text.text in lines:
                    res = "We have already received similar query and will update soon"
                    f.close()
                    flag = 1
                    break
            if flag == 0:  
                f.write("Intent needed '{}'".format(intent))
                res = "We never encountered this situation. We will update soon"
                f.close()
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
                self.info_flag = 1
                self.course = coursecode
                if semester != "":
                    if row[0] == semester:
                        res = "Yes, it will open in '{}".format(semester)

                    else:
                        res = "No, it will open in '{}'".format(row[0])
                else:
                    res = "{} will be open in {}".format(coursecode,row[0])
                

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
                self.info_flag = 1
                self.course = coursecode
        
        return res


    def unitWeb(self,offer):
        coursecode = offer.query_result.parameters["CourseCode"]
        res = ''
        if len(coursecode) == 0:
            if self.info_flag == 1:
                cur = self.mydb.cursor()
                cur.execute("SELECT More_Info FROM Unit_details WHERE Unit_Code = '{}'".format(self.course))
                row = cur.fetchone ()
                res = "You can get more information here: {}".format(row[0])
            else:
                res = "Sorry the course code is invaild"

        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT More_Info FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()

            if row == None:
                res = self.invaildUnitCode(coursecode)
            
            else:
                res = "You can get more information here: {}".format(row[0])
       
        self.info_flag = 0
        self.course = None
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
                self.info_flag = 1
                self.course = coursecode
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
                res = "The area of unit {} is {}".format(coursecode,row[0])
                self.info_flag = 1
                self.course = coursecode
        return res


    def mainloop(self):
        while True:
        
            user_input=input()

            # handle loop

    def get_reply(self,user_input):
        #Create user input to Google
        # user_input = "Will SOIL2005 open in semester 1"
        self.mydb = mysql.connector.connect(
        host="mysql-test-main.cdhjcu6guj5i.ap-southeast-2.rds.amazonaws.com",
        user="admin",
        passwd="0987654321!",
        database='4712project'
        )

        #Create a dialogflow client 
        client = df.SessionsClient()

        project_id = "testflow-uidytk"


        self.info_flag = 0
        self.course = None
        
        session = client.session_path(project_id,123)
        textinput = df.types.TextInput(text=user_input,language_code="en")
        query = df.types.QueryInput(text=textinput)

        offer = client.detect_intent(session,query)

        intent = offer.query_result.intent.display_name
        if intent == "Default Welcome Intent":
            print(offer.query_result.fulfillment_text)
            return offer.query_result.fulfillment_text
            
        
        # print("000000000000000000",offer.query_result)
        #print("intent is ",intent)
        if intent == "OfferSemester":
            print(offer.query_result.fulfillment_text)
            res = self.offerSemester(offer)
            return res
            # return offer.query_result.fulfillment_text

        if intent =="UnitName":
            print(offer.query_result.fulfillment_text)
            res = self.unitName(offer)
            return res

        if intent == "AreaStudyofUnit":
            print(offer.query_result.fulfillment_text)
            res = self.areaUnit(offer)
            return res

        if intent == "UnitInfo":
            res =self.unitInfo(offer)
            return res

            

        if intent == "UnitWeb":
            res = self.unitWeb(offer)
            return res

        #small talk training happen here
        if intent =='':
            self.info_flag = 0
            self.course = None
            return offer.query_result.fulfillment_text

        if intent == "Default Fallback Intent":
            self.invaildIntent(query)
            self.info_flag = 0
            self.course = None
            return offer.query_result.fulfillment_text
        

        if intent == "about agent":
            self.info_flag = 0
            self.course = None
            return offer.query_result.fulfillment_text


        if intent == "About users":
            self.info_flag = 0
            self.course = None
            return offer.query_result.fulfillment_text


        if intent == "End":
            self.info_flag = 0
            self.course = None
            return offer.query_result.fulfillment_text
            # break
        
            # coursecode = offer.query_result.parameters["CourseCode"]
            # semester = offer.query_result.parameters["semesterChoice"]
            # # print("type is ",type(coursecode))
            # cur = self.mydb.cursor()
            # cur.execute("SELECT Offered FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            # row = cur.fetchone ()
            # if row == None:
            #     print("Sorry I don't know the answer")
            # # print("@@@@@@@@@@@@@@@@@@@@@@@@@@",row,"*********",row[0])
            # else:
            #     if semester != "":
            #         if row[0] == semester:
            #             print("Yes, it will open in '{}".format(semester))
            #         else:
            #             print("No, it will open in '{}'".format(row[0]))
            #     else:
            #         print("{} will be open in {}".format(coursecode,row[0]))
            # print("&&&&&&&&",row)
            # print("&&&&&&&&",type(row))
            # # response = fulfillment_messages

                # # return "id = {}, name = {}, qu = {}".format(row[0],row[1],row[2])

                    # print("####",coursecode)


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

if __name__ == "__main__":
    # mainloop()
    app.run(debug=True, host='localhost', port=15888)