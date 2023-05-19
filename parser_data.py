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
        # self.lst = lst
        # self.lft = lft
        # self.eft = eft
        # self.est = est


def transform(and_constraints):
    precedences = {}
    for successor, predecessor in and_constraints:
        if successor in precedences:
            precedences[successor].append(predecessor)
        else:
            precedences[successor] = []
            precedences[successor].append(predecessor)

    print(precedences)
    return precedences


# EST of tasks with no predecessors = First logical starting point.
# EST of tasks with predecessors = Predecessor EFT.
# LFT  = EST of the first dependent task
# LST  = LFT – Task duration
# EFT of tasks with no predecessors = Estimated task duration.
# EFT of tasks with predecessors = (Task EST + Estimated task duration).
# do this before generating or and bi constraints!!!!!!!!
# def calculate_est_fst_lft(and_constraints, activities, durations):
#     est = {}
#     eft = {}
#     lst = {}
#     lft = {}
#
#     precedences = transform(and_constraints)
#     # this is a forward pass
#     queue = []
#     critical_path = []
#     successors = []
#     print("start", and_constraints, "finish")
#     for i in range(activities):
#         if i not in precedences.keys():
#             est[i] = 0
#             eft[i] = durations[i]
#
#             for succ in precedences.keys():
#                 if i in precedences[succ]:
#                     queue.append(succ)
#     while queue:
#         current_task = queue.pop(0)
#         preds = []
#         for pred in precedences[current_task]:
#             if pred in eft.keys():
#                 preds.append(pred)
#         est[current_task] = max([eft[pred] for pred in preds], default= 0)
#         eft[current_task] = est[current_task] + durations[current_task]
#
#         for succ in precedences.keys():
#             if current_task in precedences[succ]:
#                 queue.append(succ)
#
#     last_task = activities - 1
#     lft[last_task] = eft[last_task]
#     lst[last_task] = lft[last_task] - durations[last_task] + 1
#     for pred in precedences[last_task]:
#         queue.append(pred)
#
#     while queue:
#         current_task = queue.pop(0)
#         successors = []
#         for succ in precedences.keys():
#             if current_task in precedences[succ] and succ in lst.keys():
#                 successors.append(succ)
#         lft[current_task] = min([lst[succ] for succ in successors])
#         lst[current_task] = lft[current_task] - durations[current_task] + 1
#         if current_task in precedences.keys():
#             for pred in precedences[current_task]:
#                 queue.append(pred)
#
#     #
#     # for task in reversed(critical_path):
#     #     successors = []
#     #     for i in precedences.keys():
#     #         if task in precedences[i]:
#     #             successors.append(i)
#     #     if successors:
#     #         continue
#     #     lft[task] = max([est[succ] for succ in successors])
#     #     lst[task] = lft[task] - durations[task]
#     # print(est)
#     # print(eft)
#     # print(lst)
#     # print(lft)
#
#     return est, eft, lst, lft


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

    # est, eft, lst, lft = calculate_est_fst_lft(precedences, activities, durations)
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
                    resource_use)


if __name__ == '__main__':
    instance = parse_file("test", 1, 1)
