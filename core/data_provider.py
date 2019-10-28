import os
from api import Todoist
from task_parser import TaskParser

class DataProvider:
    """
    Provides data from the API on a given criteria
    + stores in db
    + caches (avoid asking for API data too often?)
    """
    # wx: make the others inherit from it?
    # wx: have a fuckton of methods for getting data in different formats for representing in the charts
    def __init__(self):
        # self.t_api = Todoist() # unc
        self.t_parser = TaskParser()

    def get_completed_task_counts(self, per='day', lookback=7):
        """
        Gives completed task counts per project or day
        :param per: (day|week|month), default day
        :param lookback int - number of %per% stats to return (i.e. lookback = 7, per='day' => return 7 days)
        :return: dict, 'per' values in keys, counts in values
        """
        per_values = ['day', 'week', 'month']
        if per not in per_values:
            return False

        task_counts = {}
        # events = self.t_api.api.activity.get(
        #     object_type='item',
        #     event_type='completed',
        #     # event_date='2019-10-27', # wx1: rm hardcode
        #     limit=200 # wx3: maybe remove or change, right now we're going to filter by date on our side
        # )

        # unc getter from api after done debugging get_completed_task_counts
        # data = self.get_test_data('item', 'completed')
        # for d in data:
        #     if d['count']:
        #         return d['count']

        return {
            '2019-10-25': {'Avia': 27, 'Home': 32, 'Work': 33},
            '2019-10-26': {'Avia': 27, 'Home': 32, 'Work': 33},
            '2019-10-27': {'Avia': 30, 'Home': 22, 'Work': 22},
            '2019-10-28': {'Avia': 27, 'Home': 32, 'Work': 33},
            '2019-10-29': {'Avia': 27, 'Home': 32, 'Work': 33},
        }

        # wx: here go the caching logic
        #return task_counts

    def get_test_data(self, object_type, event_type):
        filename = f"sample_data/api_{event_type}_{object_type}.txt" # api_completed_item, api_forgotten_object
        sample = os.path.join(os.path.abspath('.'), filename)
        f = open(sample, 'r')
        data = f.readline() # api call files have only one line

        return data


    def test(self):
        self.get_completed_task_counts() # wx3: mv this to tests

# for testing library
if __name__ == '__main__':
    dp = DataProvider()
    dp.test()
