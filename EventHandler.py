import CAFG_variables as gv  # Import Global Variables
import CAFG_items
import random
import CAFG_events
import mysql.connector
import math

from CAFG_variables import shop_items, player_items

def mysqlconnector():
    conn = mysql.connector.connect(
        host="localhost",
        user="surviver",
        password="123",
        database="flight_game",
        charset="latin1",
        collation="latin1_swedish_ci",
    )
    return conn
conn = mysqlconnector()


# handlers that perform the basic functions


# handles the holistic airport visits
def turnhandler():
    # global CAFG_variables
    timeunitrefresher(10)
    itemchecker()
    globalthreathandler()
    gv.current_score += 100
    if gv.global_threat == 20000:
        deathhandler()
    shoprandomiser(3)
    timehandler(0, 0)
    eventhandler()
    #actionhandler()
    # movementhandler()


# formula for increasing global threat


def globalthreathandler():
    gv.global_threat += gv.previous_travel_distance + (
            gv.local_threat[gv.current_airport] // 2
    )
    return


def localthreathandler(timespent, threat):
    if not gv.local_threat.get(
            gv.current_airport
    ):  # Checks if country has an assigned gv.local_threat in [dict] yet. If not, adds one.
        if len(gv.local_threat.keys()) == 0:
            gv.local_threat.update({gv.current_airport: 0})
        gv.local_threat.update({gv.current_airport: 0})

    gv.local_threat.update(
        {
            gv.current_airport: gv.local_threat.get(gv.current_airport)
                                + (threat * timespent)
        }
    )  # Increase gv.local_threat for current country.


def timehandler(timespent, threat):
    gv.time_units -= timespent
    localthreathandler(timespent, threat)


# handles the arrival events
def eventhandler():
    eventhandlersub()


def eventhandlersub():
    # vv THESE MULTIPLIERS ARE PLACEHOLDERS vv
    event_luck = (gv.local_threat.get(gv.current_airport) * 1) * (
            gv.global_threat * 1
    ) - (gv.player_luck * 1)

    event_happening = random.randint(0, 5)
    match event_happening:
        case 1:
            gv.player_money += 200
            return "You gained your yearly tax returns... again?... YIPPII"
        case 2:
            shoprandomiser(5)  # Shop has 5 random items instead of 3.
            return (
                "You found a bazaar in the basement of the airport! Time for a shopping spree!"
            )
        case 3:
            gv.time_units += 2
            return (
                "You spontaneously grew a moustache. You feel strangely at peace with the universe."
            )
        case 4:
            gv.local_threat[gv.current_airport] -= 5  # drops gv.local_threat by 5 units
            return (
                "It's the anniversary of the airport! People are celebrating without a care in the world."
            )
        case 5:
            event = random.randint(0, len(CAFG_events.used_events) - 1)
            # prints special event start bar
            print(
                "___________________________________________________________________________"
            )
            print(CAFG_events.used_events[int(event)].desc)
            match CAFG_events.used_events[int(event)]:
                # gives player luck between 50 and 100
                case CAFG_events.fox_fires:
                    return CAFG_events.fox_fires.activate()

                # Adds a random item from the qwawason_items to player_items.
                case CAFG_events.space_express:
                    return CAFG_events.space_express.activate()

                # If player succeeds, resets local threat. If player fails, game ends.(Unless player has bulletproof vest)
                case CAFG_events.national_hero:  #

                    #die = False
                    #CAFG_events.national_hero.activate()
                    #if die:
                    #    deathhandler()
                    gv.local_threat =-1
                    return ("The airport is on fire.\n"
                            "-1 local threat \n"
                            " ")
            # prints special event end bar.
            print(
                "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"
            )
            return

        case _:
            return "It's a very boring airport! One star out of five!"


'''
# handles the actions that the player can perform
def actionhandler():
    jobrandomiser()
    doingactions = True
    while doingactions:
        doingactions = actionhandlersub(
            input("Input command (? for a list of commands): ")
        )
'''
'''
# Receives player action commands and calls further functions to execute rest of the action.
def actionhandlersub(command):
    match command:
        case "info":
            return listcommands()
        case "use":
            actionuse()
            return True
        case "buy":
            return actionbuy()
        case "check":
            actioncheck()
            return True
        case "work":
            actionwork()
            return True
        case "chill":
            print("You chilled for a while")
            return True
        case "leave":
            print("Moving to the next country")
            leaveornot = input("Do you want to leave the airport?(y/N): ")
            if leaveornot == "y":
                return False
            else:
                return True

        # debug tools
        case "stats":
            checkstats()
            return True
        case "giveitem":
            giveitem()
            return True
        case "takeitem":
            takeitem()
            return True

        # incorrect input
        case _:
            print("Unknown command (? for a list of commands)")
            return True
'''

# list of actions that the player can perform
def listcommands():
    return (f"{'check'} ---  check your items\n "
            f"{'use'} ---  use your items\n "
            f"{'buy'} ---  buy more items\n "
            f"{'work'} ---  work for money\n"
            f"{'leave'} ---  go to the next airport\n")

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

f"{'check' :<10} ---  check you items\n"


# DEV TOOL! Gives player an item corresponding to itemid
def giveitem():
    give_item = True
    print(f"There are {len(CAFG_items.all_items)} items in the game.")
    while give_item:
        itemid = input("Enter itemid(N to cancel): ")
        if itemid == "N":
            print()
            give_item = False
        elif not itemid.isdigit():
            print("Incorrect input.")
            print()
        elif int(itemid) > len(CAFG_items.all_items):
            print("Invalid ID.")
            print()
        else:
            print(f"{CAFG_items.all_items[int(itemid) - 1].name} added to player_items.")
            gv.player_items.append(CAFG_items.all_items[int(itemid) - 1])
            give_item = False


# DEV TOOL! Removes an item from player inventory
def takeitem():
    if len(gv.player_items) > 0:
        print("Your items:")
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        # prints gv.player_items
        for i, item in enumerate(gv.player_items):
            print(f"{i + 1} {item.name}\n")
        print()
        take_item = True
        while take_item:
            itemnum = input("Enter item number(N to cancel): ")
            if itemnum == "N":
                print()
                take_item = False
            elif not itemnum.isdigit():
                print("Incorrect input.")
                print()
            elif 1 > int(itemnum) or int(itemnum) > len(gv.player_items):
                print("Invalid number")
                print()
            else:
                print(
                    f"{gv.player_items[int(itemnum) - 1].name} removed from gv.player_items."
                )
                gv.player_items.pop(int(itemnum) - 1)
                take_item = False
    else:
        print("gv.player_items is empty.")
        print()


# prints player and game stats
def checkstats():
    print("Game status")
    print(f"Score is {gv.current_score}")
    print(f"Global threat is {gv.global_threat}")
    print(f"Current country is {gv.current_airport}")
    print(f"Local treat is {gv.local_threat.get(gv.current_airport)}")
    print()

    print("Your status")
    print(f"Your balance: {gv.player_money}€")
    print(f"Your luck: {gv.player_luck}")
    print(f"The timeunits you have: {gv.time_units}")
    print()


# next 2 uses your items
def actionuse():
    text = ""
    list_of_item_names = []
    if len(gv.player_items) == 0:
        text = "You have no items. Go buy some"
    else:
        text = "What item do you want to use"
        for i, item in enumerate(gv.player_items):
            list_of_item_names.append(item.name)
    return [text, list_of_item_names]

def actionusesub(used_item):
    text =""
    list_of_item_names = []
    owned_item_number = 0
    for i, item in enumerate(gv.player_items):
        list_of_item_names.append(item.name)
        if item.name == used_item:
            owned_item_number = i

    # here the match case structure for item use
    use_item = gv.player_items[owned_item_number]
    print(f"You've decided to use {use_item.name}")
    # checks if item is the active kind. If so, uses it.
    if gv.player_items[owned_item_number].active:
        gv.player_items.pop(owned_item_number)
        text = f"You used {used_item}!"
        gv.current_score += 50
        timeunithandler(1)
    else:
        text = "Item is passive"
    match use_item:
        # uses the fake lottery coupon
        case CAFG_items.lottery_fake:
            text += f'\n {CAFG_items.lottery_fake.activate()}'
            return [text, list_of_item_names]
        # uses lottery coupon
        case CAFG_items.lottery_coupon:
            text += f'\n {CAFG_items.lottery_coupon.activate()}'
            return [text, list_of_item_names]
        # uses the invisibility cape
        case CAFG_items.invis_cape:
            text += f'\n {CAFG_items.invis_cape.activate()}'
            return [text, list_of_item_names]
        # uses the fortune cookie
        case CAFG_items.luck_cookie:
            text += f'\n {CAFG_items.luck_cookie.activate()}'
            return [text, list_of_item_names]
        # uses the Ebin-Sip -energy drink
        case CAFG_items.energydrink:
            text += f'\n {CAFG_items.energydrink.activate()}'
            return [text, list_of_item_names]
        # ponders the used 1k bill.
        case CAFG_items.tonnin_seteli:
            text += f'\n {CAFG_items.tonnin_seteli.activate()}'
            return [text, list_of_item_names]
        # uses the arcade ticket and gives score
        case CAFG_items.arcade_ticket:
            text += f'\n {CAFG_items.arcade_ticket.activate()}'
            return [text, list_of_item_names]
        # uses the snow globe and gives score
        case CAFG_items.snow_globe:
            text += f'\n {CAFG_items.snow_globe.activate()}'
            return [text, list_of_item_names]

    return [text, list_of_item_names]

# next 2 buys more items
def actionbuy():
    text = ""
    list_of_item_names = []

    if len(gv.shop_items) == 0:
        text = "You bought all the items. You lament that your shopping time has ended."
    else:
        #lists item names and prices to be used in text element in html
        prices = ""
        for i, item in enumerate(gv.shop_items):
            prices += f'{item.name} : {item.price}€    |     '

        text = ("What do you want to buy? Select from the buttons on the side below.\n"
                f"_________________________[Todays offers]_________________________\n"
                f"{prices}")
        #lists item names to be used as button elements in html
        for i, item in enumerate(gv.shop_items):
            list_of_item_names.append(item.name)
    return [text, list_of_item_names]

def buythis(itemtobuy):
    text = ""
    shop_item_number = 0
    shop_item_names = []
    for i, item in enumerate(gv.shop_items):
        shop_item_names.append(item.name)
        if item.name == itemtobuy:
            shop_item_number = i

    if gv.shop_items[shop_item_number].price > gv.player_money:
        text = "The item is too expensive"

    # buys the item and places it in player_items while also removing it from the shop
    else:
        bought_item = gv.shop_items[shop_item_number]
        gv.player_items.append(bought_item)
        gv.player_money -= gv.shop_items[shop_item_number].price
        if gv.shop_items[shop_item_number] == CAFG_items.tonnin_seteli:
            gv.player_money -= 998
        timehandler(1, gv.shop_items[shop_item_number].price)
        # uses 1 unit of time and increases local threat by 10 with said amount of time.
        text = (f"You bought {itemtobuy} for {gv.shop_items[shop_item_number].price}€ !\n"
                f"{gv.shop_items[shop_item_number].buy}")
        gv.shop_items.pop(shop_item_number)

    return [text, shop_item_names]


# checks your items
def actioncheck():
    if len(gv.player_items) == 0:
        return ["You have no items. Go buy some"]
    else:
        desc = {}
        for item in gv.player_items:
            desc[item.name] = item.desc

        items = []
        for item in gv.player_items:
            items.append(item.name)
        text = "Here you can check the effects of your items by clicking one of them."
        return [text, items, desc]
    # ^^^^^ should work ^^^^^


# allows you to do work
def actionwork():
    text = "What work do you want to do"
    list_of_jobs = ["clean", "rob"]
    return [text, list_of_jobs]


def actionworksub(used_job):
    match used_job:
        # clean airport job
        case "clean":
            worktime = 3
            stopwork = False
            while not stopwork:
                if (
                        CAFG_items.janitor in gv.player_items
                ):  # Gives extra money if player has janitors clothes
                    money = 50 * int(worktime)
                    gv.player_money += money
                    stopwork = True
                else:
                    money = 20 * int(worktime)
                    gv.player_money += money
                    stopwork = True
            timeunithandler(3)
            return f"You enjoyed your time cleaning the floor. It is beautiful. (Earned {money}€)"

        # ROBS AN MF
        case "rob":
            if CAFG_items.firearm in gv.player_items:
                robbed = random.randint(10 + gv.player_luck, 500 + gv.player_luck)
                gv.player_money += robbed
                text = f"Using your firearm you committed an efficient robbery! (+{robbed}€)"
            else:
                robbed = random.randint(1 + gv.player_luck, 200 + gv.player_luck)
                gv.player_money += robbed
                text = f"Successful robbery! (+{robbed}€)"
            # threat increases by 10 for every € stolen, player luck decreases this
            localthreathandler(1, robbed * (10 - (int(gv.player_luck / 10))))
            timeunithandler(1)
            return text

        case _:
            return "Unknown job"

# checks for passive and active item effects at the start of the turn
def itemchecker():
    # checks if player has a nuclear warhead and acts accordingly.
    if CAFG_items.warhead in gv.player_items:
        die = False
        CAFG_items.warhead.activate()
        if die:
            deathhandler()

    # checks if player has the rabbit paw and acts accordingly
    if CAFG_items.s_rabbit_paw in gv.player_items:
        CAFG_items.s_rabbit_paw.activate()
    print()
    return


# randomises shop at start of the turn
def shoprandomiser(amount_of_items):
    # !!!!!!!!!!!!PLACEHOLDER!!!!!!!!!!!!
    # UTILIZE LUCK IN THIS!!
    gv.shop_items.clear()
    for i in range(amount_of_items):
        gv.shop_items.append(
            CAFG_items.shop_items[random.randint(0, len(CAFG_items.shop_items) - 1)]
        )
    return


# randomises jobs at the start of the turn
def jobrandomiser():
    # currently unused
    return


# refreshesh usable time units at the start of the turn
def timeunitrefresher(amount):
    gv.time_units = amount


# handles the movement from country to country
def updatecoords():
    cursor = conn.cursor()
    cursor.execute(""
                   f"SELECT latitude_deg FROM airport WHERE gps_code = '{gv.current_airport}';")
    player_lat = cursor.fetchall()
    cursor.execute(""
                   f"SELECT longitude_deg FROM airport WHERE gps_code = '{gv.current_airport}';")
    player_long = cursor.fetchall()
    print(f'{player_lat[0][0]} {player_long[0][0]}')
    return [player_lat[0][0],
            player_long[0][0],
            ]
    #SELECT longitude_deg FROM airport WHERE gps_code = 'AGGH';

def haversine(lat1, lon1, lat2, lon2):
    #Calculate the great-circle distance between two points using the Haversine formula.
    r = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
            math.sin(delta_phi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c  # Distance in km

def nearbyairports(travel_range):
    text=str("Select an airport from the map or one of the buttons from the side.")
    if not conn.is_connected():
        conn.reconnect()

    cursor = conn.cursor()
    '''
    # Get all airport data including ICAO codes and coordinates
    
    cursor.execute(
        "SELECT id, gps_code, name, latitude_deg, longitude_deg FROM airport WHERE gps_code IS NOT NULL"
    )
    airports = cursor.fetchall()
    
    # Find the current airport based on gv.current_airport (which is stored as an ICAO code)

    if not current_airport:
        text = "Error: Player current_airport could not be found in the database."
        return [text]

    current_lat, current_lon = current_airport[3], current_airport[4]

    #print(f"\nYou are currently at {current_airport[2]} ({current_airport[1]}).")

    # Find nearby airports within the range
    nearby_airports = [
        port
        for port in airports
        if port[0] != current_airport[0]
        and haversine(current_lat, current_lon, port[3], port[4]) < travel_range
    ]
    

    if not len(nearby_airports):
        text = "No airports within range. You may need a longer-range aircraft."

    #print("\nNearby airports within range:")
    #for port in nearby_airports:
    #    distance = haversine(current_lat, current_lon, port[3], port[4])
    #    print(f"{port[0]} ({port[1]}): {port[2]} - {distance:.2f} km away")
'''

    cursor.execute(
        "SELECT gps_code, name, latitude_deg, longitude_deg FROM airport WHERE gps_code IS NOT NULL"
    )
    allAirports = cursor.fetchall()
    current_airport_stats = next(
        (port for port in allAirports if port[0] == gv.current_airport), None
    )
    nearby_airports = []
    #checks wheter airport is within range, if so, adds it to allAirports list.
    for i in allAirports:
        distance = haversine(current_airport_stats[2],current_airport_stats[3], i[2], i[3])
        if gv.current_airport != i[0] and distance < gv.travel_range_km:
            airport_info = [i[0],i[1],i[2],i[3], distance]
            nearby_airports.append(airport_info)


    #if gv.current_airport
    return [text,
            nearby_airports
            ]

def flyToAirport(name):
    text = str(f'moving to airport: {name}')
    if not conn.is_connected():
        conn.reconnect()

    cursor = conn.cursor()

    cursor.execute(
        f"SELECT gps_code FROM airport WHERE name ='{name}'"
    )
    target_icao = cursor.fetchall()[0][0]
    print(f"Target airport icao: {target_icao}")
    gv.update_current_country(target_icao)
    print(f'Airport set to {gv.current_airport}')


'''
    # Choose destination
    dest_choice = None
    while dest_choice not in [str(port[0]) for port in nearby_airports]:
        dest_choice = input("Enter the ID of the airport you want to go to: ")

    chosen_airport = next(
        port for port in nearby_airports if str(port[0]) == dest_choice
    )
    print (r"""
              .
               
              |
     .               /
      \       I     
                  /
        \  ,g88R_
          d888(`  ).                   _
 -  --==  888(     ).=--           .+(`  )`.
)         Y8P(       '`.          :(   .    )
        .+(`(      .   )     .--  `.  (    ) )
       ((    (..__.:'-'   .=(   )   ` _`  ) )
`.     `(       ) )       (   .  )     (   )  ._
  )      ` __.:'   )     (   (   ))     `-'.:(`  )
)  )  ( )       --'       `- __.'         :(      ))
.-'  (_.'          .')                    `(    )  ))
                  (_  )                     ` __.:'                    
         ______
          _\ _~-\___
  =  = ==(____AA____D
              \_____\___________________,-~~~~~~~`-.._
              /     o O o o o o O O o o o o o o O o  |\_
              `~-.__        ___..----..                  )
                    `---~~\___________/------------`````
                    =  ===(_________D
""")
    print(f"\nYou have chosen to go to {chosen_airport[2]} ({chosen_airport[1]}).")

    # Update game Variables
    gv.update_current_country(chosen_airport[1])
    gv.current_score += 300
    gv.previous_travel_distance = haversine(
        current_lat, current_lon, chosen_airport[3], chosen_airport[4]
    )
def airportandcountryfetch():
    print("works1")
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="surviver",
        password="123",
        database="flight_game",
        charset="latin1",
        collation="latin1_swedish_ci",
    )
    print("works2")
    if not conn.is_connected():
        conn.reconnect()
    print("works2")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT latitude_deg FROM airport WHERE gps_code = 'AGGH';"
        #f"SELECT airport.name, country.name FROM airport, country WHERE airport.id = {str(gv.current_airport)}"
    )
    portandcountry = cursor.fetchall()
    print(portandcountry)

'''
def timeunithandler(amount):
    localthreathandler(200, amount)
    gv.time_units -= amount
    if gv.time_units < 0:
        gv.global_threat+=1000


# you are dead
def deathhandler():
    print()
    print("You are dead")
    print()
    gv.current_score += gv.player_money // 4
    print(f"Your final score is {gv.current_score}")
    quit()


'''
conn.close()
'''