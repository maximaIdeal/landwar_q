#!/usr/bin/env python
#
#
#
#
#

import json
import math
import os
import sys
import time

sys.path.append("../")
sys.path.append("../engine")
sys.path.append("../ai")
sys.path.append("../")
import random
import copy
from core.agent.base_agent import BaseAgent
from core.utils.map import Map
from yours.const import BopType, ActionType, MoveType

RED = 0
BLUE = 1
ChangeState = ActionType.ChangeState
GetOff = ActionType.GetOff
GetOn = ActionType.GetOn
GuideShoot = ActionType.GuideShoot
JMPlan = ActionType.JMPlan
Move = ActionType.Move
StopMove = ActionType.StopMove
Occupy = ActionType.Occupy
RemoveKeep = ActionType.RemoveKeep
Shoot = ActionType.Shoot
Waiting = 999

TANK = 0
CAR = 1
SOILDER = 2
ARTILLERY = 3
AUTO_CAR = 4
AUTO_PLANE = 5
HELICOPTER = 6
MISSILE = 7
ALL_OPT = [TANK, CAR, SOILDER, ARTILLERY, AUTO_CAR, AUTO_PLANE, HELICOPTER, MISSILE]
CARS = [TANK, CAR, AUTO_CAR]
ALL_OPT_1 = [TANK, CAR, AUTO_CAR, SOILDER]
FLY_OPT = [MISSILE, HELICOPTER, AUTO_PLANE]
#
FIRST_MOVING_STEP = 0
ALL_ATTACKI_STEP = 1
ALL_ASSISTOCCUPY_STEP = 2
ALL_OCCUPY_STEP = 3

NormalMove = 0  #
March = 1  #
Charge_1 = 2  #
Charge_2 = 3  #
Hide = 4  #

MoveType_car = 0  #
MoveType_march = 1  #
MoveType_soilder = 2  #
MoveType_fly = 3  #

#
STRATEGY_AUTO = 0  #
STRATEGY_FIRSTSTEP = 1  #
STRATEGY_TANK_PROTECT_CAR = 2  #
STRATEGY_PUSH = 3  #
STRATEGY_WAITING = 4
STRATEGY_BOOMING_TEAM = 5
FIRST_POS_S1 = {
    #
    100: [
        #
        4539, 4537, 4435, None, None, 4536, 4435, None, None, None,  #
        4641, 4339, 4338, 3936, 3935, 3734, 3732, 3733, None, None,  #
        4742, 4643, None, None, None, None, None, None, None, None,  #
        4539, 4536, 4436, None, None, None, None, None, None, None,  #
        4029, 4030, None, None, None, None, None, None, None, None,  #
        None],
    400: [
        4945, 4943, 4642, 4537, 4435, None, None, None, None, None,  #
        #
        #
        4843, 4743, 4140, 3839, 3430, 4029, None, None, None, None,  #
        4029, 4030, None, None, None, None, None, None, None, None,  #
        None],
    0: [  #
        4334, 4435, 4436, None, None, None, None, None, None, None,  #
        4338, 3936, 3935, 3734, 3730, 4029, 4030, None, None, None,  #
        4339, 4440, 4539, 4535, 4435, 4335, None, None, None, None,  #
        4029, 4030, None, None, None, None, None, None, None, None,  #
        4536, 4539, 4440, 4339, 4338, None, 3936, 3935, 3734, 3730,
        4029, 4030, 3929, None, None, None, None, None, None, None,  #
        None],
    200: [
        4435, 4334, None, None, 4436, 4435, 4334, None, None, None,  #
        4029, None, None, None, None, None, None, None, None, None,  #
        5438, 5437, 5439, 4435, None, None, None, None, None, None,  #
        None],
    700: [
        4635, 4535, 4436, 4437, 4436, 4435, 4334, 4234, 4133, 4033, 4032, 4031, 4030,
        None],
    701: [
        4436, 4435, 4030, None, None, None, None, None, None, None,  #
        None],
    10101: [  #
        4232, 4332, 4334, None, None, None, None, None, None, None,  #
        4031, 3930, 4030, None, None, None, None, None, None, None,  #
        #
        None],
    10201: [  #
        4333, 4334, 4435, 4436, 4435, None, None, None, None, None,
        4335, 4334, None, None, None, None, None, None, None, None,
        None],
    10100: [  #
        #
        4029, 4333, 4334, None, None, None, None, None, None, None,  #
        4031, 3930, 4030, None, None, None, None, None, None, None,  #
        None],
    10200: [  #
        4333, 4434, 4435, 4334, None, None, None, None, None, None,
        None],
    10000: [
        4734, 4935, 4938, 4937, 4436, 4437, None, None, None, None,
        4129, 4029, None, None, 4435, 4334, None, None, None, None,
        None]  #
}
FIRST_POS_S8_1 = {
    #
    100: [
        2931, None, None, None, None, None, None, None, None, None,  #
        3337, 2930, None, None, None, None, None, None, None, None,  #
        3338, 2640, None, None, None, None, None, None, None, None,  #
        2931, 3032, None, None, None, None, None, None, None, None,  #
        None],
    400: [
        3426, 3826, 3827, 3828, None, None, None, None, None, None,  #
        None],
    0: [  #
        3636, 4140, None, None, None, None, None, None, None, None,  #
        None],
    200: [
        3636, 3032, 2932, 2933, 3436, 3637, 3636, None, None, None,  #
        None],
    700: [
        4635, 4535, 4436, 4437, 4436, 4435, 4334, 4234, 4133, 4033, 4032, 4031, 4030,
        None],
    701: [
        4436, 4435, 4030, None, None, None, None, None, None, None,  #
        None],
    10101: [  #
        4041, 4040, None, None, None, None, None, None, None, None,  #
        3942, 4040, None, None, None, None, None, None, None, None,  #
        None],
    10201: [  #
        4038, 3837, 3736, 3636, 4038, None, None, None, None, None,  #
        3940, 3939, 4039, 4038, None, 3735, None, None, None, None,  #
        None],
    10100: [  #
        4139, 3836, None, None, None, None, None, None, None, None,  #
        3841, 3836, None, None, None, None, None, None, None, None,  #
        None],
    10200: [  #
        4039, 3837, 3736, 3636, 4038, None, None, None, None, None,  #
        3737, 3736, 3636, None, None, 3735, None, None, None, None,  #
        None],
    10000: [  #
        #
        3636, 3735, 3835, 3735, 3736, None, None, None, None, None,  #
        None],
    10001: [  #
        #
        3636, 3735, 3835, 3735, 3736, None, None, None, None, None,  #
        None]
}
FIRST_POS_S8_2 = {
    #
    100: [
        4244, 3640, None, None, None, None, None, None, None, None,  #
        3337, 2930, None, None, None, None, None, None, None, None,  #
        3338, 2640, None, None, None, None, None, None, None, None,  #
        2931, 3032, None, None, None, None, None, None, None, None,  #
        None],
    400: [
        4245, 3740, None, None, None, None, None, None, None, None,  #
        None],
    0: [  #
        #
        3841, 3940, None, None, 3639, 3539, None, None, None, None,
        4238, 4241, 3941, 3740, 3640, 3737, 3736, 3636, 3735, None,
        None],
    200: [
        3841, 3739, 3639, 3636, 3735, None, None, None, None, None,  #
        None],
    700: [
        3739, 3736, 3636, 3634, 3434, 3636, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
        None],
    701: [
        3739, 3736, 3636, 3634, 3434, 3636, None, None, None, None,  #
        None, None, None, None, None, None, None, None, None, None,
        None],
    10101: [  #
        3534, 3735, None, None, None, None, None, None, None, None,  #
        3942, 4040, None, None, None, None, None, None, None, None,  #
        None],
    10201: [  #
        #
        3636, 3736, 3739, 3639, None, None, None, None, None, None,  #
        3637, None, None, None, None, None, None, None, None, None,  #
        None],
    10100: [  #
        3333, 3334, 3737, 3735, None, None, None, None, None, None,  #
        3841, 3836, None, None, None, None, None, None, None, None,  #
        None],
    10200: [  #
        #
        3636, 3736, 3739, 3738, 3738, None, None, None, None, None,  #
        3736, None, None, None, None, None, None, None, None, None,  #
        3737, 3739, None, None, None, None, None, None, None, None,
        #
        None],
    10000: [  #
        #
        3636, 3739, 3940, 4040, 4041, 3944, None, None, None, None,  #
        3740, 3640, 3737, 3736, 3637, None, None, 3639, None, 3737,
        None],
    10001: [  #
        #
        4136, 4138, 4239, 4242, None, None, None, None, None, None,  #
        3740, 3640, 3737, 3736, 3637, None, None, 3639, None, 3737,
        None]
}
#
UNIT = 1  #
GROUP = 3  #

SUCCESS = 1
FAILURE = 0
RUNNING = 3
FIRST_POS_Q32 = {
    #
    5300: [
        #
        1006, 1105, 1407, 1506, 1908, 2008, 2309, 2311, 2412, 2611, 2613,
        None],
    5301: [
        #
        1006, 1105, 1407, 1506, 1908, 2008, 2309, 2311, 2412, 2611, 2614,
        None],
    5302: [
        #
        1006, 1105, 1407, 1506, 1908, 2008, 2309, 2311, 2412, 2611, 2711,
        None],
    5303: [
        1006, 1105, 1407, 1506, 1908, 2008, 2309, 2311, 2412, 2611, 2712,
        #
        None],
    5304: [
        #
        1006, 1105, 1407, 1506, 1908, 2008, 2309, 2311, 2412, 2511, 2813,
        None],
    5305: [
        #
        1006, 1105, 1407, 1506, 1908, 2008, 2309, 2311, 2412, 2511, 2814,
        None],
    #
    400: [
        #
        #
        2022, 2025, 2326, 2725, 2924, 3025, 3124, 3426, 3724, 4026,
        4029, 4129, 4131, 3932, None, None, None, None, None, None,
        None],
    1400: [
        #
        2321, 2426, 2725, 2924, 3025, 3124, 3426, 3724, 4026, 4029,
        4129, 4131, 3933, None, None, None, None, None, None, None,
        #
        None],
    2400: [
        2218, 2124, 2526, 2725, 2924, 3025, 3124, 3426, 3724, 4026,
        4029, 4129, 4131, 3831, None, None, None, None, None, None,
        #
        #
        None],
    3400: [
        2316, 2517, 2521, 2722, 2724, 2625, 2524, 2725, 2924, 3025,
        3124, 3426, 3724, 4026, 4029, 4129, 4131, 3930, None, None,
        #
        #
        None],
    #
    100: [
        #
        1311, 1412, 1414, 2117, 2120, 2723, 2724, 3026, None, None,
        None],
    1100: [
        #
        #
        1412, 1414, 2117, 2120, 2723, 2724, 3026, 3025, None, None,
        None],
    2100: [
        #
        1817, 2319, 2822, 2721, 3020, 3120, 3221, None, None, None,
        None],
    3100: [
        #
        #
        1917, 2219, 2822, 2721, 3020, 3120, 3221, None, None, None,
        None],
    #
    200: [
        3032, 3333, 3435, None, None, None, None, None, None, None,  #
        None],
    1200: [
        3628, 3827, 4028, 4030, 3829, 3630, None, None, None, None,  #
        #
        None],
    2200: [
        1818, 1821, 1921, 1928, 2330, 2331, 2335, 2737, 2736, None,  #
        #
        None],
    3200: [
        2220, 2320, 2523, 2624, 2826, 3630, 3829, 3729, None, None,  #
        None],

    #

    0: [
        #
        #
        1719, 1819, 2924, 3025, 3124, 3426, 3724, 4026, 4029, 4129,
        4131, 3833, None, None, None, None, None, None, None, None,
        None],
    1000: [
        1623, 2427, 2825, 2924, 2925, 3025, 3124, 3426, 3724, 4026,
        4029, 4129, 4131, 3834, None, None, None, None, None, None,
        #
        #
        None],
    2000: [
        2721, 2723, 2924, 2925, 3025, 3124, 3426, 3724, 4026, 4029,
        4129, 4131, 3733, None, None, None, None, None, None, None,
        #
        None],
    3000: [
        1920, 2021, 2022, 2725, 2825, 3025, 3124, 3426, 3724, 4026,
        4029, 4129, 4131, 3732, None, None, None, None, None, None,
        #
        #
        None],
    #
    700: [
        #
        2436, 2838, None, None, None, None, None, None, None, None,
        None],
    1700: [
        3729, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    2700: [
        3729, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    3700: [
        3729, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    701: [
        2436, 2838, None, None, None, None, None, None, None, None,
        #
        #
        None],
    1701: [
        3729, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    2701: [
        3729, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    3701: [
        3729, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    #
    4600: [
        #
        2411, 3810, 4613, 5119, 5229, 5641, 5150, 5167, 2564, None,
        None],
    4601: [
        2320, None, None, None, None, None, None, None, None, None,  #
        None],
    #
    4500: [
        2431, 2128, 1929, 1733, 1938, 1845, None, None, None, None,  #
        None],
    4501: [
        3023, 3824, 4128, 4534, 4540, 4442, None, None, None, None,  #
        None],
    #
    #
    10000: [  #
        #

        #
        2332, 2331, 2330, None, None, None, None, None, None, None,  #
        2729, 2829, 2828, 2727, 2627, 2526, 2427, 2326, 2028, 1827,
        2829, 2828, 2727, 2721, 3118, 2116, None, None, None, None,
        None],
    10100: [  #
        #
        2436, None, None, None, None, None, None, None, None, None,  #
        2531, None, None, None, None, None, None, None, None, None,  #
        None],
    10101: [  #
        2535, None, None, None, None, None, None, None, None, None, None,  #
        None],
    10200: [  #
        2034, 2737, None, None, None, None, None, None, None, None,  #
        2738, 2838, 2837, 2736, 2637, 2638, 2737, None, None, None,
        None],
    10201: [  #
        2331, 2737, None, None, None, None, None, None, None, None,  #
        2738, 2838, 2837, 2736, 2637, 2638, 2737, None, None, None,
        3242, None, None, None, None, None, None, None, None, None,  #
        3243, 3342, 3341, 3241, 3141, 3142, 3242, None, None, None,
        None],
    #

    #
    #

    11000: [  #
        #
        #
        2432, 2431, 2430, None, None, None, None, None, None, None,  #
        2829, 2828, 2426, 1826, None, None, None, None, None, None,
        2829, 2828, 2727, 2721, 3118, 2017, None, None, None, None,
        None],
    11100: [  #
        2941, 2838, None, None, None, None, None, None, None, None, None,  #
        None],
    11101: [  #
        2532, None, None, None, None, None, None, None, None, None,  #
        None],
    11200: [  #
        3136, None, None, None, None, None, None, None, None, None,  #
        #
        3137, 3237, 3236, 3135, 3036, 3037, 3136, None, None, None,
        None],
    11201: [  #
        #
        #
        3242, None, None, None, None, None, None, None, None, None,  #
        3243, 3342, 3341, 3241, 3141, 3142, 3242, None, None, None,
        None],
    #

    #
    #

    12000: [  #
        #
        #
        4028, 3929, 3636, 3032, 2633, 2532, 2531, 2530, None, None,
        2828, 2729, 2829, 2828, 2727, 2627, 2526, 2427, 2326, 1826,
        2928, 2929, 2829, 2828, 2727, 2721, 3118, 2118, None, None,
        None],
    12100: [  #
        #
        #
        3137, None, None, None, None, None, None, None, None, None,
        None],
    12101: [  #
        #
        #
        3436, None, None, None, None, None, None, None, None, None,
        None],
    12200: [  #
        3829, None, None, None, None, None, None, None, None, None,  #
        3830, 3929, 3928, 3828, 3728, 3729, 3829, None, None, None,
        None],
    12201: [  #
        3630, None, None, None, None, None, None, None, None, None,  #
        3631, 3730, 3729, 3629, 3529, 3530, 3630, None, None, None,
        None],
    #

    #
    #

    13000: [  #
        #
        #
        2936, 2937, 2838, 2737, 2736, None, None, None, None, None,
        2828, 2526, 2326, 2027, None, None, None, None, None, None,
        2828, 2727, 2721, 3118, 2018, None, None, None, None, None,
        None],
    13100: [  #
        #
        3730, None, None, None, None, None, None, None, None, None,
        None],
    13101: [  #
        #
        3929, None, None, None, None, None, None, None, None, None,
        None],
    13200: [  #
        3033, None, None, None, None, None, None, None, None, None,  #
        3034, 3133, 3132, 3032, 2932, 2933, 3033, None, None, None,
        None],
    13201: [  #
        3435, None, None, None, None, None, None, None, None, None,  #
        3436, 3535, 3534, 3434, 3334, 3335, 3435, None, None, None,
        None],
    #

    #
    #

    15300: [  #
        4442, None, None, None, None, None, None, None, None, None,  #
        None],
    15301: [  #
        4443, None, None, None, None, None, None, None, None, None,  #
        None],
    15302: [  #
        4540, None, None, None, None, None, None, None, None, None,  #
        None],
    15303: [  #
        4541, None, None, None, None, None, None, None, None, None,  #
        None],
    15304: [  #
        4542, None, None, None, None, None, None, None, None, None,  #
        None],
    15305: [  #
        4543, None, None, None, None, None, None, None, None, None,  #
        None],
    #

    #
    #

    14600: [  #
        3119, None, None, None, None, None, None, None, None, None,  #
        None],
    14601: [  #
        2230, None, None, None, None, None, None, None, None, None,  #
        None],
    14500: [  #
        3228, 2723, 2514, 2319, 2115, 1918, 1713, None, None, None,  #
        None],
    14501: [  #
        2030, 1727, 2225, 1623, 2120, 1618, 1715, 1414, None, None,  #
        None]
    #
}

FIRST_POS_Q8_1 = {

    #
    5300: [
        #2735,
        None],
    5301: [
        #2535,
        None],
    5302: [
        #2635,
        None],
    5303: [
        #2734,
        None],
    5304: [
        #2737,
        None],
    5305: [
        #2837,
        None],
    #
    400: [
        #
        #
        #
        2028,
        None],
    1400: [
        3132,
        #3245,  #
        None],
    2400: [
        3245,  #
        None],
    3400: [
        3245,  #
        None],
    #
    100: [
        #
        2130, 2129, 2328, 2529, 2530, 2631,
        None],
    1100: [
        2437,
        #
        None],
    2100: [
        2846,3142,

        None],
    3100: [
        1953, 2053, 2152, 2253, 2352, 2453, 2553, 2653, 2651, 2750, 2748,3142,
        None],
    #
    200: [
        3837,
        None],
    1200: [

        #
        #
        3341, 3640,
        None],
    2200: [
        #
        #
        3939,

        #
        None],
    3200: [
        #
        #
        #
        #
        3747,

        None],

    #

    0: [
        #
        #
        3445, None, None, None, None, None, None, None, None, None,
        #3646, 3647, 3648, 3640, 3837, None, None, None, None, None,
        3446, 3746, 3647, 3648, 3640, 3838, 3937, 3938, None, None,
        None],
    1000: [
        3445, None, None, None, None, None, None, None, None, None,
        #3646, 3647, 3648, 3640, 3837, None, None, None, None, None,
        3747, 3746, 3647, 3648, 3640, 3838, 3937, 3938, None, None,
        None],
    2000: [
        3445, None, None, None, None, None, None, None, None, None,
        3747, 3746, 3647, 3648, 3640, 3838, 3937, 3938, None, None,
        #3646, 3647, 3648, 3640, 3837, None, None, None, None, None,
        None],
    3000: [
        3445, None, None, None, None, None, None, None, None, None,
        #3646, 3647, 3648, 3640, 3837, None, None, None, None, None,
        3446, 3746, 3647, 3648, 3640, 3838, 3937, 3938, None, None,
        None],
    #
    700: [
        5539, 6136, 6043, 5644, 5551, 4546, 4550, 5555, 5553, 4146,
        None],
    1700: [
        5539, 6136, 6043, 5644, 5551, 4546, 4550, 5555, 5553, 4146,
        None],
    2700: [
        5539, 6136, 6043, 5644, 5551, 4546, 4550, 5555, 5553, 4146,
        None],
    3700: [
        5539, 6136, 6043, 5644, 5551, 4546, 4550, 5555, 5553, 4146,
        None],
    701: [
        5539, 6136, 6043, 5644, 5551, 4546, 4550, 5555, 5553, 4146,
        None],
    1701: [
        3640, 3837, 3939, 3747, 3947, 3939,
        None],
    2701: [
        3640, 3837, 3939, 3747, 3947, 3939,
        None],
    3701: [
        3640, 3837, 3939, 3747, 3947, 3939,
        None],
    #
    4600: [
        4137,4522,6022,7438,
        None],
    4601: [
        #
        4146,4522,6022,7537,
        None],
    #
    4500: [
        4045, 3453,4458,5254,5249,
        None],
    4501: [
        4049,3453,4458,5254,5241,
        None],
    #
    #
    10000: [  #
        #
        #
        5938, 5639, 5042, 4641, 4540, 4344, 4246, 3946, 3846, None,
        None, None, None, None, None, None, None, None, None, None,
        #
        #
        None],
    10001: [  #
        5938, 5639, 5042, 4641, 4540, 4344, 4246, 3946, 3846, None,
        #
        #
        #
        None],
    10100: [  #
        #
        4641, None, None, None, None, None, None, None, None, None,
        None],
    10101: [  #
        #
        4641, None, None, None, None, None, None, None, None, None,
        None],
    10200: [  #
        #
        4246, None, None, None, None, None, None, None, None, None,
        4540, None, None, None, None, None, None, None, None, None,
        None],
    10201: [  #
        #
        4540, None, None, None, None, None, None, None, None, None,
        None],
    #

    #
    #
    11000: [  #
        #
        #
        #
        #
        4641, 4540, 4344, 4246, 3946, 3846, None, None, None, None,
        None],
    11001: [  #
        #
        #
        #
        #
        4641, 4540, 4344, 4246, 3946, 3846, None, None, None, None,
        None],
    11100: [  #
        #
        #
        #
        #
        6347, 5948, 5548, 5046, 4646, 4642, 4641, None, None, None,
        #
        #
        #
        None],
    11101: [  #
        6347, 5948, 5548, 5046, 4646, 4642, 4641, None, None, None,
        #
        #
        #
        None],
    11200: [  #
        3939, None, None, None, None, None, None, None, None, None,
        3837, None, None, None, None, None, None, None, None, None,
        None],
    11201: [  #
        #
        #
        4542, 3939, None, None, None, None, None, None, None, None,
        4540, None, None, None, None, None, None, None, None, None,
        #
        #
        #
        #
        None],
    #

    #
    #

    12000: [  #
        #
        #
        #
        #
        #
        5453, 4249, 4147, 3947, 3946, 3846, None, None, None, None,
        None],
    12001: [  #
        #
        #
        #
        #
        5453, 4249, 4147, 3947, 3946, 3846, None, None, None, None,
        None],
    12100: [  #
        #
        #
        #
        #
        5049, 4648, 4247, None, None, None, None, None, None, None,
        #
        None],
    12101: [  #
        #
        #
        #
        #
        5049, 4648, 4247, None, None, None, None, None, None, None,
        #
        None],
    12200: [  #
        #
        4247, 4147, 4048, 3947, None, None, None, None, None, None,
        #
        None],
    12201: [  #
        #
        4248, 4147, 4048, 3947, None, None, None, None, None, None,
        #
        None],
    #

    #
    #

    13000: [  #
        #
        #
        #
        #
        #
        #
        #
        5453, 4249, 4147, 3947, 3946, 3846, None, None, None, None,
        None],
    13001: [  #
        #
        #
        #
        #
        5453, 4249, 4147, 3947, 3946, 3846, None, None, None, None,
        None],
    13100: [  #
        #
        #
        #
        4549, 4247, None, None, None, None, None, None, None,
        None],
    13101: [  #
        #
        #
        #
        #
        #
        4549, 4247, None, None, None, None, None, None, None,
        None],
    13200: [  #
        4147, 4048, 3948, 3848, 3747, None, None, None, None, None,
        #
        #
        None],
    13201: [  #
        4147, 4048, 3948, 3848, 3747, None, None, None, None, None,  #
        #
        None],
    #

    #
    #

    15300: [  #
        None, None, None, None, None, None, None, None, None, None,  #
        None],
    15301: [  #
        None, None, None, None, None, None, None, None, None, None,  #
        None],
    15302: [  #
        None, None, None, None, None, None, None, None, None, None,  #
        None],
    15303: [  #
        None, None, None, None, None, None, None, None, None, None,  #
        None],
    15304: [  #
        None, None, None, None, None, None, None, None, None, None,  #
        None],
    15305: [  #
        None, None, None, None, None, None, None, None, None, None,  #
        None],
    #

    #
    #

    14600: [  #
        4042, 3918, 1921, 1038, 938, None, None, None, None, None,  #
        None],
    14601: [  #
        4050, 3918, 1921, 1038, 938, None, None, None, None, None,  #
        None],
    14500: [  #
        3445, 2847, 2053, 2759, None, None, None, None, None, None,  #
        None],
    14501: [  #
        3142, 2843, 3239, 2837, 2537, 2530, 3433, 2625, 3639, None,  #
        None]
    #
}

FIRST_POS_Q8_2 = {

    #
    5300: [  #
        #6539,  #
        None],
    5301: [  #
        #6540,
        None],
    5302: [  #
        #6542,
        None],
    5303: [  #
        #6639,
        None],
    5304: [  #
        #6640,
        None],
    5305: [  #
        #6642,
        None],
    #
    400: [
        #4431,
        5023,
        None],
    1400: [
        5344, 4349,
        #4541,4243,  4044, #4147,
        #3245,  #
        None],
    2400: [
        4349, #4546, 4044, #4147,  #
        None],
    3400: [
        4349, #4546, 4044, #4147,  #
        None],
    #
    100: [
        #
        6535,6136, 6037,5838, 5539, 5042,
        None],
    1100: [
        6150, 5648, 5548, 5347, 5046,
        #6150, 5648, 5548, 5347, 5049, 4948,
        #
        None],
    2100: [
        #5148, 5049, 4948,
        5148, 5049, 4848, 4748, 4648, 4548, 4448, 4348, 4249,
        #4947,
        None],
    3100: [
        #5551, 5450, 5148, 5049, 4948,
        5253, 4951, 4549, 4548, 4448, 4348, 4249,
        #5153, 5054, 4853, 4653,
        None],
    #
    200: [
        5339, 5041 , 4940, 4841, 4740 , 4640 , 4540 , 4341 ,3939,
        #4540, 4341, 3939,
        None],
    1200: [
        4540,
        None],
    2200: [
        5452, 4246,
        None],
    3200: [
        5353 , 5254 , 5053, 3947,
        None],

    #

    0: [
        #
        #
        #3945, 3846, None, None, None, None, None, None, None, None,
        6436, 6136, 6037, 5838, 5539, 5142, 4745, 4147, 4048, None,
        4541, 4243, 4045, 3945, 4048, None, None, None, None, None,
        3645, 3646, 3647, 3648, 3640, 3837, None, None, None, None,
        None],
    1000: [
        5243, 4745, 4147, 4048, None, None, None, None, None, None,
        #3945, 3846, None, None, None, None, None, None, None, None,
        4541, 4243, 4045, 3945, 4048, None, None, None, None, None,
        3645, 3646, 3647, 3648, 3640, 3837, None, None, None, None,

        None],
    2000: [
        3947, 4147, 4048, None, None, None, None, None, None, None,
        #3945, 3846, None, None, None, None, None, None, None, None,
        4045, 3945, 4048, None, None, None, None, None, None, None,
        3645, 3646, 3647, 3648, 3640, 3837, None, None, None, None,
        None],
    3000: [
        4147, 4048, None, None, None, None, None, None, None,
        #3945, 3846, None, None, None, None, None, None, None, None,
        4045, 3945, 4048, None, None, None, None, None, None, None,
        3645, 3646, 3647, 3648, 3640, 3837, None, None, None, None,
        None],
    #
    700: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    1700: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    2700: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    3700: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    701: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    1701: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    2701: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    3701: [
        2846, 2343, 2837, 2734, 4039,2653, 3847,
        None],
    #
    4600: [
        #4045,5746,
        4045, 4059,3064, 1054, 1039,
        None],
    4601: [
        #
        #4038, 5545, 5746,
        4038, 4059,3064, 1054, 939,
        None],
    #
    4500: [
        3745,3757, 3061, 2759, 2749,
        None],
    4501: [
        3747,3757, 3061, 2759, 2744,
        None],
    #
    #
    10000: [  #
        #
        3837, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,
        None],
    10001: [
        4540, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,
        None],
    11000: [  #
        4540, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,
        None],
    11001: [
        4540, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,
        None],
    12000: [  #
        4540, 5247, None, None, None, None, None, None, None, None,
        4545, None, None, None, None, None, None, None, None, None,
        #
        #

        None],
    12001: [
        4540, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,
        None],
    13000: [  #
        4540, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,

        None],
    13001: [
        4540, 5247, None, None, None, None, None, None, None, None,
        #
        3645, 3646, 3647, 3648, 3640, 3837, 3939, 4540, 5141, 5341,
        None],

    10100: [
        #
        1933, 2136, 2237, 2337, 2437,  #
        None],
    10101: [3031,
            #
            None],

    10200: [  #
        3939, None, None, None, None, None, None, None, None, None,
        3837, 3939, None, None, None, None, None, None, None, None,
        None],
    10201: [  #
        3837,
        None],
    #

    #
    #

    11100: [  #
        #
        2343, 3244, None, None, None, None, None, None, None, None,
        3746, None, None, None, None, None, None, None, None, None,
        3946, None, None, None, None, None, None, None, None, None,
        4145,
        None],
    11101: [  #
        2343, 2443, 3244, None, None, None, None, None, None, None,
        3746, None, None, None, None, None, None, None, None, None,
        3946, None, None, None, None, None, None, None, None, None,
        4145,
        None],

    12100: [  #
        2843, 3244, None, None, None, None, None, None, None, None,
        3746, None, None, None, None, None, None, None, None, None,
        3946, None, None, None, None, None, None, None, None, None,
        4145,
        None],
    12101: [  #
        2844, 3244, None, None, None, None, None, None, None, None,
        3746, None, None, None, None, None, None, None, None, None,
        3946, None, None, None, None, None, None, None, None, None,
        4145,
        None],

    13100: [  #
        2849, 2848, 2847, 2946, 3046, 3146, 3246, 3344, None, None,
        3746, None, None, None, None, None, None, None, None, None,
        3946, None, None, None, None, None, None, None, None, None,
        4145,
        None],
    13101: [  #
        2849, 2848, 2847, 2946, 3046, 3146, 3246, 3345, 3344, None,
        3746, None, None, None, None, None, None, None, None, None,
        3946, None, None, None, None, None, None, None, None, None,
        4145,
        None],

    11200: [  #
        3640, 3939, None, None, None, None, None, None, None, None,
        3837, 3939, None, None, None, None, None, None, None, None,
        None],
    11201: [  #
        3747,
        None],
    #

    #
    #

    12200: [  #
        3946, None, None, None, None, None, None, None, None, None,
        3939, None, None, None, None, None, None, None, None, None,
        None],
    12201: [  #
        3747, 3947, 4048, None, None, None, None, None, None, None,
        4247, 4246, None, None, None, None, None, None, None, None,
        None],
    #

    #
    #

    13200: [  #
        3948, None, None, None, None, None, None, None, None, None,
        4247, 4246,
        None],
    13201: [  #
        3947, 4048, None, None, None, None, None, None, None, None,
        4247, 4246,
        None],
    #

    #
    #

    #
    #

    15300: [
        None,
        None],
    15301: [
        None,
        None],
    15302: [
        None,
        None],
    15303: [
        None,
        None],
    15304: [
        None,
        None],
    15305: [
        None,
        None],
    #

    #
    #

    14600: [  #
        4453, 5049, 4245, None, None, None, None, None, None, None,
        3846, 3522, 7224, 7538, None],
    14601: [  #
        4245, None, None, None, None, None, None, None, None, None,
        3846, 3522, 7224, 7538, None],
    14500: [  #
        4045, 3453, 4458, 4856, 4947, 5233, 5732, 5548, None],
    14501: [  #
        4049, 3453, 4458, 5254, 5241, 4737, 4756, 4556, 4756]
    #
}
def my_print(*param):
    #
    pass
COMPOSITE = 'composite'
DECORATOR = 'decorator'
ACTION = 'action'
CONDITION = 'condition'
RED = 0
BLUE = 1


#
class situation:
    def __init__(self, observation, color, map, scenario_info):
        self.stack_pos_list = []  #
        self.artillery_pos_list = []  #
        self.observation = observation
        self.color = color
        self.s32_back_flg = False
        self.enemy_color = (self.color + 1) % 2
        self.map = map
        self.scenario_info = scenario_info
        self.our_opt = []
        self.enemy_tank_opt = []
        self.enemy_soilder_opt = []

        self.enemy_car_opt = []
        self.enemy_autocar_opt = []
        self.enemy_missile_opt = []
        self.enemy_operators = []
        self.wantoccupy_cities_list = []
        self.missile_patrol_find_enemy = True  #
        self.enenmy_is_coming = False  #
        self.myLandTool = land_tool(self.map, self.scenario_info)
        self.myFireTool = FireTool(self.map)
        self.mychecktool = check_tool(self.observation, self.map)
        #
        self.enemy_history = {}
        self.mainCityCarWanted = False
        self.secondCityCarWanted = False
        self.enemy_tank_dead_num = 0
        self.enemy_car_dead_num = 0
        self.enemy_soilder_dead_num = 0
        self.enemy_autocar_dead_num = 0
        self.our_tank_dead_num = 0
        self.our_car_dead_num = 0
        self.our_soilder_dead_num = 0
        self.our_autocar_dead_num = 0
        self.my_artillery_pos_list = []
        self.booming_pos = []
        self.distance_enemy_maincity = 999  #
        self.distance_enemy_secondcity = 999  #
        #
        self.fire_zone = {}
        #
        self.hide_enemy = {}
        self.shoot_list = []
        self.guideshoot_list = []
        self.shoot_list_changed = False
        #
        self.num_enemy_helicopter_missile_remain = [4, 4]
        if self.color == RED:
            self.set_red_shootlist()
            self.num_enemy_helicopter_missile_remain = [4, 4]
        else:
            self.set_blue_shootlist()
            self.num_enemy_helicopter_missile_remain = [6, 6]
        if my_ai.scenario_type == UNIT:  #
            self.all_attack_time = 0  #
            self.all_occupy_time = 0  #
        else:  #
            self.all_attack_time = 1800  #
            self.all_occupy_time = 2300  #
        self.attack_car_time = 600
        #
        self.situation_hash = {}
        self.fight_step = FIRST_MOVING_STEP
        self.occupy_list = [SOILDER, TANK, AUTO_CAR, CAR, HELICOPTER, AUTO_PLANE, ARTILLERY, MISSILE]

        self.clean_pos_list = []
        self.command_num = None
        self.opt_waiting_time = {}
        self.opt_is_waiting = {}
        self.final_occupy = False
        for each_enemy in self.scenario_info['-1']['operators']:
            if each_enemy['color'] != self.color:
                self.opt_waiting_time[each_enemy['obj_id']] = 0
                self.opt_is_waiting[each_enemy['obj_id']] = False
                self.enemy_history[each_enemy['obj_id']] = (each_enemy, 0, False , False)
        for each_enemy in self.scenario_info['-1']['passengers']:
            if each_enemy['color'] != self.color:
                self.opt_waiting_time[each_enemy['obj_id']] = 0
                self.opt_is_waiting[each_enemy['obj_id']] = False
                self.enemy_history[each_enemy['obj_id']] = (each_enemy, 0, True , False)
        if my_ai.scenario == 2010431153:
            self.is_vain_attack_flg = False
        else:
            self.is_vain_attack_flg = True
        self.attack_add_num = 1
        self.enemy_remain = 1000
        self.my_remain = 1000
        self.want_to_move_pos = []
        self.get_guide = []
        self.old_time = -1

    def update(self, observation):
        self.observation = observation
        self.enemy_operators = []
        self.enemy_tank_opt = []
        self.enemy_soilder_opt = []
        self.enemy_car_opt = []
        self.enemy_autocar_opt = []
        self.enemy_missile_opt = []
        self.enenmy_is_coming = False
        self.enemy_tank_dead_num = 0
        self.enemy_car_dead_num = 0
        self.enemy_soilder_dead_num = 0
        self.enemy_autocar_dead_num = 0
        self.our_tank_dead_num = 0
        self.our_car_dead_num = 0
        self.our_soilder_dead_num = 0
        self.our_autocar_dead_num = 0
        self.planning_pos = []
        self.distance_enemy_maincity = 999  #
        self.distance_enemy_secondcity = 999  #
        self.cur_step = self.observation['time']['cur_step']
        land_tool._stack_pos_list = []

        self.my_artillery_pos_list = []
        #
        for key in self.enemy_history.keys():
            opt = self.enemy_history[key][0]
            last_time = self.enemy_history[key][1] - (self.observation['time']['cur_step'] - self.old_time)
            is_dead = self.enemy_history[key][2]
            is_seen = self.enemy_history[key][3]
            self.enemy_history[key] = (opt, last_time, is_dead, is_seen)
        self.old_time = self.observation['time']['cur_step']
        #
        self.update_bodycount()
        #
        for opt in self.our_opt[::-1]:
            #
            is_distroied = True
            for operator in self.observation['operators']:  #
                if opt.operator['obj_id'] == operator['obj_id']:
                    is_distroied = False
                    break
            for operator in self.observation['passengers']:  #
                if opt.operator['obj_id'] == operator['obj_id']:
                    is_distroied = False
                    break
            for operator in self.observation['operators']:  #
                if opt.operator['obj_id'] == operator['obj_id']:
                    if operator['lose_control']:
                        is_distroied = True
                    break
            if is_distroied:
                if opt.operator['sub_type'] == TANK:
                    self.our_tank_dead_num += 1
                elif opt.operator['sub_type'] == CAR:
                    self.our_car_dead_num += 1
                elif opt.operator['sub_type'] == AUTO_CAR:
                    self.our_autocar_dead_num += 1
                elif opt.operator['sub_type'] == SOILDER:
                    self.our_soilder_dead_num += 1
                    if opt.cityWanted and opt.cityWanted['coord'] in self.wantoccupy_cities_list:
                        self.wantoccupy_cities_list.remove(opt.cityWanted['coord'])
                elif opt.operator['sub_type'] == MISSILE:
                    pass  #
                else:
                    opt = None
                if opt is not None:
                    self.our_opt.remove(opt)
                    print(opt.operator['sub_type'], 'is_distroied:')
        #
        for opt in self.observation['operators']:
            if opt['color'] == self.color:
                this_opt = None
                for my_opt in self.our_opt:
                    if opt['obj_id'] == my_opt.operator['obj_id']:
                        this_opt = my_opt
                if this_opt:
                    this_opt.update(opt, observation)
                else:
                    if opt['sub_type'] == TANK:
                        opt_tmp = ai_tank_operator(opt,
                                                   self.color,
                                                   self.map, self.observation, self.scenario_info)
                    elif opt['sub_type'] == CAR:
                        opt_tmp = ai_car_operator(opt,
                                                  self.color,
                                                  self.map, self.observation, self.scenario_info)
                    elif opt['sub_type'] == SOILDER:
                        opt_tmp = ai_soilder_operator(opt,
                                                      self.color,
                                                      self.map, self.observation, self.scenario_info)
                    elif opt['sub_type'] == AUTO_CAR:
                        opt_tmp = ai_autocar_operator(opt,
                                                      self.color,
                                                      self.map, self.observation, self.scenario_info)
                    elif opt['sub_type'] == MISSILE:
                        opt_tmp = ai_missile_operator(opt,
                                                      self.color,
                                                      self.map, self.observation, self.scenario_info)
                        for opt_car in self.our_opt:  #
                            if opt_tmp.operator['launcher'] == opt_car.operator['obj_id']:
                                opt_tmp.cityWanted = opt_car.city_first_step
                                if opt_car.send_missile:
                                    opt_tmp.first_missile = False
                                opt_car.send_missile = True
                                break
                    elif opt['sub_type'] == HELICOPTER:
                        opt_tmp = ai_helicopter_operator(opt,
                                                         self.color,
                                                         self.map, self.observation, self.scenario_info)
                    elif opt['sub_type'] == AUTO_PLANE:
                        opt_tmp = ai_autoplane_operator(opt,
                                                        self.color,
                                                        self.map, self.observation, self.scenario_info)
                    elif opt['sub_type'] == ARTILLERY:
                        opt_tmp = ai_aritllery_operator(opt,
                                                        self.color,
                                                        self.map, self.observation, self.scenario_info)
                    else:
                        opt_tmp = None
                    if opt_tmp is not None:
                        temp_list = []
                        for each_subtype in self.occupy_list:
                            temp_list.append(each_subtype)
                            if opt_tmp.operator['sub_type'] == each_subtype:
                                idx = len(self.our_opt) - 1
                                for i in range(len(self.our_opt)):
                                    each_opt = self.our_opt[i]
                                    if each_opt.operator['sub_type'] not in temp_list:
                                        idx = i
                                        break
                                self.our_opt.insert(idx, opt_tmp)
            else:
                if opt['sub_type'] == TANK:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                    self.enemy_tank_opt.append(opt)
                if opt['sub_type'] == CAR:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                    self.enemy_car_opt.append(opt)
                if opt['sub_type'] == SOILDER:

                    #
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                    self.enemy_soilder_opt.append(opt)
                    #
                    #
                    list = self.get_artillery_nearcity()
                    if my_ai.scenario == 2030331196:
                        if self.color == RED:
                            list = [3745, 3847, 3947, 4047, 4146, 4246]
                        else:
                            if self.cur_step < 1500:
                                list = [3339, 3340, 3341, 3342, 3439, 3440, 3441]
                    #
                    if len(list) > 0:
                        self.my_artillery_pos_list += list
                    else:
                        self.my_artillery_pos_list.append(opt['cur_hex'])
                if opt['sub_type'] == AUTO_CAR:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                    self.enemy_autocar_opt.append(opt)
                if opt['sub_type'] == MISSILE:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                    self.enemy_missile_opt.append(opt)
                if opt['sub_type'] == HELICOPTER:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                if opt['sub_type'] == AUTO_PLANE:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                if opt['sub_type'] == ARTILLERY:
                    self.enenmy_is_coming = True
                    self.enemy_operators.append(opt)
                #
                opt_id = opt['obj_id']
                #
                tmp_opt = copy.deepcopy(opt)
                if self.enemy_history.get(opt_id):  #
                    tmp_opt['launcher'] = self.enemy_history[opt_id][0]['launcher']
                    if opt['cur_pos'] == self.enemy_history[opt_id][0]['cur_pos']:
                        self.opt_waiting_time[opt_id] += 1
                    else:
                        self.opt_waiting_time[opt_id] = 0
                    if self.opt_waiting_time[opt_id] > 3:
                        self.opt_is_waiting[opt_id] = True
                    else:
                        self.opt_is_waiting[opt_id] = False
                else:  #
                    self.opt_waiting_time[opt_id] = 0
                    self.opt_is_waiting[opt_id] = False

                if tmp_opt['sub_type'] == MISSILE:
                    self.enemy_history[opt_id] = (tmp_opt, 0, True, False)
                else:
                    self.enemy_history[opt_id] = (tmp_opt, 0, False, False)
        #是否有敌方算子不在其历史位置：
        self.set_enemy_history_3()
        #
        if not self.shoot_list_changed and observation['time']['cur_step'] > self.attack_car_time:
            if self.color == RED:
                self.set_red_shootlist_after()
            else:
                self.set_blue_shootlist_after()
        #
        self.set_remain_mark()
        #
        self.set_fight_step_func()
        #
        self.set_stack_pos_list()
        #
        self.update_booming_pos(observation)
        #
        self.set_artillery_pos_list()
        #
        self.set_red_occupy_stratage()
        #
        self.set_final_occupy()
        #
        if not self.is_vain_attack_flg:
            for each in self.our_opt:
                if each.operator['sub_type'] == TANK:
                    self.is_vain_attack_flg = self.is_vain_attack(each.operator)
                    if self.is_vain_attack_flg:
                        break

    #
    def get_cur_opt_by_id(self, opt_id):
        #
        for opt in self.our_opt:
            opt = opt.operator
            if opt['obj_id'] == opt_id:
                return opt

        for enemy_opt in self.enemy_operators:
            if enemy_opt['obj_id'] == opt_id:
                return enemy_opt
        return None
    def set_enemy_history_3(self):
        for key in self.enemy_history.keys():
            each_enemy = self.enemy_history[key]
            #没有挂：
            if not each_enemy[2]:
                if each_enemy[1] < 0:#现在看不见
                    enemy_opt = each_enemy[0]
                    dis = self.get_beseen_distance(enemy_opt)
                    for each_my_opt in self.our_opt:
                        my_opt = each_my_opt.operator
                        type = self.get_cansee_type(my_opt , enemy_opt)
                        if self.map.can_see(my_opt['cur_hex'], enemy_opt['cur_hex'], type):
                            if my_opt['sub_type'] == MISSILE or my_opt['sub_type'] == AUTO_PLANE:
                                distance = 1
                            else:
                                distance = dis
                            if self.map.get_distance( my_opt['cur_hex'], enemy_opt['cur_hex']) <= distance:
                                self.enemy_history[key] = (each_enemy[0] ,each_enemy[1] ,each_enemy[2] , True)
                                break

    def get_cansee_type(self , source , direct):
        if source['type'] == 3:
            if direct['type'] == 3:
                return 1
            else:
                return 2
        else:
            if direct['type'] == 3:
                return 3
            else:
                return 0
    def get_beseen_distance(self , direct_opt):
        dis = 10

        if direct_opt['type'] == 2:
            dis = 25
        elif direct_opt['type'] == 1:
            dis = 10
        elif direct_opt['sub_type'] == HELICOPTER:
            dis = 25
        else:
            dis =2
        if self.myLandTool.is_town( direct_opt['cur_hex']) or \
                self.myLandTool.is_jungle(direct_opt['cur_hex']):
            dis = dis // 2
        dis =  dis // 2
        if dis < 1:
            dis = 1
        return dis

    #
    def get_enemy_history_by_id(self, opt_id):
        for key in self.enemy_history.keys():
            if key == opt_id:
                return self.enemy_history[key]

        return None

    def is_solier_in_car(self):
        combat_score_all = 0
        for judge_info in my_ai.my_judge_info:
            damage = judge_info['damage']
            enemy_id = judge_info['target_obj_id']
            #
            enemy_in_history = self.get_enemy_history_by_id(enemy_id)

            if self.color == BLUE:
                pass  #
            if enemy_in_history is None:
                continue
            enemy_opt = enemy_in_history[0]
            #

            if damage == 0 and enemy_opt['sub_type'] == SOILDER and enemy_opt['keep'] == 1:
                damage = 1

            if damage < 0:
                damage = 0
            if enemy_opt['blood'] < damage:
                damage = enemy_opt['blood']
            combat_score_all += self.combat_score(damage, enemy_opt['sub_type'])
            print("damage ", damage)
        sub_res = 0
        if self.color == RED:
            sub_res = self.enemy_remain - self.observation['scores']['blue_remain'] - combat_score_all
        else:
            sub_res = self.enemy_remain - self.observation['scores']['red_remain'] - combat_score_all
        #

        #
        #
        if sub_res >= 4:
            return True
        else:
            return False


    #
    def update_bodycount(self):
        #
        flag_solier_in_car = self.is_solier_in_car()

        #
        #

        for judge_info in my_ai.my_judge_info:
            #
            enemy_id = judge_info['target_obj_id']
            damage = judge_info['damage']
            #
            enemy_in_history = self.get_enemy_history_by_id(enemy_id)

            if self.color == BLUE:
                pass  #
            if enemy_in_history is None:
                continue
            enemy_opt = enemy_in_history[0]
            #

            if damage == 0 and enemy_opt['sub_type'] == SOILDER and enemy_opt['keep'] == 1:
                damage = 1

            if damage < 0:
                damage = 0

            #

            enemy_opt['blood'] -= damage
            #
            enemy_time = self.enemy_history[enemy_id][1]
            enemy_isseen = self.enemy_history[enemy_id][3]
            #
            if enemy_opt['blood'] <= 0:
                enemy_opt['blood'] = 0
                self.enemy_history[enemy_id] = (enemy_opt, enemy_time, True, enemy_isseen)
                if enemy_opt['sub_type'] == TANK:
                    self.enemy_tank_dead_num = self.enemy_tank_dead_num + 1
                if enemy_opt['sub_type'] == CAR:
                    self.enemy_car_dead_num = self.enemy_car_dead_num + 1
                    #
                    for id in self.enemy_history.keys():
                        opt = self.enemy_history[id][0]
                        if opt is not None and opt['launcher'] == enemy_opt['obj_id']:
                            #
                            if opt['sub_type'] == AUTO_CAR or flag_solier_in_car:
                                self.enemy_history[id] = (self.enemy_history[id][0], self.enemy_history[id][1], True,self.enemy_history[id][3])
                                print(self.observation['time']['cur_step'], "dead")
                            #
                            #
                if enemy_opt['sub_type'] == SOILDER:
                    self.enemy_soilder_dead_num = self.enemy_soilder_dead_num + 1
                if enemy_opt['sub_type'] == AUTO_CAR:
                    self.enemy_autocar_dead_num = self.enemy_autocar_dead_num + 1
                if enemy_opt['sub_type'] == HELICOPTER:
                    self.num_enemy_helicopter_missile_remain[enemy_opt['obj_id'] % 2] = 0

                    #

                #
            #
            else:
                self.enemy_history[enemy_id] = (enemy_opt, enemy_time, False, enemy_isseen)

            #
        my_ai.my_judge_info = []

    def seek_enemy(self, judge_info):
        att_obj_id = judge_info['att_obj_id']
        target_obj_id = judge_info['target_obj_id']
        is_enemy, enemy_opt = self.is_enemy(att_obj_id)
        #
        if self.hide_enemy.get(att_obj_id) is None:
            #
            if is_enemy is False:
                return
            #
            enemy_history = self.get_enemy_history_by_id(att_obj_id)
            if enemy_history is not None:
                enemy_opt = enemy_history[0]
                last_time = enemy_history[1]
                is_dead = enemy_history[2]

            #
            if enemy_history is not None and last_time == 0:
                return

            #
            self.hide_enemy[att_obj_id] = []

        #
        atk_distance = judge_info['distance']
        atk_ele_diff = judge_info['ele_diff']
        target_opt = self.get_cur_opt_by_id(target_obj_id)
        target_xy = target_opt['cur_hex']

        doubt_list = self.myLandTool.get_target_list(target_xy, atk_distance, atk_ele_diff)
        doubted_list = self.hide_enemy[att_obj_id]

        #
        doubt_set = set(doubt_list)
        doubted_set = set(doubted_list)

        #
        self.hide_enemy[att_obj_id] = doubt_list
        inter_set = set(doubt_set & doubted_set)
        #

        if len(list(inter_set)) == 0:
            self.hide_enemy[att_obj_id] = doubt_list
        else:
            self.hide_enemy[att_obj_id] = list(inter_set)

    def is_enemy(self, obj_id):

        tmp_scenario_info = self.scenario_info['-1']

        for opt in tmp_scenario_info['operators']:
            if opt['obj_id'] == obj_id and self.color != opt['color']:
                return True, opt['obj_id']

        for opt in tmp_scenario_info['passengers']:
            if opt['obj_id'] == obj_id and self.color != opt['color']:
                return True, opt['obj_id']

        return False, None

    def set_remain_mark(self):
        if self.color == RED:
            self.my_remain = self.observation['scores']['red_remain']
            self.enemy_remain = self.observation['scores']['blue_remain']
        else:
            self.enemy_remain = self.observation['scores']['red_remain']
            self.my_remain = self.observation['scores']['blue_remain']

    #
    def update_firezone(self):
        self.fire_zone = {}
        #
        for history_tmp in self.enemy_history.values():
            enemy_opt = history_tmp[0]
            last_time = history_tmp[1]
            is_dead = history_tmp[2]

            if is_dead:
                continue

            enemy_type = enemy_opt['sub_type']
            enemy_stoptime = enemy_opt['stop']
            enemy_xy = enemy_opt['cur_hex']
            can_fire = True
            shoot_range = 20

            #
            #
            #
            #

            if enemy_type == SOILDER:
                shoot_range = 10

            if can_fire is False:
                continue
            select_xy_list = self.myLandTool.get_big_six(enemy_xy, shoot_range)
            for tmp_xy in select_xy_list:
                if not self.map.can_see(tmp_xy, enemy_xy, 0):
                    continue
                if self.fire_zone.get(tmp_xy) is not None:
                    if enemy_type == SOILDER:
                        self.fire_zone[tmp_xy] += 999
                    else:
                        self.fire_zone[tmp_xy] += 1
                else:
                    self.fire_zone[tmp_xy] = 999

    def get_fire_zone_list(self):
        res_list = []
        for xy in self.fire_zone.keys():
            res_list.append(xy)
        return res_list

    #
    def get_current_enmey_situation_hash(self):
        hash_str = ""
        for history_tmp in self.enemy_history.values():
            enemy_opt = history_tmp[0]
            last_time = history_tmp[1]
            is_dead = history_tmp[2]

            if is_dead:
                continue
            enemy_xy = enemy_opt['cur_hex']
            hash_str += str(enemy_xy)
        hash_res = hash(hash_str)
        return hash_res

    #
    def is_same_situation(self, old_step):
        if old_step > self.cur_step or old_step <= 0:
            return False
        hash_res = self.get_current_enmey_situation_hash()
        if self.situation_hash.get(hash_res) is None:
            return None
        step_list = self.situation_hash[hash_res]
        if old_step in step_list and len(step_list) > 0:
            return True
        return False

    def get_alive_enemy_car(self):
        res_opts_list = []
        for history_tmp in self.enemy_history.values():
            enemy_opt = history_tmp[0]
            last_time = history_tmp[1]
            is_dead = history_tmp[2]
            if is_dead: continue

            if enemy_opt['sub_type'] == CAR:
                res_opts_list.append(enemy_opt)

        return res_opts_list

    #
    def set_fight_step_func(self):

        if self.observation['time']['cur_step'] < self.all_attack_time:
            self.fight_step = ALL_ATTACKI_STEP
        if self.observation['time']['cur_step'] > self.all_attack_time and \
                self.observation['time']['cur_step'] < self.all_occupy_time:
            self.fight_step = ALL_ASSISTOCCUPY_STEP
        if self.observation['time']['cur_step'] > self.all_occupy_time:
            self.fight_step = ALL_OCCUPY_STEP

    def set_red_shootlist(self):
        self.shoot_list = []
        self.guideshoot_list = []
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        #
        self.shoot_list.append([1, 0, 2, 4, 5, 6, 3])  #
        self.shoot_list.append([1, 0, 4, 3])  #
        self.shoot_list.append([1, 0, 5, 6, 2])  #
        self.shoot_list.append([2, 1, 0, 4, 5, 6, 3])  #
        #
        self.guideshoot_list = [1, 0, 4, 3]

        self.attack_add_num = 1

    def set_blue_shootlist(self):
        self.shoot_list = []
        self.guideshoot_list = []
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 3])  #
        self.shoot_list.append([1, 0, 5, 6, 2])  #
        self.shoot_list.append([1, 2, 4, 0, 5, 6, 3])  #
        #
        self.guideshoot_list = [1, 0, 4, 3]

        self.attack_add_num = 1

    def set_red_shootlist_after(self):
        self.shoot_list_changed = True
        self.shoot_list = []
        self.guideshoot_list = []
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 0, 4, 5, 6, 2, 3])  #
        #
        self.shoot_list.append([2, 1, 0, 4, 5, 6, 3])  #
        self.shoot_list.append([1, 0, 4, 3])  #
        self.shoot_list.append([1, 0, 5, 6, 2])  #
        self.shoot_list.append([2, 1, 0, 4, 5, 6, 3])  #
        #
        self.guideshoot_list = [1, 0, 4, 3]

        self.attack_add_num = 1

    def set_blue_shootlist_after(self):
        self.shoot_list = []
        self.guideshoot_list = []
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        self.shoot_list.append([1, 4, 0, 5, 6, 2, 3])  #
        #
        self.shoot_list.append([1, 4, 0, 2, 5, 6, 3])  #
        self.shoot_list.append([1, 0, 4, 3])  #
        self.shoot_list.append([1, 0, 5, 6, 2])  #
        self.shoot_list.append([2, 1, 0, 4, 5, 6, 3])  #
        #
        self.guideshoot_list = [1, 0, 4, 3]

        self.attack_add_num = 1

    #
    def set_stack_pos_list(self):
        self.stack_pos_list = []
        self.want_to_move_pos = []
        for each_opt in self.our_opt:
            if each_opt.operator['sub_type'] not in FLY_OPT:
                self.stack_pos_list.append(each_opt.operator['cur_hex'])
                if each_opt.move2hex:
                    self.stack_pos_list.append(each_opt.move2hex)
                    if each_opt.operator['cur_hex'] != each_opt.move2hex:
                        self.want_to_move_pos.append(each_opt.move2hex)

    def update_booming_pos(self, observation):
        jm_list = observation['jm_points']
        self.booming_pos = self.planning_pos
        for jm_dict in jm_list:
            if jm_dict['status'] == 1:
                self.booming_pos.append(jm_dict['pos'])
        self.planning_pos = []

    #
    def set_artillery_pos_list(self):
        self.artillery_pos_list = self.booming_pos

    def get_artillery_nearcity(self):
        if my_ai.scenario == 2030331196 and self.color == BLUE:
            fire_zone_set_1 = set(self.myLandTool.get_big_six(3939, 1))
            fire_zone_set_2 = set(self.myLandTool.get_big_six(3640, 1))
            fire_zone_set_3 = set(self.myLandTool.get_big_six(3747, 1))
        else:
            fire_zone_set_1 = set(self.myLandTool.get_big_six(3829, 1))
            fire_zone_set_2 = set(self.myLandTool.get_big_six(3630, 1))
            fire_zone_set_3 = set(self.myLandTool.get_big_six(3435, 1))
        for enemy in self.enemy_operators:
            xy = enemy['cur_hex']
            if enemy['sub_type'] != SOILDER:
                continue
            enemy_set = set(self.myLandTool.get_big_six(xy, 1))

            list1 = list(enemy_set & fire_zone_set_1)
            list2 = list(enemy_set & fire_zone_set_2)
            list3 = list(enemy_set & fire_zone_set_3)
            if len(list1) > 0:
                fire_zone_set = fire_zone_set_1
            elif len(list2) > 0:
                fire_zone_set = fire_zone_set_2
            elif len(list3) > 0:
                fire_zone_set = fire_zone_set_3
            else:
                continue
            import random as rd

            set_xy = set([xy])
            fire_zone_set = fire_zone_set - set_xy
            remove_idx = rd.randint(0, len(fire_zone_set))
            list1 = list(fire_zone_set)

            res_list = []
            for i in range(len(list1)):
                if i == remove_idx:
                    res_list.append(list1[i])
            res_list.append(xy)
            return res_list
        return []

    #
    def set_red_occupy_stratage(self):
        if self.observation['time']['cur_step'] >= 334 and self.command_num == None:
            self.command_num = self.get_red_occupy_stratage()

    def get_red_occupy_stratage(self):
        #
        #
        OCCUPY_MAIN = 0
        OCCUPY_SECOND = 1
        OCCUPY_4140 = 2
        red_occupy_stratage = OCCUPY_MAIN  #
        main_area = [4234, 4235,
                     4333, 4334, 4335,
                     4434, 4435, 4436, 4437]
        secondary_area = [3929, 3930,
                          4029, 4030, 4031,
                          4129, 4130]
        powerInMainarea = 0
        powerInSecondaryarea = 0

        soilderNumInMainarea = 0
        tankNumInMainarea = 0
        carNuminMainarea = 0
        soilderNuminSecondaryarea = 0
        tankNuminSecondaryarea = 0
        carNuminSecondaryarea = 0

        for enemy_opt_history in self.enemy_history.values():
            enemy_opt = enemy_opt_history[0]
            see_time = enemy_opt_history[1]
            is_dead = enemy_opt_history[2]
            if is_dead:
                continue
            if enemy_opt['cur_hex'] in main_area:
                if enemy_opt['sub_type'] == TANK:
                    tankNumInMainarea += 1
                    powerInMainarea += enemy_opt['blood'] * enemy_opt['value']
                if enemy_opt['sub_type'] == CAR:
                    carNuminMainarea += 1
                    powerInMainarea += enemy_opt['blood'] * enemy_opt['value']
                if enemy_opt['sub_type'] == SOILDER:
                    soilderNumInMainarea += 1
            elif enemy_opt['cur_hex'] in secondary_area:
                if enemy_opt['sub_type'] == TANK:
                    tankNuminSecondaryarea += 1
                    powerInSecondaryarea += enemy_opt['blood'] * enemy_opt['value']
                if enemy_opt['sub_type'] == CAR:
                    carNuminSecondaryarea += 1
                    powerInSecondaryarea += enemy_opt['blood'] * enemy_opt['value']
                if enemy_opt['sub_type'] == SOILDER:
                    soilderNuminSecondaryarea += 1

        if soilderNumInMainarea < 2 and self.observation['scores']['red_remain'] - powerInMainarea >= 40:
            red_occupy_stratage = OCCUPY_MAIN
        elif soilderNuminSecondaryarea < 2 and self.observation['scores']['red_remain'] - powerInSecondaryarea >= 60:
            red_occupy_stratage = OCCUPY_SECOND
        else:
            red_occupy_stratage = OCCUPY_4140
        return red_occupy_stratage

    def set_final_occupy(self):
        enemy_remain = 0
        my_remain = 0
        if self.color == RED:
            enemy_remain = self.observation['scores']['blue_remain']
            my_remain = self.observation['scores']['red_remain']
        else:
            enemy_remain = self.observation['scores']['red_remain']
            my_remain = self.observation['scores']['blue_remain']
        if self.observation['time']['cur_step'] > 1000 and \
                enemy_remain < 25 and my_remain > 40:
            soilder = 0
            car = 0
            for each_enemy in self.enemy_history.values():
                opt = each_enemy[0]
                is_dead = each_enemy[2]
                if not is_dead:
                    if opt['sub_type'] == SOILDER:
                        soilder += 1
                    else:
                        car += 1
            if soilder == 0 and car < 2:
                self.final_occupy = True

    def is_vain_attack(self, opt):
        if self.observation['judge_info'] != []:
            for judge_info in self.observation['judge_info']:
                if judge_info['target_obj_id'] == opt['obj_id']:
                    enemy = self.enemy_history[judge_info['att_obj_id']][0]
                    if enemy:
                        if enemy['sub_type'] == MISSILE:
                            continue
                        if enemy['sub_type'] == CAR and self.color == 1:
                            if judge_info['att_obj_id'] not in opt['see_enemy_bop_ids']:
                                if 200 not in opt['see_enemy_bop_ids'] and 400 not in opt['see_enemy_bop_ids']:
                                    return True
                        else:
                            if judge_info['att_obj_id'] not in opt['see_enemy_bop_ids']:
                                return True
        return False

    def is_air_defense_safe(self, observation):
        num_destroy_enemy_tank = 0
        num_destroy_enemy_car = 0
        num_destroy_enemy_soilder = 0
        num_destroy_enemy_helicopter = 0
        num_destroy_enemy_autocar = 0
        num_destroy_enemy_autoplane = 0
        num_destroy_enemy_artillery = 0

        pos_helicopter_enemy_0 = -1
        pos_helicopter_enemy_1 = -1
        pos_soilder_enemy_0 = -1
        pos_soilder_enemy_1 = -1
        #
        #
        #
        #
        #
        #

        for history_tmp in self.enemy_history.values():
            enemy_opt = history_tmp[0]
            last_time = history_tmp[1]
            is_dead = history_tmp[2]
            if is_dead:
                if enemy_opt['sub_type'] == TANK:
                    num_destroy_enemy_tank += 1
                if enemy_opt['sub_type'] == CAR:
                    num_destroy_enemy_car += 1
                if enemy_opt['sub_type'] == SOILDER:
                    num_destroy_enemy_soilder += 1
                if enemy_opt['sub_type'] == HELICOPTER:
                    num_destroy_enemy_helicopter += 1
                    self.num_enemy_helicopter_missile_remain[enemy_opt['obj_id'] % 2] = 0
                if enemy_opt['sub_type'] == AUTO_CAR:
                    num_destroy_enemy_autocar += 1
                if enemy_opt['sub_type'] == AUTO_PLANE:
                    num_destroy_enemy_autoplane += 1
                if enemy_opt['sub_type'] == ARTILLERY:
                    num_destroy_enemy_artillery += 1
        if num_destroy_enemy_helicopter == 2:
            return True
        if self.num_enemy_helicopter_missile_remain[0] + \
                self.num_enemy_helicopter_missile_remain[1] < 3:
            return True
        return False

class my_ai(BaseAgent):
    def __init__(self):
        my_ai.scenario = None
        my_ai.color = None
        self.priority = None
        self.observation = None
        self.map = None
        self.scenario_info = None
        self.ret_msg = []
        self.our_tank_opt = []
        self.our_soilder_opt = []
        self.our_car_opt = []
        self.our_autocar_opt = []
        self.our_missile_opt = []
        self.enemy_tank_opt = []
        self.enemy_soilder_opt = []
        self.enemy_car_opt = []
        self.enemy_autocar_opt = []
        self.enemy_missile_opt = []
        self.enemy_operators = []
        self.missile_patrol_find_enemy = True  #
        self.enenmy_is_coming = False  #
        self.myLandTool = None
        self.myFireTool = None
        self.mychecktool = None
        self.my_situation = None
        self.my_strategy_list = []
        self.cure_strategy_list = []
        self.cur_opt_idx = 0
        my_ai.scenario_type = None
        my_ai.my_xy = 0
        my_ai.enemy_xy = 0
        my_ai.all_first_city = {}
        my_ai.all_first_pos = {}
        my_ai.command_number = 0  #

        my_ai.my_judge_info = []

    #
    def step(self, observation: dict):
        #
        begin_time = time.time()
        my_ai.my_judge_info.extend(observation['judge_info'])
        self.ret_msg = []
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        if self.color == RED:
            self.ret_msg.extend(self.guide_first_IDlist(observation))
        else:
            self.ret_msg.extend(self.shoot_first_blue(observation))
        #
        #
        #
        if len(self.ret_msg) > 0:
            print(observation['time']['cur_step'], 'RED:**************************', time.time() - begin_time)
            return self.ret_msg
        self.update(observation)
        #
        #
        for each_opt in self.my_situation.our_opt:
            if each_opt.is_in_new_function:
                self.ret_msg.extend(each_opt.do_s1_action())

        ####self.ret_msg.extend(self.test_autoplane())
        #
        for each_strategy in self.cure_strategy_list[::-1]:
            if each_strategy.is_finished():
                each_strategy.release_allmember()  #
                self.cure_strategy_list.remove(each_strategy)  #
        #
        #
        #
        #
        #
        #
        for each_strategy in self.my_strategy_list[::-1]:
            if each_strategy.check():
                self.cure_strategy_list.append(each_strategy)
                self.my_strategy_list.remove(each_strategy)
                #
                #
                #
                #
        #
        for each_strategy in self.cure_strategy_list:
            self.ret_msg.extend(each_strategy.run())

        #
        #
        #
        #
        #
        #
        if self.my_situation.fight_step == ALL_OCCUPY_STEP:
            self.cur_opt_idx = 0
        len_opt = len(self.my_situation.our_opt)
        idx = 0

        sta_time = time.time()
        for i in range(len_opt):
            idx = i
            opt = self.my_situation.our_opt[(i + self.cur_opt_idx) % len_opt]
            if opt.is_in_new_function:
                #
                #
                continue
            if (time.time() - begin_time) > 15:
                break
            #
            #
            BaseNode.ai_opt = opt
            state = self.BehaviorTreeRoot.do_execute()
            if state == SUCCESS:
                pass
        if len_opt == 0:
            self.cur_opt_idx = 0
        else:
            self.cur_opt_idx = (idx + self.cur_opt_idx + 1) % len_opt

        self.ret_msg.extend(self.BehaviorTreeRoot.ret_msg)
        if len(self.ret_msg) > 0:
            for each in self.ret_msg[::-1]:
                if each['type'] == Waiting:
                    self.ret_msg.remove(each)
        #
        return self.ret_msg
        #
        #
        #

    def remove_redtank_attack_2(self, ret_msg1):
        #
        ret_msg = copy.deepcopy(ret_msg1)
        for each in ret_msg[::-1]:
            if each['obj_id'] == 0:
                for opt_id, act in self.observation['valid_actions'].items():  #
                    if opt_id != 0:
                        continue
                    if act.get(ActionType.Shoot) is not None:  #
                        for each_act in act[ActionType.Shoot]:
                            if each_act['target_obj_id'] == each['target_obj_id'] and each_act['attack_level'] <= 2:
                                ret_msg.remove(each)
                break
        return ret_msg

    #
    def update(self, observation):
        self.observation = observation
        self.ret_msg = []
        check_tool.update(self.observation)
        self.my_situation.update(self.observation)  #
        ai_my_operator.class_update(self.observation, self.my_situation)
        strategy.class_update(self.observation, self.my_situation)
        BaseNode.class_update(self.my_situation)

    #
    def reset(self):
        self.__init__()

    #
    def setup(self, scenario: int, color: int):
        my_ai.scenario = scenario
        #
        #
        #
        #
        #
        my_ai.scenario_type = GROUP
        self.get_scenario_info(scenario)
        my_ai.color = color  #
        self.observation = None
        self.map = Map(scenario)  #
        self.missile_patrol_find_enemy = True  #
        self.enenmy_is_coming = False  #
        self.myLandTool = land_tool(self.map, self.scenario_info)
        land_tool._stack_pos_list = []
        self.myFireTool = FireTool(self.map)
        self.mychecktool = check_tool(self.observation, self.map)
        self.my_situation = situation(self.observation, self.color, self.map, self.scenario_info)
        #
        #
        self.my_strategy_list.append(booming_team(self.color))  #
        #
        #
        #
        #

        #
        my_ai.plan_pos_list = {}
        if scenario == 2010211129:
            my_ai.plan_pos_list = copy.deepcopy(FIRST_POS_S1)
            my_ai.scenario_type = UNIT
        elif scenario == 2010431153:
            my_ai.plan_pos_list = copy.deepcopy(FIRST_POS_S8_1)
            my_ai.scenario_type = UNIT
        elif scenario == 2010441253:
            my_ai.plan_pos_list = copy.deepcopy(FIRST_POS_S8_2)
            my_ai.scenario_type = UNIT
        elif scenario == 2030111194:
            my_ai.plan_pos_list = copy.deepcopy(FIRST_POS_Q32)
            my_ai.scenario_type = GROUP
        elif scenario == 2030331196:
            my_ai.plan_pos_list = copy.deepcopy(FIRST_POS_Q8_1)
            my_ai.scenario_type = GROUP
        elif scenario == 2030341296:
            my_ai.plan_pos_list = copy.deepcopy(FIRST_POS_Q8_2)
            my_ai.scenario_type = GROUP
        self.BehaviorTreeRoot = self.buildBT()
        my_ai.city_poslist = []
        for eachcity in self.scenario_info['-1']['cities']:
            my_ai.city_poslist.append(eachcity['coord'])
        self.get_myandenemy_xy(self.scenario_info)
        #
        self.myLandTool.get_first_step_points()

    #
    def shoot_first_red(self, observation):
        ret_msg = []
        id_to_opt = {}
        id_to_subtype = {}
        guidedcar_list = []  #
        best = None
        for opt in observation['operators']:  #
            id_to_subtype[opt['obj_id']] = opt['sub_type']
            id_to_opt[opt['obj_id']] = opt
        for opt_id, act in observation['valid_actions'].items():  #
            opt_msg = []
            #
            if id_to_subtype[opt_id] == MISSILE:  #
                continue
            if act.get(ActionType.GuideShoot) is not None:
                if ['launch_ids'] not in guidedcar_list:  #
                    for target_subtype in self.my_situation.guideshoot_list:  #
                        shoot_list_temp = []
                        for each in act[ActionType.GuideShoot]:
                            if id_to_subtype[each['target_obj_id']] == target_subtype:
                                shoot_list_temp.append(each)
                        if len(shoot_list_temp) > 0:
                            best = max(shoot_list_temp, key=lambda x: x['attack_level'])
                            guidedcar_list.append(best['guided_obj_id'])
                            opt_msg.append({
                                'obj_id': opt_id,
                                'type': ActionType.GuideShoot,
                                'target_obj_id': best['target_obj_id'],
                                'weapon_id': best['weapon_id'],
                                'guided_obj_id': best['guided_obj_id'],
                            })
                            #
                            break
            if len(opt_msg) > 0:
                pass
            elif act.get(ActionType.Shoot) is not None:  #
                for target_subtype in self.my_situation.shoot_list[id_to_subtype[opt_id]]:  #
                    shoot_list_temp = []
                    for each in act[ActionType.Shoot]:
                        if id_to_subtype[each['target_obj_id']] == target_subtype:
                            shoot_list_temp.append(each)
                    if len(shoot_list_temp) > 0:
                        best = max(shoot_list_temp, key=lambda x: x['attack_level'])
                        opt_msg.append({
                            'obj_id': opt_id,
                            'type': ActionType.Shoot,
                            'target_obj_id': best['target_obj_id'],
                            'weapon_id': best['weapon_id']
                        })
                        #
                        break
            ret_msg.extend(opt_msg)
        return ret_msg

    def shoot_first_blue(self, observation):
        opt_ID_list = []
        for each in observation['operators']:
            opt_ID_list.append(each['obj_id'])
        return self.shoot_first_IDlist_attacklevelfirst(opt_ID_list, observation)

    def shoot_fast_first(self, observation):
        ret_msg = []
        for opt_id in observation['valid_actions']:
            act = observation['valid_actions'][opt_id]
            #
            for each_act in act:
                if each_act == ActionType.Shoot:
                    best = act[ActionType.Shoot][0]
                    ret_msg.append({
                        'obj_id': opt_id,
                        'type': ActionType.Shoot,
                        'target_obj_id': best['target_obj_id'],
                        'weapon_id': best['weapon_id']
                    })
                    break
        return ret_msg

    def shoot_best_first(self, observation):
        ret_msg = []
        for opt_id, act in observation['valid_actions'].items():  #
            if act.get(ActionType.Shoot) is not None:  #
                best = max(act[ActionType.Shoot], key=lambda x: x['attack_level'])
                ret_msg.append({
                    'obj_id': opt_id,
                    'type': ActionType.Shoot,
                    'target_obj_id': best['target_obj_id'],
                    'weapon_id': best['weapon_id']
                })
        return ret_msg

    def guide_first_IDlist(self, observation):
        guide_type = [CAR, AUTO_CAR, SOILDER, AUTO_PLANE]
        can_shoot = []
        can_guide = {}
        ret_msg = []
        id_to_opt = {}
        id_to_subtype = {}
        guidedcar_list = {}  #
        best = None
        car_guiders = {}
        opt_used = []
        attacklevel = {}  #
        guidelevel = {}  #
        car_maxguidelevel = {}  #
        guide_about_ids = []
        for opt in observation['operators']:  #
            id_to_subtype[opt['obj_id']] = opt['sub_type']
            id_to_opt[opt['obj_id']] = opt
            if opt['sub_type'] == CAR:
                car_guiders[opt['obj_id']] = []
                car_maxguidelevel[opt['obj_id']] = 0
                attacklevel[opt['obj_id']] = 0
        #

        for opt_id, act in observation['valid_actions'].items():
            if act.get(ActionType.GuideShoot) is not None:
                #
                max_expect = 0
                for each_act in act[ActionType.GuideShoot]:
                    if opt_id not in guide_about_ids:
                        guide_about_ids.append(opt_id)
                    if each_act['guided_obj_id'] not in guide_about_ids:
                        guide_about_ids.append(each_act['guided_obj_id'])
                    if opt_id not in car_guiders[each_act['guided_obj_id']]:
                        car_guiders[each_act['guided_obj_id']].append(opt_id)
                    car_opt = self.get_opt_by_id_fast(each_act['guided_obj_id'], observation)
                    my_opt = self.get_opt_by_id_fast(opt_id, observation)
                    enemy_opt = self.get_opt_by_id_fast(each_act['target_obj_id'], observation)
                    begin_time = time.time()
                    expect = self.my_situation.myFireTool.get_simulate_gudie_damage_A2B(my_opt,
                                                                                        car_opt['cur_hex'],
                                                                                        car_opt,
                                                                                        enemy_opt,
                                                                                        self.myLandTool,
                                                                                        each_act['weapon_id'],
                                                                                        each_act['attack_level']
                                                                                        )
                    print(observation['time']['cur_step'], 'guide_time:', time.time() - begin_time)
                    if car_maxguidelevel[each_act['guided_obj_id']] < expect:
                        car_maxguidelevel[each_act['guided_obj_id']] = expect
                    if max_expect < expect:
                        max_expect = expect
                guidelevel[opt_id] = max_expect
                #
                #
                #
        for opt_id, act in observation['valid_actions'].items():
            attacklevel[opt_id] = 0
            if opt_id in guide_about_ids:
                if act.get(ActionType.Shoot) is not None:
                    can_shoot.append(opt_id)
                    my_opt = self.get_opt_by_id_fast(opt_id, observation)

                    best = max(act[ActionType.Shoot], key=lambda x: x['attack_level'])
                    enemy_opt = self.get_opt_by_id_fast(best['target_obj_id'], observation)
                    begin_time = time.time()
                    attacklevel[opt_id] = self.my_situation.myFireTool.get_simulate_damage_A2B(my_opt,
                                                                                               my_opt['cur_hex'],
                                                                                               enemy_opt,
                                                                                               self.myLandTool,
                                                                                               best['weapon_id'],
                                                                                               best['attack_level'])
                    print(observation['time']['cur_step'], 'shoot_time:', time.time() - begin_time)
                    if attacklevel[opt_id] is None:
                        attacklevel[opt_id] = 0
                        print('bbb')
        #
        car_id_list = []
        for car_id, each_car in car_guiders.items():
            if car_maxguidelevel[car_id] <= attacklevel[car_id] \
                    or len(each_car) == 0:
                car_id_list.append(car_id)
        for each in car_id_list:
            del car_guiders[each]
        #
        for car_id, each_car in car_guiders.items():
            if car_id not in opt_used:
                if len(each_car) == 1:
                    if id_to_subtype[each_car[0]] == AUTO_PLANE:
                        if each_car[0] not in opt_used:
                            opt_used.append(each_car[0])
                            opt_used.append(car_id)
                            guidedcar_list[car_id] = each_car[0]
        for car_id, each_car in car_guiders.items():
            if car_id not in opt_used:
                if len(each_car) == 2:
                    if id_to_subtype[each_car[0]] == AUTO_PLANE \
                            and id_to_subtype[each_car[1]] == AUTO_PLANE:
                        for each_guider in each_car:
                            if each_guider not in opt_used:
                                opt_used.append(each_guider)
                                opt_used.append(car_id)
                                guidedcar_list[car_id] = each_guider
        #
        for car_id, each_car in car_guiders.items():
            if car_id not in opt_used:
                for each_guider in each_car:
                    if id_to_subtype[each_car[0]] != AUTO_PLANE:
                        if each_guider not in can_shoot:
                            if each_guider not in opt_used:
                                opt_used.append(each_guider)
                                opt_used.append(car_id)
                                guidedcar_list[car_id] = each_guider
                                break
        #
        for car_id, each_car in car_guiders.items():
            if car_id not in opt_used:
                for each_guider in each_car:
                    if id_to_subtype[each_guider] == AUTO_PLANE:
                        if each_guider not in opt_used:
                            opt_used.append(each_guider)
                            opt_used.append(car_id)
                            guidedcar_list[car_id] = each_guider
                        break
        #
        for car_id, each_car in car_guiders.items():
            if car_id in opt_used:
                for each_guider in each_car:
                    if id_to_subtype[each_guider] == AUTO_PLANE:
                        if each_guider not in opt_used:
                            if guidedcar_list[car_id] != each_guider:
                                opt_used.remove(guidedcar_list[car_id])
                                guidedcar_list[car_id] = each_guider
                        break
        #
        for car_id, each_car in car_guiders.items():
            if car_id not in opt_used:
                for each_guider in each_car:
                    if each_guider not in opt_used:
                        print(self.observation['time']['cur_step'])
                        print('soilder:', each_guider, '      ', attacklevel[each_guider])
                        print('car:', car_id, '      ', attacklevel[car_id])
                        print('guide:', car_id, '      ', guidelevel[each_guider])
                        if attacklevel[car_id] >= guidelevel[each_guider]:
                            break
                        if attacklevel[each_guider] >= guidelevel[each_guider]:
                            break
                        if attacklevel[car_id] + attacklevel[each_guider] > guidelevel[each_guider]:
                            break
                        opt_used.append(each_guider)
                        opt_used.append(car_id)
                        guidedcar_list[car_id] = each_guider
                        break
        shoot_id_list = []
        #
        for opt_id, act in observation['valid_actions'].items():  #
            if opt_id not in opt_used:
                if id_to_subtype[opt_id] != MISSILE:  #
                    shoot_id_list.append(opt_id)
                continue
            opt_msg = []
            if id_to_subtype[opt_id] != CAR:
                for car_id, guider_id in guidedcar_list.items():
                    if guider_id == opt_id:
                        break
                guide_act_list = []
                for each in act[ActionType.GuideShoot]:
                    if car_id == each['guided_obj_id']:
                        guide_act_list.append(each)
                if len(guide_act_list) == 0:
                    continue
                best = max(guide_act_list, key=lambda x: x['attack_level'])
                #
                #
                if best['attack_level'] > 6:
                    bigger6_act_list = []
                    for each in guide_act_list:
                        if each['attack_level'] <= best['attack_level'] \
                                and each['attack_level'] >= best['attack_level'] - 1:
                            bigger6_act_list.append(each)
                    for target_subtype in self.my_situation.guideshoot_list:  #
                        biggest_attact = -999
                        for each in bigger6_act_list:
                            if id_to_subtype[each['target_obj_id']] == target_subtype:
                                if each['attack_level'] >= biggest_attact:
                                    biggest_attact = each['attack_level']
                                    best = each
                        if biggest_attact != -999:
                            break
                ret_msg.append({
                    'obj_id': opt_id,
                    'type': ActionType.GuideShoot,
                    'target_obj_id': best['target_obj_id'],
                    'weapon_id': best['weapon_id'],
                    'guided_obj_id': best['guided_obj_id'],
                })
        #
        ret_msg.extend(self.shoot_first_IDlist_attacklevelfirst(shoot_id_list, observation))
        return ret_msg

    #
    #
    def shoot_first_IDlist_attacklevelfirst(self, opt_ID_list, observation):
        ret_msg = []
        id_to_opt = {}
        id_to_subtype = {}
        for opt in observation['operators']:  #
            id_to_subtype[opt['obj_id']] = opt['sub_type']
        for opt_id, act in observation['valid_actions'].items():  #
            if opt_id not in opt_ID_list:
                continue
            #
            if id_to_subtype[opt_id] == MISSILE or id_to_subtype[opt_id] == ARTILLERY:
                continue
            if act.get(ActionType.Shoot) is not None:  #
                best = max(act[ActionType.Shoot], key=lambda x: x['attack_level'])
                #
                if id_to_subtype[opt_id] == TANK:
                    if self.observation['time']['cur_step'] < 600:
                        if best['attack_level'] <= 2:
                            continue
                #
                #
                #
                #
                #
                if best['attack_level'] > 6:
                    sub_attack = self.my_situation.attack_add_num
                else:
                    sub_attack = 0

                bigger6_act_list = []
                for each in act[ActionType.Shoot]:
                    if each['attack_level'] <= best['attack_level'] \
                            and each['attack_level'] >= best['attack_level'] - sub_attack:
                        bigger6_act_list.append(each)
                for target_subtype in self.my_situation.shoot_list[id_to_subtype[opt_id]]:  #
                    biggest_attact = -999
                    for each in bigger6_act_list:
                        if id_to_subtype[each['target_obj_id']] == target_subtype:
                            if each['attack_level'] >= biggest_attact:
                                biggest_attact = each['attack_level']
                                best = each
                    if biggest_attact != -999:
                        break
                ret_msg.append({
                    'obj_id': opt_id,
                    'type': ActionType.Shoot,
                    'target_obj_id': best['target_obj_id'],
                    'weapon_id': best['weapon_id']
                })
        return ret_msg

    def shoot_first_IDlist_TYPEfirst(self, opt_ID_list, observation):
        ret_msg = []
        id_to_opt = {}
        id_to_subtype = {}
        guidedcar_list = []  #
        best = None
        for opt in observation['operators']:  #
            id_to_subtype[opt['obj_id']] = opt['sub_type']
            id_to_opt[opt['obj_id']] = opt
        for opt_id, act in observation['valid_actions'].items():  #
            if opt_id not in opt_ID_list:
                continue
            opt_msg = []
            if act.get(ActionType.Shoot) is not None:  #
                for target_subtype in self.my_situation.shoot_list[id_to_subtype[opt_id]]:  #
                    shoot_list_temp = []
                    for each in act[ActionType.Shoot]:
                        if id_to_subtype[each['target_obj_id']] == target_subtype:
                            shoot_list_temp.append(each)
                    if len(shoot_list_temp) > 0:
                        best = max(shoot_list_temp, key=lambda x: x['attack_level'])
                        opt_msg.append({
                            'obj_id': opt_id,
                            'type': ActionType.Shoot,
                            'target_obj_id': best['target_obj_id'],
                            'weapon_id': best['weapon_id']
                        })
                        #
                        break
            ret_msg.extend(opt_msg)
        return ret_msg

    def shoot_first_arrange(self, observation):
        ret_msg = []
        id_to_opt = {}
        id_to_subtype = {}
        best = None
        loss_blood = {}
        type = None
        for opt in observation['operators']:  #
            id_to_subtype[opt['obj_id']] = opt['sub_type']
            id_to_opt[opt['obj_id']] = opt
            loss_blood[opt['obj_id']] = 0
        for opt_id, act in observation['valid_actions'].items():  #
            opt_msg = []
            #
            if id_to_subtype[opt_id] == MISSILE:  #
                continue
            if act.get(ActionType.GuideShoot) is not None:
                for target_subtype in self.my_situation.guideshoot_list:  #
                    shoot_list_temp = []
                    for each in act[ActionType.GuideShoot]:
                        if id_to_subtype[each['target_obj_id']] == target_subtype:
                            shoot_list_temp.append(each)
                    if len(shoot_list_temp) > 0:
                        shoot_list_temp = sorted(shoot_list_temp, key=lambda x: x['attack_level'])
                        for each in shoot_list_temp:
                            if loss_blood[each['target_obj_id']] > 1.8 * id_to_opt[each['target_obj_id']]['blood']:
                                continue
                            if loss_blood[each['target_obj_id']] > 1 + id_to_opt[each['target_obj_id']]['blood']:
                                if best is None:
                                    type = ActionType.GuideShoot
                                    best = copy.deepcopy(each)
                                continue
                            loss_blood[each['target_obj_id']] += self.get_num(id_to_opt[opt_id],
                                                                              id_to_opt[each['target_obj_id']],
                                                                              each['attack_level'])
                            opt_msg.append({
                                'obj_id': opt_id,
                                'type': ActionType.GuideShoot,
                                'target_obj_id': each['target_obj_id'],
                                'weapon_id': each['weapon_id'],
                                'guided_obj_id': each['guided_obj_id'],
                            })
                            break
                        if len(opt_msg) > 0:
                            break
            if len(opt_msg) > 0:
                pass
            elif act.get(ActionType.Shoot) is not None:  #
                for target_subtype in self.my_situation.shoot_list[id_to_subtype[opt_id]]:  #
                    shoot_list_temp = []
                    for each in act[ActionType.Shoot]:
                        if id_to_subtype[each['target_obj_id']] == target_subtype:
                            shoot_list_temp.append(each)
                    if len(shoot_list_temp) > 0:
                        shoot_list_temp = sorted(shoot_list_temp, key=lambda x: x['attack_level'])
                        for each in shoot_list_temp:
                            if loss_blood[each['target_obj_id']] > 1.8 * id_to_opt[each['target_obj_id']]['blood']:
                                continue
                            if loss_blood[each['target_obj_id']] > 1 + id_to_opt[each['target_obj_id']]['blood']:
                                if best is None:
                                    type = ActionType.Shoot
                                    best = copy.deepcopy(each)
                                continue
                            loss_blood[each['target_obj_id']] += self.get_num(id_to_opt[opt_id],
                                                                              id_to_opt[each['target_obj_id']],
                                                                              each['attack_level'])
                            opt_msg.append({
                                'obj_id': opt_id,
                                'type': ActionType.Shoot,
                                'target_obj_id': each['target_obj_id'],
                                'weapon_id': each['weapon_id']
                            })
                            break
                        if len(opt_msg) > 0:
                            break
            if len(opt_msg) == 0:
                if best is not None:
                    loss_blood[best['target_obj_id']] += self.get_num(id_to_opt[opt_id],
                                                                      id_to_opt[best['target_obj_id']],
                                                                      best['attack_level'])
                    if type == ActionType.GuideShoot:
                        opt_msg.append({
                            'obj_id': opt_id,
                            'type': type,
                            'target_obj_id': best['target_obj_id'],
                            'weapon_id': best['weapon_id'],
                            'guided_obj_id': best['guided_obj_id'],
                        })
                    else:
                        opt_msg.append({
                            'obj_id': opt_id,
                            'type': type,
                            'target_obj_id': best['target_obj_id'],
                            'weapon_id': best['weapon_id']
                        })

            ret_msg.extend(opt_msg)
        return ret_msg

    def get_num(self, my_opt, enemy_opt, attack_level):
        return 1

    def shoot_first_red_KM(self, observation):
        ret_msg = []
        guide_type_list = [CAR, SOILDER, AUTO_PLANE, AUTO_CAR]
        shoot_type_list = [TANK, HELICOPTER]
        shoot_opt_list = []
        guide_opt_list = []
        for opt in observation['operators']:  #
            if opt['sub_type'] in guide_type_list:
                guide_opt_list.append(opt)
            if opt['sub_type'] in shoot_type_list:
                shoot_opt_list.append(opt)
        ret_msg.extend(self.guide_first_IDlist(guide_opt_list, observation))
        ret_msg.extend(self.shoot_first_IDlist(shoot_opt_list, observation))

        return ret_msg

    def guide_first_IDlist_KM(self, opt_list, observation):
        ret_msg = []
        id_to_opt = {}
        id_to_subtype = {}
        opt_ID_list = []
        guidedcar_list = []  #
        best = None
        shoot_list_temp = []
        left = []
        right = []
        weight = []
        msg = []
        for i in range(len(opt_list)):
            temp = []
            for j in range(len(opt_list)):
                temp.append(0)
            weight.append(temp)
            msg.append(temp)
        for opt in opt_list:  #
            id_to_subtype[opt['obj_id']] = opt['sub_type']
            id_to_opt[opt['obj_id']] = opt
            opt_ID_list.append(opt['obj_id'])
        for opt_id, act in observation['valid_actions'].items():  #
            if opt_id not in opt_ID_list:
                continue
            opt_msg = []
            if act.get(ActionType.GuideShoot) is not None:
                for target_subtype in self.my_situation.guideshoot_list:  #
                    shoot_list_temp = []
                    for each in act[ActionType.GuideShoot]:
                        if id_to_subtype[each['target_obj_id']] == target_subtype:
                            shoot_list_temp.append(each)
                    if len(shoot_list_temp) > 0:
                        best = max(shoot_list_temp, key=lambda x: x['attack_level'])
                        guidedcar_list.append(best['guided_obj_id'])
                        opt_msg.append({
                            'obj_id': opt_id,
                            'type': ActionType.GuideShoot,
                            'target_obj_id': best['target_obj_id'],
                            'weapon_id': best['weapon_id'],
                            'guided_obj_id': best['guided_obj_id'],
                        })
                        #
                        #
                        if id_to_opt[opt_id] not in left:  #
                            left.append(id_to_opt[opt_id])
                            shoot_list_temp.append(id_to_opt[opt_id])
                            l1 = len(left) - 1
                        else:
                            l1 = left.index(id_to_opt[opt_id])
                        if id_to_opt[best['target_obj_id']] not in right:  #
                            right.append(id_to_opt[best['target_obj_id']])
                            shoot_list_temp.append(id_to_opt[best['target_obj_id']])
                            r1 = len(right) - 1
                        else:
                            r1 = right.index(id_to_opt[best['target_obj_id']])
                        weight[l1][r1] = best['attack_level']  #
                        msg[l1][r1] = opt_msg
                        break
            if len(opt_msg) > 0:
                pass
            elif act.get(ActionType.Shoot) is not None:  #
                shoot_list_temp.append(id_to_opt[opt_id])
        msg_temp = self.shoot_first_IDlist(shoot_list_temp, observation)
        left_tmp = copy.deepcopy(left)
        right_tmp = copy.deepcopy(right)
        for each in msg_temp[::-1]:
            for idx in range(left_tmp):
                if each['obj_id'] == left_tmp[idx]['obj_id']:
                    right.append(1)
                    weight[idx][len(right) - 1] = each['attack_level']  #
                    msg[idx][len(right) - 1] = each
                    msg_temp.remove(each)
                    break
            for idx in range(right_tmp):
                if each['obj_id'] == right_tmp[idx]['obj_id']:
                    left.append(1)
                    weight[len(left) - 1][idx] = each['attack_level']  #
                    msg[len(left) - 1][idx] = each
                    msg_temp.remove(each)
                    break
        #
        #
        couple = []
        for idx in couple:
            if weight[idx][couple[i]] != 0:
                msg_temp.extend(msg[idx][couple[i]])

            #
        return msg_temp

    #

    def find_path(self, i):
        self.visit_left[i] = True
        for j in range(self.label_right):
            if self.visit_right[j]:  #
                continue
            gap = self.label_left[i] + self.label_right[j] - self.match_weight[i][j]
            if gap == 0:
                #
                self.visit_right[j] = True
                if self.np.isnan(self.match_right[j]) or self.find_path(self.match_right[j]):
                    self.match_right[j] = i
                    return True
            else:
                if self.slack_right < gap:
                    self.slack_right[j] = gap
                    return False

    def KM(self, N=10, M=10):
        self.max_inf = 99999999
        self.label_right = []  #
        self.label_left = []  #
        self.match_right = []  #
        self.match_left = []  #
        self.match_weight = [[]]
        self.visit_left = []  #
        self.visit_right = []
        self.slack_right = []  #
        for i in range(N + 1):
            self.visit_left.appand(False)  #
            self.visit_right.appand(False)
            self.slack_right.appand(self.max_inf)  #
        for i in range(N):
            for j in range(N):
                self.slack_right[j] = self.max_inf
            while True:
                for j in range(N):
                    self.visit_left[j] = False
                    self.visit_right[j] = False
                if self.find_path(i):
                    break
                d = self.max_inf
                for j in range(N):  #
                    if not self.visit_right[j] and self.slack_right[j] < d:
                        d = self.slack_right[j]
                for k in range(N):  #
                    if self.visit_left[k]:
                        self.label_left[k] -= d
                for n in range(N):
                    if self.visit_right[n]:
                        self.label_right[n] += d
        res = 0
        for j in range(N):
            if self.match_right[j] >= 0 and self.match_right[j] < N:
                res += self.adj_matrix[self.match_weight[j]][j]
        return res

    #

    def buildBT(self):
        tankRoot = self.buildBTTank()
        missileRoot = self.buildBTMissile()
        autocarRoot = self.buildBTAutocar()
        soilderRoot = self.buildBTSoilder()
        carRoot = self.buildBTCar()
        helicopterRoot = self.buildBTHelicopter()
        autoplaneRoot = self.buildBTAutoplane()
        artilleryRoot = self.buildBTArtillery()
        btRoot = Selector(children=[tankRoot, carRoot, missileRoot, autocarRoot, soilderRoot,
                                    helicopterRoot, autoplaneRoot, artilleryRoot],
                          description='行为树根节点，遍历我方算子，按算子类型执行相应逻辑')
        return btRoot

    def buildBTCar(self):
        #
        carOccupy = ActionOccupy(description='夺控')
        #
        isStop = ConditionIsStop(description='处于停止状态')
        carGetoff = ActionCarGetoff()
        carGetoffStrategy = Sequence(children=[isStop, carGetoff])
        #
        carMoveToBestSightPositiontoMaincity = ActionCarMoveToBestSightPositiontoMaincity(
            description='战车把士兵卸载后，选择一个便于导弹打击的有利位置')
        #
        need_to_hide = ConditionIsNeed_to_hide(description='战车切换隐蔽的前提条件')
        carHide = ActionHide(description='隐蔽')
        carNeedToHide = Sequence(children=[need_to_hide, carHide], description='战车尽量隐蔽')
        #
        carMovetoassistoccupy = ActionCarMovetoAssistoccupy(description='战车辅助夺控')
        #
        carMoveAndProtectcities = ActionSoilder_MoveAndProtectcities(description='战车后期夺控')

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #

        #

        car_do_Strategy_AUTO = Selector(children=[carOccupy,
                                                  #
                                                  #
                                                  carGetoffStrategy,
                                                  carMoveAndProtectcities,
                                                  carMovetoassistoccupy,
                                                  #
                                                  carNeedToHide],
                                        description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        car_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                               car_do_Strategy_AUTO])

        #
        isSTRATEGY_FIRSTSTEP = ConditionIsSTRATEGY_FIRSTSTEP(
            description='首回合策略')
        my_do_Strategy_FIRSTSTEP = ActionSTRATEGY_FIRSTSTEP()
        my_STRATEGY_FIRSTSTEP = Sequence(children=[isSTRATEGY_FIRSTSTEP,
                                                   my_do_Strategy_FIRSTSTEP])
        #
        car_BEHEAVIERTREE = Selector(children=[car_STRATEGY_AUTO,
                                               my_STRATEGY_FIRSTSTEP])
        isCarType = ConditionIsCar(description='战车')
        isMoving = ConditionIsMoving(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在移动')
        update = ActionMyUpdate(description='更新')
        carBTRoot = Sequence(children=[isCarType,
                                       isNotMoving,
                                       update,
                                       car_BEHEAVIERTREE])
        return carBTRoot

    def buildBTMissile(self):
        #
        maincityIsNotOurs = ConditionMaincityIsNotOurs(description='主控点未夺取')
        moveToMaincity = ActionMoveToMainCity()
        missileFlyToMaincityWhenIsNotOurs = Sequence(children=[maincityIsNotOurs,
                                                               moveToMaincity],
                                                     description='巡飞弹主控点周边巡逻')
        #
        secondcityIsNotOurs = ConditionSecondcityIsNotOurs(description='次控点未夺取')
        moveToSecondcity = ActionMoveToSecondCity()
        missileFlyToSecondcityWhenIsNotOurs = Sequence(children=[secondcityIsNotOurs,
                                                                 moveToSecondcity],
                                                       description='巡飞弹次控点周边巡逻')
        #
        maincityIsOccupiedByEnemy = ConditionMaincityIsOccupiedByEnemy()
        missileFlyToMaincityWhenEnemyOccupied = Sequence(children=[maincityIsOccupiedByEnemy,
                                                                   moveToMaincity],
                                                         description='主控点被敌人夺取，巡飞弹去监视')
        #
        maincityNotOccupiedByEnemy = DecoratorNot(child=maincityIsOccupiedByEnemy)
        secondcityIsOccupiedByEnemy = ConditionSecondcityIsOccupiedByEnemy()
        missileFlyToSecondityWhenEnemyOccupied = Sequence(children=[maincityNotOccupiedByEnemy,
                                                                    secondcityIsOccupiedByEnemy,
                                                                    moveToSecondcity])
        #
        missileAttack = ActionMissileAttack(description='巡飞弹执行攻击,按目标优先级')
        isMissleLifeLeast = ConditionIsMissleLifeLeast(description='巡飞弹生命末期')
        missleAttackWhenLifeLeast = Sequence(children=[isMissleLifeLeast, missileAttack],
                                             description='巡飞弹生命末期,即使不攻击也将自毁')
        #
        missileMovetoattack = ActionMissile_MovetoAttack(description='巡飞弹执行选择目标，向目标移动并攻击')
        #
        missilePatrol = ActionMissile_Patrol(description='围绕主控点巡逻（只有分队）')
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #

        #
        missile_do_Strategy_AUTO = Selector(children=[missileMovetoattack,
                                                      missilePatrol,
                                                      missileFlyToMaincityWhenIsNotOurs,
                                                      missileFlyToSecondcityWhenIsNotOurs,
                                                      missileFlyToMaincityWhenEnemyOccupied,
                                                      missileFlyToSecondityWhenEnemyOccupied,
                                                      missleAttackWhenLifeLeast],
                                            description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        missile_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                   missile_do_Strategy_AUTO])
        #
        missile_BEHEAVIERTREE = Selector(children=[missile_STRATEGY_AUTO])
        isMissileType = ConditionIsMissile(description='判断算子类型是否为巡飞弹')
        isMoving = ConditionIsMoving_FLY(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在移动')
        update = ActionMyUpdate(description='更新')
        missileBTRoot = Sequence(children=[isMissileType,
                                           isNotMoving,
                                           update,
                                           missile_BEHEAVIERTREE])
        return missileBTRoot

    def buildBTTank(self):
        #
        tankOccupy = ActionOccupy(description='坦克夺控')
        #
        canSeeEnemy = ConditionIsSeeEnemy(description='可以看到敌人')
        isNearestEnemyDistance = ConditionIsNearestEnemyDistance(distance=12,
                                                                 description='视野内最近的敌人距离大于12')
        haveMissile = ConditionHaveMissile(description='还拥有导弹')
        isStop = ConditionIsStop(description='处于停止状态')
        notStop = DecoratorNot(child=isStop, description='处于移动状态')
        stopMove = ActionStopMove(description='执行终止移动')
        tankStopmoveForMissile = Sequence(children=[canSeeEnemy,
                                                    isNearestEnemyDistance,
                                                    haveMissile,
                                                    notStop,
                                                    #
                                                    stopMove],
                                          description='能看到敌人情况，但无法攻击，需要终止移动为导弹打击做准备')
        #
        isBlue = ConditionIsBlue()
        isEnemyComing = ConditionIsEnemyComing(description='敌情出现')
        tankMoveToEnemy = ActionMovetoEnemy(description='找一个敌人靠近实施打击')
        tankBlueMoveToEnemyForAttack = Sequence(children=[  #
            isBlue,
            #
            #
            #
            tankMoveToEnemy],
            description='蓝方坦克：有敌情出现，靠近敌人为打击做准备')
        #
        isRed = ConditionIsRed()
        isEnemyDeadTankAndCarTotalNumBiggerThanTwo = ConditionIsEnemyDeadTankAndCarTotalNumBiggerThanNum(
            description='已经消灭至少两部敌方战车')
        tankRedMoveToEnemyForAttack = Sequence(children=[  #
            isRed,
            #
            #
            #
            isEnemyDeadTankAndCarTotalNumBiggerThanTwo,
            #
            #
            tankMoveToEnemy],
            description='红方坦克：至少消灭敌方两部车辆情况下，再靠近敌人')
        #
        notHaveMissile = DecoratorNot(child=haveMissile, description='没有导弹了')
        moveToSoilder = ActionMovetoSoilder(description='靠近我方士兵，步车协同')
        tankRedMoveToOurSoilder = Sequence(children=[  #
            #
            notHaveMissile,
            isRed,
            moveToSoilder],
            description='红方坦克需保持与士兵协同，向我方士兵靠拢')
        #
        tankMovetoAssistoccupy = ActionCarMovetoAssistoccupy(description='坦克支援士兵夺控')
        #
        tankMoveAndProtectcities = ActionSoilder_MoveAndProtectcities(description='坦克后期夺控')
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        tank_do_Strategy_AUTO = Selector(children=[tankOccupy,
                                                   tankStopmoveForMissile,
                                                   tankMoveAndProtectcities,
                                                   tankMovetoAssistoccupy
                                                   #
                                                   #
                                                   #
                                                   #
                                                   ],
                                         description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        tank_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                tank_do_Strategy_AUTO])
        #
        isSTRATEGY_FIRSTSTEP = ConditionIsSTRATEGY_FIRSTSTEP(
            description='首回合策略')
        my_do_Strategy_FIRSTSTEP = ActionSTRATEGY_FIRSTSTEP()
        my_STRATEGY_FIRSTSTEP = Sequence(children=[isSTRATEGY_FIRSTSTEP,
                                                   my_do_Strategy_FIRSTSTEP])
        #
        tank_BEHEAVIERTREE = Selector(children=[tank_STRATEGY_AUTO,
                                                my_STRATEGY_FIRSTSTEP])
        isTankType = ConditionIsTank(description='判断算子类型是否为坦克')
        isMoving = ConditionIsMoving(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在攻击')
        update = ActionMyUpdate(description='更新')
        tankBTRoot = Sequence(children=[isTankType,
                                        isNotMoving,
                                        update,
                                        tank_BEHEAVIERTREE])
        #
        #
        return tankBTRoot

    def buildBTSoilder(self):
        #
        soilderOccupy = ActionOccupy(description='夺控')
        #
        maincityIsNotOurs = ConditionMaincityIsNotOurs(description='主控点未夺取')
        isOurSoilderDeadNumBiggerThan = ConditionIsOurSoilderDeadNumBiggerThan(
            description='我方有士兵被消灭')
        moveToMainCity = ActionMoveToMainCity(description='向主控点移动')
        soilderMoveToMainCityWhenOtherSoilderIsDead = Sequence(children=[maincityIsNotOurs,
                                                                         isOurSoilderDeadNumBiggerThan,
                                                                         moveToMainCity
                                                                         #
                                                                         ],
                                                               description='我方有士兵被消灭,完成被消灭士兵的夺控任务')
        #
        maincityIsOurs = ConditionMaincityIsNotOurs(description='主控点已经夺取')
        secondcityIsNotOurs = ConditionSecondcityIsNotOurs(description='次控点未夺取')
        moveToSecondCity = ActionMoveToSecondCity(description='向次控点移动')
        soilderMoveToSecondCityWhenOtherSoilderIsDead = Sequence(children=[maincityIsOurs,
                                                                           secondcityIsNotOurs,
                                                                           isOurSoilderDeadNumBiggerThan,
                                                                           moveToSecondCity
                                                                           #
                                                                           ],
                                                                 description='我方有士兵被消灭,完成被消灭士兵的夺控任务')
        #
        isStandingOccupiedCity = ConditionIsStandingOccupiedCity(description='守卫夺控点')
        #
        isMaincityInMyCircle = ConditionIsMaincityInMyCircle(description='主控点在我两格范围内')
        isEnemyAroundMaincity = ConditionIsEnemyAroundMaincity(description='主控点周边有坦克或战车')
        notEnemyAroundMaincity = DecoratorNot(child=isEnemyAroundMaincity,
                                              description='主控点周边没有坦克或战车')
        moveToMainCityInCircle = Sequence(children=[maincityIsNotOurs,
                                                    isMaincityInMyCircle,
                                                    notEnemyAroundMaincity,
                                                    moveToMainCity
                                                    #
                                                    ],
                                          description='主控点在我两格范围内,比较容易夺控，向主控点移动,默认一级冲锋')
        #
        isSecondcityInMyCircle = ConditionIsSecondcityInMyCircle(description='次控点在我两格范围内')
        isEnemyAroundSecondcity = ConditionIsEnemyAroundSecondcity(description='次控点周边有坦克或战车')
        notEnemyAroundSecondcity = DecoratorNot(child=isEnemyAroundSecondcity,
                                                description='次控点周边没有坦克或战车')
        moveToSecondCityInCircle = Sequence(children=[secondcityIsNotOurs,
                                                      isSecondcityInMyCircle,
                                                      notEnemyAroundSecondcity,
                                                      moveToSecondCity
                                                      #
                                                      ],
                                            description='次控点在我两格范围内,比较容易夺控，向次控点移动,默认一级冲锋')
        #
        isSeeEnemy = ConditionIsSeeEnemy()
        isEnemyInFireRange = ConditionIsEnemyInMyShootRange(description='看到的敌人在我火力范围内')
        notWeaponPrepared = ConditionNotWeaponPrepared()
        isWeaponPrepared = DecoratorNot(child=notWeaponPrepared)
        stopMove = ActionStopMove()
        soilderStopMoveForFire = Sequence(children=[isSeeEnemy,
                                                    isEnemyInFireRange,
                                                    isWeaponPrepared,
                                                    #
                                                    stopMove],
                                          description='看见敌人,并且该敌人在我火力范围内，停止')
        #
        soilderMoveToCarSetCityWanted = ActionSoilderMoveToCarSetCityWanted(
            description='向所属战车的目标夺控点移动，与所属战车目标一致,默认一级冲锋')

        #
        soilderMoveToMycity = ActionSoilder_MoveToMycity(
            description='移动到对应的夺控点')
        #
        soilderProtectToMycity = ActionSoilder_PortectMycity(
            description='守护当前夺控点')
        #
        soilderMoveToNearestcity = ActionSoilder_MoveToNearestcity(
            description='移动到最近的夺控点')
        #
        isTire = ConditionIsTire(description='已经疲劳')
        carHide = ActionHide(description='隐蔽')
        carNeedToHide = Sequence(children=[isTire, carHide], description='战车尽量隐蔽')
        #
        soilderMoveAndProtectcities = ActionSoilder_MoveAndProtectcities(
            description='移动到最近的夺控点')
        #
        soilderAttackMoveAndProtectcities = ActionSoilder_Attack_MoveAndProtectcities(
            description='攻击+夺控并保护夺控点：攻击+动作10+动作11+动作12')
        #
        soilderRemoveKeep = ActionSoilder_RemoveKeep(description='强制移除压制状态')
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #

        #

        soilder_do_Strategy_AUTO = Selector(children=[soilderRemoveKeep,
                                                      soilderOccupy,
                                                      #
                                                      #
                                                      #
                                                      #
                                                      soilderAttackMoveAndProtectcities
                                                      #
                                                      #
                                                      #
                                                      #
                                                      #
                                                      #
                                                      #
                                                      ],
                                            description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        soilder_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                   soilder_do_Strategy_AUTO])
        #
        isSTRATEGY_FIRSTSTEP = ConditionIsSTRATEGY_FIRSTSTEP(
            description='首回合策略')
        my_do_Strategy_FIRSTSTEP = ActionSTRATEGY_FIRSTSTEP()
        soilder_STRATEGY_FIRSTSTEP = Sequence(children=[isSTRATEGY_FIRSTSTEP,
                                                        my_do_Strategy_FIRSTSTEP])
        #
        soilder_BEHEAVIERTREE = Selector(children=[soilder_STRATEGY_FIRSTSTEP,
                                                   soilder_STRATEGY_AUTO])
        isSoilderType = ConditionIsSoilder()
        isMoving = ConditionIsMoving(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在移动')
        isNotgeton = ConditionIsNotOnBoard(description='算子未在车上')
        update = ActionMyUpdate(description='更新')
        soilderBTRoot = Sequence(children=[isSoilderType,
                                           isNotMoving,
                                           isNotgeton,
                                           update,
                                           soilder_BEHEAVIERTREE])
        return soilderBTRoot

    def buildBTHelicopter(self):
        #
        helicopter_auto = ActionSoilder_Helicopter_auto()
        #
        #
        helicopter_do_Strategy_AUTO = Selector(children=[helicopter_auto],
                                               description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        helicopter_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                      helicopter_do_Strategy_AUTO])
        #
        helicopter_BEHEAVIERTREE = Selector(children=[helicopter_STRATEGY_AUTO])
        ishelicopterType = ConditionIsHelicopter()
        isMoving = ConditionIsMoving_FLY(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在移动')
        update = ActionMyUpdate(description='更新')
        helicopterBTRoot = Sequence(children=[ishelicopterType,
                                              isNotMoving,
                                              update,
                                              helicopter_BEHEAVIERTREE])
        return helicopterBTRoot

    def buildBTAutoplane(self):
        #
        #
        autoplane_do_Strategy_AUTO = Selector(children=[autoplane_auto],
                                              description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        autoplane_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                     autoplane_do_Strategy_AUTO])
        #
        autoplane_BEHEAVIERTREE = Selector(children=[autoplane_STRATEGY_AUTO])
        isautoplaneType = ConditionIsAutoplane()
        isMoving = ConditionIsMoving_FLY(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='无法看到敌人')
        update = ActionMyUpdate(description='更新')
        autoplaneBTRoot = Sequence(children=[isautoplaneType,
                                             isNotMoving,
                                             update,
                                             autoplane_BEHEAVIERTREE])
        return autoplaneBTRoot

    def buildBTArtillery(self):
        #
        artilleryOccupy = ActionOccupy(description='夺控')
        #
        artilleryMoveToMainCity = ActionMoveToMainCity(description='移动到主控点')
        #

        artillery_do_Strategy_AUTO = Selector(children=[artilleryOccupy
                                                        #
                                                        ],
                                              description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        artillery_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                     artillery_do_Strategy_AUTO])
        #
        artillery_BEHEAVIERTREE = Selector(children=[artillery_STRATEGY_AUTO])
        isartilleryType = ConditionIsArtillery()
        isMoving = ConditionIsMoving(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在移动')
        update = ActionMyUpdate(description='更新')
        artilleryBTRoot = Sequence(children=[isartilleryType,
                                             isNotMoving,
                                             update,
                                             artillery_BEHEAVIERTREE])
        return artilleryBTRoot

    def buildBTAutocar(self):
        #
        autoCarOccupy = ActionOccupy(description='夺控')
        #
        autocarMovetoGuidepos = ActionAutocarMovetoGuidepos(description='寻找合适的引导射击点')
        #
        autocarHide = ActionHide(description='隐蔽')
        #
        autocarMoveToMainCity = ActionMoveToMainCity(description='移动到主控点')
        #
        autocarMovetoAssistoccupy = ActionCarMovetoAssistoccupy(description='辅助夺控')
        #
        autocarMoveAndProtectcities = ActionSoilder_MoveAndProtectcities(description='无人车后期夺控')

        #
        autocarFight = ActionAutocarFight(description='优先引导攻击，其次普通攻击')
        #
        autocar_do_Strategy_AUTO = Selector(children=[autoCarOccupy,
                                                      #
                                                      #
                                                      autocarMoveAndProtectcities,
                                                      autocarMovetoAssistoccupy,
                                                      autocarHide],
                                            description='非move回合执行')
        isSTRATEGY_AUTO = ConditionIsSTRATEGY_AUTO(
            description='若没有接收到协同配合指令，默认按个体行为树策略执行')
        autocar_STRATEGY_AUTO = Sequence(children=[isSTRATEGY_AUTO,
                                                   autocar_do_Strategy_AUTO])
        #
        isSTRATEGY_FIRSTSTEP = ConditionIsSTRATEGY_FIRSTSTEP(
            description='首回合策略')
        my_do_Strategy_FIRSTSTEP = ActionSTRATEGY_FIRSTSTEP()
        autocar_STRATEGY_FIRSTSTEP = Sequence(children=[isSTRATEGY_FIRSTSTEP,
                                                        my_do_Strategy_FIRSTSTEP])
        #
        autocar_BEHEAVIERTREE = Selector(children=[autocar_STRATEGY_AUTO,
                                                   autocar_STRATEGY_FIRSTSTEP])
        isAutocarType = ConditionIsAutocar()
        isMoving = ConditionIsMoving(description='算子正在移动')
        isNotMoving = DecoratorNot(child=isMoving, description='算子未在移动')
        update = ActionMyUpdate(description='更新')
        autocarBTRoot = Sequence(children=[isAutocarType,
                                           isNotMoving,
                                           update,
                                           autocar_BEHEAVIERTREE])
        return autocarBTRoot

    #
    def get_scenario_info(self, scenario: int):
        SCENARIO_INFO_PATH = os.path.join(os.path.dirname(__file__), f'scenario_{scenario}.json')
        with open(SCENARIO_INFO_PATH, encoding='utf8') as f:
            self.scenario_info = json.load(f)

    def get_myandenemy_xy(self, scenario_info):
        my_x = 0
        my_y = 0
        my_num = 0
        enemy_x = 0
        enemy_y = 0
        enemy_num = 0
        for each_opt in scenario_info['-1']['operators']:
            if each_opt['color'] == self.color:
                my_num += 1
                my_x += int(each_opt['cur_hex'] / 100)
                my_y += each_opt['cur_hex'] % 100
            else:
                enemy_num += 1
                enemy_x += int(each_opt['cur_hex'] / 100)
                enemy_y += each_opt['cur_hex'] % 100
        my_ai.my_xy = int(my_x / my_num) * 100 + int(my_y / my_num)
        my_ai.enemy_xy = int(enemy_x / enemy_num) * 100 + int(enemy_y / enemy_num)
        pass

    def get_opt_by_id_fast(self, id_num, observation):
        for each in observation['operators']:
            if each['obj_id'] == id_num:
                return each
        return None

#
class ai_my_operator():
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.circle = 0
        ai_my_operator.pos_bestSeePosition_villege_tree = []
        ai_my_operator.pos_list_bestSeePosition = []
        ai_my_operator.secondcity_select = False
        ai_my_operator.maincity_select = False
        self.is_in_new_function = True
        self.waiting_time = 0
        self.cityWanted = None  #
        self.color = color
        self.map = map
        self.scenario_info = scenario_info
        self.my_check_tool = check_tool(observation, map)
        self.myLandTool = land_tool(map, scenario_info)
        self.is_thisturn_finished = False
        self.movetype = MoveType_car
        self.operator = operator
        self.strategy = None
        self.strategy_type = STRATEGY_AUTO
        self.movepath = []
        self.move2hex = operator['cur_hex']  #
        self.first_pos = None  #
        self.action_waiting = [{'obj_id': self.operator['obj_id'],
                                'type': Waiting}]
        self.seven_neighbors_list = []
        self.nearest_soilder = None
        self.seven_cityWanted = []
        self.get_on_flag = False
        self.moving_func_list = {}
        ai_my_operator.observation = None
        self.command_num = 0
        self.move_step = 0
        self.func_done = False
        #
        if my_ai.scenario == 2010211129:
            self.set_func_list_32()
        elif my_ai.scenario == 2010431153:
            self.set_func_list_8_1()
        elif my_ai.scenario == 2010441253:
            self.set_func_list_8_2()
        elif my_ai.scenario == 2030111194:
            self.set_func_list_q32()
        elif my_ai.scenario == 2030331196:
            self.set_func_list_q8_1()
        elif my_ai.scenario == 2030341296:
            self.set_func_list_q8_2()
        self.auto_moving = False
        self.area_4227_high_mountain = [4125, 4126, 4127, 4128, 4225, 4226, 4227, 4228, 4325, 4326, 4327, 4425, 4426,
                                        4427, 4428, 4524, 4525, 4526]
        self.area_3938_road_right_up = [3837, 3838, 3839, 3936, 3937, 3938, 3939, 4038, 4039, 4040]
        self.area_4635_maincity_down_road_left = [4533, 4534, 4535, 4536, 4632, 4633, 4634, 4635, 4637, 4733, 4734,
                                                  4735, 4736, 4737]
        self.main_area = [4234, 4235, 4333, 4334, 4335, 4434, 4435, 4436, 4437]
        self.secondary_area = [3929, 3930, 4029, 4030, 4031, 4129, 4130]
        self.target_id = None
#q82
    def set_func_list_q8_2(self):
#
        self.moving_func_list[(100, 6532, 0)] = [self.do_get_off_0]
        self.moving_func_list[(1100, 6648, 0)] = [self.do_get_off_0]
        #self.moving_func_list[(2100, 5651, 0)] = [self.do_get_off_0]
        #self.moving_func_list[(3100, 5655, 0)] = [self.do_get_off_0]

        self.moving_func_list[(200, 6532, None)] = [self.do_get_on_red_0_1]
        self.moving_func_list[(200, 5042, None)] = [self.do_changepath_2]
        self.moving_func_list[(1200, 6648, None)] = [self.do_get_on_red_0_1]
        #self.moving_func_list[(2200, 5651, None)] = [self.do_get_on_red_0_1]
        #self.moving_func_list[(3200, 5655, None)] = [self.do_get_on_red_0_1]

#
        self.moving_func_list[(200, None, 9)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(1200, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(2200, None, 2)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(3200, None, 4)] = [self.do_movearound_soilder_protect_city]

        self.moving_func_list[(200, None, None)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(1200, None, None)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(2200, None, None)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(3200, None, None)] = [self.do_stop_to_shoot_cars]

#红方战车到点后下车：
        self.moving_func_list[(100, 5042, None)] = [self.do_get_off_safe, self.do_waiting_3100_q8_1]
        self.moving_func_list[(100, 5639, None)] = [self.do_waiting_100_q82_5639, self.do_get_off_safe,self.do_waiting_100_q82_5639_2]
        self.moving_func_list[(1100, 5046, None)] = [self.do_get_off_safe, self.do_waiting_3100_q8_1]
        self.moving_func_list[(1100, 5648, None)] = [self.do_waiting_1100_q82_5648, self.do_get_off_safe,self.do_waiting_100_q82_5639_2]


        self.moving_func_list[(2100, 5148, None)] = [self.do_get_off_safe]
        self.moving_func_list[(2100, 4249, None)] = [self.do_get_off_safe]
        self.moving_func_list[(3100, 4951, None)] = [self.do_get_off_safe]
        self.moving_func_list[(3100, 4653, None)] = [self.do_get_off_safe]
#
        self.moving_func_list[(400, 5023, None)] = [self.do_hide]
#

        self.moving_func_list[(0, 6433, None)] = [self.do_waiting_less75s]
        self.moving_func_list[(0, 4048, None)] = [self.do_setfinish_0_q82_4048,self.do_tank_goback]
        self.moving_func_list[(1000, 4048, None)] = [self.do_setfinish_0_q82_4048,self.do_tank_goback]
        self.moving_func_list[(2000, 4048, 3)] = [self.do_setfinish_0_q82_4048,self.do_tank_goback]
        self.moving_func_list[(3000, 4048, 2)] = [self.do_setfinish_0_q82_4048,self.do_tank_goback]
#
        #
        #
        self.moving_func_list[(4600, 4045, None)] = [self.do_waiting_whenhasc3]
        self.moving_func_list[(4601, 4038, None)] = [self.do_waiting_whenhasc3]
        #
        self.moving_func_list[(4500, 3745, None)] = [self.do_waiting_4500_q8_1]
        self.moving_func_list[(4501, 3747, None)] = [self.do_waiting_4500_q8_1]

        self.moving_func_list[(4500, 2749, None)] = [ self.do_set_finish_flag]
        self.moving_func_list[(4501, 2744, None)] = [ self.do_set_finish_flag]


        self.moving_func_list[(700, None, None)] = [self.do_set_flg_whenseecar_missile]
        self.moving_func_list[(1700, None, None)] = [self.do_set_flg_whenseecar_missile]
        self.moving_func_list[(2700, None, None)] = [self.do_set_flg_whenseecar_missile]
        self.moving_func_list[(3700, None, None)] = [self.do_set_flg_whenseecar_missile]

        self.moving_func_list[(701, None, 0)] = [self.do_set_notattackflg_missile]


        self.moving_func_list[(5300, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5301, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5302, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5303, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5304, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5305, None, None)] = [self.do_set_finish_flag]



        self.moving_func_list[(10100, 1631, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(10101, 1731, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(11100, 1741, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(11101, 1842, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(12100, 1948, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(12101, 2048, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(13100, 1554, None)] = [self.do_waiting_for_get_on]
        self.moving_func_list[(13101, 1555, None)] = [self.do_waiting_for_get_on]

        self.moving_func_list[(10200, 1631, None)] = [self.do_get_on_blue_0]

        self.moving_func_list[(10201, None, 1)] = [self.do_movearound_soilder_protect_city]

        #
        self.moving_func_list[(11200, 1741, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(11200, None, 2)] = [self.do_protect_subcity_10200_q92,self.do_movearound_soilder_protect_city]
        self.moving_func_list[(10200, None, 1)] = [self.do_protect_subcity_10200_q92,self.do_movearound_soilder_protect_city]
        self.moving_func_list[(10200, 3638, None)] = [self.do_get_subcity_10200_q82_3638]

        #
        self.moving_func_list[(11201, None, 1)] = [self.do_movearound_soilder_protect_city]

        #
        self.moving_func_list[(13200, 4048, None)] = [self.do_judge_13201_q82_4048, self.do_stop_to_shoot]
        self.moving_func_list[(13201, 4048, None)] = [self.do_judge_13201_q82_4048, self.do_stop_to_shoot]

        self.moving_func_list[(12201, 2048, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(12201, 4048, None)] = [self.do_judge_13201_q82_4048]
        self.moving_func_list[(12201, None, None)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(12201, None, 2)] = [self.do_move_to_city_six_has_enemysoilder]
        self.moving_func_list[(12201, None, 11)] = [self.do_movearound_soilder_protect_city]

        self.moving_func_list[(13200, None, None)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(13201, None, None)] = [self.do_stop_to_shoot_cars]

        self.moving_func_list[(12200, 1948, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(12200, None, None)] = [self.do_stop_to_shoot_cars]

        self.moving_func_list[(12200, None, 1)] = [self.do_protect_subcity_12200_q82,self.do_movearound_soilder_protect_city]
        #
        self.moving_func_list[(12200, 3243, None)] = [self.do_choose_12200_q82_3243]

        self.moving_func_list[(13201, None, 1)] = [self.do_move_to_city_six_has_enemysoilder]

        self.moving_func_list[(10201, None, 1)] = [self.do_movearound_soilder_protect_city]

        self.moving_func_list[(13200, None, 2)] = [self.do_movearound_soilder_protect_city]

        self.moving_func_list[(10201, 1731, None)] = [self.do_get_on_blue_0]

        self.moving_func_list[(11201, 1842, None)] = [self.do_get_on_blue_0]

        self.moving_func_list[(13200, 1554, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(13201, 1555, None)] = [self.do_get_on_blue_0]

        self.moving_func_list[(11100, None, None)] = [self.add_battle]
        self.moving_func_list[(11101, None, None)] = [self.add_battle]
        self.moving_func_list[(12100, None, None)] = [self.add_battle]
        self.moving_func_list[(12101, None, None)] = [self.add_battle]
        self.moving_func_list[(13100, None, None)] = [self.add_battle]
        self.moving_func_list[(13101, None, None)] = [self.add_battle]

        self.moving_func_list[(10000, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(10001, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(11000, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(11001, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(12000, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(12001, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(13000, None, None)] = [self.do_free_kill_car_blue]
        self.moving_func_list[(13001, None, None)] = [self.do_free_kill_car_blue]

        #


        #
        #
        #
        #
        #
        #
        #
        #

        #
        self.moving_func_list[(10100, 2437, None)] = [self.do_get_off_safe]
        self.moving_func_list[(10101, 3031, None)] = [self.do_get_off_safe]
        self.moving_func_list[(11100, 2343, None)] = [self.do_get_off_safe]
        self.moving_func_list[(11101, 2443, None)] = [self.do_get_off_safe]
        self.moving_func_list[(12100, 2843, None)] = [self.do_get_off_safe]
        self.moving_func_list[(12101, 2844, None)] = [self.do_get_off_safe]
        self.moving_func_list[(13100, 3344, None)] = [self.do_get_off_safe]
        self.moving_func_list[(13101, 3345, None)] = [self.do_get_off_safe]

        #
        self.moving_func_list[(14501, None, None)] = [self.continue_move1]
        self.moving_func_list[(14500, None, None)] = [self.continue_move]

        #
        self.moving_func_list[(14600, 4245, None)] = [self.helicopter_move]
        self.moving_func_list[(14600, 4245, None)] = [self.helicopter_move]
        #

        #

        #
#

    def do_protect_subcity_12200_q82(self):

        has_enemy = self.is_has_enemy_in_distance(3947, [SOILDER] + CARS, -1, 2)

        if self.observation['cities'][1]['flag'] != self.color:
            if has_enemy is False:
                self.move_step = 20
                self.auto_moving = False
        return []

    def do_protect_subcity_10200_q92(self):

        has_enemy = self.is_has_enemy_in_distance(3939, [SOILDER] + CARS, -1, 2)

        if self.observation['cities'][5]['flag'] != self.color:
            if has_enemy is False:
                self.move_step = 10
                self.auto_moving = False
        return []

    def do_changepath_2(self):
        self.move_step = 2
        return []
    def helicopter_move(self):
        if self.operator['C3'] == 0:
            self.move_step = 10
        return []

    def do_choose_12200_q82_3243(self):
        left_solier_id_list = [10201, 10200, 11200]
        solier_blood = 0
        for solier_id in left_solier_id_list:
            opt = self.situation.get_cur_opt_by_id(solier_id)
            if opt is not None:
                solier_blood += opt['blood']

        if solier_blood <= 6:
            self.auto_moving = False
            self.move_step = 10

        return []

    def do_judge_13201_q82_4048(self):
        enemy_list = self.operator['see_enemy_bop_ids']
        see_tk_blood = 0
        for enemy_id in enemy_list:
            opt = self.situation.get_cur_opt_by_id(enemy_id)
            if opt is not None and opt['sub_type'] == TANK:
                see_tk_blood += opt['blood']
        if see_tk_blood <= 4 and self.move_step < 10:
            self.auto_moving = False
            self.move_step = 10

        return []

    def do_get_subcity_10200_q82_3638(self):
        if self.observation['cities'][5]['flag'] != self.color and self.move_step < 10:
            self.move_step = 10

        return []
        #

    def continue_move(self):
        if self.move_step == 8:
            self.move_step = 4
        return []

    def continue_move1(self):
        if self.move_step == 9:
            self.move_step = 4
        return []

    def do_free_kill_car_blue(self):

        if self.move_step < 2:
            return []

        #
        #

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #

        #
        #
        #
        #
        #
        #

        if self.target_id is not None:
            target_history = self.situation.get_enemy_history_by_id(self.target_id)
            if target_history[2] is False and target_history[3] is False:
                return self.do_move_to_point(target_history[0]['cur_hex'])

        #
        #

        enemy_id_set = set()
        for id in range(10000, 14000, 1000):
            blue_tk1 = self.situation.get_cur_opt_by_id(id)
            if blue_tk1 is not None:
                tmp_id_set = set(blue_tk1['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set
            blue_tk2 = self.situation.get_cur_opt_by_id(id + 1)
            if blue_tk2 is not None:
                tmp_id_set = set(blue_tk2['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set

        for id in range(14500, 14700, 100):
            air1 = self.situation.get_cur_opt_by_id(id)
            if air1 is not None:
                tmp_id_set = set(air1['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set
            air2 = self.situation.get_cur_opt_by_id(id + 1)
            if air2 is not None:
                tmp_id_set = set(air2['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set

        for id in enemy_id_set:
            enemy_opt = self.situation.get_cur_opt_by_id(id)
            if enemy_opt is None:
                continue
            if enemy_opt['sub_type'] == CAR:
                return self.do_move_to_point(enemy_opt['cur_hex'])

        c_list = list(self.situation.enemy_history.values())

        sort_list = []
        for tmp_tuple in c_list:
            tmp_list = list(tmp_tuple)
            dis = self.map.get_distance(tmp_list[0]['cur_hex'], self.operator['cur_hex'])
            tmp_list.append(dis)
            sort_list.append(tmp_list)

        sort_list = sorted(sort_list, key=lambda x: (x[4] * -1, int(x[1]), x[0]['obj_id']), reverse=True)
        #

        for history in sort_list:
            opt = history[0]
            if (opt['sub_type'] == CAR) and \
                    history[2] is False and \
                    history[3] is False:
                #
                self.target_id = opt['obj_id']
                print("find ", opt['cur_hex'])
                return self.do_move_to_point(opt['cur_hex'])
        #

        free_list = [3847, 3848, 3947]
        if len(free_list) == 0:
            return []

        xy = self.operator['cur_hex']
        if xy in free_list:
            free_list.remove(xy)
        import random as rd
        return self.do_move_to_point(free_list[rd.randint(0, len(free_list) - 1)])

    def get_free_list_blue(self, step):
        if self.move_step < 4 or \
                (self.move_step >= 10):
            return []
        print(" ", self.move_step)
        #
        #

        if self.is_has_myopt_in([3747]) is False or self.situation.cur_step < 1000:
            return [  #
                3747, 3847, 3946, 4046,
                4044, 4045, 4046,
                4143, 4144, 4145
            ]

        #
        #
        #
        else:
            self.move_step = 10
        #
        #
        #
        #
        #
        #
        #
        #

#q82红方：
    def do_waiting_100_q82_5639_2(self):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if each_enemy[0]['sub_type'] == TANK:
                    if each_enemy[0]['cur_hex'] > 4200:
                        return self.action_waiting
        self.func_done = True
        return []
    def do_waiting_1100_q82_5648(self):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if each_enemy[0]['sub_type'] == TANK:
                    if each_enemy[0]['cur_hex'] > 4200:
                        return []
        self.func_done = True
        return []
    def do_waiting_100_q82_5639(self):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if each_enemy[0]['sub_type'] == TANK:
                    if each_enemy[0]['cur_hex'] > 4100:
                        return []
        self.func_done = True
        return []
    def do_setfinish_0_q82_4048(self):
        if self.observation['time']['cur_step'] > 2350:
            self.do_set_finish_flag()
            self.func_done = True
            return []
        if 4048 in self.situation.want_to_move_pos:
            return []
        return self.action_waiting
    def do_waiting_less95s(self):
        if self.observation['time']['cur_step'] < 95:
            return self.action_waiting
        return []
    def do_waiting_less75s(self):
        if self.observation['time']['cur_step']< 75:
           return self.action_waiting
        return []
    def do_waiting_less55s(self):
        if self.observation['time']['cur_step']< 55:
           return self.action_waiting
        return []
    def do_moveon_0_q82_3945(self):
        if self.observation['time']['cur_step'] > 1800:
            self.func_done = True
            return []
        return []
#q81
    def set_func_list_q8_1(self):
        #

        #

        self.moving_func_list[(100, 3035, None)] = [self.do_get_off_safe]
        self.moving_func_list[(200, None, None)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(400, 2231, None)] = [self.do_hide]
        self.moving_func_list[(200, None, 0)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(1200, None, 0)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(1200, None, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(2200, None, 0)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(3200, None, 0)] = [self.do_stop_to_shoot_cars]

        self.moving_func_list[(200, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(1200, None, 2)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(2200, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(3200, None, 1)] = [self.do_movearound_soilder_protect_city]
        #

        self.moving_func_list[(100, 1732, 0)] = [self.do_get_off_0]
        self.moving_func_list[(1100, 2039, 0)] = [self.do_get_off_0]
        self.moving_func_list[(2100, 2348, 0)] = [self.do_get_off_0]
        self.moving_func_list[(3100, 1853, 0)] = [self.do_get_off_0]

        self.moving_func_list[(200, 1732, None)] = [self.do_get_on_red_0_1]
        self.moving_func_list[(1200, 2039, None)] = [self.do_get_on_red_0_1]
        self.moving_func_list[(2200, 2348, None)] = [self.do_get_on_red_0_1]
        self.moving_func_list[(3200, 1853, None)] = [self.do_get_on_red_0_1]

        self.moving_func_list[(1200, 4246, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(2200, 4246, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(3200, 4246, None)] = [self.do_set_finish_flag]

        self.moving_func_list[(100, 2631, None)] = [self.do_get_off_safe]
        self.moving_func_list[(1100, 2437, None)] = [self.do_get_off_safe]
        self.moving_func_list[(2100, 2846, None)] = [self.do_get_off_safe, self.do_waiting_3100_q8_1]
        self.moving_func_list[(3100, 2653, None)] = [self.do_get_off_safe, self.do_waiting_3100_q8_1]
        #

        #
        #
        #

        #
        #
        #

        #
        #
        #
        #
        #
        self.moving_func_list[(0, 3445, 1)] = [self.do_changepath_10]
        self.moving_func_list[(1000, 3445, 1)] = [self.do_changepath_10]
        self.moving_func_list[(2000, 3445, 1)] = [self.do_changepath_10]
        self.moving_func_list[(3000, 3445, 1)] = [self.do_changepath_10]

        self.moving_func_list[(0, 3647, 13)] = [self.do_waiting_redtank_q81_3647,self.do_tank_goback]
        self.moving_func_list[(1000, 3647, 13)] = [self.do_waiting_redtank_q81_3647,self.do_tank_goback]
        self.moving_func_list[(2000, 3647, 13)] = [self.do_waiting_redtank_q81_3647,self.do_tank_goback]
        self.moving_func_list[(3000, 3647, 13)] = [self.do_waiting_redtank_q81_3647,self.do_tank_goback]

        self.moving_func_list[(0, 3648, 13)] = [self.do_waiting_redtank_q81_3648,self.do_tank_goback]
        self.moving_func_list[(1000, 3648, 13)] = [self.do_waiting_redtank_q81_3648,self.do_tank_goback]
        self.moving_func_list[(2000, 3648, 13)] = [self.do_waiting_redtank_q81_3648,self.do_tank_goback]
        self.moving_func_list[(3000, 3648, 13)] = [self.do_waiting_redtank_q81_3648,self.do_tank_goback]

        self.moving_func_list[(0, 3938, 18)] = [self.do_waiting_0_s81_3938]
        self.moving_func_list[(1000, 3938, 18)] = [self.do_waiting_0_s81_3938]
        self.moving_func_list[(2000, 3938, 18)] = [self.do_waiting_0_s81_3938]
        self.moving_func_list[(3000, 3938, 18)] = [self.do_waiting_0_s81_3938]

        #
        #
        #
        self.moving_func_list[(4600, 4137, None)] = [self.do_waiting_whenhasc3]
        self.moving_func_list[(4601, 4146, None)] = [self.do_waiting_whenhasc3]
        #

        #
        #
        #
        #
        #
        #
        #
        self.moving_func_list[(4500, 4045, None)] = [self.do_waiting_4500_q8_1]
        self.moving_func_list[(4501, 4049, None)] = [self.do_waiting_4500_q8_1]

        self.moving_func_list[(4500, 5249, None)] = [ self.do_set_finish_flag]
        self.moving_func_list[(4501, 5241, None)] = [ self.do_set_finish_flag]


        self.moving_func_list[(700, None, None)] = [self.do_set_flg_whenseecar_missile]
        self.moving_func_list[(1700, None, None)] = [self.do_set_flg_whenseecar_missile]
        self.moving_func_list[(2700, None, None)] = [self.do_set_flg_whenseecar_missile]
        self.moving_func_list[(3700, None, None)] = [self.do_set_flg_whenseecar_missile]

        self.moving_func_list[(701, None, 0)] = [self.do_set_notattackflg_missile]

        #
        self.moving_func_list[(5300, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5301, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5302, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5303, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5304, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5305, None, None)] = [self.do_set_finish_flag]

        self.moving_func_list[(11100, 4646, None)] = [self.do_get_off_safe]
        self.moving_func_list[(11101, 4646, None)] = [self.do_get_off_safe]
        self.moving_func_list[(12100, 4648, None)] = [self.do_get_off_safe]
        self.moving_func_list[(12101, 4648, None)] = [self.do_get_off_safe]
        self.moving_func_list[(13100, 4549, None)] = [self.do_get_off_safe]
        self.moving_func_list[(13101, 4549, None)] = [self.do_get_off_safe]

        self.moving_func_list[(10100, 4641, 1)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(10101, 4641, 1)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(11100, 4641, 7)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(11101, 4641, 7)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(12100, 4247, 3)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(12101, 4247, 3)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(13100, 4247, 2)] = [self.do_blue_car_hide_1800s_qs1_ls]
        self.moving_func_list[(13101, 4247, 2)] = [self.do_blue_car_hide_1800s_qs1_ls]

        #
        #
        #
        self.moving_func_list[(11200, 6546, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(11201, 6647, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(12200, 5551, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(12201, 5652, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(13200, 5555, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(13201, 5656, None)] = [self.do_get_on_blue_0]

        #
        self.moving_func_list[(10200, None, 1)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]
        self.moving_func_list[(10200, None, 11)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                    self.do_movearound_soilder_protect_city]

        self.moving_func_list[(10201, None, 1)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]

        self.moving_func_list[(11200, None, 1)] = [self.do_blue_soilder_10200_continue_3939_qs1_ls,
                                                   self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]
        self.moving_func_list[(11200, None, 11)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                    self.do_movearound_soilder_protect_city]

        self.moving_func_list[(11201, None, 2)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]
        self.moving_func_list[(11201, None, 11)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                    self.do_movearound_soilder_protect_city]

        self.moving_func_list[(12200, None, 4)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]
        self.moving_func_list[(12201, None, 4)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]
        self.moving_func_list[(13200, None, 5)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]
        self.moving_func_list[(13201, None, 5)] = [self.do_blue_soilder_charge_occupy_qs1_ls,
                                                   self.do_movearound_soilder_protect_city]

        self.moving_func_list[(10200, None, 0)] = [self.do_blue_soilder_10200_replace_defense_qs1_ls]
        self.moving_func_list[(11201, None, 0)] = [self.do_blue_soilder_11201_replace_defense_qs1_ls]
        self.moving_func_list[(11201, None, 1)] = [self.do_blue_soilder_11201_replace_defense_qs1_ls]

        self.moving_func_list[(10000, 3846, 9)] = [self.do_tank_goback]
        self.moving_func_list[(10001, 3846, 9)] = [self.do_tank_goback]
        self.moving_func_list[(11000, 3846, 6)] = [self.do_tank_goback]
        self.moving_func_list[(11001, 3846, 6)] = [self.do_tank_goback]
        self.moving_func_list[(12000, 3846, 6)] = [self.do_tank_goback]
        self.moving_func_list[(12001, 3846, 6)] = [self.do_tank_goback]
        self.moving_func_list[(13000, 3846, 6)] = [self.do_tank_goback]
        self.moving_func_list[(13001, 3846, 6)] = [self.do_tank_goback]

        self.moving_func_list[(10000, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(10001, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(11000, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(11001, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(12000, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(12001, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(13000, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]
        self.moving_func_list[(13001, None, None)] = [  #
            self.do_blue_tank_charge_occupy_qs1_ls]

        #
        self.moving_func_list[(15300, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(15301, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(15302, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(15303, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(15304, None, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(15305, None, None)] = [self.do_set_finish_flag]
        #
        self.moving_func_list[(14600, 4042, None)] = [self.do_waiting_whenhasc3]
        self.moving_func_list[(14601, 4050, None)] = [self.do_waiting_whenhasc3]
        #
        self.moving_func_list[(14500, 2759, 4)] = [self.do_blue_autoplane_patrol_qs1_ls]
        self.moving_func_list[(14501, 3639, 9)] = [self.do_blue_autoplane_patrol_qs1_ls]

    #
#蓝方：

    def do_tank_around_back_kill_car(self):
        if self.observation['time']['cur_step'] > 1400:
            msg = self.do_free_kill_car_blue_q81()
            if len(msg) > 0:
                self.func_done = True
                return msg
        return []

    def do_free_kill_car_blue_q81(self):
        enemy_id_set = set()
        for id in range(10000, 14000, 1000):
            blue_tk1 = self.situation.get_cur_opt_by_id(id)
            if blue_tk1 is not None:
                tmp_id_set = set(blue_tk1['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set
            blue_tk2 = self.situation.get_cur_opt_by_id(id + 1)
            if blue_tk2 is not None:
                tmp_id_set = set(blue_tk2['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set

        for id in range(14500, 14700, 100):
            air1 = self.situation.get_cur_opt_by_id(id)
            if air1 is not None:
                tmp_id_set = set(air1['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set
            air2 = self.situation.get_cur_opt_by_id(id + 1)
            if air2 is not None:
                tmp_id_set = set(air2['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set

        for id in enemy_id_set:
            enemy_opt = self.situation.get_cur_opt_by_id(id)
            if enemy_opt is None:
                continue
            if enemy_opt['sub_type'] == CAR:
                return self.do_move_to_point(enemy_opt['cur_hex'])

        c_list = list(self.situation.enemy_history.values())

        sort_list = []
        for tmp_tuple in c_list:
            tmp_list = list(tmp_tuple)
            dis = self.map.get_distance(tmp_list[0]['cur_hex'], self.operator['cur_hex'])
            tmp_list.append(dis)
            sort_list.append(tmp_list)

        sort_list = sorted(sort_list, key=lambda x: (x[4] * -1, int(x[1]), x[0]['obj_id']), reverse=True)
        #

        for history in sort_list:
            opt = history[0]
            if (opt['sub_type'] == CAR) and \
                    history[2] is False and \
                    history[3] is False:
                #

                #
                return self.do_move_to_point(opt['cur_hex'])
        return []

    def do_blue_autoplane_patrol_qs1_ls(self):
        self.move_step = 0
        return []

    def do_carstopandgetoff_whenseetank(self):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if each_enemy[0]['sub_type'] == TANK:
                    if each_enemy[0]['cur_hex'] > 4540:
                        return self.do_get_off_safe()
        self.func_done = True
        return []

    def do_blue_soilder_10200_continue_3837_qs1_ls(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 1) == False:
            self.func_done = True
            self.move_step = 20
            return []
        return []

    def do_blue_soilder_10200_continue_3939_qs1_ls(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 1) == False:
            self.func_done = True
            self.move_step = 10
            return []
        return []

    def do_blue_car_hide_1800s_qs1_ls(self):
        if self.operator['passenger_ids'] == []:
            if self.observation['time']['cur_step'] < 2000:
                return self.do_hide()
        return []

    def do_waiting_bluetank_move_30s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 30:
            return []
        return self.action_waiting

    def do_waiting_blue_car_move_1400s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 1400:
            return []
        return self.action_waiting

    def do_waiting_blue_car_move_1000s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 1000:
            return []
        return self.action_waiting

    def do_waiting_bluetank_move_75s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 75:
            return []
        return self.action_waiting

    def do_waiting_bluetank_move_120s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 120:
            return []
        return self.action_waiting

    def do_waiting_bluetank_move_40s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 40:
            return []
        return self.action_waiting

    def do_waiting_bluetank_move_1050s_qs1_ls(self):
        if self.observation['time']['cur_step'] > 1050:
            return []
        self.move_step = self.move_step - 2
        return []

    def do_waiting_whenhasc3(self):
        if self.operator['C3'] > 0:
            return self.action_waiting
        return []

    def do_waiting_bluetank_wait_for_car_qs1_ls(self):
        my_car = self.situation.get_cur_opt_by_id(self.operator['obj_id'] + 100)
        my_soilder = self.situation.get_cur_opt_by_id(self.operator['obj_id'] + 200)
        if my_car == None:
            return []
        elif my_soilder != None:
            return []
        if self.observation['time']['cur_step'] > 1200:
            return []
        self.move_step = self.move_step - 2
        return []

    def do_movetoenemycar_in_10_bluetank_s81(self):
        if self.is_has_enemyhis_in_distance(self.operator['cur_hex'], [CAR], -1, 10, 200):
            return self.do_move_to_enemy_car_blue_tank()
        return []

    def do_move_to_enemy_car_blue_tank(self):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if each_enemy[1] > -self.observation['time']['cur_step'] + 1:
                    if each_enemy[0]['sub_type'] == CAR:
                        self.auto_moving = True
                        return self.do_move_to_point(each_enemy[0]['cur_hex'])
        self.auto_moving = False
        return []

    def do_blue_soilder_charge_occupy_qs1_ls(self):
        if self.observation['time']['cur_step'] > 2600:
            for city in self.observation['cities']:
                if city['flag'] != self.color:
                    dis = self.map.get_distance(city['coord'], self.operator['cur_hex'])
                    if dis == 0:
                        return self.action_waiting
                    elif dis == 1:
                        return self.do_move_to_point(city['coord'])
        return []

    def do_waiting_bluecar_wait_for_soilder_12_steps_qs1_ls(self):
        my_soilder = self.situation.get_cur_opt_by_id(self.operator['obj_id'] + 100)
        if my_soilder != None:
            dis = self.map.get_distance(my_soilder['cur_hex'], self.operator['cur_hex'])
            if dis >= 12:
                return []
            else:
                return self.action_waiting
        return []

    def do_waiting_bluecar_wait_for_soilder_6_steps_qs1_ls(self):
        my_soilder = self.situation.get_cur_opt_by_id(self.operator['obj_id'] + 100)
        if my_soilder != None:
            dis = self.map.get_distance(my_soilder['cur_hex'], self.operator['cur_hex'])
            if dis >= 6:
                return []
            else:
                return self.action_waiting
        return []

    def do_blue_tank_charge_occupy_qs1_ls(self):
        if self.observation['time']['cur_step'] > 2000:
            for city in self.observation['cities']:
                if city['coord'] == 3947:
                    if city['flag'] != self.color:
                        self.auto_moving = True
                        self.func_done = True
                        return self.do_move_to_point(city['coord'])
                    break
            for city in self.observation['cities']:
                if city['coord'] == 4246:
                    if city['flag'] != self.color:
                        self.auto_moving = True
                        self.func_done = True
                        return self.do_move_to_point(city['coord'])
                    break
            for city in self.observation['cities']:
                if city['coord'] == 4540:
                    if city['flag'] != self.color:
                        self.auto_moving = True
                        self.func_done = True
                        return self.do_move_to_point(city['coord'])
                    break
            for city in self.observation['cities']:
                if city['coord'] == 3747:
                    if city['flag'] != self.color:
                        self.auto_moving = True
                        self.func_done = True
                        return self.do_move_to_point(city['coord'])
                    break
            for city in self.observation['cities']:
                if city['coord'] == 3939:
                    if city['flag'] != self.color:
                        self.auto_moving = True
                        self.func_done = True
                        return self.do_move_to_point(city['coord'])
                    break
        return []

    def do_blue_soilder_10200_replace_defense_qs1_ls(self):
        soilder_10201 = self.situation.get_cur_opt_by_id(10201)  #
        if soilder_10201 == None:
            self.move_step = 10  #
            return []
        return []

    def do_blue_soilder_11201_replace_defense_qs1_ls(self):
        soilder_10200 = self.situation.get_cur_opt_by_id(10200)
        soilder_10201 = self.situation.get_cur_opt_by_id(10201)
        if soilder_10201 == None and soilder_10200 == None:
            self.move_step = 10  #
            return []
        return []

    def do_blue_car_move_with_soilder(self):
        if self.operator['passenger_ids'] == []:
            return self.action_waiting
        return []

    def do_waiting_bluecar_hide(self):
        if self.observation['time']['cur_step'] > 550:
            return self.action_waiting
        if self.operator['stop'] != 1:
            return self.action_waiting
        if self.operator['move_state'] == Hide:
            return self.action_waiting
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = ActionType.ChangeState
        cure_action.target_state = Hide
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True:
            return self.get_retmsg(cure_action)
        return self.action_waiting

#红方：
    def do_waiting_redtank_q81_3648(self):
        if self.is_has_enemyhis_in_distance(3747 , ALL_OPT_1 , -1 , 1 , 300):
            return []
        self.func_done = True
        return []
    def do_waiting_0_s81_3938(self):
        if self.observation['time']['cur_step'] < 2400:
            self.func_done = True
            self.move_step = 15
            return []
        if self.observation['time']['cur_step'] < 2550:
            if self.observation['cities'][0]['flag'] != self.color or \
                    self.observation['cities'][5]['flag'] != self.color:
                self.func_done = True
                self.move_step = 15
                return []
        if self.observation['time']['cur_step'] < 2750:
            if (self.observation['scores']['red_total'] - self.observation['scores']['blue_total'] < 120) and \
                    (self.observation['scores']['red_total'] > self.observation['scores']['blue_total']):
                self.func_done = True
                self.move_step = 15
                return []
        self.do_set_finish_flag()
        return []
    def do_waiting_redtank_q81_3647(self):
        if self.observation['time']['cur_step'] > 1700:
            self.func_done = True
            return []
        return []
        if 3647 in self.situation.want_to_move_pos:
            return []
        return self.action_waiting
    def do_changepath_10(self):
        self.move_step = 10
        return []
    def do_waiting_redtank_q81_3648(self):

        if self.observation['cities'][4]['flag'] != self.color:
            if self.observation['time']['cur_step'] > 2150:
                if self.observation['cities'][0]['flag'] != self.color or \
                        self.observation['cities'][3]['flag'] != self.color or \
                        self.observation['cities'][5]['flag'] != self.color:
                    self.func_done = True
                    return []
            if self.is_has_enemyhis_in_distance(3747, ALL_OPT_1, -1, 1, 300):
                return []
        self.func_done = True
        return []
    def do_waiting_whenhasc3(self):
        if self.operator['C3'] > 0:
            return self.action_waiting
        return []
    def do_set_flg_whenseecar_missile(self):
        if self.is_has_enemy_in_distance(self.operator['cur_hex'], [CAR], -1, 20):
            self.first_missile = False
        return []
    def do_set_notattackflg_missile(self):
        self.first_missile = True
        return []
    def do_waiting_4500_q8_1(self):
        if self.is_has_enemy_in_distance(self.operator['cur_hex'] , [CAR],-1 , 1):
            return self.action_waiting
        if self.situation.cur_step > 900:
            return []
        if self.is_has_enemy_in_distance(self.operator['cur_hex'] , [SOILDER],-1 , 2):
            return []
        return self.action_waiting

    def do_waiting_3100_q8_1(self):
        if self.situation.cur_step < 600:
            return self.action_waiting
        return []
    def add_battle(self):

        if len(self.operator['passenger_ids']) > 0:
            return []

        xy_3737_flag = self.observation['cities'][4]['flag']
        xy_3947_flag = self.observation['cities'][1]['flag']
        xy_4246_flag = self.observation['cities'][2]['flag']

        xy = self.operator['cur_hex']
        enemy_ids = self.operator['see_enemy_bop_ids']

        #
        #
        #

        if xy_3737_flag != BLUE and self.is_has_myopt_in([3747]) and self.move_step < 10:
            self.move_step = 10
            return []
        elif self.move_step >= 10 and self.move_step < 20:
            if self.is_has_myopt_in([3947, 3946, 3948]) and xy_3737_flag == BLUE:
                self.move_step = 20
                return []
        #
        #
        #
        #
        elif xy_4246_flag != BLUE and self.is_has_myopt_in([4247]):
            self.move_step = 30
            return []
        #
        #

        #
        #
        return []

    def get_sets_len(self, set1, set2):
        res_set = set1 & set2
        return len(res_set)

    def get_solier_xy(self):
        solier_list = [1200, 2200, 3200]
        res_list = []
        for solier_id in solier_list:
            solier_opt = self.situation.get_cur_opt_by_id(solier_id)
            if solier_opt is not None:
                res_list.append(solier_opt['cur_hex'])
        return res_list

    def do_free_kill_car(self):

        #
        #
        #
        #

        enemy_id_set = set()
        for id in range(1000, 4000, 1000):
            red_tk = self.situation.get_cur_opt_by_id(id)
            if red_tk is not None:
                tmp_id_set = set(red_tk['see_enemy_bop_ids'])
                enemy_id_set |= tmp_id_set

        #
        #
        #
        #

        #

        free_list = self.get_free_list(self.move_step)
        if len(free_list) == 0:
            return []

        xy = self.operator['cur_hex']
        if xy in free_list:
            free_list.remove(xy)
        import random as rd
        return self.do_move_to_point(free_list[rd.randint(0, len(free_list) - 1)])

    def get_free_list(self, step):
        if self.move_step == 0 or \
                (self.move_step >= 10):
            return []
        print(" ", self.move_step)
        #
        #

        if self.is_has_myopt_in([3747]) is False:
            return [3445, 3446, 3545]

        #
        #
        #
        else:
            self.move_step = 10
        #
        #
        #
        #
        #
        #
        #
        #

    def set_func_list_q32(self):
        #
        self.moving_func_list[(100, 1417, None)] = [self.do_get_off_0]
        self.moving_func_list[(100, 1311, None)] = [self.do_waiting_100_q32_1311]
        self.moving_func_list[(100, 2221, None)] = [self.do_set_point]
        self.moving_func_list[(100, 3026, None)] = [self.do_get_off_safe]

        self.moving_func_list[(1100, 1616, None)] = [self.do_get_off_0]
        self.moving_func_list[(1100, 1412, None)] = [self.do_waiting_100_q32_1311]
        self.moving_func_list[(1100, 2221, None)] = [self.do_set_point]
        #
        #
        self.moving_func_list[(1100, 3025, None)] = [self.do_get_off_safe]

        self.moving_func_list[(2100, 1816, None)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                     self.do_waiting_2100_q32_1816]
        self.moving_func_list[(2100, 2219, None)] = [self.do_set_point, self.do_get_off_safe, self.do_stop_to_shoot,
                                                     self.do_waiting_2100_q32_2219]

        self.moving_func_list[(2100, 3020, None)] = [self.do_waiting_2100_q32_3020, self.do_get_off_safe,
                                                     self.do_waiting]
        self.moving_func_list[(2100, 3120, None)] = [self.do_waiting_2100_q32_3120, self.do_get_off_safe,
                                                     self.do_waiting]
        self.moving_func_list[(2100, 3221, None)] = [self.do_get_off_safe]

        self.moving_func_list[(3100, 1914, None)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                     self.do_waiting_2100_q32_1816]
        #
        self.moving_func_list[(3100, 2319, None)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                     self.do_waiting_2100_q32_2219]
        self.moving_func_list[(3100, 2219, None)] = [self.do_set_point]
        self.moving_func_list[(3100, 3020, None)] = [self.do_waiting_2100_q32_3020, self.do_get_off_safe,
                                                     self.do_waiting]
        self.moving_func_list[(3100, 3120, None)] = [self.do_waiting_2100_q32_3120, self.do_get_off_safe,
                                                     self.do_waiting]
        self.moving_func_list[(3100, 3221, None)] = [self.do_get_off_safe]

        #
        #
        self.moving_func_list[(200, 1417, None)] = [self.do_get_on_red_0_1]
        #
        self.moving_func_list[(200, 2125, None)] = [self.do_set_point]
        self.moving_func_list[(200, None, 3)] = [self.do_move_to_city_six_has_enemysoilder]

        #
        self.moving_func_list[(1200, 3125, None)] = [self.do_set_point]
        self.moving_func_list[(1200, 2125, None)] = [self.do_set_point]
        self.moving_func_list[(1200, 1616, None)] = [self.do_get_on_red_0_1]
        #
        #
        #
        #
        self.moving_func_list[(2200, None, 8)] = [self.do_move_to_city_six_has_enemysoilder]
        self.moving_func_list[(2200, 3630, None)] = [self.do_waiting_for_occupy_city, self.do_stop_to_shoot_cars]
        self.moving_func_list[(2200, 3829, None)] = [self.do_waiting_for_occupy_city, self.do_stop_to_shoot_cars]
        self.moving_func_list[(3200, 3630, None)] = [self.do_waiting_for_occupy_city, self.do_stop_to_shoot_cars]
        self.moving_func_list[(3200, 3829, None)] = [self.do_waiting_for_occupy_city, self.do_stop_to_shoot_cars]
        #
        self.moving_func_list[(0, 2422, None)] = [self.do_waiting_redtank_q32_1]
        self.moving_func_list[(0, 2924, None)] = [self.do_waiting_redtank_q32_2]
        self.moving_func_list[(0, 3833, None)] = [self.do_red_final_occupy_q32]
        self.moving_func_list[(0, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #

        self.moving_func_list[(1000, 2125, None)] = [self.do_waiting_redtank_q32_1]
        self.moving_func_list[(1000, 2825, None)] = [self.do_waiting_redtank_q32_2, self.do_waiting_1000_q32_2825]
        self.moving_func_list[(1000, 3731, None)] = [self.do_waiting_redtank_q32_2, self.do_waiting_1000_q32_2924]

        self.moving_func_list[(1000, 2925, None)] = [self.do_waiting_redtank_q32_2]
        self.moving_func_list[(1000, 3834, None)] = [self.do_red_final_occupy_q32]
        self.moving_func_list[(1000, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #

        self.moving_func_list[(2000, 2621, None)] = [self.do_waiting_redtank_q32_1]
        self.moving_func_list[(2000, 2925, None)] = [self.do_waiting_redtank_q32_2]
        self.moving_func_list[(2000, 3733, None)] = [self.do_red_final_occupy_q32]
        self.moving_func_list[(2000, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #

        self.moving_func_list[(3000, 2323, None)] = [self.do_waiting_redtank_q32_1]
        self.moving_func_list[(3000, 2825, None)] = [self.do_waiting_redtank_q32_2]
        self.moving_func_list[(3000, 3732, None)] = [self.do_red_final_occupy_q32]
        self.moving_func_list[(3000, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #
        self.moving_func_list[(5300, 2613, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5301, 2614, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5302, 2711, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5303, 2712, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5304, 2813, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(5305, 2814, None)] = [self.do_set_finish_flag]
        #
        self.moving_func_list[(400, 2022, None)] = [self.do_stop_to_guild, self.do_stop_to_shoot,
                                                    self.do_waiting_red_autocar_1]
        self.moving_func_list[(400, 2326, None)] = [self.do_waiting_400_q32_2]
        #
        self.moving_func_list[(400, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #
        self.moving_func_list[(1400, 2321, None)] = [self.do_stop_to_guild, self.do_stop_to_shoot,
                                                     self.do_waiting_red_autocar_1]
        self.moving_func_list[(1400, 2426, None)] = [self.do_waiting_400_q32_2]
        #
        self.moving_func_list[(1400, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #
        self.moving_func_list[(2400, 2218, None)] = [self.do_stop_to_guild, self.do_stop_to_shoot,
                                                     self.do_waiting_red_autocar_1]
        self.moving_func_list[(2400, 2526, None)] = [self.do_waiting_400_q32_2]
        #
        self.moving_func_list[(2400, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #
        self.moving_func_list[(3400, 2316, None)] = [self.do_stop_to_guild, self.do_stop_to_shoot,
                                                     self.do_waiting_red_autocar_1]
        self.moving_func_list[(3400, 2524, None)] = [self.do_waiting_400_q32_2]
        #
        self.moving_func_list[(3400, 3124, None)] = [self.do_waiting_no_stack_q32_3124]
        #
        #
        self.moving_func_list[(4600, None, None)] = [self.do_set_finish_flag_see_car18_q32]
        self.moving_func_list[(4601, None, None)] = [self.do_set_finish_flag_see_car18_q32]
        self.moving_func_list[(4600, 2564, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(4601, 2320, None)] = [self.do_set_finish_flag]
        #
        #
        #
        self.moving_func_list[(4500, 2431, None)] = [self.do_waiting_4500_q32_2928]
        self.moving_func_list[(4501, 3023, None)] = [self.do_waiting_4500_q32_2928]
        self.moving_func_list[(4500, 1845, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(4501, 4442, None)] = [self.do_set_finish_flag]

        self.moving_func_list[(700, 2838, None)] = [self.do_tank_goback]
        #
        self.moving_func_list[(10100, 2436, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(10101, 2535, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(11100, 2736, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(11101, 3137, None)] = [self.do_set_finish_flag]

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #

        #
        self.moving_func_list[(10200, 2034, None)] = [self.do_bluesoilder_10200_10201_back_defense]
        self.moving_func_list[(10201, 2331, None)] = [self.do_bluesoilder_10200_10201_back_defense]
        #
        self.moving_func_list[(10200, None, 2)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(10201, None, 2)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(11200, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(11201, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(12200, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(12201, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(13200, None, 1)] = [self.do_movearound_soilder_protect_city]
        self.moving_func_list[(13201, None, 1)] = [self.do_movearound_soilder_protect_city]
        #
        #
        #
        #
        #
        #
        #

        self.moving_func_list[(10200, 2034, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, 2330, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(11200, 2442, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(11201, 2530, 1)] = [self.do_stop_to_shoot_cars]

        self.moving_func_list[(12200, 3228, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(12201, 2831, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(13200, 3630, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(13201, 2431, 1)] = [self.do_stop_to_shoot_cars]
        #
        #
        #
        #

        self.moving_func_list[(10000, 2330, None)] = [self.do_blue_tank_not_fire_go_back]
        self.moving_func_list[(11000, 2430, None)] = [self.do_blue_tank_not_fire_go_back]
        self.moving_func_list[(12000, 2530, None)] = [self.do_blue_tank_not_fire_go_back]
        self.moving_func_list[(13000, 2736, None)] = [self.do_blue_tank_not_fire_go_back]

        #
        #
        #
        #

        #
        #
        #
        #
        #
        #
        #
        self.moving_func_list[(15300, 4442, 1)] = [self.do_set_finish_flag]
        self.moving_func_list[(15301, 4443, 1)] = [self.do_set_finish_flag]
        self.moving_func_list[(15302, 4540, 1)] = [self.do_set_finish_flag]
        self.moving_func_list[(15303, 4541, 1)] = [self.do_set_finish_flag]
        self.moving_func_list[(15304, 4542, 1)] = [self.do_set_finish_flag]
        self.moving_func_list[(15305, 4543, 1)] = [self.do_set_finish_flag]
        #
        #
        #

        self.moving_func_list[(14600, 3119, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(14601, 2230, None)] = [self.do_set_finish_flag]
        #
        #
        #
        self.moving_func_list[(14500, 1713, None)] = [self.do_set_finish_flag]
        self.moving_func_list[(14501, 1414, None)] = [self.do_set_finish_flag]

    #
    def is_has_enemy_in(self, pos_list, type_list):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                enemy_opt = each_enemy[0]
                if enemy_opt['sub_type'] in type_list:

                    if enemy_opt['cur_hex'] in pos_list:
                        return True
        return False

    def is_has_cansee_enemyhis_in_distance(self, pos, type_list, distance_min, distance_max, time):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if not each_enemy[3]:
                    if each_enemy[1] > -time:
                        enemy_opt = each_enemy[0]
                        if self.situation.map.can_see(enemy_opt['cur_hex'], pos, 0):
                            if enemy_opt['sub_type'] in type_list:
                                dis = self.situation.map.get_distance(enemy_opt['cur_hex'], pos)
                                if dis <= distance_max and dis >= distance_min:
                                    return True
        return False

    def is_has_enemyhis_in_distance(self, pos, type_list, distance_min, distance_max, time):
        for each_enemy in self.situation.enemy_history.values():
            if not each_enemy[2]:
                if not each_enemy[3]:
                    if each_enemy[1] > -time:
                        enemy_opt = each_enemy[0]
                        if enemy_opt['sub_type'] in type_list:
                            dis = self.situation.map.get_distance(enemy_opt['cur_hex'], pos)
                            if dis <= distance_max and dis >= distance_min:
                                return True
        return False

    def do_move_to_city_six_has_enemysoilder(self):
        if self.is_has_enemy_in([self.operator['cur_hex']], [SOILDER]):
            return self.action_waiting
        pos = my_ai.plan_pos_list[self.operator['obj_id']][self.move_step - 1]
        big_six = self.myLandTool.get_big_six(pos, 1)
        #
        #
        self.auto_moving = True
        for each_enemy in self.situation.enemy_operators:
            if each_enemy['sub_type'] == SOILDER:
                if each_enemy['cur_hex'] in big_six:
                    #
                    return self.do_move_to_point(each_enemy['cur_hex'])
        self.move_step = self.move_step - 1
        self.auto_moving = False
        return []

    def do_waiting_no_stack_q32_3124(self):
        if 3225 in self.situation.want_to_move_pos:
            return self.action_waiting
        return []

    def do_autocar_shoot_q32(self):
        if self.operator['C3'] == 0:
            if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 3):
                return self.action_waiting
        else:
            if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], ALL_OPT_1, -1, 10):
                return self.action_waiting
        return []

    def do_waiting_400_q32_2(self):
        if self.observation['time']['cur_step'] > 1800:
            return []
        return self.action_waiting

    def do_waiting_redtank_q32_2(self):
        if self.observation['time']['cur_step'] > 1900:
            return []
        return self.action_waiting

    def do_waiting_red_autocar_1(self):
        if 2219 in self.situation.clean_pos_list:
            return []
        car1 = self.situation.get_cur_opt_by_id(2100)
        car2 = self.situation.get_cur_opt_by_id(3100)
        if car1 is None and car2 is None:
            return []
        return self.action_waiting

    def do_waiting_redtank_q32_1(self):
        if 2221 in self.situation.clean_pos_list:
            return []
        car1 = self.situation.get_cur_opt_by_id(100)
        car2 = self.situation.get_cur_opt_by_id(1100)
        if car1 is None and car2 is None:
            return []
        if self.observation['time']['cur_step'] > 1200:
            return []
        return self.action_waiting

    def do_waiting_100_q32_1311(self):
        if self.observation['time']['cur_step'] > 460:
            return []
        return self.action_waiting

    def do_red_final_occupy_q32(self):
        if self.observation['time']['cur_step'] > 2300:
            self.do_set_finish_flag()
            self.func_done = True
            return []
        return []

    def do_waiting_4500_q32_2928(self):
        if self.observation['time']['cur_step'] > 600:
            return []
        return self.action_waiting

    def do_waiting_for_occupy_city(self):
        for each_city in self.observation['cities']:
            if self.operator['cur_hex'] == each_city['coord']:
                if each_city['flag'] != self.color:
                    return self.action_waiting
                break
        return []

    def do_waiting_2100_q32_2219(self):
        if self.observation['time']['cur_step'] > 1100:
            return []
        return self.action_waiting

    def do_waiting_2100_q32_1816(self):
        if self.is_has_enemy_in_distance(self.operator['cur_hex'], CARS, -1, 20):
            return []
        return self.action_waiting

    def do_waiting_100_q32_2214(self):
        if self.observation['time']['cur_step'] > 460:
            return []
        return self.action_waiting

    def do_move_1100_q32_1(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [HELICOPTER], -1, 10):
            return []
        self.func_done = True
        return []

    def do_waiting_2100_q32_3020(self):
        if 3120 in self.situation.stack_pos_list:
            return []
        self.func_done = True
        return []

    def do_waiting_2100_q32_3120(self):
        if 3221 in self.situation.stack_pos_list:
            return []
        self.func_done = True
        return []

    def do_waiting_whenwillstack(self):
        if len(self.movepath) > 0:
            if self.movepath[0] in self.situation.want_to_move_pos:
                return self.action_waiting
            if self.is_has_my_unmove_opt_in(CARS + [SOILDER], [self.movepath[0]]):
                return self.action_waiting
        else:
            return []
        return []

    def is_has_my_unmove_opt_in(self, type_list, pos_list):
        for each in self.situation.our_opt:
            if each.operator['sub_type'] in type_list:
                if each.operator['cur_hex'] in pos_list:
                    if each.operator['cur_pos'] == 0 or each.operator['cur_pos'] == 1:
                        #
                        return True
        return False

    def do_waiting_1000_q32_2825(self):
        if (not self.is_has_myopt_in([2924])) or (not self.is_has_myopt_in([2925])):
            return []
        return self.action_waiting

    def do_waiting_1000_q32_2924(self):
        if not self.is_has_myopt_in([2925]):
            return []
        return self.action_waiting

    def do_waiting_redcar_move_to_second_pos_q32_1(self):
        if self.situation.is_air_defense_safe(self.observation) == True:
            return []
        my_soilder = self.situation.get_cur_opt_by_id(self.operator['obj_id'] + 100)
        if my_soilder:
            if self.map.get_distance(my_soilder['cur_hex'], self.operator['cur_hex']) > 12:
                return []
        return self.action_waiting

    def do_waiting_bluecar_move_to_second_pos_q32_1(self):
        #
        for see_enemy_bop_id in self.operator['see_enemy_bop_ids']:
            if see_enemy_bop_id == 4600 or see_enemy_bop_id == 4601:
                continue
            else:
                see_enemy_bop = self.situation.get_cur_opt_by_id(see_enemy_bop_id)
                if see_enemy_bop:
                    if self.map.get_distance(see_enemy_bop['cur_hex'],
                                             self.operator['cur_hex']) < 20:
                        return self.action_waiting
        my_soilder = self.situation.get_cur_opt_by_id(self.operator['obj_id'] + 100)
        if my_soilder:
            if self.map.get_distance(my_soilder['cur_hex'],
                                     self.operator['cur_hex']) > 3:
                return []
        else:
            if self.observation['time']['cur_step'] >= 600:
                return []
        return self.action_waiting

    def do_waiting_bluesoilder_move_continue(self):
        for see_enemy_bop_id in self.operator['see_enemy_bop_ids']:
            see_enemy_bop = self.situation.get_cur_opt_by_id(see_enemy_bop_id)
            if see_enemy_bop:
                if self.map.get_distance(see_enemy_bop['cur_hex'],
                                         self.operator['cur_hex']) < 10:
                    return self.action_waiting
        return []

    def do_movetocity_redtank_q32(self):
        if self.observation['time']['cur_step'] > 2000:
            self.func_done = True
            return []
        return []

    def do_waitat2514_redtank_q32(self):
        if self.operator['C3'] > 0:
            return self.action_waiting
        return []

    def do_set_finish_flag(self):
        self.is_in_new_function = False
        return []

    def do_set_finish_flag_see_car18_q32(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [CAR], -1, 18):
            self.is_in_new_function = False
        return []

    def do_tank_goback_waitcd_20(self):
        if self.operator['weapon_cool_time'] > 20:
            return self.action_waiting
        self.move_step = self.move_step - 2
        return []

    def do_tank_goback_waitcd_40(self):
        if self.operator['weapon_cool_time'] > 40:
            return self.action_waiting
        self.move_step = self.move_step - 2
        return []

    def do_waiting_downbluecar_q32_1(self):
        if self.observation['time']['cur_step'] < 600:
            return self.action_waiting
        return []

    #
    def do_blue_tank_charge_car_q32(self):
        num_0 = 0
        num_1 = 0
        for enemy_opt in self.enemy_operators:
            if enemy_opt['sub_type'] == CAR:
                if enemy_opt['cur_hex'] in [1626, 1726, 1827, 1927, 2028,
                                            2127, 2227, 2326,
                                            2325, 2425, 2426, 2427,
                                            2523, 2524, 2526,
                                            2623, 2624, 2625, 2626]:
                    num_0 += 1
                if enemy_opt['cur_hex'] in [2720, 2721, 2722, 2723, 2724, 2725, 2726,
                                            2820, 2821, 2823, 2824,
                                            2917, 2918, 2919, 2920, 2921, 2922,
                                            3018, 3019, 3020, 3021,
                                            3117, 3118, 3119, 3120,
                                            3216, 3217, 3218, 3219,
                                            3314, 3315, 3316, 3317, 3318, 3319,
                                            3414, 3415, 3416, 3417, 3418
                                            ]:
                    num_1 += 1
        if num_0 > num_1:
            self.move_step = 10
            return []
        if num_0 < num_1:
            self.move_step = 20
            return []
        if num_0 == num_1:
            if num_0 > 0:
                self.move_step = 20
                return []
        return self.action_waiting

    def do_blue_tank_not_fire_go_back(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], CARS, -1, 15):
            if self.operator['weapon_cool_time'] > 0:
                self.move_step = self.move_step - 2
                return []
            else:
                return self.action_waiting
        else:
            self.move_step = self.move_step - 2
            return []
        return self.action_waiting

    def do_blue_tank_charge_q32_or_go_back(self):
        for enemy_opt in self.enemy_operators:
            if enemy_opt['sub_type'] == CAR:
                if enemy_opt['cur_hex'] in [1626, 1726, 1827, 1927, 2028,
                                            2127, 2227, 2326,
                                            2325, 2425, 2426, 2427,
                                            2523, 2524, 2526,
                                            2623, 2624, 2625, 2626,
                                            2720, 2721, 2722, 2723, 2724, 2725, 2726,
                                            2820, 2821, 2823, 2824,
                                            2917, 2918, 2919, 2920, 2921, 2922,
                                            3018, 3019, 3020, 3021,
                                            3117, 3118, 3119, 3120,
                                            3216, 3217, 3218, 3219,
                                            3314, 3315, 3316, 3317, 3318, 3319,
                                            3414, 3415, 3416, 3417, 3418
                                            ]:
                    return []
        if self.operator['cur_hex'] == 3618:
            return self.action_waiting
        self.move_step = self.move_step - 2
        return []

    def do_set_finish_flag_see_one_car(self):
        if self.is_has_enemy_in_distance(self.operator['cur_hex'], [CAR], -1, 20):
            self.is_in_new_function = False
        return []

    def do_bluesoilder_move_around_q32(self):
        self.move_step = 10
        return []

    def do_blue_tank_move_continue(self):
        #
        area = [3534, 3535, 3635, 3636]
        for index, tank_id in enumerate([10000, 11000, 12000, 13000]):
            tank_opt = self.situation.get_cur_opt_by_id(tank_id)
            if tank_opt:
                if tank_opt['cur_hex'] != area[index]:
                    return self.action_waiting
        return []

    def do_blue_car_defense_city(self):
        soilder_12200 = self.situation.get_cur_opt_by_id(12200)
        soilder_12201 = self.situation.get_cur_opt_by_id(12201)
        soilder_13200 = self.situation.get_cur_opt_by_id(13200)
        soilder_13201 = self.situation.get_cur_opt_by_id(13201)
        soilder_11201 = self.situation.get_cur_opt_by_id(11201)
        soilder_11200 = self.situation.get_cur_opt_by_id(11200)
        car_12100 = self.situation.get_cur_opt_by_id(12100)
        car_12101 = self.situation.get_cur_opt_by_id(12101)
        car_13100 = self.situation.get_cur_opt_by_id(13100)
        car_13101 = self.situation.get_cur_opt_by_id(13101)

        if self.operator['obj_id'] == 12100:
            if soilder_13201:
                if soilder_13201['blood'] <= 1:
                    self.func_done = True
                    self.move_step = 2
                    return []
            else:
                self.func_done = True
                self.move_step = 2
                return []
            if soilder_12200:
                if soilder_12200['blood'] <= 1:
                    self.func_done = True
                    self.move_step = 1
                    return []
            else:
                self.func_done = True
                self.move_step = 1
                return []
            if soilder_12201:
                if soilder_12201['blood'] <= 1:
                    self.func_done = True
                    self.move_step = 1
                    return []
            else:
                self.func_done = True
                self.move_step = 1
                return []
        if self.operator['obj_id'] == 12101:
            if car_12100 == None:  #
                if soilder_13201:
                    if soilder_13201['blood'] <= 1:
                        self.func_done = True
                        self.move_step = 2
                        return []
                else:
                    self.func_done = True
                    self.move_step = 2
                    return []
                if soilder_12200:
                    if soilder_12200['blood'] <= 1:
                        self.func_done = True
                        self.move_step = 1
                        return []
                else:
                    self.func_done = True
                    self.move_step = 1
                    return []

            else:
                if soilder_13201:
                    if soilder_13201['blood'] <= 1:
                        self.func_done = True
                        self.move_step = 4
                        return []
                else:
                    self.func_done = True
                    self.move_step = 4
                    return []
                if soilder_12200:
                    if soilder_12200['blood'] <= 1:
                        self.func_done = True
                        self.move_step = 3
                        return []
                else:
                    self.func_done = True
                    self.move_step = 3
                    return []

        if self.operator['obj_id'] == 13100:
            if soilder_13201:
                if soilder_13201['blood'] <= 1:
                    if car_12100 == None:
                        self.func_done = True
                        self.move_step = 3
                        return []
                    if car_12101 == None:
                        self.func_done = True
                        self.move_step = 2
                        return []
            else:
                if car_12100 == None:
                    self.func_done = True
                    self.move_step = 3
                    return []
                if car_12101 == None:
                    self.func_done = True
                    self.move_step = 2
                    return []
            if soilder_11200:
                if soilder_11200['blood'] <= 1:
                    self.func_done = True
                    self.move_step = 1
                    return []
            else:
                self.func_done = True
                self.move_step = 1
                return []

        if self.operator['obj_id'] == 13101:
            if soilder_11200:
                if soilder_11200['blood'] <= 1:
                    if car_13100 == None:
                        self.func_done = True
                        self.move_step = 1
                        return []
                    else:
                        self.func_done = True
                        self.move_step = 2
                        return []
            else:
                if car_13100 == None:
                    self.func_done = True
                    self.move_step = 1
                    return []
                else:
                    self.func_done = True
                    self.move_step = 2
                    return []
            if soilder_11201:
                if soilder_11201['blood'] <= 1:
                    self.func_done = True
                    self.move_step = 2
                    return []
            else:
                self.func_done = True
                self.move_step = 2
                return []
        return self.action_waiting

    def do_bluesoilder_10200_10201_back_defense(self):
        #
        my_dis = self.map.get_distance(self.operator['cur_hex'], 2737)
        for enemy_opt in self.enemy_operators:
            if enemy_opt['sub_type'] == SOILDER:
                dis = self.map.get_distance(enemy_opt['cur_hex'], 2737)
                if dis < my_dis:
                    return []
        for opt in self.our_opt:
            if opt.operator['cur_hex'] in [2637, 2638, 2736, 2737, 2738, 2837, 2838]:
                return self.action_waiting
        return []
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #

    def do_movearound_soilder_protect_city(self):
        pos = my_ai.plan_pos_list[self.operator['obj_id']][self.move_step - 1]
        #没夺下夺控点，则进行夺控：
        for each_city in self.observation['cities']:
            if each_city['coord'] == pos:
                if each_city['flag'] != self.color:
                    if self.observation['time']['cur_step'] > 2700:
                        return self.do_move_to_point(pos)
                    if pos not in self.situation.artillery_pos_list:
                        if self.operator['cur_hex'] != pos:
                            return self.do_move_to_point(pos)
                break
        big_six = self.myLandTool.get_big_six(pos, 1)
        my_seven = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
        #
        temp_pos_list = self.seven_in_mycity_seven(my_seven, big_six)
        if len(temp_pos_list) > 0:
            my_seven = temp_pos_list
        #
        #
        temp_pos_list = self.seven_cannot_artillery_attacked(my_seven)
        if len(temp_pos_list) > 0:
            my_seven = temp_pos_list
        else:
            #
            self.auto_moving = True
            return self.action_waiting
        #
        #
        if len(my_seven) == 0:
            #
            self.auto_moving = True
            return []
        #
        pos = my_seven[random.randint(0, len(my_seven) - 1)]
        if pos == self.operator['cur_hex']:
            self.auto_moving = True
            return self.action_waiting
        #
        self.auto_moving = True
        return self.do_move_to_point(pos)
        return []

    #
    def get_red_charge_occupy_city(self):
        if self.color == 1:
            return False
        main_area = [3535, 3536,
                     3635, 3636, 3637,
                     3735, 3736, 3737]
        second_area = [3639, 3640,
                       3738, 3739, 3740,
                       3839, 3840]
        #
        #
        #
        #
        #
        #
        #
        num_dead_soilder = 0
        num_dead_tank = 0

        for key in self.situation.enemy_history.keys():
            enemy = self.situation.enemy_history[key][0]
            is_dead = self.situation.enemy_history[key][2]
            if is_dead:
                if enemy['sub_type'] == SOILDER:
                    num_dead_soilder += 1
                if enemy['sub_type'] == TANK:
                    num_dead_tank += 1
            #
            #
            #
            #
            #
            #
            #
            #
            #
        #
        #
        our_soilder = self.situation.get_cur_opt_by_id(200)
        if self.observation['scores']['red_remain'] > self.observation['scores']['blue_remain'] + 45:
            return True
        if self.observation['scores']['red_remain'] > self.observation['scores']['blue_remain'] + 35:
            if our_soilder:
                return True
        if num_dead_soilder == 2:
            if our_soilder:
                return True
        if num_dead_tank == 2:
            if our_soilder:
                return True
        if our_soilder:
            if our_soilder['cur_hex'] in second_area:
                if 10000 not in our_soilder['see_enemy_bop_ids'] and \
                        10001 not in our_soilder['see_enemy_bop_ids'] and \
                        10100 not in our_soilder['see_enemy_bop_ids'] and \
                        10101 not in our_soilder['see_enemy_bop_ids']:
                    return True

        return False

    def do_charge_city_0_s82_3941(self):
        if self.get_red_charge_occupy_city():
            return []
        else:
            return self.action_waiting

    def do_move_back_0_s82_3636(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 10):
            if self.operator['blood'] < 4:
                self.move_step = 10
                return []
        return []

    def do_waiting_0_s82_3941(self):
        if 3739 in self.situation.clean_pos_list:
            return []
        tank1 = self.situation.enemy_history[10000]
        tank2 = self.situation.enemy_history[10001]
        soider1 = self.situation.enemy_history[10200]
        soider2 = self.situation.enemy_history[10201]
        if tank1[2] and tank2[2]:  #
            if soider1[2] or soider2[2]:  #
                self.func_done = True
                return []
        return []

    def do_waiting_0_s82_3640(self):
        if 3740 in self.situation.stack_pos_list:
            self.func_done = True
            self.move_step = 4
            return []
        if 3640 in self.situation.stack_pos_list:
            self.func_done = True
            self.move_step = 4
            return []
        return []

    def do_waiting_0_s82_3639(self):
        if 3640 in self.situation.stack_pos_list:
            return []
        self.move_step = 14
        return []

    def do_moveto3941_0_s82_3841(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 10):
            self.func_done = True
            self.move_step = 12
            return []
        soilder = self.situation.get_cur_opt_by_id(200)
        if soilder['cur_hex'] == 3841:
            self.func_done = True
            self.move_step = 12
            return []
        return []

    def do_waiting_0_s82_3740(self):
        my_soilder = self.situation.get_cur_obj_by_id(200)
        if my_soilder:
            if 3639 in self.situation.clean_pos_list:
                dis_so = self.situation.map.get_distance(my_soilder['cur_hex'], 3636)
                dis_my = self.situation.map.get_distance(self.operator['cur_hex'], 3636)
                if dis_so + 1 <= dis_my:
                    self.move_step = 15
                    return []
        else:
            #
            soilder1 = self.situation.enemy_history[10200]
            soilder2 = self.situation.enemy_history[10201]
            blood = 0
            if not soilder1[2]:
                blood += soilder1[0]['blood']
            if not soilder2[2]:
                blood += soilder2[0]['blood']
            if (soilder1[2] and soilder2[2]) or (blood < 2):
                if self.observation['scores']['red_remain'] < self.operator['blood'] * 10 + 10:
                    self.move_step = 15
                    return []
        return []

    def do_waiting_0_s82_3737(self):
        my_soilder = self.situation.get_cur_obj_by_id(200)
        if my_soilder:
            if 3639 in self.situation.clean_pos_list:
                dis_so = self.situation.map.get_distance(my_soilder['cur_hex'], 3636)
                dis_my = self.situation.map.get_distance(self.operator['cur_hex'], 3636)
                if dis_so + 1 <= dis_my:
                    return []
        else:
            #
            soilder1 = self.situation.enemy_history[10200]
            soilder2 = self.situation.enemy_history[10201]
            blood = 0
            if not soilder1[2]:
                blood += soilder1[0]['blood']
            if not soilder2[2]:
                blood += soilder2[0]['blood']
            if (soilder1[2] and soilder2[2]) or (blood < 2):
                if self.observation['scores']['red_remain'] < self.operator['blood'] * 10 + 10:
                    return []

        return self.action_waiting

    def do_waiting_0_s82_3736(self):
        if self.observation['cities'][0]['flag'] != self.color:
            my_soilder = self.situation.get_cur_obj_by_id(200)
            if not my_soilder:
                return []
        self.move_step = 18
        return []

    def do_waiting_100_s82_4244(self):

        #
        my_soilder = self.situation.get_cur_opt_by_id(200)
        #

        if self.get_red_charge_occupy_city():
            return []
        else:
            return self.action_waiting
        return []

    def do_waiting_400_s82_4245(self):

        if self.get_red_charge_occupy_city():
            return []
        else:
            return self.action_waiting

    def do_waiting_200_s82_3939(self):
        if self.get_red_charge_occupy_city():
            return []
        else:
            return self.action_waiting

    def all_blue_tk_dead(self):
        blue_tk1 = self.situation.get_enemy_history_by_id(10000)
        blue_tk2 = self.situation.get_enemy_history_by_id(10001)

        score = self.observation['scores']['red_remain'] - self.observation['scores']['blue_remain']

        if score >= 35:
            return True

        if blue_tk1 is not None and blue_tk2 is not None:
            if blue_tk1[2] and blue_tk2[2]:
                return True
        return False

    def do_move_10000_s82_3940(self):
        if 3944 in self.situation.clean_pos_list:
            return []
        else:
            self.move_step = 4
            return []
        return []

    def do_move_10000_s82_3944(self):
        self.move_step = 10
        return []

    def do_move_10000_s82_3736(self):
        if self.is_has_cansee_enemy_in_distance(3737, CARS, -1, 25):
            self.move_step = 19
            return []
        return []

    def do_move_10000_s82_3737(self):
        self.move_step = 13
        return []

    def do_move_10001_s82_4242(self):
        self.move_step = 10
        return []

    def do_move_10001_s82_4138(self):
        if 4242 in self.situation.clean_pos_list:
            return []
        else:
            self.move_step = 3
            return []
        return []

    def do_waiting_10000_to_3640_s82(self):
        tank = self.situation.get_cur_opt_by_id(10000)
        if tank:
            if tank['cur_hex'] == 3740:
                return self.action_waiting
            return []
        return []

    def do_move_to_main_bluetank_s82(self):
        #
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 2):
            big_six = self.myLandTool.get_big_six(3739, 2)
            if not self.is_has_myopt_in_aboveme([SOILDER], big_six):
                self.func_done = True
                return []
        #
        big_six = self.myLandTool.get_big_six(3739, 1)
        if self.is_has_myopt_in_aboveme([SOILDER], big_six):
            self.func_done = True
            return []
        return []

    def do_moveseccity_bluetank_s82_3740(self):
        if self.observation['cities'][1]['flag'] != self.color:
            if 3639 not in self.situation.stack_pos_list:
                self.move_step = 17
                return []
        return []

    def do_moveseccity_bluetank_s82_3639(self):
        self.move_step = 10
        return []

    def do_move_to_sec_bluetank_s82(self):
        #
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 2):
            big_six = self.myLandTool.get_big_six(3636, 2)
            if not self.is_has_myopt_in_aboveme([SOILDER], big_six):
                self.func_done = True
                return []
        #
        big_six = self.myLandTool.get_big_six(3636, 1)
        if self.is_has_myopt_in_aboveme([SOILDER], big_six):
            self.func_done = True
            self.move_step = 10
            return []
        return []

    def do_tank_goback(self):
        self.move_step = self.move_step - 2
        return []

    def do_waiting_10101_s82_3534(self):
        if 3736 in self.situation.clean_pos_list:
            return []
        enemy_tank = self.situation.enemy_history[0]
        if enemy_tank[2]:
            return []
        return self.action_waiting

    def do_movenearcity_10100_s82(self):
        for each in self.situation.enemy_history.values():
            enemy_opt = each[0]
            if not each[2]:
                if self.map.can_see(enemy_opt['cur_hex'], 3435, 0) or \
                        self.map.can_see(enemy_opt['cur_hex'], 3436, 0):
                    return []
        self.func_done = True
        return []

    def do_attackcar_missile(self):
        car1 = self.situation.enemy_history[10100]
        car2 = self.situation.enemy_history[10101]
        if car1[1] > -self.observation['time']['cur_step'] + 1 or \
                car2[1] > -self.observation['time']['cur_step'] + 1:
            self.move_step = 20
            return []
        return []

    def do_waiting_10100_s82_3334(self):
        for each in self.situation.enemy_history.values():
            if 3636 in self.situation.clean_pos_list:
                enemy_opt = each[0]
                if not each[2]:
                    if self.map.can_see(enemy_opt['cur_hex'], 3435, 0) or \
                            self.map.can_see(enemy_opt['cur_hex'], 3436, 0):
                        return self.action_waiting
        return []

    def do_waiting_10100_s82_3637(self):
        if 3737 in self.situation.clean_pos_list:
            return []
        enemy_tank = self.situation.enemy_history[0]
        if enemy_tank[2]:
            return []
        return self.action_waiting

    def do_waiting_10100_s82_3737(self):
        car = self.situation.get_cur_opt_by_id(10101)
        if not car:
            return []
        return self.action_waiting

    def do_waiting_10200_s82_3738(self):
        #
        if self.observation['cities'][1]['flag'] != self.color:
            self.move_step = 2
            return []
        #
        soilder_enemy = self.situation.enemy_history[200]
        if soilder_enemy[2]:
            self.move_step = 10
            return []
        else:
            my_dis = self.situation.map.get_distance(self.operator['cur_hex'], 3636)
            enemy_dis = self.situation.map.get_distance(soilder_enemy[0]['cur_hex'], 3636)
            if my_dis > enemy_dis:
                self.move_step = 10
                return []
            if my_dis == enemy_dis:
                return self.action_waiting
        #
        if 3639 not in self.situation.clean_pos_list:
            self.move_step = 3
            return []
        return self.action_waiting

    def do_waiting_10200_s82_3736(self):
        #
        if self.observation['cities'][0]['flag'] != self.color:
            self.move_step = 0
            return []
        #
        soilder_enemy = self.situation.enemy_history[200]
        if soilder_enemy[2]:
            if self.observation['cities'][1]['flag'] != self.color:
                self.move_step = 2
                return []
        else:
            my_dis = self.situation.map.get_distance(self.operator['cur_hex'], 3739)
            enemy_dis = self.situation.map.get_distance(soilder_enemy[0]['cur_hex'], 3739)
            if my_dis > enemy_dis:
                return []
            my_soilder = self.situation.get_cur_opt_by_id(10201)
            if my_soilder:
                if self.situation.map.get_distance(my_soilder['cur_hex'], 3739) <= 1:
                    return self.action_waiting
                else:
                    return []
            else:
                return self.action_waiting
            return []

        #
        return self.action_waiting

    def do_waiting_10200_s82_3639(self):
        #
        soilder_enemy = self.situation.enemy_history[200]
        if not soilder_enemy[2]:
            my_dis = self.situation.map.get_distance(self.operator['cur_hex'], 3636)
            enemy_dis = self.situation.map.get_distance(soilder_enemy[0]['cur_hex'], 3636)
            if my_dis > enemy_dis:
                self.move_step = 10
                return []
        #
        if self.observation['cities'][1]['flag'] != self.color:
            self.move_step = 2
            return []
        return []

    def do_changepath_10200_s82_0(self):
        self.move_step = 20
        return []

    def do_keepmove_bluesoilder_s82(self):
        if self.operator['cur_hex'] in self.situation.stack_pos_list:
            self.func_done = True
            return []
        return []

    def do_waiting_10201_s82_3639(self):
        #
        soilder_enemy = self.situation.enemy_history[200]
        if not soilder_enemy[2]:
            my_dis = self.situation.map.get_distance(self.operator['cur_hex'], 3636)
            enemy_dis = self.situation.map.get_distance(soilder_enemy[0]['cur_hex'], 3636)
            if my_dis > enemy_dis:
                self.move_step = 10
                return []
        #
        if self.observation['cities'][1]['flag'] != self.color:
            self.move_step = 2
            return []
        #
        if 3640 not in self.situation.clean_pos_list:
            return []
        return self.action_waiting

    def do_waiting_10201_s82_3637(self):
        #
        if self.observation['cities'][0]['flag'] != self.color:
            self.move_step = 0
            return []
        #
        soilder_enemy = self.situation.enemy_history[200]
        if soilder_enemy[2]:
            if self.observation['cities'][1]['flag'] != self.color:
                self.move_step = 3
                return []
        else:
            my_dis = self.situation.map.get_distance(self.operator['cur_hex'], 3739)
            enemy_dis = self.situation.map.get_distance(soilder_enemy[0]['cur_hex'], 3739)
            if my_dis > enemy_dis:
                self.move_step = 3
                return []
            enemy_dis_main = self.situation.map.get_distance(soilder_enemy[0]['cur_hex'], 3636)
            if enemy_dis_main <= 2:
                return self.action_waiting
            return []
        #
        return self.action_waiting

    def do_waiting_10201_s82_3738(self):
        if self.observation['cities'][1]['flag'] != self.color:
            return []
        self.move_step = 3
        return []

    def do_waiting_atseccity(self):
        if self.observation['cities'][1]['flag'] != self.color:
            return self.action_waiting
        return []

    def do_waiting_atmaincity(self):
        if self.observation['cities'][0]['flag'] != self.color:
            return self.action_waiting
        return []

    def do_moveaway_blue_tank_s82(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 10):
            self.move_step = 10
            return []
        return []

    #
    def set_func_list_8_1(self):
        #
        self.moving_func_list[(100, 2425, None)] = [self.do_get_off_0]
        #
        self.moving_func_list[(100, 2931, None)] = [self.do_get_off_safe]
        #
        #

        #
        self.moving_func_list[(200, 2425, None)] = [self.do_get_on_red_0_1]
        #
        #
        self.moving_func_list[(400, 4945, 1)] = [self.do_stop_to_guide4945]
        #
        #
        #

        #
        #

        #

        self.moving_func_list[(10100, 4139, None)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                      self.do_waiting_10100_s81_4139]
        self.moving_func_list[(10100, 4042, None)] = [self.do_changepath_10100_s81_4042]
        self.moving_func_list[(10100, 3841, None)] = [self.do_continue_10100_s81_3841, self.do_get_off_safe]
        self.moving_func_list[(10100, 3839, None)] = [self.do_continue_10100_s81_3841, self.do_get_off_safe]
        self.moving_func_list[(10100, 3838, None)] = [self.do_continue_10100_s81_3841, self.do_get_off_safe]
        self.moving_func_list[(10100, 3837, None)] = [self.do_get_off_safe]
        #
        #

        self.moving_func_list[(10200, 3851, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(10200, 3838, None)] = [self.do_changepath_10200_s81_3838]
        self.moving_func_list[(10200, 3837, None)] = [self.do_changepath_10200_s81_3837]
        self.moving_func_list[(10200, 3839, None)] = [self.do_changepath_10200_s81_3838]
        self.moving_func_list[(10200, 3841, None)] = [self.do_changepath_10200_s81_3838]
        self.moving_func_list[(10200, None, 0)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, None, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, None, 2)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, None, 3)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, 4038, None)] = [self.do_movefront_10200_s81_4038]
        self.moving_func_list[(10200, 3736, None)] = [self.do_stop_to_shoot_cars, self.do_moveback_10200_s81_3736]
        self.moving_func_list[(10200, 3735, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_10200_s81_3735]

        self.moving_func_list[(10200, 3636, None)] = [self.do_waiting_10200_s81_3636]

        #

        #

        self.moving_func_list[(10101, 4041, None)] = [self.do_moveto4040_10100_s81_4041, self.do_get_off_safe,
                                                      self.do_stop_to_shoot, self.do_waiting_10100_s81_4139]
        self.moving_func_list[(10101, 4040, None)] = [self.do_get_off_safe, self.do_hide]
        self.moving_func_list[(10101, 3943, None)] = [self.do_changepath_10101_s81_3943]
        self.moving_func_list[(10101, 3942, None)] = [self.do_moveto4040_10100_s81_4041, self.do_get_off_safe,
                                                      self.do_stop_to_shoot, self.do_waiting_10100_s81_4139]

        #
        #
        #
        #
        self.moving_func_list[(10201, 4140, 0)] = [self.do_changepath_10201_s81_4140]
        self.moving_func_list[(10201, 3942, 0)] = [self.do_changepath_10201_s81_4140]
        self.moving_func_list[(10201, 4052, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(10201, None, 0)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 2)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 3)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, 4038, None)] = [self.do_stop_to_shoot_cars, self.do_set_point,
                                                      self.do_movefront_10200_s81_4038]
        self.moving_func_list[(10201, 3736, None)] = [self.do_stop_to_shoot_cars, self.do_moveback_10200_s81_3736]
        self.moving_func_list[(10201, 3735, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_10200_s81_3735]
        self.moving_func_list[(10201, 3636, None)] = [self.do_waiting_10200_s81_3636]
        #
        #
        self.moving_func_list[(10000, 3534, None)] = [self.do_moveto3435_10000_s81_3534]
        self.moving_func_list[(10000, 3735, None)] = [self.do_waitingfortank10000_s81_3735, self.do_move_10000_s81_3735]
        self.moving_func_list[(10000, 3736, None)] = [self.do_move_10000_s81_3736]
        #
        self.moving_func_list[(10001, 3534, None)] = [self.do_moveto3435_10000_s81_3534]
        self.moving_func_list[(10001, 3735, None)] = [self.do_move_10000_s81_3735]
        self.moving_func_list[(10001, 3736, None)] = [self.do_move_10000_s81_3736]

    def do_moveto3041_10000_s81_3040(self):
        self.move_step = 0
        return []

    def do_waiting_10100_s81_4139(self):
        if 4038 in self.situation.clean_pos_list:
            return []
        soilder = self.situation.get_cur_opt_by_id(10201)
        if not soilder:
            return []
        return self.action_waiting

    def do_moveto4040_10100_s81_4041(self):
        tank = self.situation.enemy_history[0]
        if tank[2]:
            self.func_done = True
            return []
        else:
            if (tank[1] > -self.observation['time']['cur_step'] + 1):
                if self.situation.map.get_distance(4040, tank[0]['cur_hex']) > 8:
                    self.func_done = True
                    return []
        return []

    def do_changepath_10101_s81_3943(self):
        tank = self.situation.enemy_history[0]
        if tank[2]:
            return []
        else:
            if self.situation.map.get_distance(tank[0]['cur_hex'], 3636) <= 3:
                self.move_step = 10
                return []
        return []

    def do_changepath_10200_s81_3838(self):
        self.move_step = 10
        return []

    def do_changepath_10200_s81_3837(self):
        self.move_step = 2
        return []

    def do_changepath_10201_s81_4140(self):
        self.move_step = 10
        return []

    def do_moveto3435_10000_s81_3534(self):
        #
        if False:
            return []
        self.move_step = 0
        return []

    def do_move_10000_s81_3735(self):
        soilder = self.situation.enemy_history[200]
        if not self.situation.is_vain_attack_flg:  #
            if soilder[2] or (soilder[1] <= -self.observation['time']['cur_step'] + 1):  #
                self.move_step = 0
                return []
        if 3736 not in self.situation.stack_pos_list:
            self.move_step = 4
            return []
        self.move_step = 2
        return []

    def do_changepath_10100_s81_4042(self):
        tank = self.situation.enemy_history[0]
        if tank[2]:
            self.func_done = True
            self.move_step = 10
            return []
        else:
            if (tank[1] > -self.observation['time']['cur_step'] + 1):
                dis = self.situation.map.get_distance(3636, tank[0]['cur_hex'])
                if (tank[0]['cur_hex'] % 100) < 38 and dis >= 7:
                    self.func_done = True
                    self.move_step = 10
                    return []

        return []

    def do_continue_10100_s81_3841(self):
        tank = self.situation.enemy_history[0]
        if tank[2]:
            self.func_done = True
            return []
        else:
            if (tank[1] > -self.observation['time']['cur_step'] + 1):
                dis = self.situation.map.get_distance(3636, tank[0]['cur_hex'])
                if (tank[0]['cur_hex'] % 100) < 38 and dis >= 7:
                    self.func_done = True
                    return []
        return []

    def do_waitingfortank10000_s81_3735(self):
        tank = self.situation.get_cur_opt_by_id(10001)
        if tank:
            if tank['cur_hex'] in [3835, 3736]:
                return []
            if tank['cur_hex'] == 3636:
                if tank['cur_pos'] >= 0.5:
                    return []
            return self.action_waiting
        else:
            return []
        return []

    def do_move_10000_s81_3736(self):
        self.move_step = 3
        return []

    def do_movefront_10200_s81_4038(self):
        soilder = self.situation.enemy_history[200]
        if not soilder[2]:
            if (soilder[1] > -self.observation['time']['cur_step'] + 1) and soilder[0]['cur_hex'] < 3900:
                self.move_step = 2
                return []
        my_soilder = self.situation.get_cur_opt_by_id(10200)
        if my_soilder:
            return self.action_waiting
        else:
            self.move_step = 2
            return []
        return self.action_waiting

    def do_moveback_10200_s81_3736(self):

        soilder = self.situation.enemy_history[200]
        #
        if not soilder[2]:
            if soilder[0]['cur_hex'] == 3735:
                self.move_step = 15
                return []
        #
        if not soilder[2]:
            if soilder[0]['cur_hex'] == 3736:
                return self.action_waiting
        #
        if self.observation['cities'][0]['flag'] != self.color:
            return []
        #
        if not soilder[2]:
            if (soilder[1] > -self.observation['time']['cur_step'] + 1) and soilder[0]['cur_hex'] > 3800:
                self.move_step = 4
                return []
        #
        soilder_my = self.situation.get_cur_opt_by_id(10201)
        if soilder_my:
            if soilder_my['cur_hex'] == 3736:
                if 3735 not in self.situation.stack_pos_list:
                    self.move_step = 15
                    return []
        return self.action_waiting

    def do_waiting_10200_s81_3735(self):
        soilder = self.situation.enemy_history[200]
        if not soilder[2]:
            if soilder[0]['cur_hex'] == 3736:
                self.move_step = 2
                return []
            if soilder[0]['cur_hex'] == 3735:
                return self.action_waiting
        soilder_my = self.situation.get_cur_opt_by_id(10201)
        if soilder_my:
            if soilder_my['cur_hex'] != 3736:
                self.move_step = 2
                return []
        return self.action_waiting

    def do_waiting_10200_s81_3636(self):
        if self.observation['cities'][0]['flag'] != self.color:
            return []
        return self.action_waiting

    def waiting_solier(self):
        soilder1 = self.situation.get_cur_opt_by_id(10200)
        soilder2 = self.situation.get_cur_opt_by_id(10201)

        if soilder1 is not None or soilder2 is not None:
            return []
        return self.action_waiting

    def do_moving_func_list(self):
        my_id = self.operator['obj_id']
        if self.moving_func_list.get((my_id, self.operator['cur_hex'], self.move_step)):
            for each_func in self.moving_func_list[(my_id, self.operator['cur_hex'], self.move_step)]:
                msg = each_func()

                if len(msg) > 0:
                    return msg
                if self.func_done:
                    break
        if self.moving_func_list.get((my_id, self.operator['cur_hex'], None)):
            for each_func in self.moving_func_list[(my_id, self.operator['cur_hex'], None)]:
                msg = each_func()
                if len(msg) > 0:
                    return msg
                if self.func_done:
                    break
        if self.moving_func_list.get((my_id, None, self.move_step)):
            for each_func in self.moving_func_list[(my_id, None, self.move_step)]:
                msg = each_func()
                if len(msg) > 0:
                    return msg
                if self.func_done:
                    break
        if self.moving_func_list.get((my_id, None, None)):
            for each_func in self.moving_func_list[(my_id, None, None)]:
                msg = each_func()
                if len(msg) > 0:
                    return msg
                if self.func_done:
                    break
        return []

    def do_get_off_0(self):
        if self.observation['time']['cur_step'] < 70:
            msg = self.do_getoff()
            if len(msg) > 0:
                return msg
            return self.action_waiting
        return []

    def do_get_on_red_0_1(self):
        if self.observation['time']['cur_step'] == 0:
            return self.action_waiting
        if self.observation['time']['cur_step'] < 70:
            msg = self.do_get_on()
            if len(msg) > 0:
                return msg
        return []

    def do_get_on_blue_0(self):
        msg = self.do_get_on()
        if len(msg) > 0:
            return msg
        return []

    def do_get_off_safe(self):
        msg = self.do_getoff()
        if len(msg) > 0:
            return msg
        else:
            if len(self.operator['passenger_ids']) > 0:
                return self.action_waiting
            else:
                return []
        return []

    def do_get_off_not_see_autocar(self):
        if self.color == BLUE:
            if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [AUTO_CAR], -1, 25):
                if self.situation.opt_is_waiting[400]:
                    return []
        msg = self.do_getoff()
        if len(msg) > 0:
            return msg
        else:
            if len(self.operator['passenger_ids']) > 0:
                return self.action_waiting
            else:
                return []
        return []

    def do_waiting_10100_4029(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [AUTO_CAR], 21, 26):
            if self.situation.opt_is_waiting[400]:
                return []
        if 4031 in self.situation.clean_pos_list and (
                not self.is_has_cansee_enemy_in_distance(4031, [TANK, CAR, AUTO_CAR, SOILDER], -1, 12)):
            return []
        else:
            return self.action_waiting
        return self.action_waiting

    def do_waiting_10100_4030(self):
        #
        if self.is_has_enemy_in_distance(4029, [SOILDER, AUTO_CAR, TANK, CAR], -1, 2):
            return self.action_waiting
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [AUTO_CAR], 21, 26):
            if self.color == BLUE and self.situation.opt_is_waiting[400]:
                return []
        if 4031 in self.situation.clean_pos_list and (
                not self.is_has_cansee_enemy_in_distance(4031, [TANK, CAR, AUTO_CAR, SOILDER], -1, 12)):
            return []
        else:
            return self.action_waiting
        return self.action_waiting

    def do_waiting_10101_4031(self):
        if 4030 not in self.situation.stack_pos_list:
            #
            if self.is_has_enemy_in_distance(4029, [SOILDER, AUTO_CAR, TANK, CAR], -1, 2):
                self.move_step = 12
                return []
            if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 12):
                return []
        return self.action_waiting

    def do_moveback_to_4031_bluecar(self):
        self.move_step = 10
        return []

    def do_waiting_10101_4332(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [AUTO_CAR], 21, 26):
            return []
        #
        #
        return self.action_waiting

    def do_waiting_100_at_4539(self):
        soilder = self.situation.get_cur_opt_by_id(200)
        if soilder:
            if self.situation.map.get_distance(soilder['cur_hex'], 4435) > 1:
                return self.action_waiting
        else:
            return self.action_waiting
        return []

    def do_backto4734_10000_4835(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [AUTO_CAR], 10, 15):
            if self.situation.opt_is_waiting[400]:
                self.move_step = 0
                return []
        for each in self.situation.enemy_operators:
            if each['sub_type'] == TANK:
                big_six = self.myLandTool.get_big_six(4435, 3)
                if each['cur_hex'] in big_six:
                    self.move_step = 0
                    return []
        return []

    def do_backto4937_10000_4938(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [AUTO_CAR], 21, 25):
            if self.situation.opt_is_waiting[400]:
                self.move_step = 4
                return []
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 10):
            self.move_step = 4
            return []
        if self.is_can_attack([CAR]):
            return []
        return []

    def do_backto4435_10000_4536(self):
        if self.situation.opt_is_waiting[400]:
            if self.is_see_enemy([TANK]):
                self.move_step = 14
                return []
        return []

    def do_backto4938_10000_4937(self):
        self.move_step = 2
        return []

    def do_backto4436_10000_4437(self):
        self.move_step = 6
        return []

    def do_backto4129_10000_4029(self):
        self.move_step = 10
        return []

    def do_moveto4029_red_tank_4030(self):
        #
        if self.observation['cities'][1]['flag'] != self.color:
            self.move_step = 50
        #
        if self.is_has_cansee_enemy_in_distance(3929, [SOILDER], -1, 10):
            if self.operator['blood'] < 3:
                return self.action_waiting
        #
        big_six = self.myLandTool.get_big_six(4435, 1)
        if not self.is_has_myopt_in(big_six):
            return self.action_waiting
        #
        return []

    def do_moveto4030_red_tank_3929(self):
        self.move_step = 51
        return []

    def do_waiting_for_autocar_first(self):
        autocar = self.situation.get_cur_opt_by_id(400)
        if autocar:
            return self.action_waiting
        return []

    def do_move_to4536_100at4539(self):
        if len(self.operator['passenger_ids']) == 0:
            return []
        #
        big_six_3 = self.myLandTool.get_big_six(4435, 2)
        soilder = 0
        enemy = self.get_blue_opt_area(big_six_3, self.situation.enemy_history)
        for each_enemy in enemy:
            opt = each_enemy[0]
            if opt['sub_type'] == SOILDER:
                soilder += 1
        if soilder > 1:
            return []
        #
        if self.situation.enemy_history[10000][2]:  #
            if self.situation.get_cur_opt_by_id(0):  #
                big_six = self.myLandTool.get_big_six(4435, 1)
                if self.is_has_myopt_in(big_six):
                    enemy = self.get_blue_opt_area(big_six, self.situation.enemy_history)
                    for each in enemy:
                        time = each[1]
                        if time > -200:
                            return []
                    self.func_done = True
                    self.do_set_point()
                    self.move_step = 5
                    return []

        return []

    def do_waiting_red_tank_4535(self):
        if self.observation['cities'][0]['flag'] == self.color:
            return []
        soilder = self.situation.get_cur_opt_by_id(200)
        if not soilder:
            return []
        if not self.is_has_enemy_in_distance(4435, ALL_OPT_1, 0, 0):
            if 4435 not in self.situation.stack_pos_list:
                return []
        return self.action_waiting

    def do_waiting_red_tank_4435(self):
        if self.observation['cities'][0]['flag'] == self.color:
            return []
        if 4435 in self.situation.stack_pos_list:
            return []
        return self.action_waiting

    def do_waiting_red_tank_4335(self):
        if self.observation['cities'][0]['flag'] == self.color:
            return []
        if not self.is_has_myopt_in([4435]):
            self.move_step = 24
            return []
        return self.action_waiting

    def do_waiting_red_tank_4335_1(self):
        #
        #
        #
        #
        return []

    def do_waiting_red_tank_4435_2(self):
        #
        #
        #
        #
        for each_enemy in self.situation.enemy_history.values():
            opt = each_enemy[0]
            if opt['sub_type'] == SOILDER:
                if self.map.can_see(self.operator['cur_hex'], opt['cur_hex'], 0):
                    self.move_step = 2
                    return []
        self.move_step = 0
        return []

    def do_waiting_red_tank_4535_3(self):
        self.move_step = 1
        return []

    def do_waiting_red_tank_4436_3(self):
        self.move_step = 1
        return []

    def do_hide_for_soilder_0_4436(self):
        #
        big_six = self.myLandTool.get_big_six(4435, 1)
        flg = False
        enemy = self.get_blue_opt_area(big_six, self.situation.enemy_history)
        for each_enemy in enemy:
            opt = each_enemy[0]
            if opt['sub_type'] == SOILDER:
                flg = True
                break
        if flg:
            #
            if self.is_has_myopt_in_aboveme([SOILDER], big_six):
                if self.operator['blood'] < 4:
                    self.move_step = 40
                    return []
            #
            big_six_2 = self.myLandTool.get_big_six(4435, 2)
            if not self.is_has_myopt_in_aboveme([SOILDER], big_six_2):
                if self.operator['blood'] < 3:
                    self.move_step = 40
                    return []
        #
        big_six_3 = self.myLandTool.get_big_six(4435, 3)
        soilder = 0
        enemy = self.get_blue_opt_area(big_six_3, self.situation.enemy_history)
        for each_enemy in enemy:
            opt = each_enemy[0]
            if opt['sub_type'] == SOILDER:
                soilder += 1
        if soilder > 1:
            if self.operator['blood'] < 4:
                self.move_step = 40
                return []
        return []

    def do_move_back_red_tank(self):
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        big_six = self.myLandTool.get_big_six(4030, 2)
        enemy_list = self.get_blue_opt_area(big_six, self.situation.enemy_history)
        car_num = 0
        soilder_num = 0
        for each_enemy in enemy_list:
            each_opt = each_enemy[0]
            time = each_enemy[1]
            if time > -100:
                if each_opt['sub_type'] in [TANK, CAR, AUTO_CAR]:
                    if each_opt['blood'] > self.operator['blood']:
                        car_num = car_num + 1
                    car_num = car_num + 1
                if each_opt['sub_type'] == SOILDER:
                    #
                    soilder_num = soilder_num + 1
        if soilder_num < 1 and car_num < 2 and (soilder_num + car_num) < 2:
            self.move_step = 46
            return []
        return []

    def do_waiting_200_4435(self):
        if not self.is_has_enemy_in_distance(4435, ALL_OPT_1, 0, 0):
            if self.is_has_enemy_in_distance(4436, [SOILDER], 0, 0):
                self.move_step = 4
                return []
            if self.is_has_enemy_in_distance(4334, [SOILDER], 0, 0):
                return []
            if self.is_has_enemy_in_distance(4436, [SOILDER], 0, 0):
                self.move_step = 4
                return []
            if self.is_can_attack(ALL_OPT_1):
                return self.action_waiting
            return []
        else:
            return self.action_waiting

    def do_waiting_200_4436(self):
        if not self.is_has_enemy_in_distance(4336, ALL_OPT_1, 0, 0):
            if self.is_can_attack(CARS):
                return self.action_waiting
            if self.is_has_enemy_in_distance(4335, [SOILDER], 0, 0):
                self.move_step = 0
                return []
            if self.observation['time']['cur_step'] > 1000:
                return []
            else:
                return self.action_waiting
        else:
            return self.action_waiting

    def do_waiting_200_4334(self):
        if not self.is_has_enemy_in_distance(4334, ALL_OPT_1, 0, 0):
            if self.is_can_attack(CARS):
                return self.action_waiting
            if self.is_has_enemy_in_distance(4335, [SOILDER], 0, 0):
                self.move_step = 4
                return []
            if self.observation['cities'][0]['flag'] != self.color:
                self.move_step = 5
                return []
            if self.is_has_enemy_in_distance(4436, [SOILDER], 0, 0):
                self.move_step = 4
                return []
            return []
        else:
            return self.action_waiting
        return self.action_waiting

    def do_waiting_when_see_enemy_soilder(self):
        if self.is_see_enemy([SOILDER]):
            return self.action_waiting
        return []

    def do_back_to_4436(self):
        self.move_step = 0
        return []

    def do_stop_to_guide4945(self):
        soilder = self.situation.get_cur_opt_by_id(200)
        if soilder:
            if self.situation.map.get_distance(soilder['cur_hex'], 4435) <= 3:
                return []
        if 4539 in self.situation.clean_pos_list:
            return []

        #
        #
        #
        #
        return self.action_waiting

    def do_stop_to_guild(self):
        caropt = self.situation.get_cur_opt_by_id(100)
        if caropt:
            if self.is_can_guide(self.operator, caropt['cur_hex']):
                return self.action_waiting
        return []

    def do_tank_hide(self):
        if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 10):
            if self.operator['blood'] < 4:
                self.move_step = 10
        return []

    def do_waiting_for_soilder_to_main(self):
        soilder = self.situation.get_cur_opt_by_id(200)
        if soilder:
            if self.situation.map.get_distance(soilder['cur_hex'], 4435) > 1:
                return self.action_waiting
        else:
            return self.action_waiting
        return []

    def do_tank_move_to_main(self):
        if self.observation['cities'][0]['flag'] == self.color:
            return []
        big_six = self.myLandTool.get_big_six(4435, 2)
        enemy_list = self.get_blue_opt_area(big_six, self.situation.enemy_history)
        car_num = 0
        soilder_num = 0
        for each_enemy in enemy_list:
            each_opt = each_enemy[0]
            time = each_enemy[1]
            if time > -100:
                if each_opt['sub_type'] in [TANK, CAR, AUTO_CAR]:
                    car_num = car_num + 1
                if each_opt['sub_type'] == SOILDER:
                    soilder_num = soilder_num + 1
        if soilder_num < 2 and car_num < 3 and (soilder_num + car_num) < 3:
            if self.operator['blood'] < 2:
                if soilder_num == 0:
                    self.move_step = 20
            else:
                self.move_step = 20
        return []

    def do_tank_back(self):
        if self.observation['cities'][1]['flag'] == self.color:
            return []
        big_six = self.myLandTool.get_big_six(4030, 2)
        enemy_list = self.get_blue_opt_area(big_six, self.situation.enemy_history)
        car_num = 0
        soilder_num = 0
        for each_enemy in enemy_list:
            each_opt = each_enemy[0]
            time = each_enemy[1]
            if time > -100:
                if each_opt['sub_type'] in [TANK, CAR, AUTO_CAR]:
                    #
                    car_num = car_num + 1
                if each_opt['sub_type'] == SOILDER:
                    #
                    soilder_num = soilder_num + 1
        if soilder_num < 1 and car_num < 2 and (soilder_num + car_num) < 2:
            if self.operator['cur_hex'] != 4338:
                self.move_step = 10
        return []

    def do_blue_car_move_back(self):
        tank = self.situation.get_cur_opt_by_id(10000)
        if not tank:
            #
            for each_enemy in self.situation.enemy_operators:
                if each_enemy['sub_type'] != MISSILE:
                    if (each_enemy['cur_hex'] / 100) < 44 and (each_enemy['cur_hex'] % 100) < 33:
                        self.move_step = 10
                        return []
        #
        car_another = self.situation.get_cur_opt_by_id(10100)
        if not car_another:
            self.func_done = True
            self.move_step = 10
            return []
        return []

    def do_blue_tank_move_back(self):
        #
        for each_enemy in self.situation.enemy_operators:
            if each_enemy['sub_type'] != MISSILE:
                if (each_enemy['cur_hex'] / 100) < 44 and (each_enemy['cur_hex'] % 100) < 33:
                    self.move_step = 10
                    return []
        return []

    def do_waiting_100_5437(self):
        if len(self.operator['passenger_ids']) == 0:
            return self.action_waiting
        return []

    def do_waiting_for_get_on(self):
        if len(self.operator['passenger_ids']) > 0:
            return []
        return self.action_waiting

    def do_waiting(self):
        return self.action_waiting

    def do_waiting_for_tank(self):
        #
        enemy_list = []
        enemy_list.extend(self.get_blue_opt_area(self.area_4227_high_mountain, self.situation.enemy_history))
        enemy_list.extend(self.get_blue_opt_area(self.area_3938_road_right_up, self.situation.enemy_history))
        big_six = self.myLandTool.get_big_six(4836, 3)
        enemy_list.extend(self.get_blue_opt_area(big_six, self.situation.enemy_history))
        for each in enemy_list:
            enemy_opt = each[0]
            time = each[1]
            if time > -100:
                if enemy_opt['sub_type'] in [TANK, CAR, AUTO_CAR]:
                    return self.action_waiting
        #
        auto_car = self.situation.get_cur_opt_by_id(400)
        if auto_car:
            if self.is_can_guide(auto_car, self.operator['cur_hex']):
                return self.action_waiting
        return []

    def do_clean_200_5437(self):
        if self.is_can_guide(self.operator, 5439):
            return self.action_waiting
        return []

    def do_stop_to_shoot(self, type_list=[TANK, CAR, AUTO_CAR, SOILDER]):
        if self.is_can_attack(type_list):
            return self.action_waiting
        return []

    def do_stop_to_shoot_cars(self):
        if self.is_can_attack(CARS):
            return self.action_waiting
        return []

    def do_stop_to_shoot_car(self):
        if self.is_can_attack([CAR]):
            return self.action_waiting
        return []

    def do_set_point(self):
        if self.operator['cur_hex'] not in self.situation.clean_pos_list:
            self.situation.clean_pos_list.append(self.operator['cur_hex'])
        return []

    def do_stop_when_see_bluetank(self):
        msg = self.do_stop_when_see_enemy([TANK])
        if len(msg) > 0:
            return msg
        return []

    def do_stop_when_see_enemy(self, type_list):
        if self.is_see_enemy(type_list):
            return self.action_waiting
        return []

    def do_waiting_at_4436(self):
        if not self.is_has_myopt_in([4435]):
            return []
        if not self.is_has_myopt_in([4334]):
            self.move_step = 10
            return []
        return self.action_waiting

    def do_waiting_at_4334(self):
        if self.observation['cities'][0]['flag'] != self.color:
            if not self.is_has_myopt_in([4435]):
                self.move_step = 4
                return []
            return []
        return self.action_waiting

    def do_waiting_at_4435(self):
        if self.observation['cities'][0]['flag'] == self.color:
            if self.observation['time']['cur_step'] > 1000:
                if 4334 not in self.situation.stack_pos_list:
                    return []
        return self.action_waiting

    def do_waiting_at_4335(self):
        if self.observation['cities'][0]['flag'] != self.color:
            return []
        else:
            if self.is_has_myopt_in([4334]):
                return self.action_waiting
            else:
                return []

    def do_moveback_when_see_soilder(self):
        if self.is_see_enemy([SOILDER]):
            return []
        return self.action_waiting

    def do_waiting_10(self):
        if self.waiting_time == 0:
            self.waiting_time = 10
        self.waiting_time -= 1
        if self.waiting_time == 0:
            return []
        return self.action_waiting

    def is_see_enemy(self, type_list):
        for each_enemy in self.situation.enemy_operators:
            if each_enemy['sub_type'] in type_list:
                if each_enemy in each_enemy['see_enemy_bop_ids']:
                    return True
        return False

    def is_can_attack(self, type_list):
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] in type_list:
                if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                    ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator, self.operator['cur_hex'],
                                                                            each_enemy, self.myLandTool)
                    if ret:
                        return True
        return False

    def is_can_guide(self, guide_opt, car_pos):
        for each_enemy in self.situation.enemy_operators:
            if each_enemy['obj_id'] in guide_opt['see_enemy_bop_ids']:
                if each_enemy['sub_type'] in [TANK, CAR, AUTO_CAR]:
                    if self.situation.map.get_distance(each_enemy['cur_hex'], car_pos) <= 20:
                        return True
        return False

    def is_has_enemy_in_distance(self, pos, type_list, distance_min, distance_max):
        for each_enemy in self.situation.enemy_operators:
            if each_enemy['sub_type'] in type_list:
                dis = self.situation.map.get_distance(each_enemy['cur_hex'], pos)
                if dis <= distance_max and dis >= distance_min:
                    return True
        return False

    def is_has_cansee_enemy_in_distance(self, pos, type_list, distance_min, distance_max):
        for each_enemy in self.situation.enemy_operators:
            if each_enemy['sub_type'] in type_list:
                dis = self.situation.map.get_distance(each_enemy['cur_hex'], pos)
                if dis <= distance_max and dis >= distance_min:
                    if self.map.can_see(each_enemy['cur_hex'], pos, 0):
                        return True
        return False

    def is_has_myopt_in(self, pos_list):
        for each in self.situation.our_opt:
            if each.operator['cur_hex'] in pos_list:
                return True
        return False

    def is_has_myopt_in_aboveme(self, type_list, pos_list):
        for each in self.situation.our_opt:
            if each.operator['obj_id'] != self.operator['obj_id']:
                if each.operator['sub_type'] in type_list:
                    if each.operator['cur_hex'] in pos_list:
                        return True
        return False

    #
    def get_blue_opt_area(self, area, enemy_history):
        opt_list = []
        for enemy_opt_history in enemy_history.values():
            enemy_opt = enemy_opt_history[0]
            see_time = enemy_opt_history[1]
            is_dead = enemy_opt_history[2]
            if is_dead:
                continue
            if enemy_opt['cur_hex'] in area:
                opt_list.append(enemy_opt_history)
        return opt_list

    def is_red_car_stop(self):
        ID_CAR_RED = 100
        ID_AUTOCAR_RED = 400
        OPT_CAR_RED = self.get_bop(ID_CAR_RED)
        OPT_AUTOCAR_RED = self.get_bop(ID_AUTOCAR_RED)
        tank_blue_area_4635_maincity_down_road_left = [4533, 4534, 4535, 4536,
                                                       4632, 4633, 4634, 4635, 4637,
                                                       4733, 4734, 4735, 4736, 4737]
        car_red_area_5144_road_right = [5043, 5044, 5045, 5046,
                                        5142, 5143, 5144, 5145, 5146,
                                        5243, 5244, 5245, 5246, 5247]
        tank_blue_area_3938_road_right_up = [3837, 3838, 3839,
                                             3936, 3937, 3938, 3939,
                                             4038, 4039, 4040]
        car_red_area_4843_road_right = [4642, 4643, 4644,
                                        4741, 4742, 4743, 4744,
                                        4842, 4843, 4844]
        enemy_tank_opt = None
        for bop in self.observation['operators']:
            if bop['color'] != self.color:
                if bop['sub_type'] == TANK:
                    enemy_tank_opt = bop
                    break
        if enemy_tank_opt == None:
            return False
        dis = self.map.get_distance(enemy_tank_opt['cur_hex'], OPT_CAR_RED['cur_hex'])
        #
        if dis > 16:
            return False

        #
        if enemy_tank_opt['obj_id'] in OPT_AUTOCAR_RED['see_enemy_bop_ids']:
            return True
        #
        if enemy_tank_opt['obj_id'] in OPT_CAR_RED['see_enemy_bop_ids']:
            return True
        #
        if enemy_tank_opt['cur_hex'] in tank_blue_area_4635_maincity_down_road_left and \
                OPT_CAR_RED['cur_hex'] in car_red_area_5144_road_right:
            return True
        if enemy_tank_opt['cur_hex'] in tank_blue_area_4635_maincity_down_road_left and \
                OPT_CAR_RED['cur_hex'] in car_red_area_4843_road_right:
            return True
        if enemy_tank_opt['cur_hex'] in tank_blue_area_3938_road_right_up and \
                OPT_CAR_RED['cur_hex'] in car_red_area_4843_road_right:
            return True

        return False

    def set_move_step_all(self, command_step):

        if int(self.move_step / 10) == command_step:
            return None
        else:
            self.move_step = command_step * 10

    def do_move_step(self):
        my_id = self.operator['obj_id']
        if self.operator['cur_hex'] == my_ai.plan_pos_list[my_id][self.move_step]:  #
            if not self.auto_moving:
                self.move_step = self.move_step + 1
        msg = self.do_moving_func_list()
        if len(msg) > 0:
            return msg
        #
        if my_ai.plan_pos_list[my_id][self.move_step]:
            msg = self.do_move_to_point(my_ai.plan_pos_list[my_id][self.move_step])
            if len(msg) > 0:
                return msg
        return []

    def set_first_move_step(self):
        if self.command_num == 0:
            if self.operator['obj_id'] == 100:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 200:
                self.move_step = 0
            elif self.operator['obj_id'] == 400:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
        elif self.command_num == 1:
            if self.operator['obj_id'] == 100:
                self.move_step = 10
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 200:
                self.move_step = 10
            elif self.operator['obj_id'] == 400:
                self.move_step = 10
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
        elif self.command_num == 2:
            if self.operator['obj_id'] == 100:
                self.move_step = 20
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 200:
                self.move_step = 0
            elif self.operator['obj_id'] == 400:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
        elif self.command_num == 3:
            if self.operator['obj_id'] == 100:
                self.move_step = 50
            elif self.operator['obj_id'] == 0:
                self.move_step = 40
            elif self.operator['obj_id'] == 200:
                pass
            elif self.operator['obj_id'] == 400:
                self.move_step = 30
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0
            elif self.operator['obj_id'] == 0:
                self.move_step = 0

    @classmethod
    def class_update(cls, observation, situation):
        #
        cls.situation = situation
        cls.observation = situation.observation
        cls.our_opt = situation.our_opt
        cls.enemy_operators = situation.enemy_operators
        cls.missile_patrol_find_enemy = situation.missile_patrol_find_enemy  #
        cls.enenmy_is_coming = situation.enenmy_is_coming  #

    def update(self, operator, observation):
        self.operator = operator

    def my_update(self):
        self.seven_neighbors_list = self.myLandTool.get_big_six(self.operator['cur_hex'], 1)
        self.func_done = False
        if self.cityWanted:
            for each_city in self.observation['cities']:
                if self.cityWanted['coord'] == each_city['coord']:
                    self.cityWanted = each_city
                    break
        #
        #
        #

    def get_retmsg(self, cure_action):
        msg = []
        if cure_action.action_type == ActionType.Move:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'move_path': cure_action.move_path
            })
        elif cure_action.action_type == ActionType.Shoot:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'target_obj_id': cure_action.target_obj_id,
                'weapon_id': cure_action.weapon_id
            })
        elif cure_action.action_type == ActionType.GetOn:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'target_obj_id': cure_action.target_obj_id
            })
        elif cure_action.action_type == ActionType.GetOff:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'target_obj_id': cure_action.target_obj_id
            })
        elif cure_action.action_type == ActionType.Occupy:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type
            })
        elif cure_action.action_type == ActionType.ChangeState:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'target_state': cure_action.target_state
            })
        elif cure_action.action_type == ActionType.RemoveKeep:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type
            })
        elif cure_action.action_type == ActionType.JMPlan:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'jm_pos': cure_action.jm_pos,
                'weapon_id': cure_action.weapon_id
            })
        elif cure_action.action_type == ActionType.GuideShoot:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type,
                'target_obj_id': cure_action.target_obj_id,
                'weapon_id': cure_action.weapon_id,
                'guided_obj_id': cure_action.guided_obj_id
            })
        elif cure_action.action_type == ActionType.StopMove:
            msg.append({
                'obj_id': cure_action.cur_bop['obj_id'],
                'type': cure_action.action_type
            })
        return msg

    #
    #
    #
    def do_move_to_point(self, move_pos):
        #
        #
        #
        cur_xy = self.operator['cur_hex']
        #
        if cur_xy == move_pos and len(self.movepath) == 0:
            return []
        #
        #
        #
        if len(self.movepath) == 0 or move_pos != self.movepath[-1]:
            if self.situation.map.get_distance(self.operator['cur_hex'], move_pos) == 1:
                movepath_temp = [move_pos]
            else:
                movepath_temp = self.map.gen_move_route(cur_xy, move_pos, self.movetype)
            if len(movepath_temp) > 0:
                self.movepath = movepath_temp
                self.move2hex = self.movepath.pop(0)
            else:
                return []
        else:
            self.move2hex = self.movepath.pop(0)

        msg = self.do_move_to_nearestpoint(self.move2hex)
        if len(msg) > 0:
            return msg
        else:
            self.movepath = []
            return []
        return []

    def do_move_to_point_1(self, move_pos):
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = Move
        cure_action.XY = move_pos
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True:
            cure_action.move_path = self.map.gen_move_route(self.operator['cur_hex'], move_pos, self.movetype)
            if len(cure_action.move_path) > 0:
                return self.get_retmsg(cure_action)
        return []

    #
    def do_move_Astar(self, move_pos, enemy_list):
        #
        if self.is_moving():
            return []
        cur_xy = self.operator['cur_hex']
        #
        if cur_xy == move_pos:
            return []
        #
        if len(self.movepath) == 0 or move_pos != self.movepath[-1]:
            flg, movepath_temp = self.myLandTool.AstarFindPath_known_enemy \
                (self.operator, move_pos, enemy_list)
            if flg:
                self.movepath = movepath_temp
                self.move2hex = self.movepath.pop(0)
            else:
                return []
        else:
            self.move2hex = self.movepath.pop(0)

        return self.do_move_to_nearestpoint(self.move2hex)

    #
    def do_move_to_orderedenemy(self):
        #
        #
        for each in self.situation.shoot_list[self.operator['sub_type']]:
            for obj_bop in self.enemy_operators:
                if obj_bop['sub_type'] == each:
                    msg = self.do_move_to_point(obj_bop['cur_hex'])
                    if len(msg) > 0:
                        return msg
        return []

    def do_move_circle(self, move_pos):
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = Move
        cure_action.XY = move_pos
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True:
            dij_path = self.map.terrain.dij_CarMove(self.operator['cur_hex'], move_pos)
            cure_action.move_path.extend(dij_path)
            dij_path.reverse()
            dij_path.remove(dij_path[0])
            dij_path.append(self.operator['cur_hex'])
            cure_action.move_path.extend(dij_path)
            return self.get_retmsg(cure_action)
        return []

    #
    def do_move_to_nearestpoint(self, move_pos):

        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = Move
        cure_action.XY = move_pos
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True:
            cure_action.move_path = [
                move_pos]  #
            #
            #
            #
            #
            #
            tmp_stack_pos = move_pos
            #
            if self.operator['sub_type'] not in FLY_OPT:
                self.situation.stack_pos_list.append(tmp_stack_pos)
                self.situation.want_to_move_pos.append(tmp_stack_pos)
            #
            return self.get_retmsg(cure_action)
        else:
            self.move2hex = self.operator['cur_hex']
            return []

    #
    #
    def do_attack(self):
        #
        for each in self.situation.shoot_list[self.operator['sub_type']]:
            attack_enemy_list = []
            for obj_bop in self.enemy_operators:
                if obj_bop['sub_type'] == each:
                    attack_enemy_list.append(obj_bop)
            #
            attack_enemy_list = sorted(attack_enemy_list, key=lambda x: x['blood'])
            for obj_bop in attack_enemy_list:
                msg = self.do_fire(obj_bop)
                if len(msg) > 0:
                    return msg
        return []

    def do_fire(self, obj_bop):
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.target_obj_id = obj_bop['obj_id']
        cure_action.action_type = Shoot
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True and cure_action:
            return self.get_retmsg(cure_action)
        return []

    def do_guideshoot(self, guided_obj_id, obj_bop):
        #
        action = command_action()
        action.action_type = ActionType.GuideShoot
        action.cur_bop = self.operator
        action.guided_obj_id = guided_obj_id
        action.target_obj_id = obj_bop['obj_id']
        flg, action = self.my_check_tool.My_check_action(action)
        if flg:
            return self.get_retmsg(action)
        return []

    #
    def do_guide_attack(self):
        #
        for each in self.situation.guideshoot_list:
            attack_enemy_list = []
            for obj_bop in self.enemy_operators:
                if obj_bop['sub_type'] == each:
                    attack_enemy_list.append(obj_bop)
            #
            attack_enemy_list = sorted(attack_enemy_list, key=lambda x: x['blood'])
            for obj_bop in attack_enemy_list:
                msg = self.do_guideshoot(self.operator['launcher'], obj_bop)
                if len(msg) > 0:
                    return msg
        return []

    #
    def do_stopmove(self):
        self.movepath = []
        #
        #
        #
        #
        #
        #
        return []

    #
    def do_changestate(self, state_type):
        if self.operator['stop'] != 1:
            return []
        if self.operator['move_state'] == state_type:
            return []
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = ActionType.ChangeState
        cure_action.target_state = state_type
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True:
            return self.get_retmsg(cure_action)
        return []

    #
    def do_occupy(self):
        if self.operator['cur_hex'] in my_ai.city_poslist:  #
            for each_city in self.observation['cities']:
                if each_city['coord'] == self.operator['cur_hex']:
                    if self.color == each_city['flag']:
                        return []
                    else:
                        break
            cure_action = command_action()
            cure_action.cur_bop = self.operator
            cure_action.action_type = Occupy
            flag, cure_action = self.my_check_tool.My_check_action(cure_action)
            if flag == True:
                return self.get_retmsg(cure_action)
        return []

    #
    def do_get_on(self):
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = GetOn
        #
        #
        #
        #
        cure_action.target_obj_id = self.operator['launcher']
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True:
            return self.get_retmsg(cure_action)
        return []

    #
    def do_JM(self, pos):
        cure_action = command_action()
        cure_action.cur_bop = self.operator
        cure_action.action_type = JMPlan
        cure_action.jm_pos = pos
        flag, cure_action = self.my_check_tool.My_check_action(cure_action)
        if flag == True and cure_action:
            return self.get_retmsg(cure_action)
        return []

    #
    def is_stopping(self):
        if self.operator['move_to_stop_remain_time'] > 0:
            return True
        return False

    def is_moving(self):
        if self.operator['stop'] == 1:
            return False
        if self.operator['move_to_stop_remain_time'] > 0:
            return False
        if self.move2hex == self.operator['cur_hex']:
            return False
        return True

    def is_moving_fly(self):
        return self.is_moving()
        if self.move2hex == self.operator['cur_hex']:
            return False
        return True

    def is_enemy_moving(self, enemy_opt):
        if enemy_opt['speed'] > 0:
            return False
        return True

    #
    def get_distance_to_nearestenemy(self):
        enemy_dis = 99
        for enemy_id in self.operator['see_enemy_bop_ids']:
            for enemy_opt in self.observation['operators']:
                if enemy_id == enemy_opt['obj_id']:
                    tmp_dis = self.map.get_distance(self.operator['cur_hex'], enemy_opt['cur_hex'])
                    if tmp_dis is not None and tmp_dis < enemy_dis:
                        enemy_dis = tmp_dis
        return enemy_dis

    #
    def get_nearest_enemy(self):
        enemy_dis = 99
        res_enemy_opt = None
        res_time = -9999
        for enemy_opt_history in self.situation.enemy_history.values():

            enemy_opt = enemy_opt_history[0]
            see_time = enemy_opt_history[1]
            is_dead = enemy_opt_history[2]

            if is_dead is True:
                continue
            if self.color == BLUE:
                if enemy_opt['sub_type'] == SOILDER:
                    continue

            tmp_dis = self.map.get_distance(enemy_opt['cur_hex'], self.operator['cur_hex'])
            if tmp_dis is not None and tmp_dis < enemy_dis:
                enemy_dis = tmp_dis
                res_enemy_opt = copy.deepcopy(enemy_opt)
                res_time = see_time
        return (res_enemy_opt, res_time)

    def set_nearest_soilder(self):
        dis = 999
        self.nearest_soilder = None
        #
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['sub_type'] == SOILDER:
                enemy_dis = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt['cur_hex'])
                if enemy_dis < dis:
                    dis = enemy_dis
                    self.nearest_soilder = enemy_opt
        if dis == 999:  #
            self.nearest_soilder = None

    #
    def do_strategy_firststep(self):
        if not self.is_moving():
            return self.do_move_to_point(self.first_pos[0])
        return []

    def do_move_to_occupy(self):
        pass

    #
    #
    def do_move_to_my_city(self):
        if self.cityWanted:
            if self.cityWanted['flag'] == self.color:  #
                return []
            #
            if self.operator['cur_hex'] == self.cityWanted['coord']:
                return []
            else:  #
                msg = self.do_move_onestep_to_point(self.cityWanted['coord'])
                if len(msg) > 0:
                    return msg
        return []

    #
    def get_city_nearest_city_notprepare(self):
        dis = 9999
        city = None
        #
        for each_city in self.observation['cities']:
            if each_city['flag'] != self.color:
                if each_city['coord'] not in self.situation.wantoccupy_cities_list:
                    city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                               each_city['coord'])
                    if city_dis < dis:
                        dis = city_dis
                        city = each_city
        return city

    #
    def get_city_nearest_city_notmine(self):
        dis = 9999
        city = None
        #
        for each_city in self.observation['cities']:
            if each_city['flag'] != self.color:
                city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                           each_city['coord'])
                if city_dis < dis:
                    dis = city_dis
                    city = each_city
        return city

    #
    def get_city_not_have_myopt(self):
        dis = 9999
        city = None
        #
        for each_city in self.observation['cities']:
            if each_city['flag'] != self.color:
                city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                           each_city['coord'])
                if city_dis < dis:
                    seven_city = self.myLandTool.get_big_six(each_city['coord'], 1)
                    if self.seven_has_my_opt(seven_city):
                        continue
                    dis = city_dis
                    city = each_city

        return city

    def do_removekeep(self):
        if self.operator['blood'] > 1 and self.operator['keep'] == 1:
            cure_action = command_action()
            cure_action.cur_bop = self.operator
            cure_action.action_type = RemoveKeep
            flag, cure_action = self.my_check_tool.My_check_action(cure_action)
            if flag == True:
                return self.get_retmsg(cure_action)
        return []

    #
    #
    #
    #
    def seven_keep_distance(self, min_distance, max_distance, enemy_opt_pos, seven_list_in):
        seven_list = copy.deepcopy(seven_list_in)
        dis_enemy = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt_pos)
        for each_pos in seven_list[::-1]:
            distance = self.situation.map.get_distance(each_pos, enemy_opt_pos)
            if (dis_enemy < min_distance and distance <= dis_enemy) or \
                    (dis_enemy >= min_distance and distance < min_distance):
                seven_list.remove(each_pos)
            if (dis_enemy > max_distance and distance >= dis_enemy) or \
                    (dis_enemy <= max_distance and distance > max_distance):
                seven_list.remove(each_pos)
        return seven_list

    def seven_keep_distance_includeequal(self, min_distance, max_distance, enemy_opt_pos, seven_list_in):
        seven_list = copy.deepcopy(seven_list_in)
        dis_enemy = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt_pos)
        for each_pos in seven_list[::-1]:
            distance = self.situation.map.get_distance(each_pos, enemy_opt_pos)
            if (dis_enemy < min_distance and distance < dis_enemy) or \
                    (dis_enemy >= min_distance and distance < min_distance):
                seven_list.remove(each_pos)
            if (dis_enemy > max_distance and distance > dis_enemy) or \
                    (dis_enemy <= max_distance and distance > max_distance):
                seven_list.remove(each_pos)
        return seven_list

    def seven_is_townorjungle(self, seven_list_in):
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            if self.myLandTool.is_town(each_xy) or self.myLandTool.is_town(each_xy):  #
                pass
            else:
                seven_list.remove(each_xy)
        return seven_list

    def seven_canattack_enemy(self, enemy_opt, seven_list_in):
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator, each_xy, enemy_opt, self.myLandTool)
            if not ret:
                seven_list.remove(each_xy)
        return seven_list

    def seven_cannot_be_attacked(self, seven_list_in, attack_list=[]):
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            can_be_attacked = False
            for each_enemy in self.situation.enemy_operators:
                if each_enemy['sub_type'] == MISSILE:
                    continue
                if each_enemy['obj_id'] in attack_list:
                    continue
                if self.map.can_see(each_enemy['cur_hex'], each_xy, 0):
                    if each_enemy['sub_type'] == SOILDER:
                        if self.situation.map.get_distance(each_enemy['cur_hex'], each_xy) < 10:
                            can_be_attacked = True
                            break
                    else:
                        if self.situation.map.get_distance(each_enemy['cur_hex'], each_xy) < 15:
                            can_be_attacked = True
                            break
            if can_be_attacked:
                seven_list.remove(each_xy)
        return seven_list

    def seven_has_enemy(self, seven_list):
        for each_enemy in self.enemy_operators:
            if each_enemy['cur_hex'] in seven_list:
                return True
        return False

    def seven_has_my_opt(self, seven_list):
        for my_enemy in self.situation.our_opt:
            if my_enemy.operator['cur_hex'] in seven_list:
                return True
        return False

    def seven_not_stacked(self, seven_list_in):
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            if each_xy in self.situation.stack_pos_list:
                seven_list.remove(each_xy)
        return seven_list

    def seven_cannot_artillery_attacked(self, seven_list_in):
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            if each_xy in self.situation.artillery_pos_list:
                #
                goto_city = False
                for each_city in self.observation['cities']:
                    if each_city['coord'] == each_xy and each_city['flag'] != self.color:
                        goto_city = True
                        break
                if not goto_city:
                    seven_list.remove(each_xy)
        return seven_list

    def seven_in_mycity_seven(self, seven_list_in, city_seven):
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            if each_xy not in city_seven:
                seven_list.remove(each_xy)
        return seven_list

    def seven_attack_enemy_abovesoilder(self, seven_list_in):
        seven_list = []
        for each_xy in seven_list_in[::-1]:
            for each_enemy in self.enemy_operators:
                if each_enemy['sub_type'] != SOILDER:
                    ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator, each_xy, each_enemy,
                                                                            self.myLandTool)
                    if ret:
                        seven_list.append(each_xy)
                        break
        return seven_list

    def seven_is_town_or_jungle(self, seven_list_in):
        seven_list = []
        for each_xy in seven_list_in:
            if self.myLandTool.is_town(each_xy) or self.myLandTool.is_jungle(each_xy):  #
                seven_list.append(each_xy)
            return seven_list

    def do_move_onestep_to_point(self, xy):
        seven_list = self.seven_neighbors_list
        #
        temp_pos_list = self.seven_cannot_artillery_attacked(seven_list)
        if len(temp_pos_list) > 0:
            seven_list = temp_pos_list
        #
        dis = -1
        temp_pos_list = self.seven_keep_distance(dis, dis, xy, seven_list)
        if len(temp_pos_list) > 0:
            #
            #
            seven_list = temp_pos_list
        else:

            temp_pos_list = self.seven_keep_distance_includeequal(dis, dis, xy, seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
        #
        temp_pos_list = self.seven_not_stacked(seven_list)
        if len(temp_pos_list) > 0:
            seven_list = temp_pos_list
        #
        if self.operator['cur_hex'] in seven_list:
            return self.action_waiting
        #
        if len(seven_list) == 0:
            return []
        pos = seven_list[random.randint(0, len(seven_list) - 1)]
        return self.do_move_to_point(pos)

    def do_hide(self):
        if self.is_need_to_hide():
            return self.do_changestate(Hide)
        return []

    def is_need_to_hide(self):
        return True

    def set_func_list_32(self):
        #
        self.moving_func_list[(100, 6048, None)] = [self.do_get_off_0]
        #
        self.moving_func_list[(100, 4539, 1)] = [self.do_move_to4536_100at4539, self.do_get_off_safe,
                                                 self.do_waiting_for_autocar_first, self.do_waiting_100_at_4539]

        self.moving_func_list[(100, 4536, 6)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                 self.do_waiting_for_autocar_first]

        #
        #
        #
        self.moving_func_list[(100, None, 0)] = [self.do_waiting_for_tank]
        self.moving_func_list[(100, 4537, 2)] = [self.do_stop_to_shoot, self.do_waiting_for_autocar_first]

        #
        self.moving_func_list[(200, 6048, None)] = [self.do_get_on_red_0_1]
        #
        self.moving_func_list[(200, None, 0)] = [self.do_stop_to_guild, self.do_stop_to_shoot_cars]
        self.moving_func_list[(200, 4435, None)] = [self.do_waiting_200_4435]

        self.moving_func_list[(200, 4334, None)] = [self.do_waiting_200_4334]
        self.moving_func_list[(200, 4436, None)] = [self.do_waiting_200_4436]
        #
        self.moving_func_list[(400, 4945, 1)] = [self.do_stop_to_guide4945]
        self.moving_func_list[(400, None, 2)] = [self.do_waiting_when_see_enemy_soilder]
        self.moving_func_list[(400, None, 3)] = [self.do_waiting_when_see_enemy_soilder]
        self.moving_func_list[(400, 4537, None)] = [self.do_stop_to_shoot]

        #
        #
        #

        self.moving_func_list[(0, 4335, 1)] = [self.do_waiting_red_tank_4335_1]
        self.moving_func_list[(0, 4435, 2)] = [self.do_waiting_red_tank_4435_2]

        #

        self.moving_func_list[(0, 4436, 3)] = [self.do_waiting_red_tank_4436_3, self.do_hide_for_soilder_0_4436]

        self.moving_func_list[(0, 4338, None)] = [self.do_move_back_red_tank]

        self.moving_func_list[(0, 4535, 24)] = [self.do_waiting_red_tank_4535]
        self.moving_func_list[(0, 4435, 25)] = [self.do_waiting_red_tank_4435]
        self.moving_func_list[(0, 4335, 26)] = [self.do_waiting_red_tank_4335]

        self.moving_func_list[(0, 4030, None)] = [self.do_moveto4029_red_tank_4030]
        self.moving_func_list[(0, 3929, 53)] = [self.do_moveto4030_red_tank_3929]
        #
        #
        self.moving_func_list[(701, 4030, None)] = [self.do_back_to_4436]

        #

        self.moving_func_list[(10100, 4333, None)] = [self.do_get_off_safe, self.do_moveback_to_4031_bluecar]
        self.moving_func_list[(10100, 4133, None)] = [self.do_get_off_safe, self.do_moveback_to_4031_bluecar]

        self.moving_func_list[(10100, 4031, 11)] = [self.do_hide, self.do_waiting_10101_4031]
        self.moving_func_list[(10100, 3930, 12)] = [self.do_hide, self.do_waiting_10101_4031]

        #
        self.moving_func_list[(10200, 3426, None)] = [self.do_get_on_blue_0]
        #

        self.moving_func_list[(10200, 4435, None)] = [self.do_stop_to_shoot, self.do_waiting_at_4435]

        #

        self.moving_func_list[(10101, 4332, None)] = [self.do_get_off_safe, self.do_hide, self.do_blue_car_move_back,
                                                      self.do_waiting_10101_4332]
        self.moving_func_list[(10101, 4334, None)] = [self.do_hide, self.do_blue_car_move_back]
        self.moving_func_list[(10101, 4031, 11)] = [self.do_hide, self.do_waiting_10101_4031]
        self.moving_func_list[(10101, 3930, 12)] = [self.do_hide, self.do_waiting_10101_4031]
        #
        #
        #
        #
        #
        #
        self.moving_func_list[(10201, 3526, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(10201, 4334, 2)] = [self.do_set_point, self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, 4335, 3)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, 4436, 4)] = [self.do_stop_to_shoot_cars, self.do_waiting_at_4436]
        self.moving_func_list[(10201, 4334, 11)] = [self.do_stop_to_shoot_cars, self.do_waiting_at_4334]
        self.moving_func_list[(10201, 4335, 10)] = [self.do_stop_to_shoot_cars, self.do_waiting_at_4335]

        self.moving_func_list[(10201, 4435, 5)] = [self.do_stop_to_shoot_cars, self.do_waiting_at_4435]

        #
        #

        #
        self.moving_func_list[(10000, 4938, None)] = [self.do_backto4937_10000_4938]
        self.moving_func_list[(10000, 4937, None)] = [self.do_backto4938_10000_4937]
        self.moving_func_list[(10000, 4437, None)] = [self.do_backto4436_10000_4437]
        self.moving_func_list[(10000, 4029, None)] = [self.do_backto4129_10000_4029]

    #
    def set_func_list_8_2(self):
        #
        self.moving_func_list[(100, 4444, None)] = [self.do_get_off_0]
        self.moving_func_list[(100, 4244, None)] = [self.do_get_off_safe, self.do_waiting_100_s82_4244]
        #
        #
        self.moving_func_list[(200, None, None)] = [self.do_stop_to_shoot]
        #
        self.moving_func_list[(200, 3739, None)] = [self.do_stop_to_shoot_cars, self.do_set_point,
                                                    self.do_waiting_atseccity]
        self.moving_func_list[(200, 3639, None)] = [self.do_stop_to_shoot_cars, self.do_set_point]
        self.moving_func_list[(200, 3636, None)] = [self.do_stop_to_shoot_cars, self.do_set_point,
                                                    self.do_waiting_atmaincity]
        #
        self.moving_func_list[(400, 4245, None)] = [self.do_waiting_400_s82_4245]
        #
        self.moving_func_list[(0, 3841, 1)] = [self.do_moveto3941_0_s82_3841]
        self.moving_func_list[(0, 3940, 2)] = [self.do_moveto3941_0_s82_3841, self.do_tank_goback]
        #
        #
        self.moving_func_list[(0, 3941, 13)] = [self.do_waiting_0_s82_3941, self.do_charge_city_0_s82_3941]
        self.moving_func_list[(0, 3640, None)] = [self.do_waiting_0_s82_3640, self.do_tank_goback]
        self.moving_func_list[(0, 3639, None)] = [self.do_waiting_0_s82_3639]
        self.moving_func_list[(0, 3539, None)] = [self.do_tank_goback]
        self.moving_func_list[(0, 3740, 13)] = [self.do_waiting_0_s82_3740]
        self.moving_func_list[(0, None, 15)] = [self.do_waiting_0_s82_3737]
        self.moving_func_list[(0, 3737, 16)] = [self.do_waiting_0_s82_3737]
        self.moving_func_list[(0, 3736, 17)] = [self.do_waiting_0_s82_3736]
        #
        self.moving_func_list[(700, None, None)] = [self.do_attackcar_missile]

        #
        self.moving_func_list[(701, None, None)] = [self.do_attackcar_missile]
        #
        #
        self.moving_func_list[(10100, 3334, None)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                      self.do_waiting_10100_s82_3334]
        self.moving_func_list[(10100, 3637, None)] = [self.do_get_off_safe, self.do_stop_to_shoot,
                                                      self.do_waiting_10100_s82_3637]
        self.moving_func_list[(10100, 3737, None)] = [self.do_stop_to_shoot,
                                                      self.do_waiting_10100_s82_3737]
        #
        self.moving_func_list[(10200, 3329, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(10200, 3637, 0)] = [self.do_stop_to_shoot_cars, self.do_changepath_10200_s82_0]
        self.moving_func_list[(10200, None, 1)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, None, 2)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, None, 3)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, None, 21)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10200, 3736, None)] = [self.do_stop_to_shoot_cars, self.do_set_point,
                                                      self.do_waiting_10200_s82_3736]
        self.moving_func_list[(10200, 3737, None)] = [self.do_set_point]
        self.moving_func_list[(10200, 3639, None)] = [self.do_stop_to_shoot_cars, self.do_set_point,
                                                      self.do_waiting_10200_s82_3639]
        self.moving_func_list[(10200, 3738, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_10200_s82_3738]

        self.moving_func_list[(10200, 3636, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_atmaincity,
                                                      self.do_set_point]
        self.moving_func_list[(10200, 3739, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_atseccity]

        #
        self.moving_func_list[(10101, 3534, None)] = [self.do_get_off_safe, self.do_stop_to_shoot, self.do_hide,
                                                      self.do_waiting_10101_s82_3534]
        #
        self.moving_func_list[(10201, 3429, None)] = [self.do_get_on_blue_0]
        self.moving_func_list[(10201, None, 0)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 1)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 2)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 3)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 4)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, None, 5)] = [self.do_stop_to_shoot_cars]
        self.moving_func_list[(10201, 3636, None)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars,
                                                      self.do_waiting_atmaincity, self.do_set_point]
        self.moving_func_list[(10201, 3739, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_atseccity]
        self.moving_func_list[(10201, 3639, None)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars,
                                                      self.do_set_point, self.do_waiting_10201_s82_3639]
        self.moving_func_list[(10201, 3640, None)] = [self.do_stop_to_shoot_cars, self.do_set_point]
        self.moving_func_list[(10201, 3637, None)] = [self.do_stop_to_shoot_cars, self.do_waiting_10201_s82_3637]
        self.moving_func_list[(10201, 3738, None)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars,
                                                      self.do_waiting_10201_s82_3738]
        self.moving_func_list[(10201, 3736, None)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars,
                                                      self.do_set_point]
        self.moving_func_list[(10201, 3737, None)] = [self.do_keepmove_bluesoilder_s82, self.do_stop_to_shoot_cars,
                                                      self.do_set_point]
        #
        self.moving_func_list[(10000, 4040, None)] = [self.do_tank_goback]
        self.moving_func_list[(10000, 3940, None)] = [self.do_move_10000_s82_3940]

        self.moving_func_list[(10000, 3944, None)] = [self.do_set_point, self.do_stop_to_shoot_car,
                                                      self.do_move_10000_s82_3944]

        self.moving_func_list[(10000, None, 0)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(10000, None, 1)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(10000, None, 2)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(10000, None, 3)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(10000, None, 4)] = [self.do_stop_to_shoot_car, self.do_moveaway_blue_tank_s82]
        self.moving_func_list[(10000, None, 5)] = [self.do_stop_to_shoot_car, self.do_moveaway_blue_tank_s82]
        self.moving_func_list[(10000, 3740, 11)] = [self.do_moveseccity_bluetank_s82_3740,
                                                    self.do_move_to_main_bluetank_s82]
        self.moving_func_list[(10000, 3640, 12)] = [self.do_moveseccity_bluetank_s82_3740,
                                                    self.do_move_to_main_bluetank_s82, self.do_tank_goback]
        self.moving_func_list[(10000, 3639, 18)] = [self.do_moveseccity_bluetank_s82_3639,
                                                    self.do_move_to_main_bluetank_s82]

        self.moving_func_list[(10000, 3736, 14)] = [self.do_move_10000_s82_3736, self.do_move_to_sec_bluetank_s82]
        self.moving_func_list[(10000, 3737, 20)] = [self.do_move_10000_s82_3737]
        self.moving_func_list[(10000, 3637, 15)] = [self.do_tank_goback]
        #
        self.moving_func_list[(10001, 4242, None)] = [self.do_set_point, self.do_stop_to_shoot_car,
                                                      self.do_move_10001_s82_4242]

        self.moving_func_list[(10001, None, 0)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(10001, None, 1)] = [self.do_stop_to_shoot_car]
        self.moving_func_list[(10001, None, 2)] = [self.do_stop_to_shoot_car, self.do_moveaway_blue_tank_s82]
        self.moving_func_list[(10001, None, 3)] = [self.do_stop_to_shoot_car, self.do_moveaway_blue_tank_s82]

        self.moving_func_list[(10001, 3740, 11)] = [self.do_moveseccity_bluetank_s82_3740,
                                                    self.do_waiting_10000_to_3640_s82,
                                                    self.do_move_to_main_bluetank_s82]
        self.moving_func_list[(10001, 3640, 12)] = [self.do_moveseccity_bluetank_s82_3740,
                                                    self.do_move_to_main_bluetank_s82, self.do_tank_goback]
        self.moving_func_list[(10001, 3639, 18)] = [self.do_moveseccity_bluetank_s82_3639,
                                                    self.do_move_to_main_bluetank_s82]

        self.moving_func_list[(10001, 3736, 14)] = [self.do_move_10000_s82_3736, self.do_move_to_sec_bluetank_s82]
        self.moving_func_list[(10001, 3737, 20)] = [self.do_move_10000_s82_3737]
        self.moving_func_list[(10001, 3637, 15)] = [self.do_tank_goback]


class ai_tank_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 20
        self.movetype = MoveType_car  #
        self.target2move = -1
        self.old_enemy_cur_hex = -1
        self.final_xy = -1

        #

        self.target = None  #
        self.cal_history = {}  #
        self.node_id = ''
        self.cal_step = -1  #

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        if self.color == RED:
            if self.operator['C3'] > 0:
                self.shoot_range = 20
            else:
                self.shoot_range = 5
        else:
            self.shoot_range = 5
            pass

    def do_s1_action(self):
        if not self.is_moving():
            self.my_update()
            #
            msg = self.do_occupy()
            if len(msg) > 0:
                return msg
            #
            if self.situation.final_occupy:
                return self.do_moveandprotect_cities()
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
        return []

    #
    #
    def is_same_target(self, enemy_opt):
        if enemy_opt is None or self.target is None:
            return False

        tmp_obj_id = enemy_opt['obj_id']
        tmp_hex = enemy_opt['cur_hex']

        #
        if enemy_opt['obj_id'] != self.target['obj_id']:
            return False

        tmp_cal_res = self.cal_history.get((tmp_obj_id, tmp_hex))
        #
        if tmp_cal_res is None:
            return False

        return True

    #
    def do_move_to_attack(self):
        #
        #
        tmp_targe, last_time = self.get_nearest_enemy()
        if tmp_targe is None:
            return []

        return self.do_move_to_attack_Aopt(tmp_targe)

    #
    def do_move_to_attack_Aopt(self, tmp_targe):

        #
        if self.is_same_target(tmp_targe) and self.situation.is_same_situation(self.cal_step):
            #
            if self.target['sub_type'] == SOILDER and \
                    self.map.get_distance(self.operator['cur_hex'], self.target['cur_hex']) < 7:
                for opt in self.situation.our_opt:

                    if opt.operator['sub_type'] == MISSILE:
                        opt.target2atk = self.target['obj_id']
            if self.movepath == []:
                return self.do_move_to_attack_Aopt_keepdistance(self.target, 2)
            else:
                return self.do_move_to_point(self.movepath[-1])
        #
        else:
            self.target = tmp_targe
            enemy_xy = tmp_targe['cur_hex']
            enemy_id = tmp_targe['obj_id']
            cur_xy = self.operator['cur_hex']

            if self.color == BLUE or self.color == RED:
                self.cal_step = self.situation.cur_step
                return self.do_move2atk_plus()

            if self.map.can_see(cur_xy, enemy_xy, 0) is False or self.target['sub_type'] == SOILDER:
                #
                return self.do_move_to_attack_Aopt_near(tmp_targe, 5)
            else:
                #
                return self.do_move_to_attack_Aopt_keepdistance(tmp_targe, 2)

    #
    def do_move_to_attack_Aopt_near(self, tmp_targe, r=5):
        enemy_xy = tmp_targe['cur_hex']
        enemy_id = tmp_targe['obj_id']
        cur_xy = self.operator['cur_hex']
        cur_dis = self.map.get_distance(self.operator['cur_hex'], self.target['cur_hex'])
        if cur_dis < r:
            r = cur_dis
        select_xy_list = self.myLandTool.get_big_six(enemy_xy, r)
        move_xy, res = self.myLandTool.get_atk_pos(self.operator, self.target, select_xy_list)
        if move_xy is None:
            return []
        self.cal_history[(enemy_id, enemy_xy)] = move_xy
        #
        return self.do_move_Astar(move_xy, [self.target])

    #
    def do_move_to_attack_Aopt_keepdistance(self, tmp_targe, r=2):
        enemy_xy = tmp_targe['cur_hex']
        enemy_id = tmp_targe['obj_id']
        cur_xy = self.operator['cur_hex']
        cur_dis = self.map.get_distance(self.operator['cur_hex'], self.target['cur_hex'])
        select_xy_list = self.myLandTool.get_big_six(cur_xy, r, r - 1)

        move_xy, res = self.myLandTool.get_atk_pos(self.operator, self.target, select_xy_list)
        if move_xy is None:
            return []
        self.cal_history[(enemy_id, enemy_xy)] = move_xy  #
        #
        return self.do_move_to_point(move_xy)

    #
    #
    #
    #
    #
    def do_move2atk_plus(self):

        if self.target is None:
            return []

        enemy_id = self.target['obj_id']

        #
        #

        target_type = self.target['sub_type']
        enemy_xy = self.target['cur_hex']
        m_cd = self.operator['weapon_cool_time']
        cur_xy = self.operator['cur_hex']
        move_xy = None
        min_atk_r = self.shoot_range

        if target_type == SOILDER:
            min_atk_r = 10

        if self.myLandTool.is_jungle(enemy_xy) \
                or self.myLandTool.is_town(enemy_xy):
            min_atk_r /= 2

        dis = self.map.get_distance(cur_xy, enemy_xy)

        ql = self.myLandTool.get_quadrant_big(enemy_xy, cur_xy)

        #
        if dis <= min_atk_r and dis <= self.shoot_range and self.map.can_see(cur_xy, enemy_xy, 0):
            rev = 0
            select_xy_list = self.myLandTool.get_big_six(cur_xy, int(m_cd / 20) + 3)
        else:
            rev = 1
            select_xy_list = self.myLandTool.get_big_six(enemy_xy, min_atk_r, min_atk_r - 3, ql)

        #
        define_fire_range = self.myLandTool.get_big_six(enemy_xy, 20, quadrant_list=ql)
        unsight_list = []
        for xy in define_fire_range:
            if self.map.can_see(enemy_xy, xy, 0) is False:
                unsight_list.append(xy)
        #
        connect_list_list = self.myLandTool.get_connect_set(unsight_list)

        res_fire_xy_tuple_list = []
        for cnt_list in connect_list_list:
            dis = self.myLandTool.get_distance_list2list(cnt_list, [cur_xy])
            if dis >= 2:
                continue
            edge_list = self.myLandTool.get_edge(cnt_list)
            for xy in edge_list[::-1]:
                tmp_dis = self.map.get_distance(enemy_xy, xy)
                if tmp_dis is None or tmp_dis > 10:
                    edge_list.remove(xy)
                    continue

            move_xy, estimate_res = self.myLandTool.get_atk_pos(self.operator, self.target, edge_list)

            res_fire_xy_tuple_list.append((move_xy, estimate_res))

        sorted(res_fire_xy_tuple_list, key=lambda x: x[1], reverse=True)
        if len(res_fire_xy_tuple_list) > 0:
            move_xy = res_fire_xy_tuple_list[0][0]
            #
            forbid_list = self.situation.get_fire_zone_list()

            #
            #
            #
            #
            #
        #
        #
        if move_xy is None:
            move_xy = -1
        self.cal_history[(enemy_id, enemy_xy)] = move_xy

        #
        if move_xy != -1:
            if rev == 1:
                astarres = self.myLandTool.AstarFindPath_known_enemy(self.operator, move_xy, [self.target], forbid_list)
                if astarres[0] is True:
                    self.movepath = astarres[1]

            else:
                tmp_path = self.map.gen_move_route(cur_xy, move_xy, 0)
                if len(tmp_path) > 1:
                    self.movepath = tmp_path

            return self.do_move_to_point(move_xy)
        else:
            return []

    #
    def do_move_one_step_keepdistance(self):
        #
        #

        dis_nearest = 9999
        #

        #
        tmp_targe, last_time = self.get_nearest_enemy()
        if tmp_targe is None:
            return []
        dis_nearest = self.map.get_distance(self.operator['cur_hex'], tmp_targe['cur_hex'])
        self.myLandTool.my_firetool.get_safe_dis(self.operator, tmp_targe)

        if dis_nearest < 25:  #
            max_distance = 15
            min_distance = max_distance - 1
            for each_pos in self.seven_neighbors_list[::-1]:
                #
                #
                distance = self.situation.map.get_distance(each_pos, tmp_targe['cur_hex'])
                if distance < min_distance and distance < dis_nearest:
                    self.seven_neighbors_list.remove(each_pos)
                if distance > max_distance and distance > dis_nearest:
                    self.seven_neighbors_list.remove(each_pos)
            #
            #
            temp_pos_list = copy.deepcopy(self.seven_neighbors_list)
            temp_pos_list = self.get_poslist_cansee(tmp_targe['cur_hex'], temp_pos_list)
            if len(temp_pos_list) > 0:
                self.seven_neighbors_list = temp_pos_list
            #
            #
            #
            #
            #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        if len(self.seven_neighbors_list) == 0:
            return []
        pos = self.seven_neighbors_list[random.randint(0, len(self.seven_neighbors_list) - 1)]
        return self.do_move_to_point(pos)

    #
    def get_poslist_cansee(self, target_pos, pos_list):
        for each_pos in pos_list[::-1]:
            if not self.map.can_see(each_pos, target_pos, 0):
                pos_list.remove(each_pos)
        return pos_list

    #
    def do_move_to_assist_occupy(self):
        if self.situation.fight_step == ALL_ASSISTOCCUPY_STEP or \
                self.situation.fight_step == ALL_ATTACKI_STEP or \
                self.situation.fight_step == ALL_OCCUPY_STEP:
            pass
        else:
            return []
        self.set_nearest_soilder()
        if self.is_move_to_assist_occupy():
            seven_list = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
            #
            temp_pos_list = self.seven_not_stacked(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_cannot_artillery_attacked(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            if self.is_move_to_enemy_soilder():  #
                dis = 10
            else:  #
                dis = 11
            temp_pos_list = self.seven_keep_distance(dis, dis, self.nearest_soilder['cur_hex'], seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:
                #
                temp_pos_list = self.seven_keep_distance_includeequal(dis, dis, self.nearest_soilder['cur_hex'],
                                                                      seven_list)
                if len(temp_pos_list) > 0:
                    seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_cannot_be_attacked(seven_list, attack_list=[self.nearest_soilder['obj_id']])
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_is_townorjungle(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            if self.operator['C3'] > 0:
                if self.operator['cur_hex'] in seven_list:
                    return self.action_waiting

            #
            if len(seven_list) == 0:
                return []

            pos = seven_list[random.randint(0, len(seven_list) - 1)]
            return self.do_move_to_point(pos)
        return []

    #
    def is_move_to_enemy_soilder(self):
        if self.operator['weapon_cool_time'] > 20:
            return False
        if self.nearest_soilder['keep'] == 1 or self.nearest_soilder['cur_pos'] > 0 or \
                self.nearest_soilder['weapon_cool_time'] > 41:
            return True
        return False

    #
    def is_move_to_assist_occupy(self):
        #
        if self.is_fighting_near_city():  #
            return True
        return False

    #
    def can_attack_atcurpos(self):
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['obj_id'] in self.operator['see_enemy_bop_ids']:
                if enemy_opt['sub_type'] == SOILDER:  #
                    #
                    #
                    if enemy_opt['speed'] > 0 and self.operator['move_to_stop_remain_time'] > 0:

                        enemy_stopremaintime = int((720 / enemy_opt['basic_speed']) * (1 - enemy_opt['speed']))
                        my_stopremaintime = int((720 / self.operator['basic_speed']))
                        if my_stopremaintime < enemy_stopremaintime:
                            continue
                ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                        self.operator['cur_hex'],
                                                                        enemy_opt,
                                                                        self.myLandTool)
                if ret:
                    return True
        return False

    #
    def is_fighting_near_city(self):
        if not self.nearest_soilder:
            return False
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['sub_type'] == SOILDER:
                enemy_dis = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                            self.nearest_soilder['cur_hex'])
                if enemy_dis < 3:
                    return True
        return False

    #
    def is_protecting_city(self):
        for each_city in self.observation['cities']:
            if each_city['flag'] == self.color:
                if each_city['coord'] in self.seven_neighbors_list:
                    return True
        return False

    #
    def do_moveandprotect_cities(self):
        if self.situation.fight_step == ALL_OCCUPY_STEP:
            pass
        else:
            return []
        if self.cityWanted:  #
            self.change_to_nearcity()
        #
        msg = self.do_protect_my_city()
        if len(msg) > 0:
            return msg
        #
        self.get_wantedcity()
        #
        msg = self.do_move_to_my_city()
        if len(msg) > 0:
            return msg
        #
        #
        #
        #
        #
        #
        return []

    #
    def get_wantedcity(self):
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notprepare()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notmine()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        return None

    #
    def change_to_nearcity(self):
        city_dis_my_city = self.situation.map.get_distance(self.operator['cur_hex'],
                                                           self.cityWanted['coord'])
        if city_dis_my_city <= 2:
            return
        for each_city in self.observation['cities']:
            city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                       each_city['coord'])
            if each_city['flag'] != self.color and each_city['coord'] != self.cityWanted['coord']:
                if city_dis <= 2:  #
                    if each_city['coord'] in self.situation.wantoccupy_cities_list:
                        for each_opt in self.situation.our_opt:
                            if each_opt.operator['sub_type'] == SOILDER:
                                if each_opt.operator['obj_id'] == self.operator['obj_id']:
                                    continue
                                if each_opt.cityWanted and each_opt.cityWanted['coord'] == each_city['coord']:
                                    #
                                    city_dis2 = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                                                each_city['coord'])
                                    if city_dis2 > city_dis:
                                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                                        self.cityWanted = each_city
                                        city_dis_my_city = city_dis
                                        each_opt.cityWanted = None
                                    break
                if city_dis < city_dis_my_city:  #
                    if each_city['coord'] not in self.situation.wantoccupy_cities_list:
                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
            if each_city['flag'] == self.color:
                if city_dis <= 2:
                    seven_city = self.myLandTool.get_big_six(each_city['coord'], 1)
                    seven_city_2 = self.myLandTool.get_big_six(each_city['coord'], 2)
                    if self.seven_has_enemy(seven_city_2) and (not self.seven_has_my_opt(seven_city)):
                        self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
        return None

    #
    def is_protect_my_city(self):
        #
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['obj_id'] != self.operator['obj_id']:
                if each_opt.cityWanted and each_opt.cityWanted['coord'] == self.cityWanted['coord'] \
                        and each_opt.operator['cur_hex'] in self.seven_cityWanted:
                    return False
        #
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] not in FLY_OPT:
                enemy_dis = self.situation.map.get_distance(self.cityWanted['coord'],
                                                            each_enemy['cur_hex'])
                if each_enemy['sub_type'] == SOILDER:  #
                    if enemy_dis <= 3:
                        return True
                else:  #
                    if enemy_dis <= 5:
                        return True
        return False

    #
    def do_protect_my_city(self):
        #
        if self.cityWanted and self.cityWanted['flag'] == self.color:
            self.seven_cityWanted = self.myLandTool.get_big_six(self.cityWanted['coord'], 1)
            if self.is_protect_my_city():
                if self.operator['cur_hex'] in self.seven_cityWanted:
                    #
                    #
                    #
                    my_seven = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
                    #
                    temp_pos_list = self.seven_in_mycity_seven(my_seven, self.seven_cityWanted)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list

                    #
                    temp_pos_list = self.seven_cannot_artillery_attacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    temp_pos_list = self.seven_not_stacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    for each_enemy in self.enemy_operators:
                        if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                            ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                                    self.operator['cur_hex'],
                                                                                    each_enemy, self.myLandTool)

                            if ret:
                                return self.action_waiting
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #

                    #
                    temp_pos_list = self.seven_is_town_or_jungle(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    if self.operator['cur_hex'] in my_seven:
                        return self.action_waiting
                    #
                    if self.cityWanted['coord'] in my_seven:
                        return self.do_move_onestep_to_point(self.cityWanted['coord'])
                    #
                    if len(my_seven) == 0:
                        return []
                    pos = my_seven[random.randint(0, len(my_seven) - 1)]
                    return self.do_move_to_point(pos)
                else:
                    return self.do_move_onestep_to_point(self.cityWanted['coord'])
            else:
                self.cityWanted = None
                return []
        return []


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
class ai_car_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 20
        self.movetype = MoveType_car  #
        self.FoundBestSeePosition = False
        self.send_missile = False
        ai_car_operator.select_cities_list = []
        self.city_first_step = None

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        if self.color == RED:
            if self.operator['C3'] > 0:
                self.shoot_range = 20
            else:
                self.shoot_range = 10
        else:
            if self.operator['C3'] > 0:
                self.shoot_range = 20
            else:
                self.shoot_range = 13

    def do_strategy_firststep(self):
        if not self.is_moving() and self.observation['time']['cur_step'] >= 75:
            msg = self.do_move_to_point(self.first_pos[0])
            return msg
        return []

    def do_auto(self):
        if self.enenmy_is_coming == True:
            if len(self.operator['passenger_ids']) <= 1:  #
                msg = self.do_attack()
                if len(msg) > 0:
                    return msg
                else:
                    if self.operator['stop'] == True:
                        msg = self.do_getoff()
                        if len(msg) > 0:
                            return msg
            else:  #
                enemy_see_me = False
                for enemy_bop in self.observation['operators']:
                    if enemy_bop['color'] == self.color:
                        continue
                    if self.map.get_distance(enemy_bop['cur_hex'], self.operator['cur_hex']) > 20:
                        continue
                    if self.map.can_see(enemy_bop['cur_hex'], self.operator['cur_hex'], 0) == True:
                        #
                        enemy_see_me = True
                        circle = 2
                        opt_neighbors_circle = self.myLandTool.get_neighbors_circle(
                            self.operator['cur_hex'], circle)
                        villege_list, tree_list = self.myLandTool.get_villege_tree_list(
                            opt_neighbors_circle)
                        pos_list = []
                        pos_list.extend(villege_list)
                        pos_list.extend(tree_list)
                        if pos_list:
                            move_pos = self.myLandTool.get_closet_positon(
                                self.operator['cur_hex'], pos_list)
                        else:
                            move_pos = self.myLandTool.get_def_position(
                                self, self.operator['cur_hex'], enemy_bop['cur_hex'], -1, 3)
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
                        break
                if enemy_see_me == False:  #
                    if self.operator['stop'] == True:
                        msg = self.do_getoff()
                        if len(msg) > 0:
                            return msg
        else:
            if self.operator['stop'] == True:
                msg = self.do_getoff()
                if len(msg) > 0:
                    return msg
        return []

    def do_auto_blue(self):
        if self.operator['C3'] > 0:
            self.shoot_range = 20
        else:
            self.shoot_range = 13
        msg = self.do_getoff()
        if len(msg) > 0:
            return msg
        if self.enenmy_is_coming == True:
            msg = self.do_attack()
            if len(msg) > 0:
                return msg
        else:
            pass
        return []

    def do_move_to_BestPosition(self):
        if self.operator['passenger_ids'] == []:  #
            if self.FoundBestSeePosition == False:
                pos_list = self.situation.myLandTool.getPoint_nicesight_toXYaround(self.operator,
                                                                                   self.cityWanted['coord'],
                                                                                   start_mv_r=6)
                if pos_list:
                    move_pos = pos_list[0]
                    msg = self.do_move_to_point(move_pos)
                    if len(msg) > 0:
                        self.FoundBestSeePosition = True
                        return msg
        return []

    def do_s1_action(self):
        if not self.is_moving():
            self.my_update()
            #
            msg = self.do_occupy()
            if len(msg) > 0:
                return msg
            #
            if self.situation.final_occupy:
                return self.do_moveandprotect_cities()
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
            #
            #
            #
            #
        return []

    #
    def do_move_to_assist_occupy(self):
        if self.situation.fight_step == ALL_ASSISTOCCUPY_STEP or \
                self.situation.fight_step == ALL_OCCUPY_STEP:
            pass
        else:
            return []
        self.set_nearest_soilder()
        if self.is_move_to_assist_occupy():
            seven_list = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
            #
            temp_pos_list = self.seven_not_stacked(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_cannot_artillery_attacked(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_keep_distance(0, 5, self.nearest_soilder['cur_hex'], seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:
                #
                temp_pos_list = self.seven_keep_distance_includeequal(0, 5, self.nearest_soilder['cur_hex'], seven_list)
                if len(temp_pos_list) > 0:
                    seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_canattack_enemy(self.nearest_soilder, seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:  #
                temp_pos_list = self.seven_keep_distance(-1, -1, self.nearest_soilder['cur_hex'], seven_list)
                if len(temp_pos_list) > 0:
                    seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_cannot_be_attacked(seven_list, attack_list=[self.nearest_soilder['obj_id']])
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list

            #
            if self.operator['cur_hex'] in seven_list:
                return self.action_waiting
            #
            temp_pos_list = self.seven_is_townorjungle(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            if len(seven_list) == 0:
                return []

            pos = seven_list[random.randint(0, len(seven_list) - 1)]
            return self.do_move_to_point(pos)
        return []

    #
    def is_move_to_assist_occupy(self):
        #
        if not self.has_autocar() and (not self.can_attack_atcurpos()) \
                and self.is_fighting_near_city():  #
            return True
        return False

    #
    def has_autocar(self):
        for each_opt in self.situation.our_opt:
            if each_opt.operator['sub_type'] == AUTO_CAR:
                if each_opt.operator['launcher'] == self.operator['obj_id']:
                    return True
        return False

    #
    def can_attack_atcurpos(self):
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['obj_id'] in self.operator['see_enemy_bop_ids']:
                if enemy_opt['sub_type'] == SOILDER:  #
                    #
                    #
                    if enemy_opt['speed'] > 0 and self.operator['move_to_stop_remain_time'] > 0:

                        enemy_stopremaintime = int((720 / enemy_opt['basic_speed']) * (1 - enemy_opt['speed']))
                        my_stopremaintime = int((720 / self.operator['basic_speed']))
                        if my_stopremaintime < enemy_stopremaintime:
                            continue
                ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                        self.operator['cur_hex'],
                                                                        enemy_opt,
                                                                        self.myLandTool)
                if ret:
                    return True
        return False

    #
    def is_fighting_near_city(self):
        if not self.nearest_soilder:
            return False
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['sub_type'] == SOILDER:
                enemy_dis = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                            self.nearest_soilder['cur_hex'])
                if enemy_dis <= 3:
                    return True
        return False

    #
    def is_protecting_city(self):
        for each_city in self.observation['cities']:
            if each_city['flag'] == self.color:
                if each_city['coord'] in self.seven_neighbors_list:
                    return True
        return False

    #
    def do_moveandprotect_cities(self):
        if self.situation.fight_step == ALL_OCCUPY_STEP:
            pass
        else:
            return []
        if self.cityWanted:  #
            self.change_to_nearcity()
        #
        msg = self.do_protect_my_city()
        if len(msg) > 0:
            return msg
        #
        self.get_wantedcity()
        #
        msg = self.do_move_to_my_city()
        if len(msg) > 0:
            return msg
        #
        #
        #
        #
        #
        #
        return []

    #
    def get_wantedcity(self):
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notprepare()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notmine()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        return None

    #
    def change_to_nearcity(self):
        city_dis_my_city = self.situation.map.get_distance(self.operator['cur_hex'],
                                                           self.cityWanted['coord'])
        if city_dis_my_city <= 2:
            return
        for each_city in self.observation['cities']:
            city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                       each_city['coord'])
            if each_city['flag'] != self.color and each_city['coord'] != self.cityWanted['coord']:
                if city_dis <= 2:  #
                    if each_city['coord'] in self.situation.wantoccupy_cities_list:
                        for each_opt in self.situation.our_opt:
                            if each_opt.operator['sub_type'] == SOILDER:
                                if each_opt.operator['obj_id'] == self.operator['obj_id']:
                                    continue
                                if each_opt.cityWanted and each_opt.cityWanted['coord'] == each_city['coord']:
                                    #
                                    city_dis2 = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                                                each_city['coord'])
                                    if city_dis2 > city_dis:
                                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                                        self.cityWanted = each_city
                                        city_dis_my_city = city_dis
                                        each_opt.cityWanted = None
                                    break
                if city_dis < city_dis_my_city:  #
                    if each_city['coord'] not in self.situation.wantoccupy_cities_list:
                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
            if each_city['flag'] == self.color:
                if city_dis <= 2:
                    seven_city = self.myLandTool.get_big_six(each_city['coord'], 1)
                    seven_city_2 = self.myLandTool.get_big_six(each_city['coord'], 2)
                    if self.seven_has_enemy(seven_city_2) and (not self.seven_has_my_opt(seven_city)):
                        self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
        return None

    #
    def is_protect_my_city(self):
        #
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['obj_id'] != self.operator['obj_id']:
                if each_opt.cityWanted and each_opt.cityWanted['coord'] == self.cityWanted['coord'] \
                        and each_opt.operator['cur_hex'] in self.seven_cityWanted:
                    return False
        #
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] not in FLY_OPT:
                enemy_dis = self.situation.map.get_distance(self.cityWanted['coord'],
                                                            each_enemy['cur_hex'])
                if each_enemy['sub_type'] == SOILDER:  #
                    if enemy_dis <= 3:
                        return True
                else:  #
                    if enemy_dis <= 5:
                        return True
        return False

    #
    def do_protect_my_city(self):
        #
        if self.cityWanted and self.cityWanted['flag'] == self.color:
            self.seven_cityWanted = self.myLandTool.get_big_six(self.cityWanted['coord'], 1)
            if self.is_protect_my_city():
                if self.operator['cur_hex'] in self.seven_cityWanted:
                    #
                    #
                    #
                    my_seven = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
                    #
                    temp_pos_list = self.seven_in_mycity_seven(my_seven, self.seven_cityWanted)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list

                    #
                    temp_pos_list = self.seven_cannot_artillery_attacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    temp_pos_list = self.seven_not_stacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    for each_enemy in self.enemy_operators:
                        if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                            ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                                    self.operator['cur_hex'],
                                                                                    each_enemy, self.myLandTool)

                            if ret:
                                return self.action_waiting
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #

                    #
                    temp_pos_list = self.seven_is_town_or_jungle(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    if self.operator['cur_hex'] in my_seven:
                        return self.action_waiting
                    #
                    if self.cityWanted['coord'] in my_seven:
                        return self.do_move_onestep_to_point(self.cityWanted['coord'])
                    #
                    if len(my_seven) == 0:
                        return []

                    pos = my_seven[random.randint(0, len(my_seven) - 1)]
                    msg = self.do_move_to_point(pos)
                    return msg
                else:
                    return self.do_move_onestep_to_point(self.cityWanted['coord'])
            else:
                self.cityWanted = None
                return []
        return []

    #
    def do_getoff(self):
        for passengerId in self.operator['passenger_ids']:
            cure_action = command_action()
            cure_action.cur_bop = self.operator
            cure_action.action_type = GetOff
            cure_action.target_obj_id = passengerId
            flag, cure_action = self.my_check_tool.My_check_action(cure_action)
            if flag == True and cure_action:
                return self.get_retmsg(cure_action)
        return []
        #
        #
        if self.operator['change_state_remain_time'] > 0 or self.operator['move_state'] == 4:
            return False
        flg = True
        for each_enemy in self.enemy_operators:
            if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                if each_enemy['sub_type'] != MISSILE:
                    flg = False
                    break
        return flg
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #


class ai_soilder_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.movetype = MoveType_soilder  #
        self.shoot_range = 10
        self.iOccupidCity = False
        self.my_car = None
        if self.color == BLUE:
            self.shoot_range = 10
        else:
            self.shoot_range = 20

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)

        #
        if self.color == RED:
            if self.operator['C3'] > 0:
                self.shoot_range = 10
            else:
                self.shoot_range = 3
        else:
            if self.operator['C3'] > 0:
                self.shoot_range = 10
            else:
                self.shoot_range = 3

    def do_auto(self):
        if self.enenmy_is_coming == True:
            #
            msg = self.do_guide_attack()
            if len(msg) > 0:
                return msg
            msg = self.do_attack()
            if len(msg) > 0:
                return msg
            else:
                if self.operator['stop'] == True:
                    villege_list, tree_list = self.myLandTool.get_villege_tree_Straight_def(
                        self.operator['cur_hex'], self.observation['cities'][0]['coord'])
                    pos_list = []
                    pos_list.extend(tree_list)
                    pos_list.extend(villege_list)
                    if pos_list:
                        move_pos = self.myLandTool.get_closet_positon(
                            self.operator['cur_hex'], pos_list)
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
                    else:
                        move_pos = self.observation['cities'][0]['coord']
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
        else:
            if self.operator['stop'] == True:
                if self.missile_patrol_find_enemy == False:
                    move_pos = self.observation['cities'][0]['coord']
                    msg = self.do_move_to_point(move_pos)
                    if len(msg) > 0:
                        return msg  #
                else:
                    villege_list, tree_list = self.myLandTool.get_villege_tree_Straight_def(
                        self.operator['cur_hex'], self.observation['cities'][0]['coord'])
                    pos_list = []
                    pos_list.extend(tree_list)
                    pos_list.extend(villege_list)
                    if pos_list:
                        move_pos = self.myLandTool.get_closet_positon(
                            self.operator['cur_hex'], pos_list)
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
                    else:
                        move_pos = self.observation['cities'][0]['coord']
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
        return []

    def do_auto_blue(self):
        if self.enenmy_is_coming == True:
            msg = self.do_attack()
            if len(msg) > 0:
                return msg
            else:
                if self.operator['stop'] == True:
                    villege_list, tree_list = \
                        self.myLandTool.get_villege_tree_Straight_def(
                            self.operator['cur_hex'],
                            self.observation['cities'][0]['coord'])
                    pos_list = []
                    pos_list.extend(tree_list)
                    pos_list.extend(villege_list)
                    if pos_list:
                        move_pos = self.myLandTool.get_closet_positon(
                            self.operator['cur_hex'], pos_list)
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
                    else:
                        move_pos = self.observation['cities'][0]['coord']
                        msg = self.do_move_to_point(move_pos)
                        if len(msg) > 0:
                            return msg
        else:
            if self.operator['stop'] == True:
                if self.observation['cities'][0]['flag'] != self.color and \
                        self.maincity_select == False:
                    msg = self.do_move_to_point(self.observation['cities'][0]['coord'])
                    if len(msg) > 0:
                        return msg
                        self.maincity_select = True
                if self.observation['cities'][1]['flag'] != self.color and \
                        self.secondcity_select == False:
                    msg = self.do_move_to_point(self.observation['cities'][1]['coord'])
                    if len(msg) > 0:
                        return msg
                        self.secondcity_select = True
        return []

    def do_attack_moveandprotect_cities(self):
        msg = []
        msg = self.do_attack_first()
        if len(msg) > 0:
            return msg
        msg = self.do_moveandprotect_cities()
        if len(msg) > 0:
            return msg
        return []

    def do_strategy_firststep(self):
        if self.observation['time']['cur_step'] == 0:
            msg = self.do_get_on()
            if len(msg) > 0:
                car_id = msg[0]['target_obj_id']
                for each_opt in self.situation.our_opt:
                    if each_opt.operator['obj_id'] == car_id:
                        each_opt.get_on_flag = True
                        self.my_car = each_opt
                        break
                return msg
        return []

    def do_s1_action(self):
        if (not self.is_moving()) and not self.is_on_board():

            self.my_update()
            #
            msg = self.do_removekeep_toshoot()
            if len(msg) > 0:
                return msg
            #
            msg = self.do_occupy()
            if len(msg) > 0:
                return msg
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
        return []

    #
    def do_attack_first(self):
        if self.situation.fight_step == ALL_ASSISTOCCUPY_STEP or \
                self.situation.fight_step == ALL_ATTACKI_STEP:
            pass
        else:
            return []
        if self.operator['cur_hex'] in self.situation.artillery_pos_list:
            return []
        #
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] != SOILDER and each_enemy['sub_type'] != MISSILE:
                if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                    ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator, self.operator['cur_hex'],
                                                                            each_enemy, self.myLandTool)
                    if ret:
                        return self.action_waiting
        #
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] == SOILDER:
                if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                    if self.operator['C2'] > 0 and self.situation.map.get_distance(self.operator['cur_hex'],
                                                                                   each_enemy['cur_hex']) <= 1:
                        return self.action_waiting
                    #
                    #
                    #
        #

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        return []

    #
    def do_moveandprotect_cities(self):
        if self.operator['tire'] >= 1 or self.operator['keep'] == 1:  #
            return []
        #
        if self.cityWanted:
            self.change_to_nearcity()
        #
        msg = self.do_protect_my_city()
        if len(msg) > 0:
            return msg
        #
        self.get_wantedcity()
        #
        msg = self.do_move_to_my_city()
        if len(msg) > 0:
            return msg
        return []

    #
    def get_wantedcity(self):
        if self.operator['sub_type'] == SOILDER and self.situation.fight_step == ALL_OCCUPY_STEP:
            return None
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notprepare()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notmine()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_not_have_myopt()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        return None

    #
    def change_to_nearcity(self):
        city_dis_my_city = self.situation.map.get_distance(self.operator['cur_hex'],
                                                           self.cityWanted['coord'])
        if city_dis_my_city <= 2:
            return
        for each_city in self.observation['cities']:
            city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                       each_city['coord'])
            if each_city['flag'] != self.color and each_city['coord'] != self.cityWanted['coord']:
                if city_dis <= 2:  #
                    if each_city['coord'] in self.situation.wantoccupy_cities_list:
                        for each_opt in self.situation.our_opt:
                            if each_opt.operator['sub_type'] == SOILDER:
                                if each_opt.operator['obj_id'] == self.operator['obj_id']:
                                    continue
                                if each_opt.cityWanted and each_opt.cityWanted['coord'] == each_city['coord']:
                                    #
                                    city_dis2 = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                                                each_city['coord'])
                                    if city_dis2 > city_dis:
                                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                                        self.cityWanted = each_city
                                        city_dis_my_city = city_dis
                                        each_opt.cityWanted = None
                                    break
                if city_dis < city_dis_my_city:  #
                    if each_city['coord'] not in self.situation.wantoccupy_cities_list:
                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
            if each_city['flag'] == self.color:
                if city_dis <= 2:
                    seven_city = self.myLandTool.get_big_six(each_city['coord'], 1)
                    seven_city_2 = self.myLandTool.get_big_six(each_city['coord'], 2)
                    if self.seven_has_enemy(seven_city_2) and (not self.seven_has_my_opt(seven_city)):
                        self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
                        return None
        return None

    #
    def is_protect_my_city(self):
        #
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['obj_id'] != self.operator['obj_id']:
                if each_opt.cityWanted and each_opt.cityWanted['coord'] == self.cityWanted['coord'] \
                        and each_opt.operator['cur_hex'] in self.seven_cityWanted:
                    return False
        #
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] not in FLY_OPT:
                enemy_dis = self.situation.map.get_distance(self.cityWanted['coord'],
                                                            each_enemy['cur_hex'])
                if each_enemy['sub_type'] == SOILDER:  #
                    if enemy_dis <= 3:
                        return True
                else:  #
                    if enemy_dis <= 5:
                        return True
        return False

    #
    def do_protect_my_city(self):
        #
        if self.cityWanted and self.cityWanted['flag'] == self.color:
            self.seven_cityWanted = self.myLandTool.get_big_six(self.cityWanted['coord'], 1)
            if self.is_protect_my_city():
                if self.operator['cur_hex'] in self.seven_cityWanted:
                    #
                    #
                    #
                    my_seven = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
                    #
                    temp_pos_list = self.seven_in_mycity_seven(my_seven, self.seven_cityWanted)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list

                    #
                    temp_pos_list = self.seven_cannot_artillery_attacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    temp_pos_list = self.seven_not_stacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    for each_enemy in self.enemy_operators:
                        if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                            ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                                    self.operator['cur_hex'],
                                                                                    each_enemy, self.myLandTool)

                            if ret:
                                return self.action_waiting
                    #
                    if self.operator['C3'] > 0:
                        temp_pos_list = self.seven_attack_enemy_abovesoilder(my_seven)
                        if len(temp_pos_list) > 0:
                            my_seven = temp_pos_list
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #

                    #
                    temp_pos_list = self.seven_is_town_or_jungle(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    if self.operator['cur_hex'] in my_seven:
                        return self.action_waiting
                    #
                    if self.cityWanted['coord'] in my_seven:
                        return self.do_move_onestep_to_point(self.cityWanted['coord'])
                    #
                    if len(my_seven) == 0:
                        return []
                    pos = my_seven[random.randint(0, len(my_seven) - 1)]
                    return self.do_move_to_point(pos)
                else:
                    return self.do_move_onestep_to_point(self.cityWanted['coord'])
            else:
                self.cityWanted = None
                return []
        return []

    #
    def is_on_board(self):
        if len(self.operator['get_on_partner_id']) == 1:
            #
            return True
        return False

    def is_remove_keep(self):
        if self.operator['keep'] > 0 and self.operator['blood'] > 1:
            #
            if self.is_has_cansee_enemy_in_distance(self.operator['cur_hex'], CARS, -1, 10):
                return True
            #
            for each_city in self.observation['cities']:
                if each_city['flag'] == self.color:
                    big_six = self.myLandTool.get_big_six(each_city['coord'], 1)
                    if self.operator['cur_hex'] in big_six:
                        return False
            #
            if len(self.operator['see_enemy_bop_ids']) > 0:
                return True
        return False

    #
    def do_removekeep_toshoot(self):
        msg = []
        if self.is_remove_keep():
            msg_temp = self.do_removekeep()
            if len(msg_temp) > 0:
                msg.extend(msg_temp)
            else:
                return []
            msg_temp = self.do_guide_attack()
            if len(msg_temp) > 0:
                msg.extend(msg_temp)
                return msg
            msg_temp = self.do_attack()
            if len(msg_temp) > 0:
                msg.extend(msg_temp)
                return msg
        return msg

    #
    def do_move_to_point(self, move_pos):
        return self.do_charge_2(move_pos)

    def do_charge_1(self, move_pos):
        msg = []
        if self.operator['tire'] == 2:
            return []
        msg.extend(self.do_changestate(Charge_1))
        msg.extend(ai_my_operator.do_move_to_point(move_pos))
        return msg

    def do_charge_2(self, move_pos):
        msg = []
        if self.operator['tire'] >= 1:
            return []
        if self.operator['move_state'] != 3:
            msg.extend(self.do_changestate(Charge_2))
            return msg
        else:
            #
            msg.extend(ai_my_operator.do_move_to_point(self, move_pos))
            return msg
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #


class ai_autocar_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 10
        self.movetype = MoveType_car  #
        self.is_atpos = False
        self.is_hided = False

    def do_s1_action(self):
        if not self.is_moving():
            self.my_update()
            #
            msg = self.do_occupy()
            if len(msg) > 0:
                return msg
            #
            if self.situation.final_occupy:
                return self.do_moveandprotect_cities()
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg

        return []

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        self.shoot_range = 10

    #
    def do_move_to_guidepos(self):
        if not self.is_atpos:  #
            pos_list = self.myLandTool.get_first_tank_point(self.operator, start_mv_r=21)
            if pos_list:
                move_pos = pos_list[0]
            else:
                move_pos = self.myLandTool.get_initial_position(self.operator)
            self.is_atpos = True
            return self.do_move_Astar(move_pos, self.enemy_operators)
        return []

    #
    def do_move_to_assist_occupy(self):
        if self.situation.fight_step == ALL_ASSISTOCCUPY_STEP or \
                self.situation.fight_step == ALL_OCCUPY_STEP:
            pass
        else:
            return []
        self.set_nearest_soilder()
        if self.is_move_to_assist_occupy():
            seven_list = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
            #
            temp_pos_list = self.seven_not_stacked(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_cannot_artillery_attacked(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_keep_distance(0, 5, self.nearest_soilder['cur_hex'], seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:
                #
                temp_pos_list = self.seven_keep_distance_includeequal(0, 5, self.nearest_soilder['cur_hex'], seven_list)
                if len(temp_pos_list) > 0:
                    seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_canattack_enemy(self.nearest_soilder, seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:  #
                temp_pos_list = self.seven_keep_distance(-1, -1, self.nearest_soilder['cur_hex'], seven_list)
                if len(temp_pos_list) > 0:
                    seven_list = temp_pos_list
            #
            temp_pos_list = self.seven_cannot_be_attacked(seven_list, attack_list=[self.nearest_soilder['obj_id']])
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list

            #
            if self.operator['cur_hex'] in seven_list:
                return self.action_waiting
            #
            temp_pos_list = self.seven_is_townorjungle(seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            if len(seven_list) == 0:
                return []

            pos = seven_list[random.randint(0, len(seven_list) - 1)]
            return self.do_move_to_point(pos)
        return []

    #
    def is_move_to_assist_occupy(self):
        #
        if (not self.can_attack_atcurpos()) \
                and self.is_fighting_near_city():  #
            return True
        return False

    #
    def has_autocar(self):
        for each_opt in self.situation.our_opt:
            if each_opt.operator['sub_type'] == AUTO_CAR:
                if each_opt.operator['launcher'] == self.operator['obj_id']:
                    return True
        return False

    #
    def can_attack_atcurpos(self):
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['obj_id'] in self.operator['see_enemy_bop_ids']:
                if enemy_opt['sub_type'] == SOILDER:  #
                    #
                    #
                    if enemy_opt['speed'] > 0 and self.operator['move_to_stop_remain_time'] > 0:

                        enemy_stopremaintime = int((720 / enemy_opt['basic_speed']) * (1 - enemy_opt['speed']))
                        my_stopremaintime = int((720 / self.operator['basic_speed']))
                        if my_stopremaintime < enemy_stopremaintime:
                            continue
                ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                        self.operator['cur_hex'],
                                                                        enemy_opt,
                                                                        self.myLandTool)
                if ret:
                    return True
        return False

    #
    def is_fighting_near_city(self):
        if not self.nearest_soilder:
            return False
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['sub_type'] == SOILDER:
                enemy_dis = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                            self.nearest_soilder['cur_hex'])
                if enemy_dis <= 3:
                    return True
        return False

    #
    def is_protecting_city(self):
        for each_city in self.observation['cities']:
            if each_city['flag'] == self.color:
                if each_city['coord'] in self.seven_neighbors_list:
                    return True
        return False

    #
    def do_moveandprotect_cities(self):
        if self.situation.fight_step == ALL_OCCUPY_STEP:
            pass
        else:
            return []
        if self.cityWanted:  #
            self.change_to_nearcity()
        #
        msg = self.do_protect_my_city()
        if len(msg) > 0:
            return msg
        #
        self.get_wantedcity()
        #
        msg = self.do_move_to_my_city()
        if len(msg) > 0:
            return msg
        #
        #
        #
        #
        #
        #
        return []

    #
    def get_wantedcity(self):
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notprepare()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        #
        if self.cityWanted is None \
                or (self.cityWanted and self.situation.wantoccupy_cities_list.count(self.cityWanted['coord']) > 1):
            city = self.get_city_nearest_city_notmine()
            if city:
                self.cityWanted = city
                self.situation.wantoccupy_cities_list.append(city['coord'])
        return None

    #
    def change_to_nearcity(self):
        city_dis_my_city = self.situation.map.get_distance(self.operator['cur_hex'],
                                                           self.cityWanted['coord'])
        if city_dis_my_city <= 2:
            return
        for each_city in self.observation['cities']:
            city_dis = self.situation.map.get_distance(self.operator['cur_hex'],
                                                       each_city['coord'])
            if each_city['flag'] != self.color and each_city['coord'] != self.cityWanted['coord']:
                if city_dis <= 2:  #
                    if each_city['coord'] in self.situation.wantoccupy_cities_list:
                        for each_opt in self.situation.our_opt:
                            if each_opt.operator['sub_type'] == SOILDER:
                                if each_opt.operator['obj_id'] == self.operator['obj_id']:
                                    continue
                                if each_opt.cityWanted and each_opt.cityWanted['coord'] == each_city['coord']:
                                    #
                                    city_dis2 = self.situation.map.get_distance(each_opt.operator['cur_hex'],
                                                                                each_city['coord'])
                                    if city_dis2 > city_dis:
                                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                                        self.cityWanted = each_city
                                        city_dis_my_city = city_dis
                                        each_opt.cityWanted = None
                                    break
                if city_dis < city_dis_my_city:  #
                    if each_city['coord'] not in self.situation.wantoccupy_cities_list:
                        if self.cityWanted['coord'] in self.situation.wantoccupy_cities_list:
                            self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
            if each_city['flag'] == self.color:
                if city_dis <= 2:
                    seven_city = self.myLandTool.get_big_six(each_city['coord'], 1)
                    seven_city_2 = self.myLandTool.get_big_six(each_city['coord'], 2)
                    if self.seven_has_enemy(seven_city_2) and (not self.seven_has_my_opt(seven_city)):
                        self.situation.wantoccupy_cities_list.remove(self.cityWanted['coord'])
                        self.situation.wantoccupy_cities_list.append(each_city['coord'])
                        self.cityWanted = each_city
                        city_dis_my_city = city_dis
        return None

    #
    def is_protect_my_city(self):
        #
        #
        for each_opt in self.situation.our_opt:
            if each_opt.operator['obj_id'] != self.operator['obj_id']:
                if each_opt.cityWanted and each_opt.cityWanted['coord'] == self.cityWanted['coord'] \
                        and each_opt.operator['cur_hex'] in self.seven_cityWanted:
                    return False
        #
        for each_enemy in self.enemy_operators:
            if each_enemy['sub_type'] not in FLY_OPT:
                enemy_dis = self.situation.map.get_distance(self.cityWanted['coord'],
                                                            each_enemy['cur_hex'])
                if each_enemy['sub_type'] == SOILDER:  #
                    if enemy_dis <= 3:
                        return True
                else:  #
                    if enemy_dis <= 5:
                        return True
        return False

    #
    def do_protect_my_city(self):
        #
        if self.cityWanted and self.cityWanted['flag'] == self.color:
            self.seven_cityWanted = self.myLandTool.get_big_six(self.cityWanted['coord'], 1)
            if self.is_protect_my_city():
                if self.operator['cur_hex'] in self.seven_cityWanted:
                    #
                    #
                    #
                    my_seven = self.myLandTool.get_order_by_heighth(self.seven_neighbors_list)
                    #
                    temp_pos_list = self.seven_in_mycity_seven(my_seven, self.seven_cityWanted)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list

                    #
                    temp_pos_list = self.seven_cannot_artillery_attacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    temp_pos_list = self.seven_not_stacked(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    for each_enemy in self.enemy_operators:
                        if each_enemy['obj_id'] in self.operator['see_enemy_bop_ids']:
                            ret = self.situation.myFireTool.get_simulate_damage_A2B(self.operator,
                                                                                    self.operator['cur_hex'],
                                                                                    each_enemy, self.myLandTool)

                            if ret:
                                return self.action_waiting
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #
                    #

                    #
                    temp_pos_list = self.seven_is_town_or_jungle(my_seven)
                    if len(temp_pos_list) > 0:
                        my_seven = temp_pos_list
                    #
                    if self.operator['cur_hex'] in my_seven:
                        return self.action_waiting
                    #
                    if self.cityWanted['coord'] in my_seven:
                        return self.do_move_onestep_to_point(self.cityWanted['coord'])
                    #
                    if len(my_seven) == 0:
                        return []
                    pos = my_seven[random.randint(0, len(my_seven) - 1)]
                    return self.do_move_to_point(pos)
                else:
                    return self.do_move_onestep_to_point(self.cityWanted['coord'])
            else:
                self.cityWanted = None
                return []
        return []


#

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
class ai_missile_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 1
        self.movetype = MoveType_fly  #
        self.patrol_enemy_pos_list = []
        self.patrol_path = []
        self.life_time = observation['time']['cur_step']
        self.patrol_finish = False
        if my_ai.scenario_type == GROUP:
            self.patrol_finish = True
        self.patrol_begin = False
        self.target2atk = -1
        self.target2move = -1
        self.target_car = -1
        self.first_missile = True
        self.my_init()

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        self.shoot_range = 10

    def do_s1_action(self):
        if not self.is_moving_fly():
            self.my_update()
            self.cityWanted = self.observation['cities'][0]
            #
            msg = self.do_move_to_attack_list_first()
            if len(msg) > 0:
                return msg
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
            msg = self.do_move_to_attack_list()
            if len(msg) > 0:
                return msg
            msg = self.do_patrol()
            if len(msg) > 0:
                return msg
            msg = self.do_move_to_point(4435)
        return []

    def my_init(self):
        if my_ai.scenario_type == GROUP:
            pass

    def do_auto(self):
        if self.observation['time']['cur_step'] > 1000:
            return self.do_attack2()
        if self.life_time > 1100:  #
            self.patrol_done = True
        else:
            if self.observation['time']['cur_step'] - self.life_time > 600:  #
                self.patrol_done = True
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        return []

    def do_auto_blue(self):
        return self.do_auto()

    def do_attack(self, missile_second):
        if missile_second == False:  #
            #
            for each in self.situation.shoot_list[self.operator['sub_type']]:
                attack_enemy_list = []
                for obj_bop in self.enemy_operators:
                    if obj_bop['sub_type'] == each and obj_bop['blood'] == 1:
                        attack_enemy_list.append(obj_bop)
                #
                attack_enemy_list = sorted(attack_enemy_list, key=lambda x: x['blood'])
                for obj_bop in attack_enemy_list:
                    msg = self.do_fire(obj_bop)
                    if len(msg) > 0:
                        return msg
            return []
        else:
            return ai_my_operator.do_attack(self)
            #

    def do_move_to_attack_list_first(self):
        #
        #
        if (self.observation['time']['cur_step'] - self.life_time > 80 and \
                not self.first_missile) or (self.observation['time']['cur_step'] - self.life_time > 1000 ):  #
            for each in self.situation.shoot_list[self.operator['sub_type']]:
                for each_enemy in self.situation.enemy_history.values():
                    if not each_enemy[2]:
                        if each_enemy[1] >-100 :
                            obj_bop = each_enemy[0]
                            if obj_bop['sub_type'] == each:
                                msg = self.do_move_to_attack(obj_bop['obj_id'])
                                if len(msg) > 0:
                                    return msg
        return []

    def do_move_to_attack_list(self):
        #
        #
        if self.observation['time']['cur_step'] < self.situation.attack_car_time:
            dis_min = 999
            msg = []
            for each_enemy in self.enemy_operators:
                if each_enemy['sub_type'] == CAR:
                    dis = self.situation.map.get_distance(self.operator['cur_hex'], each_enemy['cur_hex'])
                    if dis < dis_min:
                        dis_min = dis
                        self.target_car = each_enemy['obj_id']
            if self.target_car != -1:
                #
                msg = self.do_move_to_attack(self.target_car)
                if len(msg) > 0:
                    return msg
        #
        #
        #
        #
        for each in self.situation.shoot_list[self.operator['sub_type']]:
            for each_enemy in self.situation.enemy_history.values():
                if not each_enemy[2]:
                    obj_bop = each_enemy[0]
                    if obj_bop['sub_type'] == each:
                        msg = self.do_move_to_attack(obj_bop['obj_id'])
                        if len(msg) > 0:
                            return msg
        return []

    def do_move_to_attack(self, target_id):
        #
        enemy_opt, last_time, is_dead , is_seen = self.situation.get_enemy_history_by_id(target_id)
        if is_dead is True or enemy_opt is None:
            self.target_car = -1
            return []
        #
        #
        #
        msg = self.do_fire(enemy_opt)
        if len(msg) > 0:
            return msg
        #
        return self.do_move_to_point(enemy_opt['cur_hex'])

    #

    def create_patrol_path(self, city_xy, r=5):

        src_xy = my_ai.my_xy
        dst_xy = my_ai.enemy_xy

        #
        src_x = int(src_xy / 100)
        src_y = int(src_xy % 100)
        dst_x = int(dst_xy / 100)
        dst_y = int(dst_xy % 100)
        from math import fabs
        drt_y = (dst_y - src_y)
        drt_x = (dst_x - src_x)
        #
        #
        main_city_xy = city_xy
        res = []
        #
        if fabs(drt_y) >= fabs(drt_x):
            min_x = int(main_city_xy / 100) - int(r)
            max_x = int(main_city_xy / 100) + int(r)
            min_y = int(main_city_xy % 100)
            max_y = min_y + int(r) * 2
            for idx_y in range(min_y, max_y, 2):
                res.append(min_x * 100 + idx_y)
                res.append(max_x * 100 + idx_y)
        else:
            min_x = int(main_city_xy / 100)
            max_x = int(main_city_xy / 100) + int(r)
            min_y = int(main_city_xy % 100) - int(r)
            max_y = min_y + int(r)
            for idx_x in range(min_x, max_x, 2):
                res.append(idx_x * 100 + min_y)
                res.append(idx_x * 100 + max_y)
        path_list = []

        opt_xy = self.operator['cur_hex']
        for dst_xy in res:
            res_list = self.map.gen_move_route(opt_xy, dst_xy, 3)
            opt_xy = dst_xy
            path_list += res_list
        if path_list:
            self.patrol_path = path_list

        return

    def do_patrol(self):
        if not self.patrol_begin:
            #
            self.create_patrol_path(self.cityWanted['coord'], 5)
            self.movepath = self.patrol_path
            self.patrol_begin = True
        if len(self.movepath) == 0:
            self.patrol_finish = True
            return []
        return self.do_move_to_point(self.movepath[-1])

    def do_patrol_spec(self, r, src_xy, dst_xy):
        #
        opt_xy = self.operator['cur_hex']
        #
        src_x = int(src_xy / 100)
        src_y = int(src_xy % 100)

        dst_x = int(dst_xy / 100)
        dst_y = int(dst_xy % 100)

        from math import fabs

        drt_y = (dst_y - src_y)
        drt_x = (dst_x - src_x)

        #
        #
        if fabs(drt_y) >= fabs(drt_x):
            if drt_y <= 0:
                res = self.myLandTool.get_special_list(self.myLandTool.main_city_xy, r, [3, 4])
            else:
                res = self.myLandTool.get_special_list(self.myLandTool.main_city_xy, r, [1, 2])

        else:
            if drt_x <= 0:
                res = self.myLandTool.get_special_list(self.myLandTool.main_city_xy, r, [1, 4])
            else:
                res = self.myLandTool.get_special_list(self.myLandTool.main_city_xy, r, [2, 3])
        path_list = []
        if len(res) == 0:
            return None

        for dst_xy in res:
            res_list = self.map.gen_move_route(opt_xy, dst_xy, 3)
            opt_xy = dst_xy
            path_list += res_list

        if path_list:
            self.patrol_path = path_list
            return [{
                'obj_id': self.operator['obj_id'],
                'type': Move,
                'move_path': path_list,
            }]
        else:
            return []


class ai_helicopter_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 1
        self.movetype = MoveType_fly  #
        self.nearest_enemy_opt = None

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        if self.operator['C3'] > 0:
            self.shoot_range = 20
        else:
            self.shoot_range = 10

    def do_s1_action(self):
        if not self.is_moving():
            self.my_update()
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
        return []

    #
    def do_move_to_enemy_keepdistance(self):
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        self.set_nearest_enemy_opt()
        #
        return self.do_move_one_step_fly_keepdistance()
        #
        #

    #
    def set_nearest_enemy_opt(self):
        if self.operator['C3'] > 0:  #
            if self.observation['time']['cur_step'] < self.situation.attack_car_time:
                #
                self.get_nearest_opt([CAR])
                #
                if not self.nearest_enemy_opt:
                    self.get_nearest_opt([TANK, AUTO_CAR])
            else:
                self.get_nearest_opt([CAR, TANK, AUTO_CAR])
        else:
            self.get_nearest_opt([CAR, TANK, AUTO_CAR, HELICOPTER])
        return None

    def get_nearest_opt(self, opt_list):
        dis = 999
        self.nearest_enemy_opt = None
        #
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['sub_type'] in opt_list:
                enemy_dis = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt['cur_hex'])
                if enemy_dis < dis:
                    dis = enemy_dis
                    self.nearest_enemy_opt = enemy_opt

    #
    def do_move_one_step_fly_keepdistance(self):

        seven_list = self.seven_neighbors_list
        #
        if self.is_has_enemy_in_distance(self.operator['cur_hex'], [SOILDER], -1, 10):
            temp_pos_list = seven_list
            for each in self.situation.enemy_history.values():
                if not each[2]:
                    each_enemy = each[0]
                    if each_enemy['sub_type'] == SOILDER:
                        if self.situation.map.get_distance(self.operator['cur_hex'], each_enemy['cur_hex']) <= 10:
                            temp_pos_list = self.seven_keep_distance(11, 13, each_enemy['cur_hex'], temp_pos_list)
                            if len(temp_pos_list) == 0:
                                break
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:
                for each in self.situation.enemy_history.values():
                    if not each[2]:
                        each_enemy = each[0]
                        if each_enemy['sub_type'] == SOILDER:
                            if self.situation.map.get_distance(self.operator['cur_hex'], each_enemy['cur_hex']) <= 10:
                                temp_pos_list = self.seven_keep_distance_includeequal(11, 13, each_enemy['cur_hex'],
                                                                                      seven_list)
                                if len(temp_pos_list) > 0:
                                    seven_list = temp_pos_list
        else:
            #
            if self.operator['move_to_stop_remain_time'] < 70 \
                    and self.operator['move_to_stop_remain_time'] > 0:
                #
                #
                #
                #
                #
                #
                return self.action_waiting

        #

        temp_pos_list = self.seven_cannot_be_attacked_fly(seven_list)
        if len(temp_pos_list) > 0:
            seven_list = temp_pos_list
        if self.nearest_enemy_opt:
            #
            dis = 0
            if self.operator['C3'] > 0:  #
                dis = 16
            else:
                dis = 6
            if self.operator['cur_hex'] in seven_list:
                if self.situation.map.get_distance(self.operator['cur_hex'], self.nearest_enemy_opt['cur_hex']) <= dis:
                    return self.action_waiting
            #
            dis = 0
            if self.operator['C3'] > 0:  #
                dis = 11
            else:
                dis = 6
            temp_pos_list = self.seven_keep_distance(dis, dis, self.nearest_enemy_opt['cur_hex'], seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list


        else:
            #
            temp_pos_list = self.seven_keep_distance(0, 0, my_ai.enemy_xy, seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
        #
        if len(seven_list) == 0:
            return []
        pos = seven_list[random.randint(0, len(seven_list) - 1)]
        return self.do_move_to_point(pos)

    #
    def do_move_one_step_flyto_point(self, xy):
        dis = 0
        seven_list = self.seven_neighbors_list
        temp_pos_list = self.seven_keep_distance(dis, dis, xy, seven_list)
        if len(temp_pos_list) > 0:
            seven_list = temp_pos_list
        else:
            return self.action_waiting
        #
        if len(seven_list) == 0:
            return []
        pos = seven_list[random.randint(0, len(seven_list) - 1)]
        return self.do_move_to_point(pos)

    #
    def seven_cannot_be_attacked_fly(self, seven_list_in):
        not_attack_list = [MISSILE, AUTO_PLANE, TANK, ARTILLERY]
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            can_be_attacked = False
            for each in self.situation.enemy_history.values():
                if not each[2]:
                    each_enemy = each[0]
                    if each_enemy['sub_type'] in not_attack_list:
                        continue
                    if self.map.can_see(each_enemy['cur_hex'], each_xy, 3):
                        if each_enemy['sub_type'] == SOILDER:
                            if self.situation.map.get_distance(each_enemy['cur_hex'], each_xy) <= 10:
                                can_be_attacked = True
                                break
                        else:
                            if self.situation.map.get_distance(each_enemy['cur_hex'], each_xy) < 4:
                                can_be_attacked = True
                                break
            if can_be_attacked:
                seven_list.remove(each_xy)
        return seven_list

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    #
    def get_nearest_car(self):
        dis = 999
        nearest_car = None
        #
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['sub_type'] == CAR:
                enemy_dis = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt['cur_hex'])
                if enemy_dis < dis:
                    dis = enemy_dis
                    nearest_car = enemy_opt
        return nearest_car

    def get_nearest_car_and_tank(self):
        dis = 999
        nearest_car = None
        #
        for enemy_opt in self.situation.enemy_operators:
            if enemy_opt['sub_type'] == CAR or enemy_opt['sub_type'] == TANK:
                enemy_dis = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt['cur_hex'])
                if enemy_dis < dis:
                    dis = enemy_dis
                    nearest_car = enemy_opt
        return nearest_car

    def get_poslist_cansee(self, target_pos, pos_list):
        for each_pos in pos_list[::-1]:
            if not self.map.can_see(each_pos, target_pos, 2):
                pos_list.remove(each_pos)
        return pos_list

    #
    def get_poslist_nearenemy(self, cur_pos, pos_list):
        for each_pos in pos_list[::-1]:
            if self.color == RED:
                #
                if each_pos % 100 <= cur_pos % 100:
                    pos_list.remove(each_pos)
            else:
                #
                if each_pos % 100 > cur_pos % 100:
                    pos_list.remove(each_pos)
        return pos_list

    #
    def get_poslist_away_soilder(self, cur_pos, pos_list):
        for enemy in self.enemy_operators:
            if enemy['sub_type'] == SOILDER:
                dis_nearest = distance = self.situation.map.get_distance(cur_pos, enemy['cur_hex'])
                for each_pos in pos_list[::-1]:
                    distance = self.situation.map.get_distance(each_pos, enemy['cur_hex'])
                    if distance <= 12 and distance <= dis_nearest:
                        pos_list.remove(each_pos)
        return pos_list


class ai_autoplane_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 1
        self.movetype = MoveType_fly  #

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        self.shoot_range = 0

    def do_s1_action(self):
        if not self.is_moving():
            self.my_update()
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
        return []

    #
    def do_move_to_enemy_keepdistance(self):

        self.set_nearest_enemy_opt()
        if self.nearest_enemy_opt:
            return self.do_move_one_step_fly_keepdistance()
        else:
            return self.do_move_one_step_flyto_point(my_ai.enemy_xy)

    #
    def set_nearest_enemy_opt(self):
        if self.observation['time']['cur_step'] < self.situation.attack_car_time:
            #
            self.get_nearest_opt([CAR])
            #
            if not self.nearest_enemy_opt:
                self.get_nearest_opt([TANK, AUTO_CAR])
        else:
            self.get_nearest_opt([CAR, TANK, AUTO_CAR])
        return None

    def get_nearest_opt(self, opt_list):
        dis = 999
        self.nearest_enemy_opt = None
        #
        for enemy in self.situation.enemy_history.values():
            if (not enemy[2]) and (not enemy[3])and (enemy[1] > -self.observation['time']['cur_step'] + 1):
                enemy_opt = enemy[0]
                if enemy_opt['sub_type'] in opt_list:
                    enemy_dis = self.situation.map.get_distance(self.operator['cur_hex'], enemy_opt['cur_hex'])
                    if enemy_dis < dis:
                        dis = enemy_dis
                        self.nearest_enemy_opt = enemy_opt
        return None
    #
    def do_move_one_step_fly_keepdistance(self):
        #
        if self.operator['move_to_stop_remain_time'] < 70 \
                and self.operator['move_to_stop_remain_time'] > 0:
            return self.action_waiting
        seven_list = self.seven_neighbors_list
        #
        #
        #
        #
        #
        #
        #
        #
        if self.operator['cur_hex'] in seven_list:
            if self.situation.map.get_distance(self.operator['cur_hex'], self.nearest_enemy_opt['cur_hex']) < 1:
                return self.action_waiting
        #
        dis = 0
        temp_pos_list = self.seven_keep_distance(dis, dis, self.nearest_enemy_opt['cur_hex'], seven_list)
        if len(temp_pos_list) > 0:
            seven_list = temp_pos_list
        else:
            temp_pos_list = self.seven_keep_distance_includeequal(dis, dis, self.nearest_enemy_opt['cur_hex'],
                                                                  seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            #
            #
        #
        if len(seven_list) == 0:
            return []

        pos = seven_list[random.randint(0, len(seven_list) - 1)]
        return self.do_move_to_point(pos)

    #
    def do_move_one_step_flyto_point(self, xy):
        dis = 0
        seven_list = self.seven_neighbors_list
        temp_pos_list = self.seven_keep_distance(dis, dis, xy, seven_list)
        if len(temp_pos_list) > 0:
            seven_list = temp_pos_list
        else:
            temp_pos_list = self.seven_keep_distance_includeequal(dis, dis, xy, seven_list)
            if len(temp_pos_list) > 0:
                seven_list = temp_pos_list
            else:
                return self.action_waiting
        #
        if len(seven_list) == 0:
            return []
        pos = seven_list[random.randint(0, len(seven_list) - 1)]
        return self.do_move_to_point(pos)

    #
    def seven_cannot_be_attacked_fly(self, seven_list_in):
        not_attack_list = [MISSILE, AUTO_PLANE, TANK, ARTILLERY]
        seven_list = copy.deepcopy(seven_list_in)
        for each_xy in seven_list[::-1]:
            can_be_attacked = False
            for each_enemy in self.situation.enemy_operators:
                if each_enemy['sub_type'] in not_attack_list:
                    continue
                if self.is_enemy_moving(each_enemy):
                    continue
                if self.map.can_see(each_enemy['cur_hex'], each_xy, 3):
                    if self.situation.map.get_distance(each_enemy['cur_hex'], each_xy) <= 2:
                        can_be_attacked = True
                        break
            if can_be_attacked:
                seven_list.remove(each_xy)
        return seven_list


class ai_aritllery_operator(ai_my_operator):
    def __init__(self, operator, color, map, observation, scenario_info):
        ai_my_operator.__init__(self, operator, color, map, observation, scenario_info)
        self.shoot_range = 1
        self.movetype = MoveType_car  #

    def update(self, operator, observation):
        ai_my_operator.update(self, operator, observation)
        #
        self.shoot_range = 0

    def do_s1_action(self):
        if not self.is_moving():
            self.my_update()
            #
            msg = self.do_move_step()
            if len(msg) > 0:
                return msg
        return []

    def do_jm(self, pos):
        msg = self.do_JM(pos)
        if len(msg) > 0:
            return msg
        return []


#
class strategy():
    def __init__(self, color):
        self.operator_id = {}
        self.color = color
        self.member_list = []
        self.temp_member_list = []

    def reset(self, color):
        self.__init__(color)

    @classmethod
    def class_update(cls, observation, situation):
        cls.my_situation = situation
        cls.observation = observation

    #
    def check(self):
        return False

    #
    def can_run(self):
        return True

    #
    def assignment_task(self):
        return True

    #
    def run(self):
        return []

    #
    def is_finished(self):
        #
        for each in self.member_list[::-1]:
            #
            if each not in self.my_situation.our_opt:
                if not self.release_amember(each):
                    return True
        #
        #
        if len(self.member_list) == 0:
            return True
        if self.my_situation.enenmy_is_coming:
            return False
        return False

    #
    def release_amember(self, member):
        member.strategy_type = STRATEGY_AUTO
        member.strategy = None
        self.member_list.remove(member)
        if self.can_run():
            self.assignment_task()
            return True
        else:
            self.release_allmember()
            return False

    #
    def release_allmember(self):
        for each in self.member_list:
            each.strategy_type = STRATEGY_AUTO
            each.strategy = None
        self.member_list = []
    #


class first_step_strgy(strategy):
    def __init__(self, color):
        strategy.__init__(self, color)
        self.select_cities_list = []

    #
    def check(self):
        if self.observation['time']['cur_step'] != 0:
            return False
        #
        for each_opt in self.my_situation.our_opt:
            if each_opt.operator['sub_type'] == TANK or each_opt.operator['sub_type'] == CAR \
                    or each_opt.operator['sub_type'] == AUTO_CAR or each_opt.operator['sub_type'] == SOILDER:
                if self.observation['time']['cur_step'] == 0 and each_opt.strategy_type == STRATEGY_AUTO:
                    each_opt.first_pos = my_ai.all_first_pos[each_opt.operator['obj_id']]
                    if each_opt.operator['sub_type'] == CAR:
                        each_opt.city_first_step = my_ai.all_first_city[each_opt.operator['obj_id']]
                    self.temp_member_list.append(each_opt)
        if len(self.temp_member_list) == 0:
            return False
        #
        if self.can_run():
            #
            for each_opt in self.temp_member_list:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    each_opt.strategy.release_amember(each_opt)
                each_opt.strategy = self
                each_opt.strategy_type = STRATEGY_FIRSTSTEP
                self.member_list.append(each_opt)
            self.assignment_task()
            return True
        return False

    #
    def assignment_task(self):

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        pass

    #
    def run(self):
        #
        return []

    def is_finished(self):
        #
        for each in self.member_list[::-1]:
            #
            if each not in self.my_situation.our_opt:
                if not self.release_amember(each):
                    return True
            #
            if each.operator['cur_hex'] == each.first_pos[0]:
                if not self.release_amember(each):
                    return True
            #
            if each.operator['sub_type'] == SOILDER and self.observation['time']['cur_step'] > 74:
                if not self.release_amember(each):
                    return True
            #
            #
        #
        #
        #
        if len(self.member_list) == 0:
            return True
        if self.my_situation.enenmy_is_coming:
            return False
        return False
        #
    #


class tank_protect_car_strgy(strategy):
    def __init__(self, color):
        strategy.__init__(self, color)
        self.protected_list = []
        self.safety_list = []

    #
    def check(self):
        #
        #

        #
        for each_opt in self.my_situation.our_opt:
            if each_opt.strategy_type == STRATEGY_AUTO:
                if each_opt.color == RED and \
                        (each_opt.operator['sub_type'] == TANK or each_opt.operator['sub_type'] == CAR):
                    self.temp_member_list.append(each_opt)
        if len(self.temp_member_list) == 0 \
                or len(self.protected_list) == 0 \
                or len(self.safety_list) == 0:
            return False
        #
        if self.can_run():
            #
            for each_opt in self.temp_member_list:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    each_opt.strategy.release_amember(each_opt)
                each_opt.strategy = self
                each_opt.strategy_type = STRATEGY_TANK_PROTECT_CAR
                self.member_list.append(each_opt)
            self.assignment_task()
            return True
        return False

    #
    def can_run(self):
        return True

    #
    def assignment_task(self):
        self.protected_list = []
        self.safety_list = []
        for each_opt in self.member_list:
            if each_opt.operator['sub_type'] == CAR:
                self.protected_list.append(each_opt)
            else:
                self.safety_list.append(each_opt)

    #
    def run(self):
        #
        ret_msg = []
        protected_xy = -1
        #
        for opt in self.my_situation.our_opt:
            for tmp_opt in self.protected_list:
                if tmp_opt.operator['obj_id'] == opt.operator['obj_id']:
                    protected_xy = tmp_opt.operator['cur_hex']

        if protected_xy == -1:
            return []
        #
        for opt in self.my_situation.our_opt:
            for tmp_opt in self.protected_list:
                if tmp_opt.operator['obj_id'] == opt.operator['obj_id']:
                    msg = opt.do_auto()
                    if len(msg) > 0:
                        opt.is_thisturn_finished = True
                    ret_msg.extend(msg)

        protected_xy = self.protected_list[0].operator['cur_hex']
        enemy_tuple_list = []
        for enemy_opt_history in self.my_situation.enemy_history.values():
            enemy_opt = enemy_opt_history[0]
            see_time = enemy_opt_history[1]
            is_dead = enemy_opt_history[2]
            if is_dead is True:
                continue
            #
            if enemy_opt['sub_type'] == TANK:
                enemy_weight = 5
            elif enemy_opt['sub_type'] == SOILDER:
                enemy_weight = 3
            elif enemy_opt['sub_type'] == CAR:
                enemy_weight = 1

            enemy_weight = enemy_weight * enemy_opt['blood']
            #
            dist = self.my_situation.map.get_distance(enemy_opt['cur_hex'], protected_xy)
            dist /= 3
            if dist == 0:
                dist = 1
            #

            enemy_tuple_list.append((enemy_opt, enemy_weight))

        if len(enemy_tuple_list) == 0:
            return []

        sorted(enemy_tuple_list, key=lambda x: x[1], reverse=True)

        #
        for opt in self.my_situation.our_opt:
            for tmp_opt in self.safety_list:
                if tmp_opt.operator['obj_id'] == opt.operator['obj_id']:
                    msg = opt.do_move_to_attack_Aopt(enemy_tuple_list[0][0])
                if len(msg) > 0:
                    opt.is_thisturn_finished = True
                    ret_msg.extend(msg)

        return ret_msg

    def is_finished(self):
        #
        if len(self.member_list) == 0:
            return True
        #
        for each in self.member_list:
            #
            if each not in self.my_situation.our_opt:
                if not self.release_amember(each):
                    return True
            #
        #

        return False
        #


class push(strategy):
    def __init__(self, color):
        strategy.__init__(self, color)
        self.car_list = []
        self.tank_list = []
        self.missile_list = []
        self.target = None

    #
    def check(self):
        #
        #
        #

        #
        for each_opt in self.my_situation.our_opt:
            if each_opt.strategy_type == STRATEGY_AUTO:
                if each_opt.color == RED:
                    if each_opt.operator['sub_type'] == TANK:
                        self.tank_list.append(each_opt)
                    if each_opt.operator['sub_type'] == CAR \
                            or each_opt.operator['sub_type'] == AUTO_CAR:
                        self.car_list.append(each_opt)
                    if each_opt.operator['sub_type'] == MISSILE:
                        self.missile_list.append(each_opt)
                    self.temp_member_list.append(each_opt)
        if len(self.missile_list) == 0:
            return False
        #
        if self.can_run():
            #
            for each_opt in self.temp_member_list:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    each_opt.strategy.release_amember(each_opt)
                each_opt.strategy = self
                each_opt.strategy_type = STRATEGY_PUSH
                self.member_list.append(each_opt)
            self.assignment_task()
            return True
        return True

    #
    def can_run(self):
        return True

    #
    def assignment_task(self):
        return
        #
        #
        #
        #
        #
        #
        #

    #
    def run(self):

        if len(self.car_list) == 0:
            return []

        car_opt = self.car_list[0].operator
        #
        if len(self.my_situation.enemy_history) == 0:
            return []

        find = False

        self.target = self.find_enemy()
        find = True
        #
        #
        if find:
            return self.car_go(car_opt)

            #
            #
            #
        #
        #
        #
        #
        #
        #
        #
        #

        return []

    def car_go(self, car_opt, connect_list_list=[], enemy_list=[]):

        astarres = self.my_situation.myLandTool.AstarFindPath_known_enemy(car_opt, 2808, [self.target])
        if astarres[0] is True:
            tmp_movepath = astarres[1]

            self.car_list[0].movepath = tmp_movepath
            return self.car_list[0].do_move_to_point(2808)

        return []

    def find_enemy(self):
        core_xy = -1
        if len(self.tank_list) > 0:
            tank_xy = self.tank_list[0].operator['cur_hex']

        if len(self.car_list) > 0:
            car_xy = self.car_list[0].operator['cur_hex']
            core_xy = car_xy

        res_list = []
        for history_tmp in self.my_situation.enemy_history.values():
            enemy_opt = history_tmp[0]
            last_time = history_tmp[1]
            is_dead = history_tmp[2]

            if is_dead or core_xy == -1:
                continue

            dis = self.my_situation.map.get_distance(core_xy, enemy_opt['cur_hex'])
            tmp_enmey_opt = copy.deepcopy(enemy_opt)
            res_list.append((tmp_enmey_opt, dis))

        res_list = sorted(res_list, key=lambda x: x[1], reverse=False)

        return res_list[0][0]

    def get_unsee_zone(self, enemy_xy, ql):
        ql = [3, 4]
        define_fire_range = self.my_situation.myLandTool.get_big_six(enemy_xy, 20, quadrant_list=ql)
        unsight_list = []
        for xy in define_fire_range:
            if self.my_situation.map.can_see(enemy_xy, xy, 0) is False:
                unsight_list.append(xy)
        #
        connect_list_list = self.my_situation.myLandTool.get_connect_set(unsight_list)
        return connect_list_list

    def is_finished(self):
        #
        if len(self.member_list) == 0:
            return True
        #
        for each in self.member_list:
            #
            if each not in self.my_situation.our_opt:
                if not self.release_amember(each):
                    return True
            #

        #
        for each in self.car_list:
            if each not in self.my_situation.our_opt:
                self.car_list.remove(each)
                #
        #

        return False
        #


class tank_waiting(strategy):
    def __init__(self, color):
        strategy.__init__(self, color)

    def check(self):
        for each_opt in self.my_situation.our_opt:
            if each_opt.strategy_type == STRATEGY_AUTO:
                if each_opt.color == BLUE and \
                        each_opt.operator['sub_type'] == TANK:
                    self.temp_member_list.append(each_opt)
        if len(self.temp_member_list) == 0:
            return False
            #
        if self.can_run():
            #
            for each_opt in self.temp_member_list:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    each_opt.strategy.release_amember(each_opt)
                each_opt.strategy = self
                each_opt.strategy_type = STRATEGY_TANK_PROTECT_CAR
                self.member_list.append(each_opt)
            self.assignment_task()
            return True
        return False

    def can_run(self):
        return True

    def assignment_task(self):
        return

    def run(self):
        ret_msg = []
        #
        car_list = self.my_situation.get_alive_enemy_car()
        if len(car_list) > 0:
            target = car_list[0]
            for each_opt in self.member_list:
                ret_msg.extend(each_opt.do_move_to_attack_Aopt(target))
        #
        return ret_msg

    def is_finished(self):
        return False


#
class tank_overlap(strategy):
    def __init__(self, color):
        strategy.__init__(self, color)
        self.head_tank = None
        self.move_step = -1

    def check(self):
        for each_opt in self.my_situation.our_opt:
            if each_opt.strategy_type == STRATEGY_AUTO:
                if each_opt.operator['sub_type'] == TANK:
                    self.temp_member_list.append(each_opt)
        if len(self.temp_member_list) == 0:
            return False
            #
        if self.can_run():
            #
            for each_opt in self.temp_member_list:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    each_opt.strategy.release_amember(each_opt)
                each_opt.strategy = self
                each_opt.strategy_type = STRATEGY_TANK_PROTECT_CAR
                self.member_list.append(each_opt)
            self.assignment_task()
            return True
        return False

    def can_run(self):
        return True

    def assignment_task(self):
        if len(self.member_list) > 0:
            self.head_tank = self.member_list[0]
        return

    def run(self):
        ret_msg = []

        #

        #
        self.head_tank = self.member_list[0]
        if self.is_all_overlap() and \
                self.is_all_stop():
            path = self.gen_move(self.head_tank.operator)
            if path:
                self.head_tank.movepath = path
                import copy
                for i in range(1, len(self.member_list)):
                    self.member_list[i].movepath = copy.deepcopy(path)

                self.move_step = self.my_situation.cur_step
                return self.head_tank.do_move_to_point(path[-1])

        #

        if self.my_situation.cur_step - self.move_step > 1 and \
                self.move_step > 0:
            ret_msg = []

            for i in range(len(self.member_list)):
                tmp_path = self.member_list[i].movepath
                if not self.member_list[i].is_moving() and tmp_path != []:
                    ret_msg.extend(self.member_list[i].do_move_to_point(tmp_path[-1]))
            return ret_msg

        if self.my_situation.cur_step == 0 or self.move_step == -1:
            return self.do_overlap()

        return []

    def is_all_overlap(self):
        head_hex = self.head_tank.operator['cur_hex']
        for i in range(1, len(self.member_list)):
            if head_hex != self.member_list[i].operator['cur_hex']:
                return False
        return True

    def is_all_stop(self):
        for member in self.member_list:
            if member.is_moving():
                return False
        return True

    def is_all_cd(self):
        for member in self.member_list:
            if member.is_moving():
                return False
        return True

    def do_overlap(self):
        ret_msg = []
        #
        head_hex = self.head_tank.operator['cur_hex']

        for i in range(1, len(self.member_list)):
            if not self.member_list[i].is_moving():
                ret_msg.extend(self.member_list[i].do_move_to_point(head_hex))

        return ret_msg

    def is_finished(self):

        #
        for each in self.member_list[::-1]:
            #
            if each not in self.my_situation.our_opt:
                if not self.release_amember(each):
                    return True
        #
        if len(self.member_list) == 0:
            return True
        return False

    def gen_move(self, opt):
        """Generate move action to a random city."""
        bop = opt
        if bop['sub_type'] == 3:
            return None
        destination = random.choice([city['coord'] for city in self.observation['cities']])
        if bop and bop['cur_hex'] != destination:
            move_type = self.get_move_type(bop)
            route = self.my_situation.map.gen_move_route(bop['cur_hex'], destination, move_type)
            return route
        return None

    def get_move_type(self, bop):
        """Get appropriate move type for a bop."""
        bop_type = bop['type']
        if bop_type == BopType.Vehicle:
            if bop['move_state'] == MoveType.March:
                move_type = MoveType.March
            else:
                move_type = MoveType.Maneuver
        elif bop_type == BopType.Infantry:
            move_type = MoveType.Walk
        else:
            move_type = MoveType.Fly
        return move_type


#
class booming_team(strategy):
    def __init__(self, color):
        strategy.__init__(self, color)
        #
        #
        self.planning_dict = {}

    def check(self):
        for each_opt in self.my_situation.our_opt:
            if each_opt.operator['sub_type'] == ARTILLERY:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    return False
        for each_opt in self.my_situation.our_opt:
            if each_opt.strategy_type == STRATEGY_AUTO:
                if each_opt.operator['sub_type'] == ARTILLERY:
                    self.temp_member_list.append(each_opt)
        if len(self.temp_member_list) == 0:
            return False
            #

        if self.can_run():
            #
            for each_opt in self.temp_member_list:
                if each_opt.strategy_type != STRATEGY_AUTO:
                    each_opt.strategy.release_amember(each_opt)
                each_opt.strategy = self
                each_opt.strategy_type = STRATEGY_BOOMING_TEAM
                self.member_list.append(each_opt)
            self.assignment_task()
            return True
        return False

    def can_run(self):
        return True

    def assignment_task(self):
        if len(self.member_list) > 0:
            self.head_tank = self.member_list[0]
        return

    def run(self):

        #
        #
        for pos in self.planning_dict.values():
            if pos is not None:
                self.my_situation.planning_pos.append(pos)
        if len(self.my_situation.my_artillery_pos_list) == 0:
            return []

        ret_msg = []
        for i in range(len(self.member_list)):
            if self.is_cd(self.member_list[i]) and len(self.my_situation.my_artillery_pos_list) > 0:
                obj_id = self.member_list[i].operator['obj_id']
                if self.planning_dict.get(obj_id) is not None:
                    self.planning_dict[obj_id] = None

                pos = self.my_situation.my_artillery_pos_list.pop(0)
                #
                #

                msg = self.member_list[i].do_jm(pos)
                if msg != []:
                    self.planning_dict[obj_id] = pos
                    ret_msg.extend(self.member_list[i].do_jm(pos))

        return ret_msg

    def in_planning(self, pos):

        if pos in self.planning_dict.values():
            return True
        else:
            return False

    def is_cd(self, my_opt):
        if my_opt.operator['weapon_cool_time'] == 0:
            return True
        else:
            return False

    def is_finished(self):
        #
        for each in self.member_list[::-1]:
            #
            if each not in self.my_situation.our_opt:
                if not self.release_amember(each):
                    return True
        #
        #
        if len(self.member_list) == 0:
            return True
        if self.my_situation.enenmy_is_coming:
            return False
        return False


#
class command_action:
    def __init__(self):
        self.action = {}
        self.cur_bop = None
        self.is_done = False
        self.time = 1
        self.time_end = 9999999
        self.target_obj_id = None
        self.XY = None
        self.move_path = []
        self.weapon_id = None
        self.jm_pos = None
        self.program = ['self.My_auto_shoot', 'self.My_auto_getoff']


#
class land_tool:
    #
    def __init__(self, map, scenario_info):
        self.my_firetool = FireTool(map)
        #
        self.map = map
        self.color = my_ai.color
        self._m_scenario_info = scenario_info
        #
        #
        land_tool._stack_pos_list = []
        self.map_data = self.map.get_map_data()

        self.height_dic = {}
        self.cond_dic = {}
        self.grid_id_dic = {}
        self.grid_type_dic = {}
        #
        self.forest_grid = 8
        self.soft_grid = 6
        self.city_grid = 7

        self.map_max_x = len(self.map_data)  #
        self.map_max_y = len(self.map_data[0])  #

        for idx_x in range(self.map_max_x):
            for idx_y in range(self.map_max_y):
                xy = idx_x * 100 + idx_y
                self.height_dic[xy] = self.map_data[idx_x][idx_y]['elev'] % 1000
                self.cond_dic[xy] = self.map_data[idx_x][idx_y]['cond']

        #
        self.cities_dic = self._m_scenario_info['-1']['cities']

        #
        self.main_city_xy = self.cities_dic[0]['coord']

        #
        #
        self.select_cities_list = []
        self.set_point_dir = {}

    def get_out_stack_pos(self, select_xy_list):
        select_xy_set = set(select_xy_list)
        stack_pos_set = set(land_tool._stack_pos_list)
        select_xy_list = list((select_xy_set) - (select_xy_set & stack_pos_set))

        return select_xy_list

    #
    def get_first_step_points(self):
        self.remove_firststep_bad_pos()
        self.set_first_step_points()
        operators = self._m_scenario_info['-1']['operators']
        for opt in operators:
            if opt['color'] == self.color:
                if self.set_point_dir.get(my_ai.scenario) and \
                        self.set_point_dir[my_ai.scenario][my_ai.command_number].get(opt['obj_id']) != None:
                    if opt['sub_type'] == CAR:
                        pos = self.get_pos_first_step_cars(opt)
                    pos = self.set_point_dir[my_ai.scenario][my_ai.command_number][opt['obj_id']]
                else:
                    if opt['sub_type'] == TANK:
                        pos = self.get_pos_first_step_tanks(opt)
                    elif opt['sub_type'] == CAR:
                        pos = self.get_pos_first_step_cars(opt)
                    elif opt['sub_type'] == AUTO_CAR:
                        pos = self.get_pos_first_step_autocars(opt)
                    else:
                        pos = 0
                    pos = [pos]
                my_ai.all_first_pos[opt['obj_id']] = pos
                land_tool._stack_pos_list.append(pos[0])
        return True

    def remove_firststep_bad_pos(self):
        if my_ai.scenario == 3631:
            land_tool._stack_pos_list = [2732]
        return []

    def set_first_step_points(self):
        temp_list = []
        for i in range(10):
            temp_list.append({})
        #
        #
        temp_dir = {14767: 2420
                    }
        temp_list[0] = temp_dir
        #
        self.set_point_dir[3631] = temp_list
        #
        #
        temp_dir = my_ai.plan_pos_list
        temp_list[0] = temp_dir
        #
        self.set_point_dir[2010211129] = temp_list
        return True

    #
    def get_pos_first_step_tanks(self, opt):
        if opt['color'] == RED:
            return self.get_pos_nearmaincity_wellsight_tanks(opt, start_mv_r=15)
        else:
            return self.get_pos_nearmaincity_wellsight_tanks(opt, start_mv_r=8)

    #
    def get_pos_nearmaincity_wellsight_tanks(self, opt, start_mv_r=10):
        pos_list = self.get_first_tank_point(opt, start_mv_r=start_mv_r)
        if pos_list:
            move_pos = pos_list[0]
        else:
            move_pos = self.get_initial_position(opt)
        return move_pos

    #
    def get_pos_first_step_cars(self, opt):
        for each_city in self.cities_dic:
            my_ai.all_first_city[opt['obj_id']] = self.cities_dic[random.randint(0, len(self.cities_dic) - 1)]
            if each_city not in self.select_cities_list:
                self.select_cities_list.append(each_city)
                my_ai.all_first_city[opt['obj_id']] = each_city
                break
        if self.color == RED:
            return self.get_pos_nearmaincity_safe_and_wellsight(opt, my_ai.all_first_city[opt['obj_id']]['coord'])
        else:
            return self.get_pos_nearmaincity_safe(opt, my_ai.all_first_city[opt['obj_id']]['coord'])

    #
    def get_pos_nearmaincity_safe(self, opt, city_pos, circle=5, deploy_thick=4):
        pos_found = False
        pos_list = self.get_first_blue_car_point(opt,
                                                 city_pos,
                                                 r=circle, deploy_thick=4)
        dis_opt_maincity = self.map.get_distance(opt['cur_hex'],
                                                 city_pos)
        if dis_opt_maincity == None:
            return []
        for p in pos_list:
            dis_cur_p = self.map.get_distance(p[0], opt['cur_hex'])
            if dis_cur_p == None:
                continue
            if dis_cur_p < dis_opt_maincity:
                pos_found = True
                move_pos = p[0]
                break
        if pos_found == False:
            move_pos = self.get_initial_position(opt)
        return move_pos

    #
    def get_pos_nearmaincity_safe_and_wellsight(self, opt, city_pos, deploy_thick=6):
        pos_found = False
        pos_list = self.get_first_car_point(opt, city_pos,
                                            deploy_thick=deploy_thick)
        dis_opt_maincity = self.map.get_distance(opt['cur_hex'],
                                                 city_pos)
        if dis_opt_maincity == None:
            return []
        for p in pos_list:
            dis_cur_p = self.map.get_distance(p[0], opt['cur_hex'])
            if dis_cur_p == None:
                continue
            if dis_cur_p < dis_opt_maincity:
                pos_found = True
                move_pos = p[0]
                break
        if pos_found == False:
            move_pos = self.get_initial_position(opt)
        return move_pos

    #
    def get_pos_first_step_autocars(self, opt):
        pos_list = self.get_first_tank_point(opt, start_mv_r=15)
        if pos_list:
            move_pos = pos_list[0]
        else:
            move_pos = self.get_initial_position(opt)
        return move_pos

    #
    def get_closet_positon(self, cur_pos, pos_list):  #
        if pos_list == []:
            return cur_pos
        dis_list = {}
        for p in pos_list:
            dis = self.map.get_distance(cur_pos, p)
            dis_list.update({p: dis})
        move_pos = min(dis_list, key=dis_list.get)
        return move_pos

    #
    #
    def get_atk_pos(self, src_opt, dst_opt, select_xy_list, ):
        #
        select_xy_list = self.get_out_stack_pos(select_xy_list)

        copy_src_opt = copy.deepcopy(src_opt)
        res = -999
        res_xy = None
        for xy in select_xy_list:
            copy_src_opt['cur_hex'] = xy

            if self.map.gen_move_route(src_opt['cur_hex'], xy, 0) is None:
                continue

            src2dst = self.my_firetool.get_simulate_damage(dst_opt, copy_src_opt, dst_opt['cur_hex'], self)
            dst2src = self.my_firetool.get_simulate_damage(src_opt, dst_opt, xy, self)
            #
            if src2dst == -999:
                continue

            tmp_res = src2dst - dst2src
            if tmp_res > res:
                res = tmp_res
                res_xy = xy
        return res_xy, res

    #
    #
    def get_neighbors_circle(self, cur_pos, circle):
        if circle == 0:
            return [cur_pos]
        else:
            round_list = []
            pos_list = []
            pos_list.append(cur_pos)
            round_list.append(cur_pos)
            for i in range(circle):
                new_round_list = []
                for n in round_list:
                    l_temp = self.map.get_neighbors(n)
                    for l in l_temp:
                        if l in pos_list:
                            continue
                        else:
                            pos_list.append(l)
                            new_round_list.append(l)
                round_list = new_round_list
            pos_list.remove(cur_pos)
            return pos_list

    #
    #
    #
    #
    #
    def get_first_blue_car_point(self, car_opt, dst_xy, r=7, deploy_thick=4):
        try:
            #
            tmp_opt = car_opt

            start_xy = tmp_opt['cur_hex']

            res_list = self.map.gen_move_route(start_xy, dst_xy, 0)

            if res_list is None:
                return None

            tmp_time = self.get_path_cost(res_list)

            #
            max_deploy_r = int(tmp_time / 20)

            #
            min_deploy_r = max_deploy_r - deploy_thick

            #

            #
            quadrant_list = self.get_quadrant(start_xy, dst_xy)

            our_pos_list = self.get_big_six(start_xy, max_deploy_r, min_deploy_r, quadrant_list)

            #
            our_pos_list = self.get_out_stack_pos(our_pos_list)

            #
            our_pos_list_new = []
            for our_pos_xy in our_pos_list:
                tmp_dis = self.map.get_distance(our_pos_xy, dst_xy)
                if tmp_dis is not None and tmp_dis < r:
                    our_pos_list_new.append(our_pos_xy)

            our_pos_list = our_pos_list_new

            enemy_pos_list = self.get_big_six(dst_xy, 6)

            #

            unsight_tuple_list = self.sight_list1_2_list2(our_pos_list, enemy_pos_list, res_num=1000)

            return unsight_tuple_list[:10]
        except Exception as e:
            raise e

    #
    #
    def get_villege_tree_list(self, pos_list):
        villages_list = []
        tree_list = []
        for i in pos_list:
            if self.m_terrain.df_map_data.GridType[i] == 3 and self.m_terrain.df_map_data.GridID[i] == 51:  #
                villages_list.append(i)
            if self.m_terrain.df_map_data.GridType[i] == 3 and self.m_terrain.df_map_data.GridID[i] == 52:  #
                tree_list.append(i)
        return villages_list, tree_list

    #
    #
    #
    #
    #
    #
    #
    #
    #

    #
    #
    #
    #
    #
    #
    #
    #
    #

    #
    #
    def get_initial_position(self, opt):
        #
        CircleAroundMaincity = 9
        #
        dis_opt_maincity = self.map.get_distance(opt['cur_hex'],
                                                 self.cities_dic[0]['coord'])
        villagesAroundMaincity, treeAroudMaincity = \
            self.get_villege_tree_aroundMaincity(opt['cur_hex'],
                                                 dis_opt_maincity,
                                                 CircleAroundMaincity,
                                                 land_tool._stack_pos_list)  #
        if treeAroudMaincity:
            dis_list = {}
            for tree in treeAroudMaincity:
                dis = self.map.get_distance(opt['cur_hex'], tree)
                dis_list.update({tree: dis})
            move_pos = min(dis_list, key=dis_list.get)
        elif villagesAroundMaincity:
            dis_list = {}
            for tree in villagesAroundMaincity:
                dis = self.map.get_distance(opt['cur_hex'], tree)
                dis_list.update({tree: dis})
            move_pos = min(dis_list, key=dis_list.get)
        else:
            move_step = int(dis_opt_maincity - CircleAroundMaincity)
            move_pos = self.get_def_position(opt['cur_hex'], self.cities_dic[0]['coord'], 1, move_step)
        return move_pos

    #
    #
    #
    #
    #
    #
    def getPoint_nicesight_toXYaround(self, opt, dir_xy, start_mv_r=10):
        try:
            tmp_opt = opt

            start_xy = tmp_opt['cur_hex']
            #
            quadrant_list = self.get_quadrant(dir_xy, start_xy)
            our_pos_list = self.get_big_six(dir_xy, start_mv_r, quadrant_list=quadrant_list)

            #
            enemy_pos_list = self.get_big_six(dir_xy, 6, 0)

            #
            our_pos_list = self.get_out_stack_pos(our_pos_list)

            #
            sight_tuple_list = self.sight_list1_2_list2(our_pos_list, enemy_pos_list, res_num=100, rev=1)

            sorted_list = sorted(sight_tuple_list, key=lambda x: len(x[1]), reverse=True)

            new_list = []
            for sorted_tuple in sorted_list:
                xy = sorted_tuple[0]
                #
                res_list = self.map.gen_move_route(start_xy, xy, 0)

                if res_list is None:
                    continue

                tmp_time = self.get_path_cost(res_list) + 1
                weight = 0
                if self.is_town(xy) or self.is_jungle(xy):
                    weight += 200

                if self.main_city_xy in sorted_tuple[1]:
                    weight += 50

                #
                weight += len(sorted_tuple[1])

                weight /= tmp_time

                new_list.append((xy, len(sorted_tuple[1]), tmp_time, weight))

            sorted_list = sorted(new_list, key=lambda x: x[3], reverse=True)
            res_list = []
            for tmp in sorted_list:
                res_list.append(tmp[0])

            return res_list[:10]
        except Exception as e:
            raise e

    #
    #
    def get_villege_tree_aroundMaincity(self, src_pos, dis_src_maincity, circle, pos_dirty):
        #
        y = int(self.cities_dic[0]['coord'] / 100)
        x = self.cities_dic[0]['coord'] % 100
        if x + circle > self.map_max_x:
            right = self.map_max_x
        else:
            right = x + circle
        if x - circle < 0:
            left = 0
        else:
            left = x - circle
        if y - circle < 0:
            up = 0
        else:
            up = y - circle
        if y + circle > self.map_max_y:
            down = self.map_max_y
        else:
            down = y + circle
        posIndex = []
        for i in range(up, down):
            for j in range(left, right):
                posIndex.append(i * 100 + j)
        villages_postion = []
        tree_postion = []
        for i in posIndex:
            pick = False
            for pos_ in pos_dirty:
                if i == pos_:
                    pick = True
                    break
            if pick == True:
                continue

            if self.is_town(i):
                if self.map.can_see(i, self.cities_dic[0]['coord'], 0):
                    dis_cur_i = self.map.get_distance(i, src_pos)
                    if dis_cur_i < dis_src_maincity:
                        villages_postion.append(i)
            if self.is_jungle(i):
                if self.map.can_see(i, self.cities_dic[0]['coord'], 0):
                    dis_cur_i = self.map.get_distance(i, src_pos)
                    if dis_cur_i < dis_src_maincity:
                        tree_postion.append(i)
        return villages_postion, tree_postion

    #
    def get_villege_tree_Straight_def(self, src_pos_hex, def_pos_hex):
        m_terrain = self.m_terrain
        y = int(def_pos_hex / 100)
        x = def_pos_hex % 100
        circle = self.map.get_distance(src_pos_hex, def_pos_hex)
        if x + circle > self.map_max_x:
            right = self.map_max_x
        else:
            right = x + circle
        if x - circle < 0:
            left = 0
        else:
            left = x - circle
        if y - circle < 0:
            up = 0
        else:
            up = y - circle
        if y + circle > self.map_max_y:
            down = self.map_max_y
        else:
            down = y + circle
        posIndex = []
        for i in range(up, down):
            for j in range(left, right):
                posIndex.append(i * 100 + j)
        if src_pos_hex in posIndex:
            posIndex.remove(src_pos_hex)
        villages_postion = []
        tree_postion = []

        for i in posIndex:
            dis_def_i = self.map.get_distance(def_pos_hex, i)
            if m_terrain.df_map_data.GridType[i] == 3 and m_terrain.df_map_data.GridID[i] == 51:  #
                dis_cur_i = self.map.get_distance(src_pos_hex, i)
                if dis_cur_i < circle and dis_def_i < circle:
                    villages_postion.append(i)
            if m_terrain.df_map_data.GridType[i] == 3 and m_terrain.df_map_data.GridID[i] == 52:  #
                dis_cur_i = self.map.get_distance(src_pos_hex, i)
                if dis_cur_i < circle and dis_def_i < circle:
                    tree_postion.append(i)
        return villages_postion, tree_postion

    #
    def get_def_position(self, curPosition, objPosition, ForwardOrBack, step):  #
        #
        a = int(curPosition / 100)
        b = curPosition % 100
        x = (int(objPosition / 100) - a) * ForwardOrBack
        y = (objPosition % 100 - b) * ForwardOrBack
        if x < 0:
            x_ = -1
        if x > 0:
            x_ = 1
        if x == 0:
            x_ = 0
        if y < 0:
            y_ = -1
        if y > 0:
            y_ = 1
        if y == 0:
            y_ = 0
        x = math.fabs(x)
        y = math.fabs(y)
        t = x + y
        if t == 0:
            return curPosition
        x = x / t
        y = y / t
        def_pos = int(a + step * x * x_) * 100 + int(b + step * y * y_)
        return def_pos

    #
    @staticmethod
    def get_quadrant(src_xy, dst_xy):
        quadrant_list = [(), (-1, 1), (1, 1), (1, -1), (-1, -1)]

        src_x = int(src_xy / 100)
        src_y = int(src_xy % 100)

        dst_x = int(dst_xy / 100)
        dst_y = int(dst_xy % 100)

        drt_x = dst_x - src_x
        drt_y = dst_y - src_y

        res_list = []

        for i in range(1, 5):

            if drt_x / quadrant_list[i][0] >= 0 and \
                    drt_y / quadrant_list[i][1] >= 0:
                res_list.append(i)

        return res_list

    #
    #
    #
    #
    #
    #
    def get_big_six(self, xy, max_r, min_r=0, quadrant_list=[]):
        try:
            if xy is None:
                return []
            if max_r == 1 and quadrant_list == []:
                tmp = self.map.get_neighbors(xy)
                tmp2 = [xy]
                for each in tmp:
                    if each != -1:
                        tmp2.append(each)
                return tmp2

            res_list = []

            #
            clr_quadrant_list = []
            for i in range(len(quadrant_list)):
                if quadrant_list[i] in [1, 2, 3, 4]:
                    clr_quadrant_list.append(quadrant_list[i])
            clr_quadrant_set = set(clr_quadrant_list)
            #

            for x0 in range(self.map_max_x):
                for y0 in range(self.map_max_y):
                    tmp_xy = x0 * 100 + y0
                    if len(clr_quadrant_set) != 0:
                        new_set = set(self.get_quadrant(xy, tmp_xy)).intersection(clr_quadrant_set)
                        if len(new_set) == 0:
                            continue

                    tmp_res = self.map.get_distance(xy, tmp_xy)
                    if tmp_res is not None and max_r >= tmp_res >= min_r:
                        res_list.append(tmp_xy)

            return res_list
        except Exception as e:
            raise e

    #
    #
    #
    #
    #
    #
    def sight_list1_2_list2(self, list1_xy, list2_xy, res_num=10, rev=0):

        try:
            res_dic = {}
            for xy1 in list1_xy:
                res_dic[xy1] = []
                for xy2 in list2_xy:
                    #
                    #

                    if self.sight_rule(xy1, xy2):
                        if res_dic.get(xy1) is not None:
                            res_dic[xy1].append(xy2)
                        else:
                            res_dic[xy1] = [xy2]

            if rev == 1:
                sorted_list = sorted(res_dic.items(), key=lambda d: len(d[1]), reverse=True)
            else:
                sorted_list = sorted(res_dic.items(), key=lambda d: len(d[1]), reverse=False)

            res_list = sorted_list[:res_num]
            return res_list
        except Exception as e:
            raise e

    #
    #
    #
    #
    def sight_rule(self, xy1, xy2):
        return self.map.can_see(xy1, xy2, 0)

    #
    #
    #
    #
    def is_town(self, xy):
        try:
            tmp_cond = self.cond_dic[xy]

            if tmp_cond == 2:
                return True
            else:
                return False


        except Exception as e:
            raise e

    #
    #
    #
    #
    def is_jungle(self, xy):
        try:

            tmp_cond = self.cond_dic[xy]

            if tmp_cond == 1:
                return True
            else:
                return False

        except Exception as e:
            raise e

    #
    #
    #
    #
    def is_water(self, xy):
        try:
            tmp_cond = self.cond_dic[xy]

            if tmp_cond == 4:
                return True
            else:
                return False
        except Exception as e:
            raise e

    #
    #
    #
    #
    def get_eff_lev(self, xy1, xy2):
        try:
            height_xy1 = self.height_dic[xy1]
            height_xy2 = self.height_dic[xy2]
            if height_xy1 is not None and height_xy2 is not None:
                return int((height_xy1 - height_xy2) / 20)
            else:
                return None

        except Exception as e:
            raise e

    #
    #
    #
    #
    def get_path_cost(self, path_list, time_list=[], vehicle='car'):
        try:
            if vehicle == 'car':
                defaule_time = 20

            if len(path_list) <= 0:
                return 0
            cur_xy = path_list[0]
            #

            #
            res_cost = 0
            time_list.append(0)
            for path_idx in range(1, len(path_list)):
                nxt_xy = path_list[path_idx]
                height_diff = self.height_dic[nxt_xy] - self.height_dic[cur_xy]
                mul_num = 1
                #
                #
                if height_diff > 0:
                    mul_num *= (int(height_diff / 20))

                #
                if self.is_town(nxt_xy):
                    mul_num *= 3
                res_cost += mul_num * defaule_time
                time_list.append(res_cost)
                cur_xy = nxt_xy
            return res_cost

        except Exception as e:
            raise e

    #
    #
    #
    #
    #
    #
    #
    #
    #
    def get_first_car_point(self, car_opt, dst_xy, deploy_time=75, deploy_thick=6):
        try:
            #
            tmp_opt = car_opt

            start_xy = tmp_opt['cur_hex']

            res_list = self.map.gen_move_route(start_xy, dst_xy, 0)

            if res_list is None:
                return None

            #

            tmp_time = self.get_path_cost(res_list)

            #
            tmp_time -= deploy_time

            max_move_time = tmp_time - deploy_time
            #
            max_deploy_r = int(max_move_time / 20)

            #
            min_deploy_r = max_deploy_r - deploy_thick

            #

            #
            quadrant_list = self.get_quadrant(start_xy, self.main_city_xy)

            our_pos_list = self.get_big_six(start_xy, max_deploy_r, min_deploy_r, quadrant_list)

            #
            our_pos_list = self.get_out_stack_pos(our_pos_list)

            #
            our_pos_list_new = []
            for our_pos_xy in our_pos_list:
                tmp_dis = self.map.get_distance(our_pos_xy, self.main_city_xy)
                if tmp_dis is not None and tmp_dis < 15:
                    our_pos_list_new.append(our_pos_xy)

            our_pos_list = our_pos_list_new
            #
            #
            enemy_pos_list = self.get_big_six(self.main_city_xy, 6)

            #
            #
            unsight_tuple_list = self.sight_list1_2_list2(our_pos_list, enemy_pos_list, res_num=1000)

            #
            judge_tuple_list = []

            #

            for unsight_tuple in unsight_tuple_list:
                #
                unsight_xy = unsight_tuple[0]

                #
                besight_len = len(unsight_tuple[1])
                #
                tmp_unsight_xy_round_list = self.get_big_six(unsight_xy, 1, 1)

                #
                unsight_xy_round_list = []
                for unsight_xy_round in tmp_unsight_xy_round_list:
                    if self.is_town(unsight_xy_round) or self.is_jungle(unsight_xy_round):
                        unsight_xy_round_list.append(unsight_xy_round)
                        #
                        #

                if len(unsight_xy_round_list) == 0:
                    continue
                #
                #

                #

                #
                sight_tuple_list = self.sight_list1_2_list2(unsight_xy_round_list, enemy_pos_list, res_num=100, rev=1)

                #
                tmp_set = set()
                for sight_tuple in sight_tuple_list:
                    sight_list = sight_tuple[1]

                    tmp_set = tmp_set.union(set(sight_list))

                set_len = len(tmp_set)

                #

                #

                #
                if len(sight_tuple_list):
                    tmp = sight_tuple_list[0]
                    best_xy = tmp[0]

                #
                is_spec_point = False
                if self.is_jungle(best_xy) or self.is_town(best_xy):
                    is_spec_point = True
                if is_spec_point is False:
                    continue

                #
                tmp_path_list = self.map.gen_move_route(start_xy, best_xy, 0)
                tmp_time = self.get_path_cost(tmp_path_list)

                #
                weight = (set_len + 1) / (besight_len + 1)
                judge_tuple_list.append((unsight_xy, besight_len, set_len, best_xy, tmp_time, weight
                                         ))

                #

            #
            sort_judge = sorted(judge_tuple_list, key=lambda x: (x[5]), reverse=True)

            res_tuple_list = []
            #
            for tmp_res in sort_judge:
                if len(tmp_res) >= 4:
                    res_tuple_list.append((tmp_res[0], tmp_res[3]))

            return res_tuple_list[:10]
        except Exception as e:
            raise e

        #
        #

    #
    #
    #
    #
    #
    #
    def get_first_tank_point(self, tank_opt, start_mv_r=10):
        try:
            tmp_opt = tank_opt

            #
            start_xy = tmp_opt['cur_hex']

            #
            quadrant_list = self.get_quadrant(self.main_city_xy, start_xy)
            our_pos_list = self.get_big_six(self.main_city_xy, start_mv_r, quadrant_list=quadrant_list)

            #
            our_pos_list = self.get_out_stack_pos(our_pos_list)

            #
            #

            #
            #
            #

            #
            enemy_pos_list = self.get_big_six(self.main_city_xy, 6, 0)

            #
            sight_tuple_list = self.sight_list1_2_list2(our_pos_list, enemy_pos_list, res_num=100, rev=1)

            sorted_list = sorted(sight_tuple_list, key=lambda x: len(x[1]), reverse=True)

            new_list = []
            for sorted_tuple in sorted_list:
                xy = sorted_tuple[0]
                #
                res_list = self.map.gen_move_route(start_xy, xy, 0)

                if res_list is None:
                    continue
                tmp_time = self.get_path_cost(res_list) + 1

                #
                weight = len(sorted_tuple[1]) / tmp_time

                new_list.append((xy, len(sorted_tuple[1]), tmp_time, weight))

            sorted_list = sorted(new_list, key=lambda x: x[3], reverse=True)
            res_list = []
            for tmp in sorted_list:
                res_list.append(tmp[0])

            return res_list[:10]
        except Exception as e:
            raise e

    #
    #
    def get_special_list(self, org_xy, r, quadrant_list):
        try:
            res = []
            all_xy = self.get_big_six(org_xy, r, 0, quadrant_list)
            for tmp_xy in all_xy:
                if self.is_town(tmp_xy) or self.is_jungle(tmp_xy):
                    res.append(tmp_xy)
            if len(res) == 0:
                return None
            return res

        except Exception as e:
            raise e

    def get_quadrant_big(self, src_xy, dst_xy):
        src_x = int(src_xy / 100)
        src_y = int(src_xy % 100)

        dst_x = int(dst_xy / 100)
        dst_y = int(dst_xy % 100)

        from math import fabs

        drt_y = (dst_y - src_y)
        drt_x = (dst_x - src_x)
        if fabs(drt_y) >= fabs(drt_x):
            if drt_y <= 0:
                return [3, 4]
            else:
                return [1, 2]
        else:
            if drt_x <= 0:
                return [1, 4]
            else:
                return [2, 3]

    #
    def do_patrol_spec(self, r, src_xy, dst_xy):
        #
        #
        #
        src_x = int(src_xy / 100)
        src_y = int(src_xy % 100)

        dst_x = int(dst_xy / 100)
        dst_y = int(dst_xy % 100)

        from math import fabs

        drt_y = (dst_y - src_y)
        drt_x = (dst_x - src_x)

        #
        #
        if fabs(drt_y) >= fabs(drt_x):
            if drt_y <= 0:
                res = self.get_special_list(self.main_city_xy, r, [3, 4])
            else:
                res = self.get_special_list(self.main_city_xy, r, [1, 2])

        else:
            if drt_x <= 0:
                res = self.get_special_list(self.main_city_xy, r, [1, 4])
            else:
                res = self.get_special_list(self.main_city_xy, r, [2, 3])
        path_list = []
        if len(res) == 0:
            return None

        for dst_xy in res:
            res_list = self.map.gen_move_route(opt_xy, dst_xy, 3)
            opt_xy = dst_xy
            path_list += res_list

        return path_list

    #
    #
    #
    #
    #
    def AstarFindPath_known_enemy(self, our_opt, end_hex, enemy_opts, forbid_list=[], unsee=[]):
        #
        start_hex = our_opt['cur_hex']

        isFound = False
        pathList = []

        openPointList = []
        #
        closePointList = []

        #
        h = self.map.get_distance(start_hex, end_hex)
        g = 0
        f = h

        start_point = {'hex': start_hex, 'parent': None, 'g': 0, 'h': h, 'f': h}
        openPointList.append(start_point)
        while (len(openPointList) > 0):
            #
            minFPoint = self.findPointWithMinF(openPointList)
            #
            openPointList.remove(minFPoint)
            closePointList.append(minFPoint)
            #
            #
            #
            neighbors = self.map.get_neighbors(minFPoint['hex'])
            if neighbors == -1:
                continue
            for kv in neighbors:
                if kv == -1:
                    continue
                #
                if self.get_eff_lev(minFPoint['hex'], kv) >= 5:
                    continue
                flag, indexCloseList = self.findInCloseList(kv, closePointList)
                if flag == True:
                    continue
                flag, indexOpenList = self.findInOpenList(kv, openPointList)
                if flag == True:
                    g = minFPoint['g'] + self.calMoveTimeCost_known_enemy(minFPoint['hex'], kv, our_opt, enemy_opts,
                                                                          forbid_list)
                    if g < minFPoint['g']:
                        openPointList[indexOpenList]['parent'] = minFPoint['hex']
                        openPointList[indexOpenList]['g'] = g
                        openPointList[indexOpenList]['f'] = g + openPointList[indexOpenList]['h']
                else:
                    g = minFPoint['g'] + self.calMoveTimeCost_known_enemy(minFPoint['hex'], kv, our_opt, enemy_opts,
                                                                          forbid_list)
                    #
                    h = self.map.get_distance(kv, end_hex)
                    f = g + h
                    openPointList.append({'hex': kv, 'parent': minFPoint['hex'], 'g': g, 'h': h, 'f': f})

            flag, indexEnd_hexInOpenList = self.findInOpenList(end_hex, openPointList)
            if flag == True:

                isFound = True
                pathList.append(end_hex)
                cur_hex = minFPoint['hex']
                while (cur_hex != start_hex):
                    flag, indexCloseList = self.findInCloseList(cur_hex, closePointList)
                    if flag == True:
                        pathList.append(closePointList[indexCloseList]['hex'])
                        cur_hex = closePointList[indexCloseList]['parent']
                    else:
                        isFound = False
                        return isFound, pathList
                pathList.reverse()
                return isFound, pathList
        pathList.reverse()
        return isFound, pathList

    #
    def findPointWithMinF(self, openPointList):
        currentNode = openPointList[0]
        for node in openPointList:
            if node['f'] < currentNode['f']:
                currentNode = node
        return currentNode

    def findInOpenList(self, cur_point_hex, openPointList):
        for i in range(len(openPointList)):
            if cur_point_hex == openPointList[i]['hex']:
                return True, i
        return False, None

    def findInCloseList(self, cur_point_hex, closePointList):
        for i in range(len(closePointList)):
            if cur_point_hex == closePointList[i]['hex']:
                return True, i
        return False, None

    #
    def calMoveTimeCost_known_enemy(self, cur_hex, def_hex, our_opt, enemy_opts, forbid_list=[]):

        #
        Cond = self.cond_dic[def_hex]
        #

        if len(enemy_opts) > 0:
            for enemy_opt in enemy_opts:
                if self.map.can_see(enemy_opt['cur_hex'], cur_hex, 0) is True:
                    return 999
            #
            #

        #

        if Cond == 4:  #
            cost = 2
            return cost
        if Cond == 2:  #
            cost = 3
            return cost

        if Cond == 1:  #
            cost = 2
            return cost
        if Cond == 3:  #
            cost = 4
            return cost

        #
        #
        #
        #
        #

        if self.get_eff_lev(cur_hex, def_hex) >= 5:
            return None
        if self.get_eff_lev(cur_hex, def_hex) >= 2:
            return self.get_eff_lev(cur_hex, def_hex)
        return 1

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    def get_target_list(self, cur_hex, dis, ele_diff):
        cur_ele = self.height_dic[cur_hex] / 20
        res_list = []

        select_xy_list = self.get_big_six(cur_hex, dis, dis - 1)

        for xy in select_xy_list:
            if cur_ele - (self.height_dic[xy] / 20) == ele_diff:
                res_list.append(xy)

        return res_list

    #
    #
    #
    def get_connect_set(self, xy_list):
        res_list_in_list = []

        for xy in xy_list:
            in_land = False
            for land_list in res_list_in_list:
                if self.in_set(land_list, [xy]):
                    land_list.append(xy)
                    in_land = True
                    break
            if in_land is False:
                res_list_in_list.append([xy])

        for land_list1 in res_list_in_list[::-1]:
            tmp_list = res_list_in_list
            for land_list2 in tmp_list:
                if land_list1 != land_list2 and self.in_set(land_list1, land_list2):

                    if land_list1 in res_list_in_list:
                        res_list_in_list.remove(land_list1)
                        land_list2.extend(land_list1)
                        break

            #

        return res_list_in_list

    #
    #
    def in_set(self, land_list1, land_list2):
        for tmp_xy in land_list1:
            for tmp_xy_2 in land_list2:
                if self.map.get_distance(tmp_xy, tmp_xy_2) <= 1:
                    return True
        return False

    #
    #
    def get_distance_list2list(self, land_list1, land_list2):
        res_distance = 999
        for tmp_xy in land_list1:
            for tmp_xy2 in land_list2:
                tmp_distance = self.map.get_distance(tmp_xy, tmp_xy2)
                if tmp_distance < res_distance:
                    res_distance = tmp_distance

        return res_distance

    #
    #
    def get_edge(self, land_list):
        land_list = sorted(land_list, key=lambda x: x)

        res_list = []
        res_set = set()

        for xy in land_list:
            tmp_set = self.map.get_neighbors(xy)

            res_set = res_set - set([xy])
            res_set = res_set.union(tmp_set)

        res_list = list(res_set)

        return res_list

    #
    def get_order_by_heighth(self, xy_list):
        res_tuple_list = []
        for xy in xy_list:
            res_tuple_list.append((xy, self.height_dic[xy]))
        res_tuple_list = sorted(res_tuple_list, key=lambda x: x[1], reverse=True)
        res_list = []
        for tuple in res_tuple_list:
            res_list.append(tuple[0])
        return res_list



class FireTool:
    def __init__(self, map):
        self._max_ele = 999999
        self._m_weapon_record = MyWeaponRecord()
        #
        self.map = map
        #
        self._direct_weapont_dic = self._m_weapon_record.wp_dic

        #
        self._ele_rect2car_np = self._m_weapon_record.ele_rect2car_np
        self._wp2car_judge_idx_np = self._m_weapon_record.wp2car_judge_0_np
        self._wp2car_judge_res_np = self._m_weapon_record.wp2car_judge_1_np
        self._wp2car_judge_revise_np = self._m_weapon_record.wp2car_judge_2_np

        #
        self._ele_rect2peo_np = self._m_weapon_record.ele_rect2peo_np
        self._wp2peo_judge_res_np = self._m_weapon_record.wp2peo_judge_0_np
        self._wp2peo_judge_revise_np = self._m_weapon_record.wp2peo_judge_1_np

        self._wp2plane_res_np = self._m_weapon_record.wp2plane_judge_0_np

        #
        #
        #
        #

        #
        #
        #

        #
        self._dices_num = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
        #
        self._missiles_wp_id = [69, 71, 73, 74, 75, 83, 84]
        self._indirect_wp_id = [88, 72]
        self.attract = {}
        self.attract_dir = {}

        #
        self.fast_car_res_list = [[],[1,6,9,12,15,18,24,30,39,42],
                                  [3, 9, 15, 18, 24, 30, 36, 42, 51, 58],
                                  [6, 12, 18, 24, 36, 42, 51, 58, 66, 72],
                                  [6, 12, 18, 30, 39, 51, 58, 66, 78, 91],
                                  [6, 12, 30, 39, 58, 66, 72, 91, 101, 115]]
        #
        #
        #
        self.fast_car_revise_res_list = [[3, 6, 10, 15, 21, 26, 31, 36, 42, 49, 57, 67, 77, 87, 95],
                                         [-10, -6, -2, 2, 6, 10, 16, 24, 33, 43, 54, 66, 77, 87, 95],
                                         [-31, -21, -13, -7, -3, 0, 3, 7, 14, 24, 37, 51, 66, 80, 91],
                                         [-61, -47, -34, -22, -13, -7, -2, 3, 9, 16, 25, 36, 47, 56, 63],
                                         [-95, -87, -76, -64, -51, -39, -28, -17, -7, 3, 13, 24, 36, 47, 56]]

        #
        #

    def get_simulate_damage(self, our_opt, enemy_opt, xy, land_tool):

        copy_our_opt = copy.deepcopy(our_opt)

        copy_our_opt['cur_hex'] = xy

        res = -999
        #
        for wp_index in enemy_opt['carry_weapon_ids']:
            tmp_res = self.fire_estimate(enemy_opt, wp_index, copy_our_opt, land_tool)

            if tmp_res is not None and tmp_res > res:
                res = tmp_res

        return res

    #
    def get_simulate_damage_A2B(self, our_opt, xy, enemy_opt, land_tool , my_weapon_id = None,attack_level = None):
        #print(our_opt['obj_id'],'in')
        if enemy_opt['sub_type'] == MISSILE:
            return None
        copy_our_opt = our_opt
        cur_hex = copy_our_opt['cur_hex']
        copy_our_opt['cur_hex'] = xy


        res = -999
        #
        if my_weapon_id:
            wp_ids = [my_weapon_id]
        else:
            wp_ids = copy_our_opt['carry_weapon_ids']
        for wp_index in wp_ids:

            if attack_level is None:
                #begin_time = time.time()
                tmp_res = self.fire_estimate(copy_our_opt, wp_index, enemy_opt, land_tool)
                #
            else:
                #
                if copy_our_opt['type'] == 2:
                    tmp_res = self.fast_estimate(copy_our_opt, attack_level, enemy_opt, land_tool)
                else:
                    tmp_res = self.fire_estimate(copy_our_opt, wp_index, enemy_opt, land_tool)
                #
            if tmp_res is not None and tmp_res > res:
                res = tmp_res
        copy_our_opt['cur_hex'] = cur_hex
        if res == -999:
            return None
        return res
    #
    def get_simulate_gudie_damage_A2B(self, our_opt, xy, my_guideopt , enemy_opt, land_tool , my_weapon_id = None,attack_level = None):
        #print(our_opt['obj_id'],'inguide')
        if enemy_opt['sub_type'] in FLY_OPT or enemy_opt['sub_type'] == SOILDER:
            return None
        if enemy_opt['obj_id'] not in our_opt['see_enemy_bop_ids']:
            return None


        gudied_opt = my_guideopt

        copy_our_opt = gudied_opt
        cur_hex = copy_our_opt['cur_hex']
        copy_our_opt['cur_hex'] = xy

        res = -999
        #
        if my_weapon_id:
            wp_ids = [my_weapon_id]
        else:
            wp_ids = copy_our_opt['carry_weapon_ids']
        for wp_index in wp_ids:
            if wp_index not in self._missiles_wp_id:
                continue
            if attack_level is None:
                #begin_time = time.time()
                tmp_res = self.fire_estimate(copy_our_opt, wp_index, enemy_opt, land_tool, guide=True)
                #print('guideaaaaaaaaaaaaaaa:', tmp_res, time.time() - begin_time ,copy_our_opt['blood'], enemy_opt['sub_type'])
            else:
                #begin_time = time.time()
                tmp_res = self.fast_estimate(copy_our_opt, attack_level, enemy_opt, land_tool)
                #print('guideaaaaaaaaaaaaaaa:', attack_level , tmp_res, time.time() - begin_time,copy_our_opt['blood'], enemy_opt['sub_type'])
            if tmp_res is not None and tmp_res > res:
                res = tmp_res
        copy_our_opt['cur_hex'] = cur_hex
        if res == -999:
            return None
        return res

    #
    def get_atk_dic(self, src_opt, src_wp_id, dst_type):
        try:
            src_blood = src_opt['blood']

            if dst_type != 1 or src_wp_id in self._indirect_wp_id:
                src_blood = 0

            atk_dic = self._direct_weapont_dic.get((src_wp_id, dst_type, src_blood))

            return atk_dic

        except Exception as e:
            print(e)
            raise e

    #
    #
    def fire_estimate(self, src_opt, src_wp_id, dst_opt, land_tool, guide=False):
        try:

            if dst_opt['sub_type'] == MISSILE:
                return None
            #
            src_opt_wps = src_opt['carry_weapon_ids']

            #
            src_opt_ammo_num = src_opt['C2']

            #
            if src_wp_id not in src_opt_wps:
                return None

            if src_wp_id in self._missiles_wp_id:
                if src_opt['C3'] == 0:
                    return None
            elif src_opt['C2'] == 0:
                return None

            #
            if self.map.can_see(src_opt['cur_hex'], dst_opt['cur_hex'], 0) is False and (guide is False):
                return None

            #

            if src_opt_ammo_num <= 0:
                return None

            #
            tmp_dis = self.map.get_distance(src_opt['cur_hex'], dst_opt['cur_hex'])
            if tmp_dis is None:
                return None
            dis_src_2_dst = tmp_dis

            #
            #
            see_range = src_opt['observe_distance'][dst_opt['type']]
            if land_tool.is_jungle(dst_opt['cur_hex']) or \
                    land_tool.is_town(dst_opt['cur_hex']):
                see_range /= 2

            if see_range < tmp_dis:
                return None

            #
            ele_src_2_dst = land_tool.get_eff_lev(dst_opt['cur_hex'], src_opt['cur_hex'])
            if ele_src_2_dst is None:
                return None

            #
            dst_type = dst_opt['type']

            #
            atk_dic = self.get_atk_dic(src_opt, src_wp_id, dst_type)
            if atk_dic is None:
                return None

            #
            #self.fast_estimate(self, src_opt, atk_lev, dst_opt)
            if dst_type == 2:
                res = self.fire_estimate2car(src_opt, dst_opt, atk_dic, dis_src_2_dst, ele_src_2_dst, land_tool)
            elif dst_type == 1:
                res = self.fire_estimate2peo(src_opt, dst_opt, atk_dic, dis_src_2_dst, ele_src_2_dst, land_tool)
            elif dst_type == 3:
                res = self.fire_estimate_2_plane(atk_dic, dis_src_2_dst)

            if res is not None:
                return res
            else:
                return None

        except Exception as e:
            print(e)
            raise e

    def enum_enemy_init(self, list_my_obj, list_enemy_obj):
        self.max_sum = 0
        for each_enemy_obj in list_enemy_obj:
            self.attract[each_enemy_obj.ID] = 0
        for each_obj in list_my_obj:
            self.attract_dir[each_obj] = None
        self.final_attract_dir = None

    def enum_enemy(self, list_my_obj, list_my_obj2, list_enemy_obj):

        if len(list_my_obj) == 0:
            sum = 0
            for each_enemy_obj in list_enemy_obj:
                if self.attract[each_enemy_obj.ID] <= each_enemy_obj.ObjBlood:
                    sum += self.attract[each_enemy_obj.ID] * each_enemy_obj.ObjValue
                else:
                    sum += each_enemy_obj.ObjBlood * each_enemy_obj.ObjValue
            if sum > self.max_sum:
                self.max_sum = sum
                self.final_attract_dir = copy.deepcopy(self.attract_dir)
            return 0
        list_my_obj_copy = copy.deepcopy(list_my_obj)
        obj = list_my_obj_copy[0]
        del list_my_obj_copy[0]
        for each_enemy_obj in list_enemy_obj:
            self.attract_dir[obj.ID] = each_enemy_obj
            self.attract[each_enemy_obj.ID] += self.judge[obj.ID][each_enemy_obj.ID]
            self.enum_enemy(list_my_obj_copy, list_my_obj2, list_enemy_obj)
            self.attract[each_enemy_obj.ID] -= self.judge[obj.ID][each_enemy_obj.ID]

    #

    def fire_estimate2car(self, src_opt, dst_opt, atk_dic, dis_src_2_dst, ele_src_2_dst, land_tool):
        try:
            #
            #
            #
            wp_range_min = atk_dic[0][0]
            wp_range_max = atk_dic[0][1]

            #
            if dis_src_2_dst < wp_range_min or dis_src_2_dst > wp_range_max:
                return None

            #
            if ele_src_2_dst > self._max_ele:
                return None

            #
            org_attack_lev = atk_dic[1][dis_src_2_dst]
            #print(org_attack_lev)
            #
            heighth = 0
            if ele_src_2_dst > 8:
                heighth = 8
            else:
                heighth = ele_src_2_dst
            distance = 0
            if dis_src_2_dst > 12:
                distance = 12
            else:
                distance = dis_src_2_dst
            if 1 <= distance <= 12 and heighth > 1:
                org_attack_lev += self._ele_rect2car_np[heighth - 1][distance - 1]
            #print(org_attack_lev)
            #
            #
            #
            if org_attack_lev <= 0:
                return None

            res_idx = self._wp2car_judge_idx_np[int(src_opt['blood'] - 1)][int(org_attack_lev - 1)]

            res_list = list(self._wp2car_judge_res_np[:, res_idx - 1])

            org_res = sum([a * b for a, b in zip(res_list, self._dices_num)])

            #

            res_correct = 0
            #
            #
            if src_opt['keep'] == 1:
                res_correct -= 1

                #
            if src_opt['stop'] == 0:
                res_correct -= 1

            #
            src_opt_xy = src_opt['cur_hex']
            dst_opt_xy = dst_opt['cur_hex']

            #
            if land_tool.is_water(src_opt_xy) and src_opt['sub_type'] == 0:
                res_correct -= 1

            #
            #
            if land_tool.is_town(dst_opt_xy) is True:
                res_correct -= 1

            #
            if land_tool.is_jungle(dst_opt_xy) is True:
                res_correct -= 2

            #
            if land_tool.is_water(dst_opt_xy) is True:
                res_correct -= 2

            #
            #
            if dst_opt['move_state'] == 4:
                res_correct -= 2

            #
            if dst_opt['stop'] == 0:
                res_correct -= 2

            #
            if dst_opt['stack'] == 1:
                res_correct += 2

            #
            if dst_opt['move_state'] == 1:
                res_correct += 4

            #
            dst_armour = dst_opt['armor']

            #
            rd_sta = 2 + res_correct
            res_fix = list(self._wp2car_judge_revise_np[:, dst_armour])
            res_correct_list = []

            #
            for ct in range(11):
                i = rd_sta + ct
                if i < -3:
                    res_correct_list.append(res_fix[0])
                elif i > 12:
                    res_correct_list.append(res_fix[-1])
                else:
                    res_correct_list.append(res_fix[i + 3])

            org_res_correct = sum([a * b for a, b in zip(res_correct_list, self._dices_num)])

            res = float(org_res / 36) + float(org_res_correct / 36)
            return res

        except Exception as e:
            print(e)
            raise e

    def fire_estimate2peo(self, src_opt, dst_opt, atk_dic, dis_src_2_dst, ele_src_2_dst, land_tool):
        try:
            #
            #
            #

            wp_range_min = atk_dic[0][0]
            wp_range_max = atk_dic[0][1]

            #
            if dis_src_2_dst < wp_range_min or dis_src_2_dst > wp_range_max:
                return None

            #
            if ele_src_2_dst > self._max_ele:
                return None

            #
            org_attack_lev = atk_dic[1][dis_src_2_dst]

            #
            if 1 <= dis_src_2_dst <= 12 and ele_src_2_dst > 1:
                org_attack_lev += self._ele_rect2peo_np[ele_src_2_dst - 1][dis_src_2_dst - 1]

            #
            res_list = list(self._wp2peo_judge_res_np[:, org_attack_lev - 1])

            #
            for i in range(len(res_list)):
                if res_list[i] == -1:
                    res_list[i] = 0

            org_res = sum([a * b for a, b in zip(res_list, self._dices_num)])

            #
            res_correct = 0

            #
            #
            if src_opt['keep'] == 1:
                res_correct -= 1

            #
            if src_opt['stop'] == 1:
                res_correct -= 1

            #
            #
            dst_opt_xy = dst_opt['cur_hex']

            #
            #
            if land_tool.is_town(dst_opt_xy) is True:
                res_correct -= 1

            #
            if land_tool.is_jungle(dst_opt_xy) is True:
                res_correct -= 2

            #
            #
            if dst_opt['move_state'] == 4:
                res_correct -= 2

            #
            if dst_opt['stop'] == 0:
                res_correct -= 2

            #
            if dst_opt['stack'] == 1:
                res_correct += 2

            #
            if dst_opt['move_state'] == 1:
                res_correct += 4

            res_correct_list = []
            #
            i = 2 + res_correct

            #
            for ct in range(11):
                if i <= 0:
                    res_correct_list.append(-1)
                elif i >= 8:
                    res_correct_list.append(1)
                else:
                    res_correct_list.append(0)
                i += 1

            org_res_correct = sum([a * b for a, b in zip(res_correct_list, self._dices_num)])

            res = float(org_res / 36) + float(org_res_correct / 36)
            return res

        except Exception as e:
            print(e)
            raise e

    #
    def fire_estimate_2_plane(self, atk_dic, dis_src_2_dst):
        try:
            #
            #
            #

            wp_range_min = atk_dic[0][0]
            wp_range_max = atk_dic[0][1]

            #
            if dis_src_2_dst < wp_range_min or dis_src_2_dst > wp_range_max:
                return None

            #
            org_attack_lev = atk_dic[1][dis_src_2_dst]

            #
            res_list = list(self._wp2plane_res_np[:, org_attack_lev - 1])

            #
            for i in range(len(res_list)):
                if res_list[i] == -1:
                    res_list[i] = 0

            org_res = sum([a * b for a, b in zip(res_list, self._dices_num)])

            return (org_res / 36)

        except Exception as e:
            print(e)
            raise e

    def fast_estimate(self, src_opt, atk_lev, dst_opt, land_tool):
        src_blood = src_opt['blood']
        dst_armors = dst_opt['armor']
        revise_idx = 8
        res_correct = 0
        #
        #
        if src_opt['keep'] == 1:
            res_correct -= 1

        #
        if src_opt['stop'] == 0:
            res_correct -= 1

        #
        src_opt_xy = src_opt['cur_hex']
        dst_opt_xy = dst_opt['cur_hex']

        #
        if land_tool.is_water(src_opt_xy) and src_opt['sub_type'] == 0:
            res_correct -= 1

        #
        #
        if land_tool.is_town(dst_opt_xy) is True:
            res_correct -= 1

        #
        if land_tool.is_jungle(dst_opt_xy) is True:
            res_correct -= 2

        #
        if land_tool.is_water(dst_opt_xy) is True:
            res_correct -= 2

        #
        #
        if dst_opt['move_state'] == 4:
            res_correct -= 2

        #
        if dst_opt['stop'] == 0:
            res_correct -= 2

        #
        if dst_opt['stack'] == 1:
            res_correct += 2

        #
        if dst_opt['move_state'] == 1:
            res_correct += 4
        revise_idx += res_correct
        if dst_opt['type'] == 2:
            org_res = self.fast_car_res_list[src_blood][atk_lev-1]
            revise_res = self.fast_car_revise_res_list[dst_armors][revise_idx]

            return ((org_res + revise_res) / 36)
        else:
            return 0.5

    #
    def get_wp_idx_range_base_blood(self, opt):
        blood = opt['blood']
        if blood == 1:
            return (0, 7)
        elif blood == 2:
            return (8, 12)
        elif blood == 3:
            return (13, 15)
        else:
            return (16, 17)

    def get_safe_dis(self, opt, enemy):
        wp_idx_min = self.get_wp_idx_range_base_blood(opt)[0]
        if wp_idx_min == 0:
            return 16
        if enemy['blood'] < 0 or enemy['blood'] > 4:
            return 16
        enemy_idx_range = self._wp2car_judge_idx_np[enemy['blood'] - 1]

        #
        #
        enemy_max_atk_lev = 0
        for i in enemy_idx_range:
            if i > wp_idx_min:
                break
            enemy_max_atk_lev += 1
        dis = 1
        #
        for wp_idx in enemy['carry_weapon_ids']:
            atk_dic = self.get_atk_dic(enemy, wp_idx, opt['type'])
            if atk_dic is None:
                continue

            atk_list = atk_dic[1]
            tmp_dis = 0
            for atk in atk_list:
                if atk < enemy_max_atk_lev:
                    break
                tmp_dis += 1
            if tmp_dis > dis:
                dis = tmp_dis

        return dis
        print("e")
        #
        #
        #
        #

class MyWeaponRecord:
    def __init__(self):
        #
        #
        #
        #
        #
        #
        #
        #
        self.wp_dic = {
            (71, 2, 0): ((0, 10), [7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (71, 3, 0): ((0, 10), [7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (29, 1, 1): ((0, 3), [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (29, 1, 2): ((0, 3), [4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (29, 1, 3): ((0, 3), [6, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (29, 1, 4): ((0, 3), [8, 5, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (69, 2, 0): ((2, 20), [0, 0, 5, 5, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
            (43, 1, 1): ((0, 10), [2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (43, 1, 2): ((0, 10), [3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (43, 1, 3): ((0, 10), [4, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (43, 1, 4): ((0, 10), [5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (43, 1, 5): ((0, 10), [6, 6, 6, 6, 6, 5, 5, 5, 5, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (36, 2, 0): ((0, 18), [10, 10, 10, 10, 10, 9, 9, 9, 9, 8, 8, 8, 7, 7, 6, 5, 4, 3, 2, 0, 0]),
            (36, 1, 1): ((0, 10), [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (36, 1, 2): ((0, 10), [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (36, 1, 3): ((0, 10), [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (36, 1, 4): ((0, 10), [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (36, 1, 5): ((0, 10), [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (35, 2, 0): ((0, 4), [6, 6, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 2, 0): ((0, 10), [5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 3, 0): ((0, 5), [3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 1, 1): ((0, 10), [4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 1, 2): ((0, 10), [6, 6, 6, 6, 6, 6, 5, 5, 4, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 1, 3): ((0, 10), [8, 8, 8, 8, 8, 8, 7, 7, 6, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 1, 4): ((0, 10), [9, 9, 9, 9, 9, 9, 8, 8, 7, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (56, 1, 5): ((0, 10), [10, 10, 10, 10, 10, 10, 9, 9, 8, 8, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (84, 2, 0): ((2, 20), [0, 0, 5, 5, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
            (89, 1, 0): ((0, 20), [2, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (89, 0, 0): ((0, 20), [0, 0, 0, -1, -1, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (54, 2, 0): ((0, 13), [10, 10, 9, 9, 8, 8, 7, 6, 6, 5, 5, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0]),
            (54, 1, 1): ((0, 10), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (54, 1, 2): ((0, 10), [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (54, 1, 3): ((0, 10), [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (54, 1, 4): ((0, 10), [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (54, 1, 5): ((0, 10), [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (75, 2, 0): ((0, 5), [3, 3, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (75, 1, 1): ((0, 5), [4, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (75, 1, 2): ((0, 5), [5, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (75, 1, 3): ((0, 5), [7, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (75, 1, 4): ((0, 5), [8, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (76, 2, 0): ((0, 2), [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (76, 1, 1): ((0, 2), [4, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (76, 1, 2): ((0, 2), [5, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (76, 1, 3): ((0, 2), [7, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (76, 1, 4): ((0, 2), [8, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (37, 2, 0): ((0, 15), [10, 10, 10, 9, 9, 9, 8, 8, 7, 7, 7, 6, 5, 5, 2, 2, 0, 0, 0, 0, 0]),
            (37, 1, 1): ((0, 10), [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (37, 1, 2): ((0, 10), [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (37, 1, 3): ((0, 10), [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (37, 1, 4): ((0, 10), [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (37, 1, 5): ((0, 10), [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (83, 2, 0): ((0, 20), [7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
            (74, 2, 0): ((0, 10), [7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (83, 1, 1): ((0, 10), [4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (74, 1, 1): ((0, 10), [4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (83, 1, 2): ((0, 10), [5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (74, 1, 2): ((0, 10), [5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (83, 1, 3): ((0, 10), [7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (74, 1, 3): ((0, 10), [7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (83, 1, 4): ((0, 10), [8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (74, 1, 4): ((0, 10), [8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (88, 1, 0): ((0, 20), [3, 2, 1, 1, 1, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (88, 0, 0): ((0, 20), [1, 0, -1, -1, -1, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (73, 2, 0): ((2, 20), [0, 0, 5, 5, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
            (72, 1, 0): ((0, 20), [3, 2, 2, 1, 1, 0, 1, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            (72, 0, 0): ((0, 20), [1, 1, 0, -1, 0, 0, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        }

        #
        import numpy as np
        #
        self.ele_rect2car_np = np.array([[-2, -2, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0],
                                         [-2, -2, -2, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                                         [-3, -2, -2, -2, -1, -1, -1, -1, -1, 0, 0, 0],
                                         [-3, -3, -3, -2, -2, -1, -1, -1, -1, -1, -1, 0],
                                         [-4, -3, -3, -3, -2, -2, -2, -1, -1, -1, -1, -1],
                                         [-4, -4, -4, -3, -3, -2, -2, -2, -1, -1, -1, -1],
                                         [-5, -4, -4, -4, -3, -2, -2, -2, -2, -1, -1, -1],
                                         [-5, -5, -5, -4, -3, -3, -2, -2, -2, -2, -2, -1]]
                                        )

        #
        self.ele_rect2peo_np = np.array([[-2, -2, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0],
                                         [-2, -2, -2, -1, -1, -1, -1, 0, 0, 0, 0, 0],
                                         [-3, -2, -2, -2, -1, -1, -1, -1, -1, 0, 0, 0],
                                         [-3, -3, -3, -2, -2, -1, -1, -1, -1, -1, 0, 0],
                                         [-4, -3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0],
                                         [-4, -4, -4, -3, -3, -2, -2, -2, -1, -1, 0, 0],
                                         [-5, -4, -4, -4, -3, -2, -2, -2, -2, -1, 0, 0],
                                         [-5, -5, -5, -4, -3, -3, -2, -2, -2, -2, 0, 0]])

        #
        self.wp2car_judge_0_np = np.array([[1, 3, 4, 5, 6, 7, 8, 9, 11, 12],
                                           [2, 4, 6, 7, 8, 9, 10, 12, 13, 14],
                                           [3, 5, 7, 8, 10, 12, 13, 14, 15, 16],
                                           [3, 5, 7, 9, 11, 13, 14, 15, 17, 18],
                                           [3, 5, 9, 11, 14, 15, 16, 18, 19, 20]])
        #
        self.wp2car_judge_1_np = np.array([[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 2, 3, 5],
                                           [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 2, 3, 3, 2, 1, 1],
                                           [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 5],
                                           [0, 0, 1, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 3, 4, 3],
                                           [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 4, 4, 4],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 4, 3, 4],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 4, 4, 4],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 3, 3, 2, 2, 3],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 2, 4]])

        #
        self.wp2car_judge_2_np = np.array([[0, -1, -2, -3, -3],
                                           [0, 0, -1, -2, -3],
                                           [0, 0, -1, -2, -3],
                                           [0, 0, 0, -1, -3],
                                           [0, 0, 0, -1, -2],
                                           [0, 0, 0, 0, -2],
                                           [1, 0, 0, 0, -1],
                                           [1, 0, 0, 0, -1],
                                           [1, 0, 0, 0, -1],
                                           [1, 1, 0, 0, 0],
                                           [1, 1, 0, 0, 0],
                                           [1, 1, 0, 0, 0],
                                           [1, 1, 1, 0, 0],
                                           [2, 2, 1, 1, 0],
                                           [2, 2, 2, 2, 1],
                                           [3, 3, 3, 2, 2]])

        #
        self.wp2peo_judge_0_np = np.array([[0.5, 0.5, 0.5, 0.5, 1, 2, 2, 2, 2, 2],
                                           [0, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1],
                                           [0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1],
                                           [0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 1, 1],
                                           [0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 0.5],
                                           [0, 0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5],
                                           [0, 0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5],
                                           [0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 1],
                                           [0, 0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1],
                                           [0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 2],
                                           [0.5, 0.5, 0.5, 0.5, 0.5, 1, 2, 2, 2, 2]])

        #
        self.wp2peo_judge_1_np = np.array([[0, -1],
                                           [1, 0],
                                           [2, 0],
                                           [3, 0],
                                           [4, 0],
                                           [5, 0],
                                           [6, 0],
                                           [7, 0],
                                           [8, 1]])

        #
        self.wp2plane_judge_0_np = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                                             [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                                             [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                                             [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                                             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                                             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

        #
        self.indirect_offset_0_np = np.array([[1, 2, 3, 4],
                                              [1, 1, 2, 3],
                                              [-1, 1, 1, 2],
                                              [0, 0, 1, 1],
                                              [0, 0, 0, 1],
                                              [-1, 0, 0, 0],
                                              [0, 0, 0, 1],
                                              [0, 0, 1, 1],
                                              [-1, 1, 1, 2],
                                              [1, 1, 2, 3],
                                              [1, 2, 3, 4]])

        #
        self.indirect_offset_1_np = np.array([[0, 0, 1, 3],
                                              [0, 0, 1, 2],
                                              [0, 0, 0, 1],
                                              [-1, 0, 0, 1],
                                              [-1, -1, 0, 0],
                                              [-1, -1, -1, 0],
                                              [-1, -1, 0, 0],
                                              [-1, 0, 0, 1],
                                              [0, 0, 0, 1],
                                              [0, 0, 0, 2],
                                              [0, 0, 1, 3]])

        #
        self.indirect_offset_2_np = np.array([0, 0, -1, -1, -1, -1, -1, -1, -1, 0, 0])


class check_tool():
    def __init__(self, observation, amap):
        self.map = amap
        #

    @classmethod
    def update(cls, observation):
        #
        cls.observation = observation
        pass

    def My_check_action(self, cure_action):
        if cure_action.action_type == ActionType.Move:
            return self.My_check_Move(cure_action)
        elif cure_action.action_type == ActionType.Shoot:
            return self.My_check_shoot(cure_action)
        elif cure_action.action_type == ActionType.GetOn:
            return self.My_check_geton(cure_action)
        elif cure_action.action_type == ActionType.GetOff:
            return self.My_check_getoff(cure_action)
        elif cure_action.action_type == ActionType.Occupy:
            return self.My_check_Occupy(cure_action)
        elif cure_action.action_type == ActionType.ChangeState:
            return self.My_check_changestate(cure_action)
        elif cure_action.action_type == ActionType.RemoveKeep:
            return self.My_check_removekeep(cure_action)
        elif cure_action.action_type == ActionType.JMPlan:
            return self.My_check_jmplan(cure_action)
        elif cure_action.action_type == ActionType.GuideShoot:
            return self.My_check_guideshoot(cure_action)
        elif cure_action.action_type == ActionType.StopMove:
            return self.My_check_stopmove(cure_action)
        return False, None

    def My_check_getoff(self, cure_action):
        cur_bop = cure_action.cur_bop
        if len(cur_bop['passenger_ids']) > 0:
            if cur_bop['keep'] == 0 and cur_bop['stop'] == True:
                if self.observation['valid_actions'].get(cur_bop['obj_id']):
                    valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
                else:
                    return False, None
                valid_action_types = list(valid_action_list.keys())
                if ActionType.GetOff in valid_action_types:
                    if cure_action.target_obj_id == None:
                        return True, None
                    for each in valid_action_list[ActionType.GetOff]:
                        if each['target_obj_id'] == cure_action.target_obj_id:
                            return True, cure_action
        return False, None

    def My_check_geton(self, cure_action):
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.GetOn in valid_action_types:
            if cure_action.target_obj_id == None:
                return True, None
            for each in valid_action_list[ActionType.GetOn]:
                if each['target_obj_id'] == cure_action.target_obj_id:
                    return True, cure_action
        return False, None

    def My_check_shoot(self, cure_action):
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        #
        if ActionType.Shoot in valid_action_types:
            if cure_action.target_obj_id == None:
                return True, None
            shoot_list_temp = []
            for each in valid_action_list[ActionType.Shoot]:
                if each['target_obj_id'] == cure_action.target_obj_id:
                    shoot_list_temp.append(each)
            if len(shoot_list_temp) == 0:
                return False, None
            best = max(shoot_list_temp, key=lambda x: x['attack_level'])
            cure_action.weapon_id = best['weapon_id']
            return True, cure_action
        return False, None

    def My_check_guideshoot(self, cure_action):
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.GuideShoot in valid_action_types:
            shoot_list_temp = []
            for each in valid_action_list[ActionType.GuideShoot]:
                if cure_action.target_obj_id != None:
                    if each['target_obj_id'] != cure_action.target_obj_id:
                        continue
                if cure_action.guided_obj_id != None:
                    if each['guided_obj_id'] != cure_action.guided_obj_id:
                        continue
                shoot_list_temp.append(each)
            if len(shoot_list_temp) == 0:
                return False, None
            best = max(shoot_list_temp, key=lambda x: x['attack_level'])
            cure_action.weapon_id = best['weapon_id']
            cure_action.target_obj_id = best['target_obj_id']
            cure_action.guided_obj_id = best['guided_obj_id']
            return True, cure_action
        return False, None

    def My_check_Occupy(self, cure_action):
        '''
        判断是否可以夺控
        :param cur_bop:
        :return: True/可以夺控,False/不能夺控
        '''
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.Occupy in valid_action_types:
            return True, cure_action
        return False, None

    def My_check_stopmove(self, cure_action):
        '''
        判断是否可以夺控
        :param cur_bop:
        :return: True/可以夺控,False/不能夺控
        '''
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.StopMove in valid_action_types:
            return True, cure_action
        return False, None

    def My_check_Move(self, cure_action):
        '''
        判断是否机动,若机动，返回机动路线
        :param cur_bop: 机动算子
        :param obj_pos: 目标位置
        :return: (True,list)/(需要机动，机动路线),(False,None)/(不机动，None)
        '''
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.Move in valid_action_types:
            if cure_action.XY == None:
                return True, None
            if cur_bop and cur_bop['cur_hex'] != cure_action.XY:
                #
                #
                #
                return True, cure_action
            #
            #
            #
            #

        return False, None

    def My_check_changestate(self, cure_action):
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.ChangeState in valid_action_types:
            if cure_action.target_state == None:
                return True, None
            for each in valid_action_list[ActionType.ChangeState]:
                if each['target_state'] == cure_action.target_state:
                    return True, cure_action
        return False, None

    def My_check_removekeep(self, cure_action):
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.RemoveKeep in valid_action_types:
            return True, cure_action
        return False, None

    def My_check_jmplan(self, cure_action):
        cur_bop = cure_action.cur_bop
        if self.observation['valid_actions'].get(cur_bop['obj_id']):
            valid_action_list = self.observation['valid_actions'][cur_bop['obj_id']]
        else:
            return False, None
        valid_action_types = list(valid_action_list.keys())
        if ActionType.JMPlan in valid_action_types:
            #
            #
            shoot_list_temp = []
            for each in valid_action_list[ActionType.JMPlan]:
                shoot_list_temp.append(each)

            if len(shoot_list_temp) == 0:
                return False, None
            #
            cure_action.weapon_id = shoot_list_temp[0]['weapon_id']
            return True, cure_action
        return False, None

    def get_move_type(self, bop):
        """Get appropriate move type for a bop."""
        bop_type = bop['type']
        if bop_type == BopType.Vehicle:
            if bop['move_state'] == MoveType.March:
                move_type = MoveType.March
            else:
                move_type = MoveType.Maneuver
        elif bop_type == BopType.Infantry:
            move_type = MoveType.Walk
        else:
            move_type = MoveType.Fly
        return move_type

    def My_check_missile_shoot(self, cure_action):
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        return False, None


#
class BehaviorTree(object):
    def __init__(self, root):
        self.root = root
        self.ret_msg = []

    def tick(self):
        #
        state = self.root.do_execute()
        return state


import uuid


class BaseNode(object):
    def __init__(self, description=None):
        self.description = description
        BaseNode.ai_opt = None

    @classmethod
    def class_update(cls, situation):
        cls.situation = situation
        cls.observation = situation.observation
        cls.our_opt = situation.our_opt
        cls.enemy_operators = situation.enemy_operators
        cls.missile_patrol_find_enemy = situation.missile_patrol_find_enemy  #
        cls.enenmy_is_coming = situation.enenmy_is_coming  #
        cls.ret_msg = []

    def do_execute(self):
        pass


class Composite(BaseNode):
    def __init__(self, children=None, description=None):
        super(Composite, self).__init__(description)
        self.children = children or []
        self.description = description


class Condition(BaseNode):
    def __init__(self, ai_opt=None, description=None):
        super(Condition, self).__init__(ai_opt, description)
        self.description = description


class Action(BaseNode):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description


class Sequence(Composite):
    def __init__(self, children=None, description=None):
        super(Sequence, self).__init__(description)
        self.description = description
        self.children = children
        self.state = FAILURE
        self.id = str(uuid.uuid1())

    def do_execute(self):
        for node in self.children:
            status = node.do_execute()
            self.state = status
            if status == FAILURE:
                return self.state
        return self.state


class Selector(Composite):
    def __init__(self, children=None, description=None):
        super(Selector, self).__init__(description)
        self.description = description
        self.children = children
        self.state = FAILURE
        self.id = str(uuid.uuid1())

    def do_execute(self):
        for node in self.children:
            status = node.do_execute()
            self.state = status
            if status != FAILURE:
                return self.state
        return self.state


class Parallel(Composite):
    def __init__(self, children=None, description=None):
        super(Parallel, self).__init__(children)
        self.description = description
        self.children = children
        self.state = FAILURE
        self.id = str(uuid.uuid1())

    def do_execute(self):
        for node in self.children:
            status = node.do_execute()
            self.state = self.state | status
        return self.state


class Decorator(BaseNode):
    def __init__(self, child=None, description=None):
        super(Decorator, self).__init__(description)
        self.child = child or []
        self.description = description


class ConditionIsEnemyComing(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否出现敌情'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.enenmy_is_coming == True:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsFirstStep(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['time']['cur_step'] == 0:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class DecoratorNot(Decorator):
    def __init__(self, child=None, description=None):
        super(Decorator, self).__init__(description)
        self.child = child or []
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        state = self.child.do_execute()
        if state == SUCCESS:
            self.state = FAILURE
        if state == FAILURE:
            self.state = SUCCESS
        return self.state


class ConditionIsSeeEnemy(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断视野内是否有敌人'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.ai_opt.operator['see_enemy_bop_ids']:
            for obj_id in self.ai_opt.operator['see_enemy_bop_ids']:
                for opt in self.situation.our_opt:
                    if opt.operator['sub_type'] == MISSILE:
                        opt.target2atk = obj_id
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionHaveMissile(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否还有导弹'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.ai_opt.operator['C3'] > 0:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsStop(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否处于停止状态'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.ai_opt.operator['stop'] == 1:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsMoving(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否处于停止状态'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.ai_opt.is_moving():
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionStopMove(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_stopmove()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionAttack(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_attack()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionOccupy(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_occupy()
        if len(msg) > 0:
            self.state = SUCCESS
            if self.ai_opt.operator['sub_type'] == SOILDER:
                self.ai_opt.iOccupidCity = True
            self.ret_msg.extend(msg)
        return self.state


class ConditionIsTank(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == TANK:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsCar(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == CAR:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsSoilder(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.state = FAILURE
        self.id = str(uuid.uuid1())

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == SOILDER:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsMissile(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == MISSILE:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsAutocar(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == AUTO_CAR:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsMissileTimeLess(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.life_time > 1100 or \
                (self.observation['time']['cur_step'] - BaseNode.ai_opt.life_time > 600):
            self.state = SUCCESS
        return self.state


class ActionMissileMovetoAttack(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_move_to_attack()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionMissileAttackWeakestEnemy(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_attack(False)
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionMissileMoveToOrderedenemy(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_move_to_orderedenemy()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state


class ActionMissilePatrol(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        for enemy_bop in self.observation['operators']:
            if enemy_bop['obj_id'] in BaseNode.ai_opt.operator['see_enemy_bop_ids']:
                BaseNode.ai_opt.patrol_enemy_pos_list.append(enemy_bop['cur_hex'])
        if BaseNode.ai_opt.operator['stop'] == 1:
            circle = 6
            x = 2 * int(self.observation['cities'][0]['coord'] / 100) \
                - int(BaseNode.ai_opt.operator['cur_hex'] / 100)
            y = 2 * (self.observation['cities'][0]['coord'] % 100) \
                - (BaseNode.ai_opt.operator['cur_hex'] % 100)
            dst_xy = x * 100 + y
            msg = BaseNode.ai_opt.do_patrol_spec(circle, BaseNode.ai_opt.operator['cur_hex'], dst_xy)
            if len(msg) > 0:
                self.state = SUCCESS
                self.ret_msg.extend(msg)
        return self.state


class ActionMissileMoveToPatrolEnemy(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        #
        #
        #
        #
        #
        #
        #
        #
        return self.state


class ActionMissileMoveToCities(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if self.observation['cities'][0]['flag'] != self.situation.color:
            msg = BaseNode.ai_opt.do_move_to_point(self.observation['cities'][0]['coord'])
            if len(msg) > 0:
                self.ret_msg.extend(msg)
                self.state = SUCCESS
        elif self.observation['cities'][1]['flag'] != self.situation.color:
            msg = BaseNode.ai_opt.do_move_to_point(self.observation['cities'][1]['coord'])
            if len(msg) > 0:
                self.ret_msg.extend(msg)
                self.state = SUCCESS
        return self.state


class ActionMissileAttack(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_attack(True)
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ConditionIsPassengersBiggerOne(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if len(BaseNode.ai_opt.operator['passenger_ids']) > 1:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionCarGetoff(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_getoff()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state


class ActionCarMoveToBestSightPositiontoMaincity(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_move_to_BestPosition()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state


class ActionMovetoSoilder(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        soilder_opt = None
        for opt in self.our_opt:
            if opt.operator['sub_type'] == SOILDER:
                soilder_opt = opt

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        return self.state


class ActionMovetoEnemy(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_move_to_attack()
        """
        res_r = 999
        enemy_for_me = None
        for enemy_opt in self.enemy_operators:
            src2dst = self.situation.map.get_distance(self.ai_opt.operator['cur_hex'], enemy_opt['cur_hex'])
            r = src2dst - 5
            if res_r > r:
                res_r = r
                enemy_for_me = enemy_opt
        msg = self.ai_opt.do_move_toattack(enemy_for_me)
        """
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsMaincityDistanceBigger15(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        enemy_dis = self.situation.map.get_distance(BaseNode.ai_opt.operator['cur_hex'],
                                                    self.observation['cities'][0]['coord'])
        if enemy_dis > 15:
            self.state = SUCCESS
            return self.state
        else:
            self.state = FAILURE
            return self.state


class ConditionIsNearestEnemyDistance(Condition):
    def __init__(self, distance=12, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.distance = distance

    def do_execute(self):
        enemy_dis = self.ai_opt.get_distance_to_nearestenemy()
        if enemy_dis > self.distance:
            self.state = SUCCESS
            return self.state
        else:
            self.state = FAILURE
            return self.state


class ConditionIsNearestEnemyDistanceSeven(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        enemy_dis = self.ai_opt.get_distance_to_nearestenemy()
        if enemy_dis > 7:
            self.state = SUCCESS
            return self.state
        else:
            self.state = FAILURE
            return self.state


class ActionAutocarFight(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_guide_attack()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        else:
            msg = BaseNode.ai_opt.do_attack()
            if len(msg) > 0:
                self.ret_msg.extend(msg)
                self.state = SUCCESS
        return self.state


class ActionAutocarSeclectPosition(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_autocar_move_and_hide()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state


class ActionSoilderFight(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_guide_attack()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        else:
            msg = BaseNode.ai_opt.do_attack()
            if len(msg) > 0:
                self.state = SUCCESS
                self.ret_msg.extend(msg)
        return self.state


class ActionSoilderMoveToVillegeTree(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.operator['stop'] == True:
            villege_list, tree_list = self.situation.myLandTool.get_villege_tree_Straight_def(
                BaseNode.ai_opt.operator['cur_hex'], self.observation['cities'][0]['coord'])
            pos_list = []
            pos_list.extend(tree_list)
            pos_list.extend(villege_list)
            if pos_list:
                move_pos = self.situation.myLandTool.get_closet_positon(
                    BaseNode.ai_opt.operator['cur_hex'], pos_list)
                msg = BaseNode.ai_opt.do_move_to_point(move_pos)
                if len(msg) > 0:
                    self.state = SUCCESS
                    self.ret_msg.extend(msg)
        return self.state


class ActionMoveToMainCity(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.operator['sub_type'] == SOILDER:
            msg = BaseNode.ai_opt.do_move_to_point(self.observation['cities'][0]['coord'])
        else:
            msg = BaseNode.ai_opt.do_move_to_point(self.observation['cities'][0]['coord'])
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionMoveToSecondCity(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.operator['sub_type'] == SOILDER:
            msg = BaseNode.ai_opt.do_move_to_point(self.observation['cities'][1]['coord'])
        else:
            msg = BaseNode.ai_opt.do_move_to_point(self.observation['cities'][1]['coord'])
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionSendEnemyIDToMissile(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.operator['sub_type'] == MISSILE:
            return self.state
        for obj_id in BaseNode.ai_opt.operator['see_enemy_bop_ids']:
            for opt in self.situation.our_opt:
                if opt.operator['sub_type'] == MISSILE:
                    opt.target2atk = obj_id
                    self.state = SUCCESS
                    return self.state
        return self.state


class ConditionMaincityIsNotOurs(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['cities'][0]['flag'] != self.situation.color:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionMaincityIsOurs(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['cities'][0]['flag'] == self.situation.color:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionSecondcityIsNotOurs(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['cities'][1]['flag'] != self.situation.color:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionSecondcityIsOurs(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['cities'][1]['flag'] == self.situation.color:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionMaincityIsNearestToMe_soilderBlue(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = SUCCESS
        dis_maincity = self.situation.map.get_distance(self.observation['cities'][0]['coord'],
                                                       BaseNode.ai_opt.operator['cur_hex'])
        for opt in self.our_opt:
            if opt.operator['sub_type'] != SOILDER:
                continue
            dis = self.situation.map.get_distance(self.observation['cities'][0]['coord'],
                                                  opt.operator['cur_hex'])
            if dis < dis_maincity:
                if opt.operator['keep'] == 0:
                    self.state = FAILURE
        return self.state


class ConditionIsProb(Condition):
    def __init__(self, prob=1.0, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.prob = prob

    def do_execute(self):
        self.state = FAILURE
        if random.random() < self.prob:
            self.state = SUCCESS
        return self.state


class ConditionIsEnemyInMyShootRange(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        for enemy_ID in BaseNode.ai_opt.operator['see_enemy_bop_ids']:
            enemy_opt = self.situation.get_cur_opt_by_id(enemy_ID)
            if enemy_opt:
                dis = self.situation.map.get_distance(enemy_opt['cur_hex'],
                                                      BaseNode.ai_opt.operator['cur_hex'])
                if dis < BaseNode.ai_opt.shoot_range:
                    self.state = SUCCESS
                    return self.state
        return self.state


class ConditionNotWeaponPrepared(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.operator['weapon_cool_time'] or \
                BaseNode.ai_opt.operator['weapon_unfold_time']:
            self.state = SUCCESS
        return self.state


class ConditionNotOnlySoilderInMySeeRange(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        for enemy_id in BaseNode.ai_opt.operator['see_enemy_bop_ids']:
            enemy_opt = self.situation.get_cur_opt_by_id(enemy_id)
            if enemy_opt:
                if enemy_opt['sub_type'] != SOILDER:
                    self.state = SUCCESS
        return self.state


class ConditionIsMaincityInMyCircle(Condition):
    def __init__(self, circle=2, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.circle = circle

    def do_execute(self):
        self.state = FAILURE
        dis = self.situation.map.get_distance(self.observation['cities'][0]['coord'],
                                              BaseNode.ai_opt.operator['cur_hex'])
        if dis <= self.circle:
            self.state = SUCCESS
        return self.state


class ConditionIsSecondcityInMyCircle(Condition):
    def __init__(self, circle=2, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.circle = circle

    def do_execute(self):
        self.state = FAILURE
        dis = self.situation.map.get_distance(self.observation['cities'][1]['coord'],
                                              BaseNode.ai_opt.operator['cur_hex'])
        if dis <= self.circle:
            self.state = SUCCESS
        return self.state


class ConditionIsEnemyAroundSecondcity(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        for enemy_opt in self.enemy_operators:
            if enemy_opt['cur_hex'] in self.situation.map.get_neighbors(self.observation['cities'][1]['coord']) or \
                    enemy_opt['cur_hex'] == self.observation['cities'][1]['coord']:
                if enemy_opt['sub_type'] == TANK or \
                        enemy_opt['sub_type'] == CAR:
                    self.state = SUCCESS
        return self.state


class ConditionIsEnemyAroundMaincity(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        for enemy_opt in self.enemy_operators:
            if enemy_opt['cur_hex'] in self.situation.map.get_neighbors(self.observation['cities'][0]['coord']) or \
                    enemy_opt['cur_hex'] == self.observation['cities'][0]['coord']:
                if enemy_opt['sub_type'] == TANK or \
                        enemy_opt['sub_type'] == CAR:
                    self.state = SUCCESS
        return self.state


class ActionCarSetCityWanted(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = SUCCESS

    def do_execute(self):
        self.state = SUCCESS
        if self.situation.mainCityCarWanted == False:
            self.ai_opt.cityWanted = self.observation['cities'][0]
            self.situation.mainCityCarWanted = True
        elif self.situation.secondCityCarWanted == False:
            self.ai_opt.cityWanted = self.observation['cities'][1]
            self.situation.secondCityCarWanted = True
        else:
            self.ai_opt.cityWanted = self.observation['cities'][0]
        return self.state


class ActionSoilderMoveToCarSetCityWanted(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        for opt in self.our_opt:
            if BaseNode.ai_opt.operator['launcher'] == opt.operator['obj_id']:
                #
                msg = BaseNode.ai_opt.do_move_to_point(opt.cityWanted['coord'])
                if len(msg) > 0:
                    self.state = SUCCESS
                    self.ret_msg.extend(msg)
                    break
        return self.state


class ConditionIsStandingOccupiedCity(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if self.ai_opt.iOccupidCity == True:
            if self.ai_opt.operator['cur_hex'] == self.observation['cities'][0]['coord'] or \
                    self.ai_opt.operator['cur_hex'] == self.observation['cities'][1]['coord']:
                self.state = SUCCESS
        return self.state


class ConditionIsMaincityMyTarget(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if self.observation['cities'][0]['coord'] == self.ai_opt.operator['move_path'][-1]:
            self.state = SUCCESS
        return self.state


class ConditionIsSecondMyTarget(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if self.observation['cities'][1]['coord'] == self.ai_opt.operator['move_path'][-1]:
            self.state = SUCCESS
        return self.state


class ActionHide(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_changestate(Hide)
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state


class ConditionHavePassengers(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if len(BaseNode.ai_opt.operator['passenger_ids']) > 0:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsEnemyDeadTankBiggerThan(Condition):
    def __init__(self, num=0, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.num = num

    def do_execute(self):
        if self.situation.enemy_tank_dead_num > self.num:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsEnemyDeadCarBiggerThan(Condition):
    def __init__(self, num=0, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.num = num

    def do_execute(self):
        if self.situation.enemy_car_dead_num > self.num:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsRed(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.situation.color == RED:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsBlue(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.situation.color == BLUE:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsEnemyDeadTankAndCarTotalNumBiggerThanNum(Condition):
    def __init__(self, num=2, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.num = num

    def do_execute(self):
        self.state = FAILURE
        if self.situation.enemy_car_dead_num > 0 and \
                self.situation.enemy_tank_dead_num > 0:
            self.state = SUCCESS
        if self.situation.enemy_car_dead_num > 1:
            self.state = SUCCESS
        if self.situation.enemy_tank_dead_num > 1:
            self.state = SUCCESS
        return self.state


class ConditionSecondcityIsOccupiedByEnemy(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['cities'][1]['flag'] == (1 - self.situation.color):
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionMaincityIsOccupiedByEnemy(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.observation['cities'][0]['flag'] == (1 - self.situation.color):
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ConditionIsOurSoilderDeadNumBiggerThan(Condition):
    def __init__(self, num=0, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.num = num

    def do_execute(self):
        self.state = FAILURE
        if self.situation.our_soilder_dead_num > self.num:
            self.state = SUCCESS
        return self.state


class ConditionIsMissleLifeLeast(Condition):
    def __init__(self, life=1150, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.life = life

    def do_execute(self):
        self.state = FAILURE
        if self.observation['time']['cur_step'] - BaseNode.ai_opt.life_time > self.life:
            self.state = SUCCESS
        return self.state


class ActionSoilderChargeOne(Action):
    def __init__(self, move_pos, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE
        self.move_pos = move_pos

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_charge_1(self.move_pos)
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ConditionIsSTRATEGY_AUTO(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.strategy_type == STRATEGY_AUTO:
            self.state = SUCCESS
        return self.state


#
class ConditionIsSTRATEGY_FIRSTSTEP(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        if BaseNode.ai_opt.strategy_type == STRATEGY_FIRSTSTEP:
            self.state = SUCCESS
        return self.state


class ActionSTRATEGY_FIRSTSTEP(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_strategy_firststep()
        if self.observation['time']['cur_step'] == 0:
            print(self.ai_opt.operator['obj_id'], self.ai_opt.move2hex, self.ai_opt.movepath, land_tool._stack_pos_list)
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


#
class ConditionIsTire(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否处于停止状态'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.ai_opt.operator['tire'] >= 1:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionSoilder_MoveToMycity(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_move_to_my_city()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionSoilder_PortectMycity(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_protect_my_city()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionSoilder_MoveToNearestcity(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_move_to_nearest_city()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionSoilder_MoveAndProtectcities(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_moveandprotect_cities()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionSoilder_Attack_MoveAndProtectcities(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_attack_moveandprotect_cities()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ConditionIsNotOnBoard(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否处于停止状态'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if not self.ai_opt.is_on_board():
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


#
class ActionMyUpdate(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.ai_opt.my_update()
        return SUCCESS


class ActionSoilder_RemoveKeep(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_removekeep_toshoot()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


#
class ConditionIsMoving_FLY(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = '判断是否处于停止状态'
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if self.ai_opt.is_moving_fly():
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


#
class ConditionIsHelicopter(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == HELICOPTER:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionSoilder_Helicopter_auto(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_move_to_enemy_keepdistance()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


#
class ConditionIsAutoplane(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == AUTO_PLANE:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionAutoplane_auto(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_move_to_enemy_keepdistance()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


#
class ConditionIsArtillery(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.operator['sub_type'] == ARTILLERY:
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


#
class ActionMissile_MovetoAttack(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_move_to_attack_list()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


class ActionMissile_Patrol(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = self.ai_opt.do_patrol()
        if len(msg) > 0:
            self.state = SUCCESS
            self.ret_msg.extend(msg)
        return self.state


#
class ConditionIsNeed_to_hide(Condition):
    def __init__(self, description=None):
        super(Condition, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        if BaseNode.ai_opt.is_need_to_hide():
            self.state = SUCCESS
        else:
            self.state = FAILURE
        return self.state


class ActionCarMovetoAssistoccupy(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_move_to_assist_occupy()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state


#
class ActionAutocarMovetoGuidepos(Action):
    def __init__(self, description=None):
        super(Action, self).__init__(description)
        self.description = description
        self.id = str(uuid.uuid1())
        self.state = FAILURE

    def do_execute(self):
        self.state = FAILURE
        msg = BaseNode.ai_opt.do_move_to_guidepos()
        if len(msg) > 0:
            self.ret_msg.extend(msg)
            self.state = SUCCESS
        return self.state
