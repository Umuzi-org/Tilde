import random


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
