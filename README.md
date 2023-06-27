This is part of the <a href="https://github.com/TU-Delft-CSE/Research-Project" target="_blank">Research Project 2023</a>  of <a href="https://https//github.com/TU-Delft-CSE" target="_blank">TU Delft University</a>

# Description
RCPSP-log with logical constraints is an extension of the classic RCPSP problem, adding OR and BI constraints. The approach involves SAT solving with variables selection heuristics inspired from greedy schedule as early as possible and conflict analysis.

The datasets come from PSPLIB and are transformed for RCPSP-log using the parser_data.py. Furthermore, the instances are converted to wcnf in encoder.py. The files have problem specific metadata included, allowing for reproducing the heuristics using any MAXSat solver. 
