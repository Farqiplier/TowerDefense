path = [(0, 100), (200, 100), (200, 400), (600, 400), (600, 100), (600, 0)]
from enemy import Enemy, RedEnemy, BlueEnemy, GreenEnemy, YellowEnemy

wave_1 = [
    {
        "type": "RedEnemy",         "path": path,   "amount": 5,
        "delay_from_start": 1,      "spawn_delay": 1
    },
    {
        "type": "RedEnemy",         "path": path,   "amount": 5,
        "delay_from_start": 4,      "spawn_delay": 1
    },
    {
        "type": "BlueEnemy",        "path": path,   "amount": 5,
        "delay_from_start": 10,     "spawn_delay": 1
    },
    {
        "type": "BlueEnemy",        "path": path,   "amount": 5,
        "delay_from_start": 15,     "spawn_delay": 1
    },
    {
        "type": "GreenEnemy",       "path": path,   "amount": 5,
        "delay_from_start": 20,     "spawn_delay": 1
    },
    {
        "type": "GreenEnemy",       "path": path,   "amount": 5,
        "delay_from_start": 25,     "spawn_delay": 1
    }
]