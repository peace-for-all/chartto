""" Parse task, identify my special markup and apply rules related to that """
import re

class TaskParser:
    RULES = {
        'estt:': 'est\:(?:[0-9]{1,3}(?:h|sp))' # estimate: 1 min, where min can be: 1h5m11s
    }

    def __init__(self):
        pass

    def contains_markup(self, task_string):
        """ Quickly checks, if task contains any kind of 'my special markup' """
        contains_rules = []
        for rule in self.RULES.keys():
            if task_string.find(rule): # wx: is there some kind of lightweight regex check?
                contains_rules.append(rule)

        return contains_rules # False, if empty, very convenient.

    def parse(self, task):
        """ Parses task string and gets out the values for my rules """
        pass

    def process(self, task):
        rules = self.contains_markup(task)
        if not rules:
            return False

        for rule in rules:
            # Get self.method and pull it
            # est\:(?:[0-9]{1,3}(?:h|sp))
            print(f"Checking task against rule: {self.RULES[rule]}...")
            expr = re.compile(self.RULES[rule])
            print(expr.search(task))

if __name__ == '__main__': # wx4 make this a test instead of checking here
    tasks = ["call mom est:3h5m", "chartto complete est:8d5h19m", "weekly planning est:5sp"]
    for task_string in tasks:
        print(f"Got task string: {task_string}...")

        if task_string:
            tp = TaskParser()
            tp.process(task_string)
