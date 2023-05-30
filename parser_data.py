class Instance:
    def __init__(self, activities: int, horizon: int, and_constraints, or_constraints, bi_constraints, durations,
                 resource_capacity, resource_use):
        self.activities = activities
        self.horizon = horizon
        self.and_constraints = and_constraints
        self.or_constraints = or_constraints
        self.bi_constraints = bi_constraints
        self.durations = durations
        self.resource_capacity = resource_capacity
        self.resource_use = resource_use


def transform(and_constraints):
    precedences = {}
    for successor, predecessor in and_constraints:
        if successor in precedences:
            precedences[successor].append(predecessor)
        else:
            precedences[successor] = []
            precedences[successor].append(predecessor)

    # print(precedences)
    return precedences


def generate_or_constraints(k1, k2, activities, precedences):
    or_constraints = {}
    for successor, predecessor in precedences:
        if (successor + k1) % k2 == 0 and predecessor != 0 and successor != activities - 1:
            precedences.remove((successor, predecessor))
            if successor in or_constraints:
                or_constraints[successor].append(predecessor)
            else:
                or_constraints[successor] = []
                or_constraints[successor].append(predecessor)

    return or_constraints


def generate_bi_constraints(k1, k2, activities, precedences):
    bi_constraints = {}
    for successor, predecessor in precedences:
        if (successor + k1) % k2 == 0 and predecessor != 0 and successor != activities - 1:
            if successor in bi_constraints:
                continue
            precedences.remove((successor, predecessor))
            bi_constraints[successor] = []
            bi_constraints[successor].append(predecessor)
    return bi_constraints


def parse_file(filename, k1, k2):
    precedences = []
    durations = []
    resource_use = []

    f = open(filename)
    lines = f.readlines()
    activities = int(lines[5].split()[-1])

    horizon = int(lines[6].split()[-1]) + 1
    line = 18
    # parse precedences
    for index in range(activities):
        for successor in lines[line + index].split()[3:]:
            # first is the successor, second is the predecessor
            precedences.append((int(successor) - 1, index))
    line += activities
    line += 4
    # print(precedences)
    # parse durations and resource consumption
    for index in range(activities):
        split_line = lines[line + index].split()
        durations.append(int(split_line[2]))
        resource_use.append([int(r) for r in split_line[3:]])
    line += activities
    line += 3
    resource_capacity = [int(r) for r in lines[line].split()]
    f.close()

    # or_constraints = generate_or_constraints(k1, k2, activities, precedences)
    or_constraints = {}
    # this should be done either or bi not at the same time
    bi_constraints = generate_bi_constraints(k1, k2, activities, precedences)

    and_constraints = precedences

    return Instance(activities, horizon, and_constraints, or_constraints, bi_constraints, durations, resource_capacity,
                    resource_use)
