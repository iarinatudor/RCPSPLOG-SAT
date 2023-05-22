from queue import PriorityQueue
class Instance:
    def __init__(self, activities: int, horizon: int, and_constraints, or_constraints, bi_constraints, durations,
                 resource_capacity, resource_use, est, eft, lst, lft):
        self.activities = activities
        self.horizon = horizon
        self.and_constraints = and_constraints
        self.or_constraints = or_constraints
        self.bi_constraints = bi_constraints
        self.durations = durations
        self.resource_capacity = resource_capacity
        self.resource_use = resource_use
        self.lst = lst
        self.lft = lft
        self.eft = eft
        self.est = est


def transform_preds(and_constraints):
    precedences = {}
    for successor, predecessor in and_constraints:
        if successor in precedences:
            precedences[successor].append(predecessor)
        else:
            precedences[successor] = []
            precedences[successor].append(predecessor)


    return precedences


def transform_succ(and_constraints):
    precedences = {}
    for successor, predecessor in and_constraints:
        if predecessor in precedences:
            precedences[predecessor].append(successor)
        else:
            precedences[predecessor] = []
            precedences[predecessor].append(successor)

    return precedences


def compute_level_bfs(successors):
    queue = [0]
    level = {0: 0}
    while queue:
        current_task = queue.pop(0)
        if current_task in successors.keys():
            for succ in successors[current_task]:
                if succ not in level.keys():
                    level[succ] = level[current_task] + 1
                else:
                    level[succ] = max(level[succ], level[current_task] + 1)
                queue.append(succ)
    print(level)
    return level


# EST of tasks with no predecessors = First logical starting point.
# EST of tasks with predecessors = Predecessor EFT.
# LFT  = EST of the first dependent task
# LST  = LFT – Task duration
# EFT of tasks with no predecessors = Estimated task duration.
# EFT of tasks with predecessors = (Task EST + Estimated task duration).
# do this before generating or and bi constraints!!!!!!!!
def calculate_est_fst_lft(and_constraints, activities, durations):
    est = {}
    eft = {}
    lst = {}
    lft = {}

    # successor: [predecessors]
    predecessors = transform_preds(and_constraints)

    # predecessor: [successors]
    successors = transform_succ(and_constraints)

    level = compute_level_bfs(successors)
    max_level = max(level)
    # this is a forward pass
    queue = PriorityQueue()
    for i in level.keys():
        queue.put((level[i], i))

    est[0] = 0
    eft[0] = 0

    while not queue.empty():
        priority, current_task = queue.get()
        if current_task == 0:
            continue
        print(current_task)
        if current_task == 23:
            print(eft[10])
            print(eft[18])
        est[current_task] = max([eft[pred] for pred in predecessors[current_task]])
        eft[current_task] = est[current_task] + durations[current_task]


    for i in level.keys():
        queue.put((max_level - level[i], i))

    last_task = activities - 1
    lft[last_task] = eft[last_task] + durations[last_task]
    lst[last_task] = lft[last_task] - durations[last_task] + 1

    while not queue.empty():
        priority, current_task = queue.get()
        if current_task == activities - 1:
            continue
        lft[current_task] = min([lst[succ] for succ in successors[current_task]])
        lst[current_task] = lft[current_task] - durations[current_task] + 1

    print(est)
    print(eft)
    print(lst)
    print(lft)

    return est, eft, lst, lft


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

    est, eft, lst, lft = calculate_est_fst_lft(precedences, activities, durations)
    # or_constraints = generate_or_constraints(k1, k2, activities, precedences)
    or_constraints = {}
    # this should be done either or bi not at the same time
    bi_constraints = {}  # generate_bi_constraints(k1, k2, activities, precedences)

    and_constraints = precedences
    # print(and_constraints)
    # use critical path analysis to find upperbound
    # latest_possible_time = 0
    # for j in range(activities):
    #     if lft[j] > latest_possible_time:
    #         latest_possible_time = lft[j]
    # horizon = latest_possible_time + 1

    return Instance(activities, horizon, and_constraints, or_constraints, bi_constraints, durations, resource_capacity,
                    resource_use, est, eft, lst, lft)


if __name__ == '__main__':
    instance = parse_file("test", 1, 1)
