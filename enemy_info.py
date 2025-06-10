path = [(0, 300), (450, 300), (450, 150), (300, 150), (300, 600), (150, 600), (150, 450), (600, 450), (600, 300), (750, 300), (750, 600), (450, 600), (450, 650)]
from enemy import Enemy, Red, Blue, Green, Yellow, Pink, Black, White, Purple, Lead, Zebra, Rainbow, Ceramic, MOAB

# Added 'is_regrowth' and 'is_camo' flags to each enemy definition
wave_3 = [
    {"type": "Red",            "path": path, "amount": 25, "delay_from_start": 0.000, "spawn_delay": 0.5762, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 5,  "delay_from_start": 14.4142, "spawn_delay": 0.5762, "is_camo": False, "is_regrowth": False},
]

wave_4 = [
    {"type": "Red",            "path": path, "amount": 35, "delay_from_start": 0.000, "spawn_delay": 0.3329, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 18, "delay_from_start": 11.6313, "spawn_delay": 0.3329, "is_camo": False, "is_regrowth": False},
]

wave_5 = [
    {"type": "Red",            "path": path, "amount": 5,  "delay_from_start": 0.000, "spawn_delay": 0.5323, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 27, "delay_from_start": 2.1290, "spawn_delay": 0.5323, "is_camo": False, "is_regrowth": False},
]

wave_6 = [
    {"type": "Red",            "path": path, "amount": 15, "delay_from_start": 0.000, "spawn_delay": 0.5667, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 15, "delay_from_start": 8.5333, "spawn_delay": 0.5667, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 4,  "delay_from_start": 17.2000, "spawn_delay": 0.5667, "is_camo": False, "is_regrowth": False},
]

wave_7 = [
    {"type": "Red",            "path": path, "amount": 15, "delay_from_start": 0.000, "spawn_delay": 0.6872, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 20, "delay_from_start": 10.3397, "spawn_delay": 0.6872, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 5,  "delay_from_start": 24.0813, "spawn_delay": 0.6872, "is_camo": False, "is_regrowth": False},
]

wave_8 = [
    {"type": "Blue",           "path": path, "amount": 20, "delay_from_start": 0.000, "spawn_delay": 0.6714, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 14, "delay_from_start": 12.7425, "spawn_delay": 0.6714, "is_camo": False, "is_regrowth": False},
    {"type": "Red",            "path": path, "amount": 10, "delay_from_start": 22.0079, "spawn_delay": 0.6714, "is_camo": False, "is_regrowth": False},
]

wave_9 = [
    {"type": "Green",          "path": path, "amount": 30, "delay_from_start": 0.000, "spawn_delay": 0.6534, "is_camo": False, "is_regrowth": False},
]

wave_10 = [
    {"type": "Blue",           "path": path, "amount": 102, "delay_from_start": 0.000, "spawn_delay": 0.4751, "is_camo": False, "is_regrowth": False},
]

wave_11 = [
    {"type": "Yellow",         "path": path, "amount": 3,  "delay_from_start": 0.000, "spawn_delay": 0.5635, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 12, "delay_from_start": 1.1271, "spawn_delay": 0.5635, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 10, "delay_from_start": 7.6885, "spawn_delay": 0.5635, "is_camo": False, "is_regrowth": False},
    {"type": "Red",            "path": path, "amount": 10, "delay_from_start": 13.3230, "spawn_delay": 0.5635, "is_camo": False, "is_regrowth": False},
]

wave_12 = [
    {"type": "Green",          "path": path, "amount": 10, "delay_from_start": 0.000, "spawn_delay": 0.5997, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 15, "delay_from_start": 5.9973, "spawn_delay": 0.5997, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 5,  "delay_from_start": 14.5956, "spawn_delay": 0.5997, "is_camo": False, "is_regrowth": False},
]

wave_13 = [
    {"type": "Blue",           "path": path, "amount": 50, "delay_from_start": 0.000, "spawn_delay": 0.4474, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 23, "delay_from_start": 21.4362, "spawn_delay": 0.4474, "is_camo": False, "is_regrowth": False},
]

wave_14 = [
    {"type": "Red",            "path": path, "amount": 49, "delay_from_start": 0.000, "spawn_delay": 0.3248, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 15, "delay_from_start": 15.9423, "spawn_delay": 0.3248, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 10, "delay_from_start": 20.9100, "spawn_delay": 0.3248, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 9,  "delay_from_start": 23.1555, "spawn_delay": 0.3248, "is_camo": False, "is_regrowth": False},
]

wave_15 = [
    {"type": "Red",            "path": path, "amount": 20, "delay_from_start": 0.000, "spawn_delay": 0.4098, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 15, "delay_from_start": 6.1717, "spawn_delay": 0.4098, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 12, "delay_from_start": 12.7683, "spawn_delay": 0.4098, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 10, "delay_from_start": 17.9746, "spawn_delay": 0.4098, "is_camo": False, "is_regrowth": False},
    {"type": "Pink",           "path": path, "amount": 5,  "delay_from_start": 21.1034, "spawn_delay": 0.4098, "is_camo": False, "is_regrowth": False},
]

wave_16 = [
    {"type": "Green",          "path": path, "amount": 40, "delay_from_start": 0.000, "spawn_delay": 0.3404, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 8,  "delay_from_start": 13.3872, "spawn_delay": 0.3404, "is_camo": False, "is_regrowth": False},
]

wave_17 = [
    {"type": "Yellow",         "path": path, "amount": 12, "delay_from_start": 0.000, "spawn_delay": 0.4545, "is_camo": False, "is_regrowth": True},
]

wave_18 = [
    {"type": "Green",          "path": path, "amount": 80, "delay_from_start": 0.000, "spawn_delay": 0.3395, "is_camo": False, "is_regrowth": False},
]

wave_19 = [
    {"type": "Green",          "path": path, "amount": 10, "delay_from_start": 0.000, "spawn_delay": 0.4776, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 5,  "delay_from_start": 4.7760, "spawn_delay": 0.4776, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 5,  "delay_from_start": 7.1400, "spawn_delay": 0.4776, "is_camo": False, "is_regrowth": True},
    {"type": "Pink",           "path": path, "amount": 15, "delay_from_start": 9.6158, "spawn_delay": 0.4776, "is_camo": False, "is_regrowth": False},
]

wave_20 = [
    {"type": "Black",          "path": path, "amount": 6,  "delay_from_start": 0.000, "spawn_delay": 1.0500, "is_camo": False, "is_regrowth": False},
]

wave_21 = [
    {"type": "Yellow",         "path": path, "amount": 40, "delay_from_start": 0.000, "spawn_delay": 0.3419, "is_camo": False, "is_regrowth": False},
    {"type": "Pink",           "path": path, "amount": 14, "delay_from_start": 13.1752, "spawn_delay": 0.3419, "is_camo": False, "is_regrowth": False},
]

wave_22 = [
    {"type": "White",          "path": path, "amount": 16, "delay_from_start": 0.000, "spawn_delay": 0.5333, "is_camo": False, "is_regrowth": False},
]

wave_23 = [
    {"type": "Black",          "path": path, "amount": 7,  "delay_from_start": 0.000, "spawn_delay": 0.5246, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 7,  "delay_from_start": 3.6723, "spawn_delay": 0.5246, "is_camo": False, "is_regrowth": False},
]

wave_24 = [
    {"type": "Green",          "path": path, "amount": 1,  "delay_from_start": 0.000, "spawn_delay": 0.4500, "is_camo": True, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 20, "delay_from_start": 0.4500, "spawn_delay": 0.4500, "is_camo": False, "is_regrowth": False},
]

wave_25 = [
    {"type": "Yellow",         "path": path, "amount": 25, "delay_from_start": 0.000, "spawn_delay": 0.6218, "is_camo": False, "is_regrowth": True},
    {"type": "Purple",         "path": path, "amount": 10, "delay_from_start": 15.5465, "spawn_delay": 0.6218, "is_camo": False, "is_regrowth": False},
]

wave_26 = [
    {"type": "Pink",           "path": path, "amount": 23, "delay_from_start": 0.000, "spawn_delay": 0.5581, "is_camo": False, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 4,  "delay_from_start": 12.5486, "spawn_delay": 0.5581, "is_camo": False, "is_regrowth": False},
]

wave_27 = [
    {"type": "Red",            "path": path, "amount": 100, "delay_from_start": 0.000, "spawn_delay": 0.1376, "is_camo": False, "is_regrowth": False},
    {"type": "Blue",           "path": path, "amount": 60,  "delay_from_start": 13.6261, "spawn_delay": 0.1376, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 45,  "delay_from_start": 22.8671, "spawn_delay": 0.1376, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 45,  "delay_from_start": 29.9671, "spawn_delay": 0.1376, "is_camo": False, "is_regrowth": False},
]

wave_28 = [
    {"type": "Lead",           "path": path, "amount": 6,  "delay_from_start": 0.000, "spawn_delay": 1.0000, "is_camo": False, "is_regrowth": False},
]

wave_29 = [
    {"type": "Yellow",         "path": path, "amount": 50, "delay_from_start": 0.000, "spawn_delay": 0.2383, "is_camo": False, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 15, "delay_from_start": 11.6734, "spawn_delay": 0.2383, "is_camo": False, "is_regrowth": True},
]

wave_30 = [
    {"type": "Lead",           "path": path, "amount": 9,  "delay_from_start": 0.000, "spawn_delay": 1.6338, "is_camo": False, "is_regrowth": False},
]

wave_31 = [
    {"type": "Black",          "path": path, "amount": 8,  "delay_from_start": 0.000, "spawn_delay": 0.6364, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 8,  "delay_from_start": 4.5455, "spawn_delay": 0.6364, "is_camo": False, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 8,  "delay_from_start": 9.0909, "spawn_delay": 0.6364, "is_camo": False, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 2,  "delay_from_start": 13.6363, "spawn_delay": 0.6364, "is_camo": False, "is_regrowth": True},
]

wave_32 = [
    {"type": "Black",          "path": path, "amount": 15, "delay_from_start": 0.000, "spawn_delay": 0.6355, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 20, "delay_from_start": 9.5325, "spawn_delay": 0.6355, "is_camo": False, "is_regrowth": False},
    {"type": "Purple",         "path": path, "amount": 10, "delay_from_start": 21.5629, "spawn_delay": 0.6355, "is_camo": False, "is_regrowth": False},
]

wave_33 = [
    {"type": "Red",            "path": path, "amount": 20, "delay_from_start": 0.000, "spawn_delay": 0.7920, "is_camo": True, "is_regrowth": False},
    {"type": "Yellow",         "path": path, "amount": 13, "delay_from_start": 15.8400, "spawn_delay": 0.7920, "is_camo": True, "is_regrowth": False},
]

wave_34 = [
    {"type": "Yellow",         "path": path, "amount": 160,"delay_from_start": 0.000, "spawn_delay": 0.2182, "is_camo": False, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 6,  "delay_from_start": 34.4940, "spawn_delay": 0.2182, "is_camo": False, "is_regrowth": False},
]

wave_35 = [
    {"type": "Pink",           "path": path, "amount": 35, "delay_from_start": 0.000, "spawn_delay": 0.4681, "is_camo": False, "is_regrowth": False},
    {"type": "Black",          "path": path, "amount": 30, "delay_from_start": 16.3835, "spawn_delay": 0.4681, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 25, "delay_from_start": 30.4250, "spawn_delay": 0.4681, "is_camo": False, "is_regrowth": False},
    {"type": "Rainbow",        "path": path, "amount": 5,  "delay_from_start": 41.7625, "spawn_delay": 0.4681, "is_camo": False, "is_regrowth": False},
]

wave_36 = [
    {"type": "Pink",           "path": path, "amount": 140,"delay_from_start": 0.000, "spawn_delay": 0.4681, "is_camo": False, "is_regrowth": False},
    {"type": "Green",          "path": path, "amount": 20,"delay_from_start": 65.2584, "spawn_delay": 0.4681, "is_camo": True, "is_regrowth": True},
]

wave_37 = [
    {"type": "Black",          "path": path, "amount": 25, "delay_from_start": 0.000, "spawn_delay": 0.5556, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 25, "delay_from_start": 13.8890, "spawn_delay": 0.5556, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 7,  "delay_from_start": 27.7770, "spawn_delay": 0.5556, "is_camo": True, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 10, "delay_from_start": 31.8889, "spawn_delay": 0.5556, "is_camo": False, "is_regrowth": False},
    {"type": "Lead",           "path": path, "amount": 15, "delay_from_start": 37.7789, "spawn_delay": 0.5556, "is_camo": False, "is_regrowth": False},
]

wave_38 = [
    {"type": "Pink",           "path": path, "amount": 42, "delay_from_start": 0.000, "spawn_delay": 0.5000, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 17, "delay_from_start": 20.5000, "spawn_delay": 0.5000, "is_camo": False, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 10, "delay_from_start": 28.0000, "spawn_delay": 0.5000, "is_camo": False, "is_regrowth": False},
    {"type": "Lead",           "path": path, "amount": 14, "delay_from_start": 33.5000, "spawn_delay": 0.5000, "is_camo": False, "is_regrowth": False},
    {"type": "Ceramic",        "path": path, "amount": 2,  "delay_from_start": 40.5000, "spawn_delay": 0.5000, "is_camo": False, "is_regrowth": False},
]

wave_39 = [
    {"type": "Black",          "path": path, "amount": 10, "delay_from_start": 0.000,   "spawn_delay": 0.500, "is_camo": False, "is_regrowth": False},
    {"type": "White",          "path": path, "amount": 10, "delay_from_start": 5.000,   "spawn_delay": 0.500, "is_camo": False, "is_regrowth": False},
    {"type": "Zebra",          "path": path, "amount": 20, "delay_from_start": 10.000,  "spawn_delay": 0.500, "is_camo": False, "is_regrowth": False},
    {"type": "Rainbow",        "path": path, "amount": 18, "delay_from_start": 20.000,  "spawn_delay": 0.500, "is_camo": False, "is_regrowth": False},
    {"type": "Rainbow",        "path": path,"amount": 2,  "delay_from_start": 29.000,  "spawn_delay": 1.000, "is_camo": False, "is_regrowth": True}
]

wave_40 = [
    {"type": "MOAB",           "path": path, "amount": 1,  "delay_from_start": 0.000,   "spawn_delay": 0.000, "is_camo": False, "is_regrowth": False}
]

# A master list containing all defined waves
ALL_WAVES = [
    wave_3, wave_4, wave_5, wave_6, wave_7, wave_8, wave_9, wave_10,
    wave_11, wave_12, wave_13, wave_14, wave_15, wave_16, wave_17, wave_18,
    wave_19, wave_20, wave_21, wave_22, wave_23, wave_24, wave_25, wave_26,
    wave_27, wave_28, wave_29, wave_30, wave_31, wave_32, wave_33, wave_34,
    wave_35, wave_36, wave_37, wave_38, wave_39, wave_40
]