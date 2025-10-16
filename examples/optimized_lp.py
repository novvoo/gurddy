"""Advanced LP/MIP demo: production planning, LP relaxation vs MIP, timing and simple sensitivity.

This script uses PuLP directly to demonstrate solver options, timings, and basic sensitivity analysis.
"""
import time
import pulp
from typing import Dict


def build_problem(profits, consumption, capacities, integer=True, name='prod'):
    prob = pulp.LpProblem(name, pulp.LpMaximize)
    products = list(profits.keys())
    # variables
    qty = {}
    for p in products:
        if integer:
            qty[p] = pulp.LpVariable(f'q_{p}', lowBound=0, upBound=None, cat=pulp.LpInteger)
        else:
            qty[p] = pulp.LpVariable(f'q_{p}', lowBound=0, upBound=None, cat=pulp.LpContinuous)

    # objective
    prob += pulp.lpSum([profits[p] * qty[p] for p in products]), 'Profit'

    # resource constraints
    for r, cap in capacities.items():
        prob += (pulp.lpSum([consumption[p][r] * qty[p] for p in products]) <= cap), f'Res_{r}'

    return prob, qty


def solve_and_report(prob, qty, solver_cmd=None):
    t0 = time.perf_counter()
    if solver_cmd is None:
        solver_cmd = pulp.PULP_CBC_CMD(msg=False)
    status = prob.solve(solver_cmd)
    t1 = time.perf_counter()
    obj = pulp.value(prob.objective)
    vals = {name: v.varValue for name, v in qty.items()}
    return status, obj, vals, t1 - t0


def main():
    # Problem data
    profits = {'A': 20, 'B': 24, 'C': 15, 'D': 10}
    # consumption[p][resource]
    consumption: Dict[str, Dict[str, float]] = {
        'A': {'R1': 3, 'R2': 2, 'R3': 2},
        'B': {'R1': 4, 'R2': 3, 'R3': 3},
        'C': {'R1': 2, 'R2': 1, 'R3': 2},
        'D': {'R1': 1, 'R2': 2, 'R3': 1},
    }
    capacities = {'R1': 100, 'R2': 80, 'R3': 90}

    print('Building LP relaxation (continuous vars)')
    lp_prob, lp_qty = build_problem(profits, consumption, capacities, integer=False, name='LP_relax')
    print('Solving LP relaxation...')
    status_lp, obj_lp, val_lp, time_lp = solve_and_report(lp_prob, lp_qty)
    print(f'LP status: {pulp.LpStatus[status_lp]} obj={obj_lp:.4f} time={time_lp:.4f}s')

    print('\nBuilding MIP (integer vars)')
    mip_prob, mip_qty = build_problem(profits, consumption, capacities, integer=True, name='MIP')
    print('Solving MIP...')
    # set a time limit to demonstrate solver options
    solver_cmd = pulp.PULP_CBC_CMD(msg=False, timeLimit=30)
    status_mip, obj_mip, val_mip, time_mip = solve_and_report(mip_prob, mip_qty, solver_cmd=solver_cmd)
    print(f'MIP status: {pulp.LpStatus[status_mip]} obj={obj_mip:.4f} time={time_mip:.4f}s')

    print('\nComparison:')
    print(f'  LP obj = {obj_lp:.4f}  MIP obj = {obj_mip:.4f}  gap = {((obj_lp-obj_mip)/obj_lp*100) if obj_lp else 0:.2f}%')

    print('\nMIP solution:')
    for p, v in val_mip.items():
        print(f'  {p} = {v}')

    # Resource usage and slack
    print('\nResource usage and slacks:')
    for r in capacities:
        used = sum(consumption[p][r] * val_mip[p] for p in profits)
        slack = capacities[r] - used
        print(f'  {r}: used={used:.2f} cap={capacities[r]} slack={slack:.2f}')

    # Simple sensitivity: increase R1 capacity by 10% and re-solve MIP
    print('\nSensitivity: increase R1 by 10% and re-solve MIP')
    capacities2 = dict(capacities)
    capacities2['R1'] = capacities['R1'] * 1.1
    mip2, qty2 = build_problem(profits, consumption, capacities2, integer=True, name='MIP_R1_plus')
    status2, obj2, val2, t2 = solve_and_report(mip2, qty2, solver_cmd=solver_cmd)
    print(f'  New MIP obj={obj2:.4f} time={t2:.4f}s (status {pulp.LpStatus[status2]})')
    print('  Delta obj =', obj2 - obj_mip)


if __name__ == '__main__':
    main()
