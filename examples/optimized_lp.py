"""Advanced LP solver demo using gurddy's LPSolver (PuLP backend).

This script constructs a small mixed-integer LP as a demo:
- variables: x1,x2 continuous, y binary
- objective: maximize 3*x1 + 4*x2 + 10*y
- constraints: 2*x1 + x2 <= 20, x1 + 3*x2 + 5*y <= 30, bounds on vars

Requires PuLP installed in the environment. The project's `LPSolver` wraps PuLP.
"""
import sys
from gurddy.model import Model

try:
    from gurddy.solver.lp_solver import LPSolver
except Exception as e:
    print("LPSolver import failed. Ensure PuLP is installed and gurddy package is importable.")
    print(e)
    sys.exit(1)


def build_demo_model():
    m = Model('demo_lp', problem_type='LP')
    # variables: x1,x2 continuous; y binary
    x1 = m.addVar('x1', low_bound=0, cat='Continuous')
    x2 = m.addVar('x2', low_bound=0, cat='Continuous')
    y = m.addVar('y', low_bound=0, up_bound=1, cat='Binary')

    # objective: maximize 3*x1 + 4*x2 + 10*y
    from gurddy.variable import Expression
    obj = Expression(x1) * 3 + Expression(x2) * 4 + Expression(y) * 10
    m.setObjective(obj, sense='Maximize')

    # constraints
    # 2*x1 + x2 <= 20  (use Expression explicitly)
    from gurddy.variable import Expression
    c1 = (Expression(x1) * 2 + Expression(x2) * 1) <= 20
    m.addConstraint(c1)

    # x1 + 3*x2 + 5*y <= 30
    c2 = (Expression(x1) * 1 + Expression(x2) * 3 + Expression(y) * 5) <= 30
    m.addConstraint(c2)

    return m


def main():
    model = build_demo_model()
    solver = LPSolver(model)
    sol = solver.solve()
    if sol is None:
        print('No optimal solution found')
        return
    print('Solution:')
    for k, v in sol.items():
        print(f'  {k} = {v}')


if __name__ == '__main__':
    main()
