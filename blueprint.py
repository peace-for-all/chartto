from flask import Blueprint
import views

ch = Blueprint(
    'chart',
    __name__,
    url_prefix='/chart'
)

ch.add_url_rule('/overview', views.IndexView.as_view('index'))
ch.add_url_rule('/settings', views.SettingsView.as_view('settings'))
