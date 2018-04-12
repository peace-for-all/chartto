from flask import Flask, render_template
from logic import get_data
from nvd3 import pieChart

app = Flask(__name__)

app.debug = True
app.TEMPLATES_AUTO_RELOAD = True

@app.route('/', methods=['GET', 'POST'])
def index():
    pass

@app.route('/example', methods=['GET', 'POST'])
def example():
    type = 'pieChart'
    chart = pieChart(name=type, color_category='category20c', height=450, width=450)
    xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
    ydata = [3, 4, 0, 1, 5, 7, 3]
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildcontent()
    chart.buildhtml()

    return chart.htmlcontent
    #return render_template('index.html', name=name)