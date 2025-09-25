import mysql.connector as sqltor
mycon=sqltor.connect(host="localhost",user="root",password="1021", database="project")

def bdr():
    print()
    print("_____________________")
    print()

def isconnected():
    if mycon.is_connected():
        return True
    else:
        return False


def executer(command,inp):
    list1=[]
    mycursor=mycon.cursor()
    mycursor.execute(command)
    if inp==True:
        for x in mycursor:
         print(x)
    for x in mycursor:
        list1.append(x)
    return list1 

def tablecreator():
    pass

def searchbot():
    if isconnected():
        print("The tables in our database are as follows : ")
        executer("Show tables",True)
        tbl=input("Enter the name of the table you want to search: ")
        bdr()
        print(f"The structure of the table '{tbl}' is :")
        a=executer(f"describe {tbl}",False)
        for i in range(0,len(a)):
            print(a[i][0])
        bdr()
        fld=input("Enter the field you want to search : ")
        data=input(f"Enter the {fld} of your search item : ")
        executer(f"select * from {tbl} where {fld}={data}",True)

    else:
        print("The Database is not connected !!")

searchbot()