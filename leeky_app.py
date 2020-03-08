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
                # print("Sorry the course haven't been recorded yet. We will update soon")
                res = "Sorry the course haven't been recorded yet. We will update soon"
                f.close()
                return res
            
        else:
            flag = 0
            f = open(filename,"r")
            lines = f.readlines()
            for lines in lines:
                if coursecode in lines:
                    # print("We have already received similar query and will update soon")
                    res = "We have already received similar query and will update soon"
                    f.close()
                    flag = 1
                    break
            if flag == 0:  
                f = open(filename,"a")
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
            return res
        else:
            flag = 0
            f = open(filename,"r")
            lines = f.readlines()
            for lines in lines:
                if intent.text.text in lines:
                    res = "We have already received similar query and will update soon"
                    f.close()
                    flag = 1
                    break
            if flag == 0:  
                f = open(filename,"a")
                f.write("Intent needed '{}'".format(intent))
                res = "We never encountered this situation. We will update soon"
                f.close()
            return res

        



    def offerSemester(self,offer):

        coursecode = offer.query_result.parameters["CourseCode"]
        semester = offer.query_result.parameters["semesterChoice"]
        if len(coursecode) == 0:
            res = "Sorry the course code is invaild"
            # print("Sorry the course code is invaild")
            return res
        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT Offered FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                res = self.invaildUnitCode(coursecode)
                return res
            
            else:
                if semester != "":
                    if row[0] == semester:
                        res = "Yes, it will open in '{}".format(semester)
                        # print("Yes, it will open in '{}".format(semester))
                        return res
                    else:
                        res = "No, it will open in '{}'".format(row[0])
                        # print("No, it will open in '{}'".format(row[0]))
                        return res
                else:
                    res = "{} will be open in {}".format(coursecode,row[0])
                    # print("{} will be open in {}".format(coursecode,row[0]))
                    return res





    def unitInfo(self,offer):

        coursecode = offer.query_result.parameters["CourseCode"]
        
        if len(coursecode) == 0:
            res = "Sorry the course code is invaild"
            return res, None, self.info_flag
        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT * FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                res = self.invaildUnitCode(coursecode)
                return res, None, self.info_flag
            
            else:
                res =  "Unit {} is {} in {} faculty which offered in {} and it is {} level".format(row[5],row[6],row[0],row[4],row[3])
                self.info_flag = 1
                return res,coursecode,self.info_flag


    def unitWeb(self,offer,course):
        coursecode = offer.query_result.parameters["CourseCode"]
        res = ''
        if self.info_flag == 1:
            if len(coursecode) == 0:
                cur = self.mydb.cursor()
                cur.execute("SELECT More_Info FROM Unit_details WHERE Unit_Code = '{}'".format(self.course))
                row = cur.fetchone ()
                res = "You can get more information here: {}".format(row[0])
            
            
            
            else:

                cur = self.mydb.cursor()
                cur.execute("SELECT More_Info FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
                row = cur.fetchone ()

                if row == None:
                    res = self.invaildUnitCode(coursecode)
                
                else:
                    res = "You can get more information here: {}".format(row[0])
                    if self.info_flag == 1:
                        self.info_flag = 0
                

        else:
            if len(coursecode) == 0:
                res = "Sorry the course code is invaild"

            else:
                cur = self.mydb.cursor()
                cur.execute("SELECT More_Info FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
                row = cur.fetchone ()

                if row == None:
                    res = self.invaildUnitCode(coursecode)
                
                else:
                    res = "You can get more information here: {}".format(row[0])
                    if self.info_flag == 1:
                        self.info_flag = 0
        return res       
    


    def unitName(self,offer):
        coursecode = offer.query_result.parameters["CourseCode"]
        if len(coursecode) == 0:
            # print("Sorry the course code is invaild")
            res =  "Sorry the course code is invaild"
            return res
        else:
        
            cur = self.mydb.cursor()
            cur.execute("SELECT Unit_Name FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                self.invaildUnitCode(coursecode)
            
            else:
                # print("{} name is {}".format(coursecode,row[0]))
                res = "{} name is {}".format(coursecode,row[0])
                return res

    def areaUnit(self,offer):
        coursecode = offer.query_result.parameters["CourseCode"]
        if len(coursecode) == 0:
            print("Sorry the course code is invaild")
        else:
            cur = self.mydb.cursor()
            cur.execute("SELECT Area_of_Study FROM Unit_details WHERE Unit_Code = '{}'".format(coursecode))
            row = cur.fetchone ()
            if row == None:
                self.invaildUnitCode(coursecode)
            
            else:
                print("The area of unit {} is {}".format(coursecode,row[0]))


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
            self.info_flag = 0
            return offer.query_result.fulfillment_text
            
        
        # print("000000000000000000",offer.query_result)
        #print("intent is ",intent)
        if intent == "OfferSemester":
            print(offer.query_result.fulfillment_text)
            res = self.offerSemester(offer)
            self.info_flag = 0
            return res
            # return offer.query_result.fulfillment_text

        if intent =="UnitName":
            print(offer.query_result.fulfillment_text)
            res = self.unitName(offer)
            self.info_flag = 0
            return res

        if intent == "AreaStudyofUnit":
            print(offer.query_result.fulfillment_text)
            res = self.areaUnit(offer)
            self.info_flag = 0
            return res

        if intent == "UnitInfo":
            res,self.course,self.info_flag =self.unitInfo(offer)
            return res

            

        if intent == "UnitWeb":
            res = self.unitWeb(offer,self.course)
            return res

        #small talk training happen here
        if intent =='':
            self.info_flag = 0
            return offer.query_result.fulfillment_text

        if intent == "Default Fallback Intent":
            self.invaildIntent(query) 
            return offer.query_result.fulfillment_text
        

        if intent == "about agent":
            return offer.query_result.fulfillment_text


        if intent == "About users":
            return offer.query_result.fulfillment_text


        if intent == "End":
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