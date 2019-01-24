#Process Data

import json

#global data
courses = {}


class course:
    def __init__(self, crsid, dept, num, descr, link, prereq):
        self.crsid = crsid
        self.dept = dept
        self.num = num
        self.descr = descr
        self.link = link
        self.prereq = prereq


def populateCourses(courseArr):
    for i in range(80):  #len(courseArr)):
        # get crsid
        crsid = courseArr[i]["title"].split("-")
        crsid = crsid[0].strip()

        #get dept and num
        for j in range(len(crsid)):
            if crsid[j].isdigit():
                dept = crsid[:j]
                num = crsid[j:]
                break

        # get descr and link
        descr = courseArr[i]["descr"]
        link = courseArr[i]["link"]

        # get prerquisites
        prereq = getPrereq(descr)

        #put in class
        courses[crsid] = course(crsid, dept, num, descr, link, prereq)


def getPrereq(descr):
    reqArr = []
    if descr.find("Prerequisite") == -1:
        reqArr.append(["No Prereqs"])
        return reqArr
    else:
        reqLine = descr.split("Prerequisite")[1]
        reqLine = reqLine.split(":")[1]
        #print(reqLine.split(".")[0])
        reqLine = reqLine.split(".")[0]
        reqArr = reqLine.split(",")
        for i in range(len(reqArr)):
            reqArr[i] = reqArr[i]
            #print(reqArr[i][:4])
            if reqArr[i][:4] == " and":
                reqArr[i] = reqArr[i][4:]

            reqArr[i] = reqArr[i].strip()
            reqArr[i] = reqArr[i].split(" or ")

        #reqArr.append(reqLine)
        return reqArr


treeDict = {}
def makeTreeDict():
    for key, courseInstance in courses.items():
            reqArr = []
            prereq = courseInstance.prereq
            for i in prereq:
                for j in i:
                    reqArr.append(j)
            treeDict[key] = reqArr


# This function takes the treeDict{} dictionary and makes a parralel tree array for porting to javascript and display in D3
def makeTree(search, last):
    if search in treeDict:
        searchType = "lst"
        reqArr = treeDict[search]
    else:
        searchType = "end"

    textArray = []

    #case 1
    if (searchType == "lst") and not last:
        print()
        textArray.append('{"name": "' + search + '", "children":[')
        for i in range(len(reqArr)):
            if i != len(reqArr):
                text = makeTree(reqArr[i], False)
                textArray.append(text)
            else:
                text = makeTree(reqArr[i], True)
                textArray.append(text)
        textArray.append(']},')

    #case 2
    if (searchType == "lst") and last:
        textArray.append('{"name": "' + search + '", "children":[')
        for i in range(len(reqArr)):
            if i != len(reqArr):
                text = makeTree(reqArr[i], False)
                textArray.append(text)
            else:
                text = makeTree(reqArr[i], True)
                textArray.append(text)
        textArray.append(']}')

    #case 3
    if (searchType == "end") and not last:
        textArray.append('{"name": "' + search + '"},')

    #case 4
    if (searchType == "end") and last:
        textArray.append('{"name": "' + search + '"}')

    #concatenate the array to form a json string
    return "".join(textArray)






def makeJson():
    outArr = []
    f = open("data.json", "w+")
    for key, courseInstance in treeDict.items():
        
        print(key)
        outstr = makeTree(key, False)
        outstr = "[" + outstr + "],"
        outstr = outstr.replace("},]","}]")
        outArr.append(outstr)
    print("".join(outArr)) 
    f.write("".join(outArr))
        


def main():
    with open('data_old.txt', 'r') as f:
        courseArr = json.load(f)

    populateCourses(courseArr)

    makeTreeDict()
    makeJson()


if __name__ == "__main__":
    main()
