from flask import current_app as app, request
from flask import Blueprint
import datetime

course = Blueprint('course', __name__, url_prefix='/data/api')


@course.route('/addCourse', methods=['POST'])
def add_course():
    start_date = request.json.get('start_date') if request.json.get('start_date') else str(datetime.date.today())
    batchno = request.json.get('batchno') if request.json.get('batchno') else 1
    data = add_courses_live()
    return app.rc_resp.ok(data=data)


@course.route('/addCoursesOutline', methods=['POST'])
def add_coursesOutline():
    data = request.json
    if not data['start_date']:
        data['start_date'] = str(datetime.date.today())
    data = add_courses_outline(data=data)
    return app.rc_resp.ok(data=data)


@course.route('courseList', methods=['GET'])
def get_courselist():
    data = request.args
    res = course_list(data=data)
    return app.rc_resp.ok(data=res)