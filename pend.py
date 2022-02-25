import os

import numpy as np
from matplotlib import pyplot as plt
from numpy import cos, pi as PI, sin
from scipy.integrate import odeint


fig, ax = plt.subplots(1, 1, figsize=(20, 20))

# CONSTANTS
class Pendulum(object):
    """docstring for Pendulum"""
    def __init__(self, THETA_1=None, MASS_1=None, LEN_1=None, THETA_2=None, MASS_2=None, LEN_2=None, GRAV=None):

        if THETA_1 is None: self.THETA_1 = PI/4
        else: self.THETA_1 = THETA_1

        if MASS_1 is None: self.MASS_1 = 1
        else: self.MASS_1 = MASS_1

        if LEN_1 is None: self.LEN_1 = 3
        else: self.LEN_1 = LEN_1

        if THETA_2 is None: self.THETA_2 = PI/8
        else: self.THETA_2 = THETA_2

        if MASS_2 is None: self.MASS_2 = 2
        else: self.MASS_2 = MASS_2

        if LEN_2 is None: self.LEN_2 = 4
        else: self.LEN_2 = LEN_2

        if GRAV is None: self.GRAV = 9.81
        else: self.GRAV = GRAV

        self.CAP_DELTHETA = lambda t1, t2: t1 - t2
        self.CAP_MASS = self.MASS_2 / (self.MASS_1 + self.MASS_2)
        self.CAP_LEN = self.LEN_2/self.LEN_1
        self.CAP_OMEGA = self.GRAV / self.LEN_1

    def solveAngles(self, theta1, theta2, dtheta1, dtheta2):
        mass = self.CAP_MASS
        LEN = self.CAP_LEN
        omega = self.CAP_OMEGA
        deltatheta = self.CAP_DELTHETA(theta1, theta2)
        omegatwo = pow(omega, 2)
        
        top_left_first = omegatwo * LEN
        top_left_second = mass * cos(deltatheta) * sin(theta2)
        top_left_second -= sin(theta1)
        top_left = top_left_first * top_left_second
        top_right_first = mass * LEN
        top_right_second = pow(dtheta1, 2) * cos(deltatheta)
        top_right_second += LEN * pow(dtheta2, 2)
        top_right_third = sin(deltatheta)
        top_right = top_right_first * top_right_second * top_right_third
        top = top_left - top_right
        
        theta_2_top = ( omegatwo * cos(deltatheta) * sin(theta1) ) - ( omegatwo * sin(theta2) )
        theta_2_top += ( pow(dtheta1, 2) + ( mass * LEN * dtheta2 * dtheta2 * cos(deltatheta) )) * sin(deltatheta)
        
        bottom = LEN - mass * LEN * pow( cos(deltatheta), 2 )
        second_theta_1 = top / bottom
        second_theta_2 = theta_2_top / bottom
        
        return second_theta_1, second_theta_2

    def polarToCartesian(self, dist, thet, spoint=[0,0]):
        xi, yi = spoint
        return [ xi + (dist * cos(thet)), yi + (dist * sin(thet)) ]

    def pendulumToXY(self, theta1L, theta2L):
        len1 = self.LEN_1
        len2 = self.LEN_2
        LST = [theta1L, theta2L]
        PLOT_THETA1_X, PLOT_THETA1_Y = [ [], [] ]
        PLOT_THETA2_X, PLOT_THETA2_Y = [ [], [] ]
        for theta1i, theta2i in list(zip(*LST)):
            theta1 = theta1i - PI/2
            theta2 = theta2i - PI/2
            pointM1 = self.polarToCartesian(len1, theta1)
            pointM2 = self.polarToCartesian(len2, theta2, spoint=pointM1)
            PLOT_THETA1_X.append( pointM1[0] )
            PLOT_THETA2_X.append( pointM2[0] )
            
            PLOT_THETA1_Y.append( pointM1[1] )
            PLOT_THETA2_Y.append( pointM2[1] )
        return [ [ PLOT_THETA1_X, PLOT_THETA1_Y ], [ PLOT_THETA2_X, PLOT_THETA2_Y ] ]


    def derive(self, z, t):
        tmp_dtheta1, tmp_dtheta2, tmp_theta1, tmp_theta2 = z
        # Second Derivative Theta 1
        # Second Derivative Theta 2
        # First Derivative Theta 1
        # First Derivative Theta 2
        second_1, second_2 = self.solveAngles(tmp_theta1, tmp_theta2, tmp_dtheta1, tmp_dtheta2)
        return np.array([
            second_1,
            second_2,
            tmp_dtheta1,
            tmp_dtheta2
        ])

    def generate(self, tmax=10, dt=0.01, manim=True):
        t = np.arange(0, tmax, dt)
        SOLS = []
        MN = None
        MX = 0

        sol = odeint(self.derive, [self.THETA_1, self.THETA_2, 0, 0], t)
        THETA_SOL_1 = sol[..., 0]
        THETA_SOL_2 = sol[..., 1]

        (graph_theta1), (graph_theta2) = self.pendulumToXY(THETA_SOL_1, THETA_SOL_2)
        theta1x, theta1y = graph_theta1
        theta2x, theta2y = graph_theta2

        times = []
        if manim:
            NODE_INIT = [ 0, 0 ]
            FIRS_INIT = [ theta1x[0], theta1y[0] ]
            SECO_INIT = [ theta2x[0], theta2y[0] ]
            for i in range(1, len(theta1x)):
                theta1X = theta1x[i]
                theta1Y = theta1y[i]
                theta2X = theta2x[i]
                theta2Y = theta2y[i]
                POS_1 = [ theta1X, theta1Y ]
                POS_2 = [ theta2X, theta2Y ]
                times.append( [ [0,0], POS_1, POS_2, ] )
            return times, dt, NODE_INIT, FIRS_INIT, SECO_INIT, self.LEN_1, self.LEN_2
        else:
            return theta1x, theta1y, theta2x, theta2y

if __name__ == "__main__":
    CLASS = Pendulum()
    t1x, t1y, t2x, t2y = CLASS.generate(manim=False)
    plt.plot(t2x, t2y)
    plt.savefig(os.path.join(os.path.dirname(__file__), "pendulum.png"))