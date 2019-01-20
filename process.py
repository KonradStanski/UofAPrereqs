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

# def exportJson(courses):
#     strArr = []
#     f = open("data.json", "w+")
#     f.write("[")
#     for key, courseInstance in courses.items():
#         prereq = courseInstance.prereq
#         f.write('{"name": "' + key + '", "children": ' + repr(prereq) + "}, \n")

treeDict = {}
def makeTreeDict():
    for key, courseInstance in courses.items():
            reqArr = []
            prereq = courseInstance.prereq
            for i in prereq:
                for j in i:
                    reqArr.append(j)
            treeDict[key] = reqArr



def makeTree(search):
    # check if key in dict
    # if in dict, call makeTree on all courses in reqArr and concatenate function calls and return them
    if search in treeDict:
        reqArr = treeDict[search]
        textArray = []
        for req in reqArr:
            return makeTree(req)
            #print(result)

            #textArray.append[result]


    # if not, return base string
    else:
        return '{"name": ' + search + ', "children":'


    # open file to write to
    #f = open("data.json", "w+")
    #     f.write('{"name": "' + key + '", "children": ' + repr(prereq) + "}, \n")



def main():
    with open('data_old.txt', 'r') as f:
        courseArr = json.load(f)

    populateCourses(courseArr)

    makeTreeDict()
    print(makeTree("ECE212"))

    # for key, courseInstance in treeDict.items():
    #     print(key)
    #     print(courseInstance)

    #exportJson(courses)

    # for key, courseInstance in courses.items():
    #     print(key)
    #     #print(courseInstance.dept)
    #     #print(courseInstance.num)
    #     #print(courseInstance.descr)
    #     #print(courseInstance.link)
    #     print(courseInstance.prereq)
    #     print(" ")



if __name__ == "__main__":
    main()
