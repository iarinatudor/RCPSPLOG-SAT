from parser_data import Instance
import os


def create_metadata(instance: Instance, filename):
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
        metadata[i] = [(i * instance.horizon + 1), (i * instance.horizon + instance.horizon + 1), instance.est[i],
                       instance.lst[i], logical_constraints[i]]

    output = os.path.join("metadata", filename)

    with open(output, 'w') as file:
        for values in metadata.values():
            line = ' '.join(map(str, values)) + '\n'
            file.write(line)

    file.close()


# def nr_logical_constraints(instance: Instance, filename):
#     logical_constraints = {}
#
#     for succ, predecessor in instance.and_constraints:
#         if succ in logical_constraints.keys():
#             logical_constraints[succ] += 1
#         else:
#             logical_constraints[succ] = 1
#
#     for succ in instance.or_constraints.keys():
#         if succ in logical_constraints.keys():
#             logical_constraints[succ] += len(instance.or_constraints[succ])
#         else:
#             logical_constraints[succ] = len(instance.or_constraints[succ])
#
#     for succ in instance.bi_constraints.keys():
#         if succ in logical_constraints.keys():
#             logical_constraints[succ] += len(instance.bi_constraints[succ])
#         else:
#             logical_constraints[succ] = len(instance.bi_constraints[succ])
#
#     output = os.path.join("metadata", filename)
#
#     with open(output, 'w') as file:
#         for values in logical_constraints.values():
#             line = ' '.join(map(str, values)) + '\n'
#             file.write(line)
#
#     file.close()
