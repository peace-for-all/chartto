import todoist  # @see https://github.com/Doist/todoist-python and https://todoist-python.readthedocs.io/en/latest/modules.html
from dotenv import load_dotenv
from os import environ as env


class Todoist:
    def __init__(self):
        load_dotenv()
        api_token = env.get('TODOIST_API_TOKEN')

        if not api_token:
            print("Can't initialize API, no token, check .env")

        self.api = todoist.TodoistAPI(api_token)
        # self.api.sync() # wx figure, how often this should be done + where the data is stored
        # wx: def first run should do the sync, because then the data appears!

    def get_projects(self):
        projects = self.api.state['projects']
        return projects

    def get_tasks(self, kind):
        tasks = []

        if kind == 'uncompleted':
            tasks = [task.data for task in self.api.state['items']]
        if kind == 'completed':
            tasks = self.api.activity.get(
                object_type='item',
                event_type='completed',
                limit=30 # wx: change default limit to anything else
            )

        return tasks

    # def get_state(self):
    #     return self.api.state


if __name__ == '__main__':
    t = Todoist()
    print(t.get_tasks('completed'))
