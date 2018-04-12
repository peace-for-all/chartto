
import os
import json
import requests # this needed for version, that asks todoist api

# yet now token is file address actualy
# and key is tasks|projects, obv
def get_data(key, token):
    data_path = '/home/walx/tmp/projects/chartto/data'
    if key == 'projects':
        token = 'all_projects_1104.json'
    if key == 'tasks':
        token = 'all_tasks_1104.json'
    path = os.path.join(data_path, token)

    f = open(path, 'r')
    data = json.load(f)
    if data:
        if key == 'projects':
            projects = get_project_tree(data)
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


def get_project_tree(projects):
    """Makes project tree instead of plain list"""
    last_parent_id = False
    for p in projects:
        if p['indent'] == 1:
            last_parent_id = p['id']
            p['parent_id'] = 0
        elif p['indent'] >= 2:
            p['parent_id'] = last_parent_id

    return projects

def get_child_counters():
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


def get_children_list(projects, project_id):
    """For a given project returns all children of this project, as a list"""
    children = []
    for p in projects:
        if p['parent_id'] == project_id:
            children.append(p['id'])
    return children


def get_tasks_in_project_count(tasks, project_id, with_children = False, projects = False):
    """Returns amount of tasks"""
    cnt_tasks_in_project = 0

    for t in tasks:
        if t['project_id'] == project_id:
            cnt_tasks_in_project += 1

    if with_children:
        ch = get_children_list(projects, project_id)
        for c in ch:
            for t in tasks:
                if t['project_id'] == c:
                    cnt_tasks_in_project += 1

    return cnt_tasks_in_project


def main():
    tasks = get_data('tasks', None)
    projects = get_data('projects', None)
    # for t in tasks:
    #     priority = t['priority']
    #     is_done = t['completed']
    #     id = t['id']
    #     project_id = t['project_id']
    # also avail: label_ids (list), content, url, comment_count
    # and due: u'due': {u'date': u'2018-04-11', u'recurring': False, u'string': u'11 Apr'}

    for p in projects:
        tip = get_tasks_in_project_count(tasks, p['id'], True, projects)
        if tip > 20:
            print p['name']
            print tip
        #    print p['name']


main()