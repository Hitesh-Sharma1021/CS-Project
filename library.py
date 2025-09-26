import mysql.connector as sqltor
# db=input("Enter name of the database : ")
db="project"
mycon=sqltor.connect(host="localhost",user="root",password="1021", database=db)

def bdr():
    print()
    print("_____________________")
    print()

def isconnected():
    if mycon.is_connected():
        return True
    else:
        return False
def inputchart():
    print("Field types Chart:\n1. For 'integer' enter 1\n2. For 'text' enter 2\n3. For 'date' enter 3\n4. For 'decimal values' enter 4")
    opt=int(input("Enter the option : "))
    if opt==1:
        ln=input("Enter the length of the field : ")
        fldtyp=f"int({ln})"
        return fldtyp
    elif opt==2:
        ln=input("Enter the length of the field : ")
        fldtyp=f"varchar({ln})"
        return fldtyp
    elif opt==3:
        fldtyp=f"date"
        return fldtyp
    elif opt==4:
        ln=input("Enter the length of the field : ")
        dp=input("Enter the no of decimal points : ")
        fldtyp=f"float({ln},{dp})"
        return fldtyp
    else:
        print("Invalid Input !!")

def feedchart():
    a=executer(f"describe {tbl}",False)
    for i in range(0,len(a)):
        print(a[i][0])
    pass

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

def feedbot():
    print("The tables in our database are as follows : ")
    executer("Show tables",True)
    tbl=input("Enter the name of the table you want to feed data: ")
    bdr()
    ans="y"
    feed=f"insert into {tbl} values"
    while ans[0].upper()=="Y":
        ans=input("Do you want to continue?")

def tablecreator():
    print("The tables in our database are as follows : ")
    executer("Show tables",True)
    tbl=input("Enter the name of the table you want to create: ")
    bdr()
    ans="y"
    pricount=0
    iskey=" "
    data=f"create table {tbl} ("
    while ans[0].upper()=="Y":
        fldnm=input("Enter the field name : ")
        fldtyp=inputchart()
        if pricount==0:
            prikey=input("Do you want to make this a primary key? : ")
            if prikey[0].upper()=="Y":
                iskey="Primary key"
                pricount+=1
            else:
                unikey=input("Do you want to make it unique key? : ")
                if unikey[0].upper()=="Y":
                    iskey="Unique"      
        else:
            unikey=input("Do you want to make it unique key? : ")
            if unikey[0].upper()=="Y":
                iskey="Unique"      
            else:
                iskey=" "
        info=f"{fldnm}  {fldtyp}    {iskey}"
        data+=info
        ans=input("Do you want to continue? : ")
        if ans[0].upper()=="Y":
            data+=","
        elif ans[0].upper()=="N":
            data+=")"
    executer(data,False)
    bdr()
    executer(f"describe {tbl}",True)
            

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

# searchbot()
# tablecreator()
feedchart()