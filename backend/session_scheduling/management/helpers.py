import random
import re


def group_learners(users, group_size):
    count = len(users)
    number_of_groups = count // group_size + bool(count % group_size)
    users = users[:]
    random.shuffle(users)

    groups = [[] for _ in range(number_of_groups)]
    current_group = 0
    while len(users):
        groups[current_group].append(users.pop())
        current_group += 1
        if current_group == len(groups):
            current_group = 0
    return groups


def get_skill_name_from_pod_column_name(column_name):
    return re.search(".*\[(.*)\]$", column_name).groups()[0]


# used for fundamentals sessions. We need to map cards to pod skills
card_name_skill_name_mapping = {
    "Assessment: Functions, return statements and printing to the terminal": "How skilled do you think you are? [Functions, return statements and printing to the terminal]",
    "Assessment: For loops": "How skilled do you think you are? [For loops]",
    "Assessment: Classes and objects": "How skilled do you think you are? [Classes and objects]",
    "Assessment: Basic data analysis - part 1": "How skilled do you think you are? [Basic data analysis]",
    "Assessment: Basic data analysis - part 2": "How skilled do you think you are? [Probability and hypothesis testing]",
}
