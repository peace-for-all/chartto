from flask import Flask, render_template, url_for, request, redirect
import nvd3
from logic import Analyzer
from utils import date2d3

app = Flask(__name__)

app.debug = True
app.TEMPLATES_AUTO_RELOAD = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['api_token']:  # TODO: validate!
            return report()

    return render_template('index.html') #, result=result, form=form)

# @app.route('/login', methods=['GET', 'POST'])
# error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'], request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#         # the code below is executed if the request method
#         # was GET or the credentials were invalid
#     return render_template('login.html', error=error)


@app.route('/report', methods=['GET', 'POST'])
def report():
    a = Analyzer(request.form['api_token'])
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
