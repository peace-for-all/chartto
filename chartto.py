from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
import nvd3
from logic import Analyzer
from core.validator import Validator
from core.user import User
from utils import date2d3

app = Flask(__name__)
SESSION_TYPE = 'memcached'
app.config.from_object(__name__)
Session(app)
v = Validator()

app.debug = True
app.TEMPLATES_AUTO_RELOAD = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print request.form['api_token']
        if v.check_token(request.form['api_token']) or 'username' in session:
            return report()
        else:
            return render_template('index.html') # TODO make it show errors instead

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if v.check_password_matches(request.form['username'], request.form['password']):
            return log_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


def log_in(username):
    """Save login in session?"""
    # TODO: implement login itself
    session_set('username', username)
    u = User(username)
    api_token = u.get_token()
    session_set('api_token', api_token) # FIXME: this lacks error processing, add case, when user is unable to login, bcs token unavail

    return report()  # TODO: check, is this correct?

def get_report_for_login():
    """Returns report with api token specific to this user"""
    return

@app.route('/logout', methods=['GET', 'POST'])
def logout(username):
    """Remove login from session"""
    pass


@app.route('/report', methods=['GET', 'POST'])
def report():
    try:
        api_token = session_get('api_token')
    except:
        api_token = request.form['api_token']

    a = Analyzer(api_token)
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.1/nv.d3.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.1/nv.d3.min.js"></script>
    </head>
    """
    html += "<p><h3>Tasks finished in the last week</h3></p>"
    html += get_finish_line(a)
    html += "<p><h3>Projects sorted by amount of tasks to do</h3></p>"
    html += get_bar_easiest(a)
    html += "<br />"
    html += "<p><h3>Projects by total amount of tasks in project</h3></p>"
    html += get_projects_pie(a)

    return html


def get_finish_line(a):
    serie = a.get_finished_timeserie()
    xdata = []
    ydata = []
    for date, finished in sorted(serie.iteritems()):
        u_ts = date2d3(date)
        xdata.append(u_ts)
        ydata.append(finished)

    chart = nvd3.lineChart(name="Tasks finished over last week", x_is_date=True, x_axis_format="%d %b %Y", height=300, width=900, color_category='category20c')
    extra = {"tooltip": {"y_start": "", "y_end": " tasks done"}}
    chart.add_serie(x=xdata, y=ydata, name="Tasks done", extra=extra)
    chart.buildcontent()

    return chart.htmlcontent


def get_projects_pie(a):
    projects = a.get_data('projects')
    tasks = a.get_data('tasks')
    data = a.get_project_list_tasks_count(tasks, projects)
    xdata = data.keys()
    ydata = data.values()
    extra_serie = {"tooltip": {"y_start": "", "y_end": " tasks in project"}}

    type = 'pieChart'
    chart = nvd3.pieChart(name=type, color_category='category20c', height=450, width=450)
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildcontent()

    return chart.htmlcontent


def get_bar_easiest(a):
    projects = a.get_data('projects')
    tasks = a.get_data('tasks')
    xdata = []
    ydata = []
    data = a.get_project_list_easiest_fo_finish(tasks, projects)
    for k, v in sorted(data.iteritems(), key=lambda (k, v): (v, k)):
        xdata.append(k)
        ydata.append(v)

    chart = nvd3.discreteBarChart(name='discreteBarChart', height=450, width=900) # was some 400?
    chart.add_serie(y=ydata, x=xdata)
    chart.buildcontent()

    return chart.htmlcontent


@app.route('/example', methods=['GET', 'POST'])
def example():
    type = 'pieChart'
    chart = nvd3.pieChart(name=type, color_category='category20c', height=450, width=450)
    xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
    ydata = [3, 4, 0, 1, 5, 7, 3]
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildcontent()

    return chart.htmlcontent


def session_get(key):
    """ref: https://pythonhosted.org/Flask-Session/, don't use Session obj directly"""
    return session.get(key, None)


def session_set(key, value):
    session[key] = value