from flask import render_template
from core.data_provider import DataProvider

CHART_TYPES = ['burndown', 'bar']

class IndexView(AbstractView):
    """'Overview view. :D Or, like, everything on one page """
    def get(self):
        overview_data = self.dp.get_completed_task_counts()
        return render_template(
            'index.html',
            data=overview_data
        )


class SettingsView(AbstractView):
    """ Settings page for the app """
    def get(self):
        return render_template(
            'settings.html'
        )

class BurndownView(AbstractView):
    """ Burndown chart view for today by default """ # wx4: later on maybe add week/month or something like this
    # wx1: get data for it and display
    def get(self):
        data = {} # wx1: figure out the data structure necessary for this
        return render_template(
            'burndown.html',
            data=data
        ) # wx1: should I really override the get method?

class ChartView(AbstractView, type): # wx4: chart views should inherit from this one and just supply their type, bcs the rest is similar
    SUPPORTED_TYPES = ['burndown'] # add chart types here

    def __init__(self, type):
        if type not in self.SUPPORTED_TYPES:
            pass # wx3: type validation: without valid type we shouldn't init
        self.type = type
        self.dp = DataProvider()

    def get(self):
        data = self.get_data()
        return render_template(
            'burndown.html',
            data=data
        )

    def get_data(self):
        """ Get data to show in the view; format depends on the type """
        dp = DataProvider() # could use the Todoist API directly, this is a bit for the future; to support weird data formats

        return {} # wx2 NotImplementedError on get data for view


class AbstractView:
    """ Empty for now, maybe add something useful later on """
    pass
