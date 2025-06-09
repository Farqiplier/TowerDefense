path = [(0, 300), (450, 300), (450, 150), (300, 150), (300, 600), (150, 600), (150, 450), (600, 450), (600, 300), (750, 300), (750, 600), (450, 600), (450, 650)]
from enemy import Enemy, Red, Blue, Green, Yellow, Pink, Black, White, Purple, Lead, Zebra, Rainbow, Ceramic, MOAB

wave_1 = [
    {
        "type": "Green",         "path": path,   "amount": 10,
        "delay_from_start": 0,      "spawn_delay": 0.75
    },
    {
        "type": "Red",         "path": path,   "amount": 5,
        "delay_from_start": 2,      "spawn_delay": 1
    },
    {
        "type": "Blue",        "path": path,   "amount": 5,
        "delay_from_start": 10,     "spawn_delay": 1
    },
    {
        "type": "Blue",        "path": path,   "amount": 5,
        "delay_from_start": 15,     "spawn_delay": 1
    },
    {
        "type": "Green",       "path": path,   "amount": 5,
        "delay_from_start": 20,     "spawn_delay": 1
    },
    {
        "type": "Green",       "path": path,   "amount": 5,
        "delay_from_start": 25,     "spawn_delay": 1
    }
    # {
    #     "type": 
    # }
]