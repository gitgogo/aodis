from client.TeacherClient import TeacherClient
import time


def add_teacher_and_config(**kwargs):
    data = kwargs['data']
    mode = data.get('config')
    name = data.get('name')
    subjectid = data.get('subjectid')
    branch_id = data.get('branch_id')
    teacher_type = data.get('teacher_type')
    result = {}
    teacher = TeacherClient(name)
    if int(teacher_type) == 2:
        res = teacher.add_teacher(subjectid, branch_id)
        teacherid = res.get('data')['teacher_id']
        result['teacher_id'] = teacherid
        if mode:
            if len(mode) > 1:
                teacher.add_config(teacherid, 2)
                time.sleep(1)
                res = teacher.add_config(teacherid, 1)
                result['config_num'] = res['data']['num']
            elif int(mode) == 1:
                res = teacher.add_config(teacherid, 1)
                result['config_num'] = res['data']['num']
            elif int(mode) == 2:
                res = teacher.add_config(teacherid, 2)
                result['config_num'] = res['data']['num']
            return result
    elif int(teacher_type) == 1:
        res = teacher.add_teacher_zhujiang(subjectid)
        return {'teacher_id': res.get('data')}
    else:
        return {'msg': '参数有误'}


if __name__ == '__main__':
    data = {"name":"测试班主任姓名","subjectid":"1,2","branch_id":19,"config":"2","teacher_type":2,"createDate":1611651731247}
    add_teacher_and_config(data=data)
