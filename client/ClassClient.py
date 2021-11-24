import requests
from faker import Faker
import datetime

fake = Faker(locale='zh_CN')


class ClassClient:
    def __init__(self, name):
        self.name = name if name else '-'.join(fake.words(2))
        self.headers = {'X-Auth-Appid': '1001583', 'X-Auth-TimeStamp': '1604572254', 'X-Auth-Sign': '79c04ff44831aa22a398722ca696837c', 'RESPONSE-TYPE': 'application/json'}

    def add_class(self, counselorId, courseid, prename='测试', type=1):
        url = "http://courseapi.xesv5.com/LiveClass/LiveClassAdmin/addLiveClass"
        data = {'className': prename + self.name,
                'counselorId': counselorId, 'userId': 11476,
                'classQuota': '100', 'recommend': '1', 'isExpand': '1', 'autoBuildroom': '1', 'classStuType': '1',
                'courseId': courseid, 'classType': type}
        res = requests.post(url, data)
        # print(res.json())
        return res.json()

    # 特训班开班
    def special_class_add(self, counselor_id, course_id):
        url = "http://api.xesv5.com/classadmin/LiveClass/Specialclass/Createclass"
        data = {
            'counselor_ids': counselor_id,
            'course_id': course_id
        }
        res = requests.post(url, data, headers=self.headers)
        print(res.json())

    def add_continu_rule(self, firstid, secondid):
        url = 'http://courseapi.xesv5.com/Continuation/ContinuationAdmin/addContinuationRule'
        data = {'courseId': firstid, 'continuationCourseId': secondid, 'createrId': 11476}
        res = requests.post(url, data)
        print(res.json())

    # 添加联报规则
    def add_union_rule(self, subjectid, gradeid):
        url = 'http://courseapi.xesv5.com/Continuation/CourseUnionAdmin/addUnionRule'
        today = datetime.date.today()
        data = {
            "name": "{}年级秋寒联报".format(gradeid),
            "unionTermType": "3,4",
            "gradeIds": gradeid,
            "subjectIds": subjectid,
            "discountType": "1",
            "unionDiscount": "11",
            "startDate": str(today),
            "endDate": str(today + datetime.timedelta(days=30)),
            "createrId": "11467"
        }
        res = requests.post(url, data)
        print(res.json())

    # 续报课开班
    # courseid 为续报/联报课ID；前提是原课先手动开班完成
    def add_class_continu(self, courseid):
        url = 'http://courseapi.xesv5.com/Shell/LiveClass/CreateContinuationClass/createContinuationClass?ontinuationCourseId={}'.format(
            courseid)
        res = requests.get(url)
        print(res.json())

    # 联报课开班
    def lianbao(self, courseid):
        url = 'http://stucouapi.xesv5.com/Shell/LiveClass/CreateUnionClass/createUnionClassNew?courseId={}'.format(courseid)
        res = requests.get(url)
        print(res.json())


if __name__ == '__main__':
    cc = ClassClient('ss')
    # cc.special_class_add(5802, 279859)
    print(cc.add_class(45140, 313444))
