
import os
import json
import requests # this needed for version, that asks todoist api
from utils import date2d3


class Analyzer:
    def __init__(self, api_token):
        self.data_path = '.tmp/data'
        self.projects = self.get_data('projects', api_token)
        self.tasks = self.get_data('tasks', api_token)


        # TODO validate received token

    # yet now token is file address actualy
    # and key is tasks|projects, obv
    def get_data(self, key, token = False):
        if key == 'projects':
            token = 'projects.json'
        if key == 'tasks':
            token = 'tasks.json'
        path = os.path.join(self.data_path, token)

        data = self.get_json(path)
        if data:
            if key == 'projects':
                projects = self.get_project_tree(data)
                return projects
            return data
        else:
            return False

    # """Next version: give key and token, get data"""
    # base_url = "https://beta.todoist.com/API/v8/"
    # url = base_url + key # FIXME should I check this key for validity? ;-)
    # data = requests.get(url, headers={"Authorization': 'Bearer %s" % token}).json()
    # if data:
    #     return data
    # else:
    #     return false # todo return error here

    def get_productivity_stats(self, key, token = False):
        token = 'productivity_stats.json'
        path = os.path.join(self.data_path, token)
        data = self.get_json(path)

        if data:
            if data[key]:
                return data[key]
            else:
                return False

    def get_json(self, f):
        f = open(f, 'r')
        data = json.load(f)
        if data:
            return data
        else:
            return False

    def get_project_tree(self, projects):
        """Makes project tree instead of plain list"""
        last_parent_id = False
        for p in projects:
            if p['indent'] == 1:
                last_parent_id = p['id']
                p['parent_id'] = 0
            elif p['indent'] >= 2:
                p['parent_id'] = last_parent_id

        return projects

    def get_child_counters(self):
        """Returns dict of project: subprojects counts (+ porject itself)"""
        last_parent_id = False
        parent_name = False

        project_child_cnts = {}
        projects = get_data('projects', None)
        for p in projects:
            if p['indent'] == 1:
                last_parent_id = p['id']
                parent_name = p['name']
                project_child_cnts[parent_name] = 1
            elif p['indent'] >= 2:
                p['parent_id'] = last_parent_id # fixme make this less dumb in the future.
                project_child_cnts[parent_name] += 1

        print project_child_cnts


    def get_children_list(self, projects, project_id):
        """For a given project returns all children of this project, as a list"""
        children = []
        for p in projects:
            if p['parent_id'] == project_id:
                children.append(p['id'])
        return children


    def get_tasks_in_project_count(self, tasks, project_id, with_children = False, projects = False):
        """Returns amount of tasks"""
        cnt_tasks_in_project = 0

        for t in tasks:
            if t['project_id'] == project_id:
                cnt_tasks_in_project += 1

        if with_children:
            ch = self.get_children_list(projects, project_id)
            for c in ch:
                for t in tasks:
                    if t['project_id'] == c:
                        cnt_tasks_in_project += 1

        return cnt_tasks_in_project

    def get_project_list_tasks_count(self, tasks, projects):
        """Returns project_name: number, where number == amt of tasks in projects and all its children"""
        data = {}
        for p in projects:
            if p['parent_id']:
                continue
            tip = self.get_tasks_in_project_count(tasks, p['id'], True, projects)
            data[p['name']] = tip
        return data

    def get_project_list_easiest_fo_finish(self, tasks, projects):
        """Returns list or projects with amt of unfinished tasks"""
        data = {}
        for p in projects:
            tuf = 0
            for t in tasks:
                if t['project_id'] == p['id']:
                    if t['completed'] is False:
                        if 'due' in t and t['due']['recurring'] is True:
                            continue
                        tuf += 1
            if not tuf == 0:
                data[p['name']] = tuf

        return data

    def get_finished_timeserie(self):
        """Returns dict formatted as date: amount of tasks finished"""
        serie = {}
        days_items = self.get_productivity_stats('days_items')
        for it in days_items:
            serie[it['date']] = it['total_completed']
        return serie

    def main(self):
        tasks = a.get_data('tasks', None)
        projects = a.get_data('projects', None)
        # for t in tasks:
        #     priority = t['priority']
        #     is_done = t['completed']
        #     id = t['id']
        #     project_id = t['project_id']
        # also avail: label_ids (list), content, url, comment_count
        # and due: u'due': {u'date': u'2018-04-11', u'recurring': False, u'string': u'11 Apr'}

        # print get_project_list_tasks_count(tasks, projects)
        serie = a.get_finished_timeserie()

        xdata = []
        ydata = []
        for date, finished in sorted(serie.iteritems()):
            print date
            print finished
            u_ts = date2d3(date)
            xdata.append(u_ts)
            ydata.append(finished)

        print xdata
        print ydata


# for testing library
if __name__ == '__main__':
    a = Analyzer()
    a.main()