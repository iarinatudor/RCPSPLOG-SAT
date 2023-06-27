import sys
import time
import os

from pysat.formula import WCNF
from pysat.pb import PBEnc
from pysat.examples.fm import FM
from pysat.card import *

from parser_data import parse_file


def wcnf_file(instance, output_file):
    wcnf = WCNF()

    # y_i,t = 1 means an activity i starts at time t
    # Calculate y_i,t = i * horizon + t + 1

    # Add the completion clauses, with a given horizon this adds clauses
    # that ensure that activities start early enough to finish before the horizon
    # for i in range(instance.activities):
    #     clause = []
    #     for t in range(instance.horizon - instance.durations[i]):
    #         clause.append(i * instance.horizon + t + 1)
    #     wcnf.append(clause)

    for i in range(instance.activities - 1):
        card = []
        for t in range(instance.horizon - instance.durations[i]):
            card.append(i * instance.horizon + t + 1)
        cnf = CardEnc.equals(card, encoding=EncType.pairwise)

        for clause in cnf.clauses:
            # print(clause)
            wcnf.append(clause)




    # Add the AND precedence clauses to ensure an activity doesn't start before its predecessors have finished
    for succ, pred in instance.and_constraints:
        for succ_t in range(instance.horizon - instance.durations[succ]):
            clause = []
            for pred_t in range(succ_t - instance.durations[pred] + 1):
                clause.append(pred * instance.horizon + pred_t + 1)
            clause.append(-(succ * instance.horizon + succ_t + 1))
            wcnf.append(clause)

    # Add clauses that ensure that the project cannot finish without finishing all jobs
    if len(instance.or_constraints) != 0 or len(instance.bi_constraints) != 0:
        for i in range(instance.activities - 1):
            for succ_t in range(instance.horizon):
                clause = []
                for pred_t in range(succ_t - instance.durations[i] + 1):
                    clause.append(i * instance.horizon + pred_t + 1)
                clause.append(-((instance.activities - 1) * instance.horizon + succ_t + 1))
                wcnf.append(clause)

    # Add the OR precedence clauses to ensure an activity can start once one of its predecessors has finished

    for succ in instance.or_constraints.keys():
        for succ_t in range(instance.horizon - instance.durations[succ]):
            clause = []
            for pred in instance.or_constraints[succ]:
                for pred_t in range(succ_t - instance.durations[pred] + 1):
                    clause.append(pred * instance.horizon + pred_t + 1)
            clause.append(-(succ * instance.horizon + succ_t + 1))
            wcnf.append(clause)

    # x_i,t means an activity i is active at time t
    # Calculate x_i,t = activities * horizon + i * horizon + t + 1

    for i in range(instance.activities - 2):
        for t in range(instance.horizon - instance.durations[i + 1] + 1):
            for runtime in range(instance.durations[i + 1]):
                clause = []
                clause.append(-((i + 1) * instance.horizon + t + 1))
                clause.append(instance.activities * instance.horizon + (i + 1) * instance.horizon + t + runtime + 1)
                wcnf.append(clause)

    # Add the BI precedence clauses to ensure an activity cannot
    # start if it has a bi constraint with an active activity, using activity variables
    for succ in instance.bi_constraints.keys():
        for pred in instance.bi_constraints[succ]:
            for t in range(instance.horizon):
                wcnf.append([-(instance.activities * instance.horizon + pred * instance.horizon + t + 1),
                             -(instance.activities * instance.horizon + succ * instance.horizon + t + 1)])

    # add constraints for est and eft
    # print(instance.est)
    # for i in range(instance.activities):
    #     for t in range(instance.est[i]):
    #         print(t)
    #         print(i, i * instance.horizon + t + 1)
    #         wcnf.append([-(i * instance.horizon + t + 1)], 1)
    #
    # for i in range(instance.activities):
    #     for t in range(instance.eft[i] + 1, instance.horizon + 1, 1):
    #         wcnf.append([(i * instance.horizon + t + 1)])

    # Add the resource constraint clauses that ensure for each resource
    # at each time point, that the consumption is less than or equal to the availability
    for r in range(len(instance.resource_capacity)):
        for t in range(instance.horizon):
            resourcereqcnfs = PBEnc.atmost(
                lits=[instance.activities * instance.horizon + i * instance.horizon + t + 1 for i in
                      range(instance.activities - 1)],
                weights=[instance.resource_use[i][r] for i in range(instance.activities - 1)],
                bound=instance.resource_capacity[r],
                top_id=wcnf.nv,
                encoding=0
            )
            wcnf.extend(resourcereqcnfs)

    # Add the soft clauses that determine the makespan of the project
    for value in range(instance.horizon):
        wcnf.append([((instance.activities - 1) * instance.horizon + value + 1)], weight=1)

    fm = FM(wcnf, verbose=0)
    # fm.compute()  # set of hard clauses should be satisfiable
    # print(fm.compute())
    # print(fm.cost)
    # print(fm.model)
    # j = 0
    # for i in fm.model:
    #     if i > 0 and j <= instance.activities:
    #         print("activity " + str(j) + " is scheduled from " + str(i - 1 - j * instance.horizon) )
    #         j +=1
    wcnf.to_file(output_file)

def create_metadata(instance, filename):
    # the key is the activity and the
    metadata = {}
    logical_constraints = {}

    for succ, predecessor in instance.and_constraints:
        if succ in logical_constraints.keys():
            logical_constraints[succ] += 1
        else:
            logical_constraints[succ] = 1

    for succ in instance.or_constraints.keys():
        if succ in logical_constraints.keys():
            logical_constraints[succ] += len(instance.or_constraints[succ])
        else:
            logical_constraints[succ] = len(instance.or_constraints[succ])

    for succ in instance.bi_constraints.keys():
        if succ in logical_constraints.keys():
            logical_constraints[succ] += len(instance.bi_constraints[succ])
        else:
            logical_constraints[succ] = len(instance.bi_constraints[succ])

    for i in range(instance.activities):
        nr = 0
        if i in logical_constraints.keys():
            nr = logical_constraints[i]
        metadata[i] = ['c', instance.est[i], instance.lst[i], nr]

    output = os.path.join("metadata", filename)

    with open(filename, "a") as file:
        line = ' '.join(map(str, ['c', instance.activities, instance.horizon, max(instance.lft.values())])) + '\n'
        file.write(line)
        for values in metadata.values():
            line = ' '.join(map(str, values)) + '\n'
            file.write(line)

    file.close()

if __name__ == '__main__':

    # # filename = sys.argv[1]
    j = 1
    for filename in os.listdir("datasets\j60"):
        f = os.path.join("datasets\j60", filename)
        # checking if it is a file

        if os.path.isfile(f) and j < 71:
            # k1 = 1
            k2_range = [10]
            for k2 in k2_range:
                output_file = os.path.join("encodings\j60\BI10", filename)
                instance = parse_file(f, 1, k2)
                wcnf_file(instance, output_file)

                [os.rename(output_file, output_file.replace('.sm', '.wcnf'))]
                create_metadata(instance, output_file.replace('.sm', '.wcnf'))
        j += 1
        print(j)
        if j >= 71:
            break
    # wcnf_file(parse_file("test3", 1, 1), "test2")
