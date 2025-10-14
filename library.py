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
        fldtyp=f"bigint({ln})"
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
    fldlist=[]
    fldtyplist=[]
    a=executer(f"describe {tbl}",False)
    for i in range(0,len(a)):
        fldlist.append(a[i][0])
    for i in range(0,len(a)):
        fldtyplist.append(a[i][1])
    while ans[0].upper()=="Y":
        feed=f'insert into {tbl} values('
        count=0
        for fldnm in fldlist:
            data=input(f"Enter the {fldnm} : ")
            if fldtyplist[count][0].upper()=='B':
                data=f"{data}"
            elif fldtyplist[count][0].upper()=='V':
                data=f"'{data}'"
            elif fldtyplist[count][0].upper()=='D':
                data=f"'{data}'"
            elif fldtyplist[count][0].upper()=='F':
                data=f"{data}"  
            feed+=data+','
            count+=1
        feed=feed.rstrip(',')
        feed+=')'
        print()
        ans=input("Do you want to continue adding data ?")    
        bdr()
        print(feed)
        executer(feed,False)
        mycon.commit()  

def modifybot():
    print("The tables in our database are as follows : ")
    executer("Show tables",True)
    tbl=input("Enter the name of the table you want to modify structure: ")
    bdr()
    fldlist=[]
    a=executer(f"describe {tbl}",False)
    ans="y"
    for i in range(0,len(a)):
        mod=f'alter table {tbl} '
        fldlist.append(a[i][0])
    while ans[0].upper()=="Y":
        mode=input("Enter the mode: \n(1) for adding field and constraint\n(2) for modifying field\n(3) for deleting field\n\nEnter Here : ")
        bdr()
        if mode=='1':
            mod=f'alter table {tbl} add '
            ask=input("Type (1) for adding constraint \n(2) for adding field\n\nEnter here : ")
            bdr()
            if ask=='1':
                const=input("(1) for primary key\n(2) for unique\n(3) for foreign key\n(4) for not null\n(5) for default\nEnter here : ")
                bdr()
                for i in range(0,len(a)):
                    print(f"{i+1}. {a[i][0]}")
                var=input("Enter the field name : ")
                if const=='1':
                    # mod=alter table {tbl} add 
                    mod+='constraint '
                    # mod=alter table {tbl} add constraint
                    mod+=f' primary key ({var})'
                    # mod=alter table {tbl} add constraint primary key ({var})
                    print(mod)
                elif const=='2':
                    mod+=f' unique ({var})'
                    print(mod)
                elif const=='3':
                    mod+=f' foreign key {var}'
                    print("in progress")
                elif const=='4':
                    b=executer(f"SHOW COLUMNS FROM {tbl} LIKE '{var}'",False)
                    for i in range(0,len(b)):
                        print(b[i][1])
                    mod=f'alter table {tbl} modify {var} {b[i][1]} not null'
                    print(mod)
                elif const=='5':
                    b=executer(f"SHOW COLUMNS FROM {tbl} LIKE '{var}'",False)
                    for i in range(0,len(b)):
                        vartype=b[i][1]                    
                    val=input("Enter a value for default : ")
                    mod=f'alter table {tbl} modify {var} {vartype} default {val}'
                    print(mod)

            elif ask=='2':
                print("The fields currently are : ")
                pricount=0
                for i in range(0,len(a)):
                    print(a[i][0])
                ans='y'
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
                                notnullkey=input("Do you want to make it not null field? : ")
                                if notnullkey[0].upper()=="Y":
                                    iskey="not null"
                                else:
                                    defaultkey=input("Do you want to make it default field? : ")                         
                                    if defaultkey[0].upper()=="Y":
                                        value=input("Enter a value to put in default : ")
                                        if fldtyp[0].upper()=='I':
                                            iskey=f"default {value}"
                                        elif fldtyp[0].upper()=='V':
                                            iskey=f"default '{value}'"
                                        elif fldtyp[0].upper()=='D':
                                            iskey=f"default '{value}'"
                                        elif fldtyp[0].upper()=='F':
                                            iskey=f"default {value}"  
                                    else:
                                        iskey=' '
                                        

                    else:
                        unikey=input("Do you want to make it unique key? : ")
                        if unikey[0].upper()=="Y":
                            iskey="Unique"
                        else:
                            notnullkey=input("Do you want to make it not null field? : ")
                            if notnullkey[0].upper()=="Y":
                                iskey="not null"
                            else:
                                defaultkey=input("Do you want to make it default field? : ")                         
                                if defaultkey[0].upper()=="Y":
                                    value=input("Enter a value to put in default : ")
                                    if fldtyp[0].upper()=='I':
                                        iskey=f"default {value}"
                                    elif fldtyp[0].upper()=='V':
                                        iskey=f"default '{value}'"
                                    elif fldtyp[0].upper()=='D':
                                        iskey=f"default '{value}'"
                                    elif fldtyp[0].upper()=='F':
                                        iskey=f"default {value}"  
                                    else:
                                        iskey=' '

                    info=f"{fldnm}  {fldtyp}    {iskey}"
                    mod+=info
                    ans=input("Do you want to continue? : ")                    
                    print(mod)
                    # executer(mod,False)
                    ans=input("Do you want to continue? : ")
                    if ans[0].upper()=='Y':
                        mod=f'alter table {tbl} add '
                bdr() 
        
        elif mode=='2':
            mod+=' change column '
            print("The fields currently are : ")
            pricount=0
            for i in range(0,len(a)):
                print(a[i][0])
            while ans[0].upper()=="Y":
                fld=input("Enter the field name to modify : ")
                fldnm=input("Enter the new field name : ")
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
                            notnullkey=input("Do you want to make it not null field? : ")
                            if notnullkey[0].upper()=="Y":
                                iskey="not null"
                            else:
                                defaultkey=input("Do you want to make it default field? : ")                         
                                if defaultkey[0].upper()=="Y":
                                    value=input("Enter a value to put in default : ")
                                    if fldtyp[0].upper()=='I':
                                        iskey=f"default {value}"
                                    elif fldtyp[0].upper()=='V':
                                        iskey=f"default '{value}'"
                                    elif fldtyp[0].upper()=='D':
                                        iskey=f"default '{value}'"
                                    elif fldtyp[0].upper()=='F':
                                        iskey=f"default {value}"  
                                else:
                                    iskey=' '
                            
                else:
                    unikey=input("Do you want to make it unique key? : ")
                    if unikey[0].upper()=="Y":
                        iskey="Unique"
                    else:
                        notnullkey=input("Do you want to make it not null field? : ")
                        if notnullkey[0].upper()=="Y":
                            iskey="not null"
                        else:
                            defaultkey=input("Do you want to make it default field? : ")                         
                            if defaultkey[0].upper()=="Y":
                                value=input("Enter a value to put in default : ")
                                if fldtyp[0].upper()=='I':
                                    iskey=f"default {value}"
                                elif fldtyp[0].upper()=='V':
                                    iskey=f"default '{value}'"
                                elif fldtyp[0].upper()=='D':
                                    iskey=f"default '{value}'"
                                elif fldtyp[0].upper()=='F':
                                    iskey=f"default {value}"  
                                else:
                                    iskey=' '
                info=f"{fld} {fldnm}  {fldtyp}    {iskey}"
                mod+=info
                print(mod)
                ans=input("Do you want to continue? : ")
                if ans[0].upper()=="Y":
                    mod=f'alter table {tbl} '
                # executer(mod,False)
                bdr()
                # executer(f"describe {tbl}",True)
                               
        elif mode=='3':
            mod+=' drop '
            while ans[0].upper()=="Y":
                ask=input("Press(1) for deleting constraint and\nPress(2) for deleting field\nEnter here : ")
                if ask=='1':
                    a=executer(f"Describe {tbl}",True)
                    qn=input('Enter the name of the field from which you want to delete constraint : ')
                    const=input("Enter the constraint : ")
                    if const.upper()=='PRIMARY KEY':
                        mod=f'alter table {tbl} drop '
                        mod+=f'{const}'
                        print(mod)
                    elif const.upper()=='UNIQUE':
                        mod=f'alter table {tbl} drop '
                        a=executer(f"show index from new where column_name='{qn}'",False)
                        for i in range(0,len(a)):
                            print(a[i][2])
                            mod+=' index '+a[i][2]
                        print(mod)
                    elif const.upper()=='NOT NULL':
                        a=executer(f"SHOW COLUMNS FROM {tbl} LIKE '{qn}'",False)
                        for i in range(0,len(a)):
                            print(a[i][1])
                        mod=f'alter table {tbl} modify column {qn} {a[i][1]} null'
                        print(mod)
                    elif const.upper()=='DEFAULT':
                        mod=f'alter table {tbl} alter column {qn} drop default'
                        print(mod)
                    else:
                        print("Invalid Input!!")
                    
                elif ask=='2':
                    mod+=' column '
                    print("The fields currently are : ")
                    for i in range(0,len(a)):
                        print(a[i][1])
                    mod+=input('Enter the name of the field you want to delete : ')
                    print(mod)
                else:
                    print("Invalid Input!!")
            
                ans=input("Do you want to continue? : ")
                if ans[0].upper()=='Y':
                    mod=f'alter table {tbl} '
    
        ans=input("Do you want to continue? : ")

def updatebot():
    print("The tables in our database are as follows : ")
    executer("Show tables",True)
    tbl=input("Enter the name of the table you want to update data: ")
    bdr()
    ans="y"
    fldlist=[]
    a=executer(f"describe {tbl}",False)
    for i in range(0,len(a)):
        fldlist.append(a[i][0])
    while ans[0].upper()=="Y":
        upd=f'update {tbl} set '
        for fldnm in fldlist:
            data=input(f"Enter the {fldnm} : ")
            x=0
            for i in a:
                if a[x][0].upper()==f'{fldnm}'.upper():
                    fldtyp=a[x][1]
                x+=1
            if fldtyp[0].upper()=='B':
                data=f'{data}'
            elif fldtyp[0].upper()=='V':
                data=f'"{data}"'
            elif fldtyp[0].upper()=='D':
                data=f'"{data}"'
            elif fldtyp[0].upper()=='F':
                data=f'{data}'
            fdata=fldnm+'='+data
            upd+=fdata+' ,'
        upd=upd.rstrip(',')
        bdr()
        print("You want to update the data where ... ")
        cond_ans="y"
        upd+='where '
        while cond_ans[0].upper()=="Y":
            for i in range(0,len(a)):
                print(a[i][0])
            bdr()
            fld=input("Enter the field you want to restrict (set condition) : ")
            fldval=input(f"Enter the {fld} of your row : ")
            upd+=f'{fld}={fldval} '
            cond_ans=input("Do you want to add condition? : ")
            if cond_ans[0].upper()=="Y":
                for i in range(0,len(a)):
                    print(a[i][0])
                ask=input("Is this condition 'OR'(1) or 'AND'(2) : ")
                if ask=="1":
                    upd+=' or '
                elif ask=="2":
                    upd+=' and '
                else:
                    print("Wrong input!!")
        bdr()
        ans=input("Do you want to continue updating ?")    
        bdr()
        print(upd)
        executer(upd,False)
        mycon.commit()  

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
        iskey=" "
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
                    notnullkey=input("Do you want to make it not null field? : ")
                    if notnullkey[0].upper()=="Y":
                        iskey="not null"
                    else:
                        defaultkey=input("Do you want to make it default field? : ")                         
                        if defaultkey[0].upper()=="Y":
                            value=input("Enter a value to put in default : ")
                            if fldtyp[0].upper()=='B':
                                iskey=f"default {value}"
                            elif fldtyp[0].upper()=='V':
                                iskey=f"default '{value}'"
                            elif fldtyp[0].upper()=='D':
                                iskey=f"default '{value}'"
                            elif fldtyp[0].upper()=='F':
                                iskey=f"default {value}"  
                        else:
                            iskey=' '
                            

        else:
            unikey=input("Do you want to make it unique key? : ")
            if unikey[0].upper()=="Y":
                iskey="Unique"
            else:
                notnullkey=input("Do you want to make it not null field? : ")
                if notnullkey[0].upper()=="Y":
                    iskey="not null"
                else:
                    defaultkey=input("Do you want to make it default field? : ")                         
                    if defaultkey[0].upper()=="Y":
                        value=input("Enter a value to put in default : ")
                        if fldtyp[0].upper()=='B':
                            iskey=f"default {value}"
                        elif fldtyp[0].upper()=='V':
                            iskey=f"default '{value}'"
                        elif fldtyp[0].upper()=='D':
                            iskey=f"default '{value}'"
                        elif fldtyp[0].upper()=='F':
                            iskey=f"default {value}"  
                        else:
                            iskey=' '

        info=f"{fldnm}  {fldtyp}    {iskey}"
        data+=info
        print()
        ans=input("Do you want to continue adding field? : ")
        bdr()
        if ans[0].upper()=="Y":
            data+=","
        elif ans[0].upper()=="N":
            data+=")"
    print(data)
    executer(data,False)
    bdr()
    executer(f"describe {tbl}",True)

def searchbot():
    if isconnected():
        ans='y'
        while ans[0].upper()=='Y':
            print("The tables in our database are as follows : ")
            executer("Show tables",True)
            tbl=input("Enter the name of the table you want to search: ")
            bdr()
            print(f"The structure of the table '{tbl}' is :")
            a=executer(f"describe {tbl}",False)
            for i in range(0,len(a)):
                print(a[i][0]) 
            x=0
            fld=input("Enter the field you want to search : ")
            for i in a:
                if a[x][0].upper()==f'{fld}'.upper():
                    fldtyp=a[x][1]
                x+=1
            data=input(f"Enter the {fld} of your search item : ") 
            bdr()
            if fldtyp[0].upper()=='B':
                data=f'{data}'
            elif fldtyp[0].upper()=='V':
                data=f'"{data}"'
            elif fldtyp[0].upper()=='D':
                data=f'"{data}"'
            elif fldtyp[0].upper()=='F':
                data=f'{data}'  
            executer(f"select * from {tbl} where {fld}={data}",True)
            ans=input("Do you want to continue? : ")
        else:
            print("Thank You!!")

    else:
        print("The Database is not connected !!")

def reportbot():
    print("The tables in our database are as follows : ")
    executer("Show tables",True)
    tbl=input("Enter the name of the table for a report : ")
    bdr()
    report=f'select * from {tbl} where '
    a=executer(f"describe {tbl}",False)
    ans='y'
    fldlist=[]
    for i in range(0,len(a)):
        fldlist.append(a[i][0])
    no=1
    print("Press")    
    for fldnm in fldlist:
        print(f"{no}. {fldnm}")
        no+=1
    while ans[0].upper()=='Y':
        print("Enter condition in format :\n\nField_name (Operators) Field_value\nFor eg: itno >= 100\nitname='name'\ndate='2020-08-08'\n")
        userinp=input("Enter here : ")
        report+=userinp
        ans=input("Do you want to continue adding filter? : ")
        if ans[0].upper()=='Y':
            choose=input("Press\n(1) for 'OR'\n(2) for 'AND\nEnter Here : ")
            if choose=='1':
                report+=' or '
            elif choose=='2':
                report+=' and '
            else:
                print("Wrong Input!")
    print(report)
    executer(report,True)

def dropbot():
    print("\n\n*** This is very dangerous mode.  Use it wisely ***\n")
    print("The tables in our database are as follows : ")
    executer("Show tables",True)
    tbl=input("Enter the name of the table you want to delete : ")
    ask=input("Do you really confirm to delete {tbl} completely ? : ")
    if ask[0].upper()=='Y':
        executer(f'drop table {tbl}',False)
        print("Table {tbl} is successfully deleted.")
    else:
        print(f"The {tbl} is not deleted.")

try:
    bdr()
    print("Hello user !! Welcome to Database Management Program ")
    bdr()
    ask='n'
    while ask[0].upper()=='N':
        print("The functions that you can use are : \n1. Searching for a data\n2. Create a new table\n3. Feeding data in the Tables\n4. Update the old data\n5. Modify the structure of the table\n6. Create a Report\n7. Delete the existing table")
        bdr()
        fn=input("Enter the desired function here: ")
        if fn =='1':
            bdr()
            print("*** Welcome to the searching module !! ***")
            searchbot()
        elif fn=='2':
            bdr()
            print("*** Welcome to the table creating module !! ***")
            tablecreator()
        elif fn=='3':
            bdr()
            print("*** Welcome to the data feeding module !! ***")
            feedbot()
        elif fn=='4':
            bdr()
            print("*** Welcome to the updating data module !! ***")
            updatebot()
        elif fn=='5':
            bdr()
            print("*** Welcome to the modifying table module !! ***")
            modifybot()
        elif fn=='6':
            bdr()
            print("*** Welcome to the report creating module !! ***")
            reportbot()
        elif fn=='7':
            bdr()
            print("*** Welcome to the deleting module !! ***")
            dropbot()
        else:
            print("Oops, You Entered Wrong Input!!")
        ask=input("Do you want to end the program ? : ")
except Exception as e:
    print("Oops an error occured.")
    print(f"The error is : {e}")
finally:
    print("Thank you so much for using the program !! ")
    print("Program is Over.")