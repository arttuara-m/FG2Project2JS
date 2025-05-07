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
    eventhandler(gv.player_luck)
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
def eventhandler(luck):
    # vv THESE MULTIPLIERS ARE PLACEHOLDERS vv
    event_luck = (gv.local_threat.get(gv.current_airport) * 1) * (
            gv.global_threat * 1
    ) - (luck * 1)
    eventhandlersub(event_luck)


def eventhandlersub(event_luck):
    event_happening = random.randint(0, 5)
    match event_happening:
        case 1:
            print("You gained your yearly tax returns... again?... YIPPII")
            gv.player_money += 200
            return
        case 2:
            print(
                "You found a bazaar in the basement of the airport! Time for a shopping spree!"
            )
            shoprandomiser(5)  # Shop has 5 random items instead of 3.
            return
        case 3:
            print(
                "You spontaneously grew a moustache. You feel strangely at peace with the universe."
            )
            gv.time_units += 2
            return
        case 4:
            print(
                "It's the anniversary of the airport! People are celebrating without a care in the world."
            )
            gv.local_threat[gv.current_airport] -= 5  # drops gv.local_threat by 5 units
            return
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
                    CAFG_events.fox_fires.activate()

                # Adds a random item from the qwawason_items to player_items.
                case CAFG_events.space_express:
                    CAFG_events.space_express.activate()

                # If player succeeds, resets local threat. If player fails, game ends.(Unless player has bulletproof vest)
                case CAFG_events.national_hero:  #
                    die = False
                    CAFG_events.national_hero.activate()
                    if die:
                        deathhandler()
                    return
            # prints special event end bar.
            print(
                "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"
            )
            return

        case _:
            print("It's a very boring airport! One star out of five!")
            return

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
            f"{'chill'} ---  just take it easy\n"
            f"{'leave'} ---  go to the next airport\n"
            f"{'status'} ---  check your commands")


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
            CAFG_items.lottery_fake.activate()
            return [text]
        # uses lottery coupon
        case CAFG_items.lottery_coupon:
            CAFG_items.lottery_coupon.activate()
            return [text]
        # uses the invisibility cape
        case CAFG_items.invis_cape:
            CAFG_items.invis_cape.activate()
            return [text]
        # uses the fortune cookie
        case CAFG_items.luck_cookie:
            CAFG_items.luck_cookie.activate()
            return [text]
        # uses the Ebin-Sip -energy drink
        case CAFG_items.energydrink:
            CAFG_items.energydrink.activate()
            return [text]
        # ponders the used 1k bill.
        case CAFG_items.tonnin_seteli:
            CAFG_items.tonnin_seteli.activate()
            return [text]
        # uses the arcade ticket and gives score
        case CAFG_items.arcade_ticket:
            CAFG_items.arcade_ticket.activate()
            return [text]
        # uses the snow globe and gives score
        case CAFG_items.snow_globe:
            CAFG_items.snow_globe.activate()
            return [text]

    return [text, list_of_item_names]

# next 2 buys more items
def actionbuy():
    text = ""
    list_of_item_names = []

    if len(gv.shop_items) == 0:
        text = "You bought all the items. You lament that your shopping time has ended."
    else:
        text = "What do you want to buy"
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
        timehandler(1, gv.shop_items[shop_item_number].price)
        # uses 1 unit of time and increases local threat by 10 with said amount of time.
        # gv.shop_items.pop(shop_item_number)
        text = f"You bought {itemtobuy}!"

    return [text, shop_item_names]


# checks your items
def actioncheck():
    if len(gv.player_items) == 0:
        return "You have no items. Go buy some"
    else:
        items = ""
        for item in gv.player_items:
            items = f"{item.name}\n{item.desc}\n\n" + items
        return items

    # ^^^^^ should work ^^^^^


# allows you to do work
def actionwork():
    # PLACEHOLDER, REPLACE ONCE THERE'S MORE JOBS!
    print("'clean' to clean airport.")
    print("'rob' to rob a random person.")
    print()
    job_to_do = input("What work do you want to do (N to go back): ")

    # check valid input
    if job_to_do == "N":
        return
    else:
        print()
        actionworksub(job_to_do)


def actionworksub(used_job):
    match used_job:
        # clean airport job
        case "clean":
            stopwork = False
            while not stopwork:
                worktime = input("How long do you want to work for?(N to go back): ")
                print()

                # checks for valid input
                if worktime == "N":
                    print("You've decided you didn't want to clean the airport.")
                    stopwork = True
                elif not worktime.isdigit():
                    print("Invalid work time.")
                    print()
                else:
                    cleaning_art = [
                        r"""        "Sweep, sweep sweep..."
                (ㆆ_ㆆ)
               🧹 /|
                  / \ """,
                        r"""       "I should've just robbed a guy..."
                (ㆆ_ㆆ)
               🧹 /|
                  / \ """,
                        r"""        "Is this blood...?"
                (⊙_⊙;)
               🧹 /|
                  / \ """,
                        r"""
    "d̴̼͉̈̆f̵̭̒̅̎̆̚o̴̗͙͎̍͐͊͠g̸̢̟͎̜͌̚͘s̴̯̒̓̈p̸̹͚͌̎̿̂͠ǧ̵̰͛ͅò̸͍̃̇̄̈́͜ẽ̸̱̻̞̹r̸͖͉̃͆͘j̷̡̲̹̯̍͜g̶̡̲̠͙̐̂̾͜p̶̧̟̱̲̐́̓̚"
                  👽
               🧹 /|
                  / \
                        """,
                        r"""
        "WI WI WI WI UWAUWA"
                ₍^. .^₎
               🧹 /|
                  / \
                          """,
                    ]
                    print(random.choice(cleaning_art))
                    print("Cleaning the airport...")
                    if (
                            CAFG_items.janitor in gv.player_items
                    ):  # Gives extra money if player has janitors clothes
                        money = 50 * int(worktime)
                        gv.player_money += money
                        print(f"You cleaned the airport for {money}€!")
                        print(f"Your current balance is {gv.player_money}€.")
                        stopwork = True
                    else:
                        money = 20 * int(worktime)
                        gv.player_money += money
                        print(f"You cleaned the airport for {money}€...")
                        print(f"Your current balance is {gv.player_money}€.")
                        stopwork = True
                print()
                timehandler(
                    int(worktime), -5
                )  # Uses worktime amount of gv.time_units and decreases the local threat by -5 per spent unit.
            return

        # ROBS AN MF
        case "rob":
            robbed = random.randint(1 + gv.player_luck, 200 + gv.player_luck)
            print(r"""                 "Give money thx."
                   ( ͡❛ ͜ʖ ͡❛)      (⊙_⊙;)
                       |\ 🔪         /|      
                     / \            / \ """)
            print(f"You robbed an random civilian for {robbed}€!")
            gv.player_money += robbed
            # threat increases by 10 for every € stolen, player luck decreases this
            localthreathandler(1, robbed * (10 - (int(gv.player_luck / 10))))
            return

        case _:
            print("Unknown job")
            return


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


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points using the Haversine formula."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
            math.sin(delta_phi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in km

def movementhandler():
    conn = mysqlconnector()
    if not conn.is_connected():
        conn.reconnect()

    cursor = conn.cursor()

    # Get all airport data including ICAO codes and coordinates
    cursor.execute(
        "SELECT id, gps_code, name, latitude_deg, longitude_deg FROM airport WHERE gps_code IS NOT NULL"
    )
    airports = cursor.fetchall()

    # Find the current airport based on gv.current_airport (which is stored as an ICAO code)
    current_airport = next(
        (port for port in airports if port[1] == gv.current_country), None
    )

    if not current_airport:
        print("Error: Your current airport could not be found in the database.")
        return

    current_lat, current_lon = current_airport[3], current_airport[4]

    print(f"\nYou are currently at {current_airport[2]} ({current_airport[1]}).")

    # Set travel range (change this value to fit your game mechanics)
    travel_range_km = 3000  # Example range

    # Find nearby airports within the range
    nearby_airports = [
        port
        for port in airports
        if port[0] != current_airport[0]
        and haversine(current_lat, current_lon, port[3], port[4]) < travel_range_km
    ]

    if not nearby_airports:
        print("No airports within range. You may need a longer-range aircraft.")
        return

    print("\nNearby airports within range:")
    for port in nearby_airports:
        distance = haversine(current_lat, current_lon, port[3], port[4])
        print(f"{port[0]} ({port[1]}): {port[2]} - {distance:.2f} km away")


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

def timeunithandler(amount):
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
