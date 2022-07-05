import psycopg2
from flask import Flask,request
from flask_restful import Resource,Api
import re
app=Flask(__name__)
api=Api(app)

employees=[]

hostname='localhost'
database='employee'
username='postgres'
pwd='root@123'
port_id=5432
conn=None
cur=None
conn=psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
cur=conn.cursor()
cur.execute('DROP TABLE IF EXISTS employee')
conn.commit()

create_script='''CREATE TABLE employee(
        employee_id   int PRIMARY KEY,
        first_name    varchar(40) NOT NULL,
        last_name     varchar(40) NOT NULL,
        designation   varchar(30) NOT NULL,
        email         varchar(70) NOT NULL
    ) '''
cur.execute(create_script)
conn.commit()
class employee(Resource):
    def get(self,id):
        for emp in employees:
            if emp['employee_id']==id:
                pscript='select * from employee where employee_id=%s'
                data=(str(id),)
                cur.execute(pscript,data)
                print("all details :",cur.fetchall())
                return emp, 200
        return {'message': '404 error, Employee not found'},404
    def post(self,id):
        data=request.get_json()
        if data!=None:
            employee={
            'employee_id':id,
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'designation':data['designation'],
            'email':data['email']
                }
            regex1 = '^[0-9]+$'#to check employee id
            regex2= '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #to verify user mail-id
            if(re.search(regex1, str(employee['employee_id']))):
                pass
            else:
                return {'message':'INVALID EMPLOYEE ID , EMPLOYEE ID MUST BE NUMERICAL '}, 400

            if( employee['first_name'].isalpha() and  employee['last_name'].isalpha()):
                pass
            else:
                return{'message': 'INVALID NAME CREDENTIALS, MUST CONTAIN ONLY ALPHABETS'}, 400
            
            if(re.search(regex2,employee['email'])):
                pass
            else:
                return{'message': 'INVALID  MAIL ID , PLEASE CORRECT YOUR MAIL ID'}, 400
            

            
            insert_script='INSERT INTO employee (employee_id,first_name,last_name,designation,email) VALUES (%s, %s, %s, %s,%s)'
            insert_value=(str(id),data['first_name'],data['last_name'],data['designation'],data['email'])
            cur.execute(insert_script,insert_value)
            conn.commit()
            employees.append(employee)
            return({'employee added':employee}), 201
        else:
            return {'message ': 'INVALID DATA'} ,400
        

    
    def put(self,id):
        data=request.get_json()
        employee={
        'employee_id':id,
        'first_name':data['first_name'],
        'last_name':data['last_name'],
        'designation':data['designation'],
        'email':data['email']
            }
        c=None
        for emp in employees:
            if emp['employee_id']==id:
                employees.remove(emp)
                dscript='DELETE FROM employee WHERE employee_id=%s'
                data=(str(id),)
                cur.execute(dscript,data)
                conn.commit()
               # iscript='INSERT INTO employee (employee_id,first_name,last_name,designation,email) VALUES (%s, %s, %s, %s,%s)'
                #ivalue=(str(id),data['first_name'],data['last_name'],data['designation'],data['email'])
               # cur.execute(iscript,ivalue)
              #  conn.commit()
                employees.append(employee)
                return ({'corrected_employee':employee})

    def delete(self,id):
        for emp in employees:
            if emp['employee_id']==id:
                employees.remove(emp)
                dscript='DELETE FROM employee WHERE employee_id=%s'
                data=(str(id),)
                cur.execute(dscript,data)
                conn.commit()
                return {'removed_employee':emp} , 200

class employees_list(Resource):
    def get(self):
        cur.execute('select * from employee')
        print("all details :",cur.fetchall())
        return {'employees':employees} ,200

api.add_resource(employee, '/employee/<string:id>')
api.add_resource(employees_list, '/employees')
app.run(port=5000,debug=True)

cur.close()
conn.close()