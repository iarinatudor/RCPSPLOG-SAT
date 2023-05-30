import sys
import time
import os

from pysat.formula import WCNF
from pysat.pb import PBEnc
from pysat.examples.fm import FM

from parser_data import parse_file


def wcnf_file(instance, output_file):
    wcnf = WCNF()

    # y_i,t = 1 means an activity i starts at time t
    # Calculate y_i,t = i * horizon + t + 1

    # Add the completion clauses, with a given horizon this adds clauses
    # that ensure that activities start early enough to finish before the horizon
    for i in range(instance.activities):
        clause = []
        for t in range(instance.horizon - instance.durations[i]):
            clause.append(i * instance.horizon + t + 1)
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

    # Add consistency clauses for the activity variables
    for i in range(instance.activities - 2):
        for t in range(instance.horizon - instance.durations[i + 1] + 1):
            for runtime in range(instance.durations[i + 1]):
                clause = [-((i + 1) * instance.horizon + t + 1),
                          instance.activities * instance.horizon + (i + 1) * instance.horizon + t + runtime + 1]
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

    # fm = FM(wcnf, verbose=0)
    # # fm.compute()  # set of hard clauses should be satisfiable
    # print(fm.compute())
    # # print(fm.model)
    # print(fm.cost)
    wcnf.to_file(output_file)


if __name__ == '__main__':

    # # filename = sys.argv[1]
    # j = 1
    # for filename in os.listdir("datasets\j60"):
    #     f = os.path.join("datasets\j60", filename)
    #     # checking if it is a file
    #
    #     if os.path.isfile(f):
    #         k1 = 1
    #         k2_range = [1, 2, 5, 10]
    #         for k2 in k2_range:
    #             output_file = os.path.join("encodings\BI" + str(k2), filename)
    #             wcnf_file(parse_file(f, k1, k2), output_file)
    #         j += 1
    #         print(j)
    os.chdir('C:/Users/Iarina/PycharmProjects/RP/ResearchProject/encodings/BI2')
    [os.rename(f, f.replace('.sm', '.wcnf')) for f in os.listdir('.') if f.endswith('.sm')]
