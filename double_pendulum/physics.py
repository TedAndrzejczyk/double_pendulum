from animation import animating  # physics module imports animation module

import numpy as np  # for calculations
import sympy as smp  # for symbolic
from scipy.integrate import odeint  # odeint calculations


# import parameters as [g, l1, l2, m1, m2]
def physics_calcs(parameters):
    # Defining the variables
    t, g = smp.symbols('t g')
    m1, m2 = smp.symbols('m1 m2')
    L1, L2 = smp.symbols('L1 L2')

    # symbols
    the1, the2 = smp.symbols(r'\theta_1, \theta_2', cls=smp.Function)

    # function of time
    the1 = the1(t)
    the2 = the2(t)

    # differentiate thetas
    the1_d = smp.diff(the1, t)
    the2_d = smp.diff(the2, t)
    the1_dd = smp.diff(the1_d, t)
    the2_dd = smp.diff(the2_d, t)

    # calculate coordinates
    x1 = L1 * smp.sin(the1)
    y1 = -L1 * smp.cos(the1)
    x2 = L1 * smp.sin(the1) + L2 * smp.sin(the2)
    y2 = -L1 * smp.cos(the1) - L2 * smp.cos(the2)

    # Kinetic
    K1 = 1 / 2 * m1 * (smp.diff(x1, t) ** 2 + smp.diff(y1, t) ** 2)
    K2 = 1 / 2 * m2 * (smp.diff(x2, t) ** 2 + smp.diff(y2, t) ** 2)
    K = K1 + K2

    # Potential
    U1 = m1 * g * y1
    U2 = m2 * g * y2
    U = U1 + U2

    # Lagrangian
    L = K - U

    # Differentiates Lagrangian
    LE1 = smp.diff(L, the1) - smp.diff(smp.diff(L, the1_d), t).simplify()
    LE2 = smp.diff(L, the2) - smp.diff(smp.diff(L, the2_d), t).simplify()

    # solves the Lagrangian
    sols = smp.solve([LE1, LE2], (the1_dd, the2_dd),
                     simplify=False, rational=False)

    # numerical evaluation
    dz1dt_f = smp.lambdify((t, g, m1, m2, L1, L2, the1, the2, the1_d, the2_d), sols[the1_dd])
    dz2dt_f = smp.lambdify((t, g, m1, m2, L1, L2, the1, the2, the1_d, the2_d), sols[the2_dd])
    dthe1dt_f = smp.lambdify(the1_d, the1_d)
    dthe2dt_f = smp.lambdify(the2_d, the2_d)

    # returns lambdify expressions
    def dSdt(S, t, g, m1, m2, L1, L2):
        the1, z1, the2, z2 = S
        return [
            dthe1dt_f(z1),
            dz1dt_f(t, g, m1, m2, L1, L2, the1, the2, z1, z2),
            dthe2dt_f(z2),
            dz2dt_f(t, g, m1, m2, L1, L2, the1, the2, z1, z2),
        ]

    # time
    t = np.linspace(0, 40, 1001)

    g = parameters[0]  # m/s^2
    L1 = parameters[1] / 100  # cm -> m
    L2 = parameters[2] / 100  # cm -> m
    m1 = parameters[3]  # kg
    m2 = parameters[4]  # kg

    # find answer using odeint
    ans = odeint(dSdt, y0=[1, -3, -1, 5], t=t, args=(g, m1, m2, L1, L2))

    # transpose thetas
    the1 = ans.T[0]
    the2 = ans.T[2]

    # manual computation for K and U lists
    x1 = L1 * np.sin(the1)
    y1 = -L1 * np.cos(the1)
    x2 = L1 * np.sin(the1) + L2 * np.sin(the2)
    y2 = -L1 * np.cos(the1) - L2 * np.cos(the2)
    K1 = 1 / 2 * m1 * (np.gradient(x1, t) ** 2 + np.gradient(y1, t) ** 2)
    K2 = 1 / 2 * m2 * (np.gradient(x2, t) ** 2 + np.gradient(y2, t) ** 2)
    U1 = m1 * g * y1
    U2 = m2 * g * y2
    K = list(K1 + K2)
    U = list(U1 + U2)

    # function to get coordinates
    def get_x1y1x2y2(t, the1, the2, L1, L2):
        return (L1 * np.sin(the1),
                -L1 * np.cos(the1),
                L1 * np.sin(the1) + L2 * np.sin(the2),
                -L1 * np.cos(the1) - L2 * np.cos(the2))

    # assign coordinates
    x1, y1, x2, y2 = get_x1y1x2y2(t, ans.T[0], ans.T[2], L1, L2)

    # animate using coordinates and energy values
    animating(x1, y1, x2, y2, K, U)
