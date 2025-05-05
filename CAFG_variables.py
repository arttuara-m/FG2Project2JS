# system global variables
current_score = 0
global_threat = 0
shop_items = []
# player global variables
time_units = 10
player_money = 1000
player_luck = 0
player_items = []
previous_travel_distance = 0
current_airport = "AGGH"  # change this to the starting current_country
local_threat = {current_airport: 0}
# VV part of the movementhandler placeholder VV
global_country_index = 0


def update_current_country(new_country):
    global current_airport
    current_airport = new_country
    if new_country not in local_threat:
        local_threat[new_country] = 0
