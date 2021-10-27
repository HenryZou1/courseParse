
import sys
import csv
import pandas


#error message writer function
def errorMessage(pathname):
    with open(pathname, mode='w') as error:
        error.write("{\n")
        error.write("\"error\": \" Invalid course weights\" \n")
        error.write("}")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Not Enough arguments")
        exit(1)
    else:
        pathCourse = sys.argv[1]
        pathStudent = sys.argv[2]
        pathTest = sys.argv[3]
        pathMark = sys.argv[4]
        pathOutput = sys.argv[5]
    course = pandas.read_csv(pathCourse)
    student = pandas.read_csv(pathStudent)
    mark = pandas.read_csv(pathMark)
    test = pandas.read_csv(pathTest)
    #merge two tables together with test id as merge key
    testresults = pandas.merge(mark,test, on=None, left_on = "test_id",right_on = "id")
    studentresult = {}

    # store student results in a dictionary
    # {student id, {courseid, [mark,  sum of test weight]}}
    for row in testresults.itertuples():
        studentid = row[2]
        courseid = row[5]
        weight = row[6]
        mark = row[3]
        if studentid in studentresult:
            if courseid in studentresult[studentid]:
                mark = studentresult[studentid][courseid][0] +mark*weight/100
                weight += studentresult[studentid][courseid][1]
                studentresult[studentid][courseid] = [mark, weight]
            else:
                studentresult[studentid][courseid] = [mark*weight/100, weight]
        else:
            studentresult[studentid] = {courseid: [mark*weight/100, weight]}
    #using the student results find the a students average and also check if any class has weights not equal to 100
    studentaverage = {}
    for key in studentresult:
        total, amount = 0,0
        for keycourse in studentresult[key]:
            if studentresult[key][keycourse][1] != 100:
                errorMessage(pathOutput)
            total = total +studentresult[key][keycourse][0]
            amount = amount + 1
        studentaverage[key] = total/amount

    studentname={}
    #key student id , value  average of all grades
    with open(pathStudent) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                studentname[row[0]] = row[1]
            line_count += 1
    courseinfo={}
    # key course id , value [course name , teacher]
    with open(pathCourse) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                courseinfo[row[0]] = [row[1],row[2]]

            line_count += 1

    #to tell if its the first value or not to tell if you need to add ,
    flag1 , flag2 = True, True
    # writing the json file
    with open(pathOutput, mode='w') as file:
        file.write("{\n")
        file.write("\"students\": [\n")
        for key, value in studentresult.items():

            if flag1:
                flag1 = False
            else:
                file.write(",")
            file.write("{\n")
            file.write("\"id\": " + str(key) + ",\n")
            file.write("\"name\": \"" + studentname.get(str(key)) + "\",\n")
            file.write("\"totalAverage\": " + "{:.2f}".format(studentaverage.get(key)) + ",\n")
            file.write("\"courses\": [ \n")
            for keycourse in studentresult[key]:
                if flag2:
                    flag2 = False
                else:
                    file.write(",")
                file.write("{\n")
                file.write("\"id\": " + str(keycourse) + ",\n")
                file.write("\"name\": \"" + courseinfo[str(keycourse)][0] + "\",\n")
                file.write("\"Teacher\": \"" + courseinfo[str(keycourse)][1] + "\",\n")
                file.write("\"courseAverage\": " + "{:.2f}".format(studentresult.get(key).get(keycourse)[0])+ "\n")
                file.write("}\n")
            file.write("]\n")
            file.write("}\n")
            flag2 = True;

        file.write("]\n")
        file.write("}")































