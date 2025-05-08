very_expensive = 1000
expensive = 500
costly = 100
average = 50
cheap = 10
very_cheap = 2
free = 0

import time
import random
import CAFG_variables as gv #Import Global Variables

# About attribute.rarity: Items rarity placeholder.
#   Rarities ranging from most common to most rare:
common = 1
uncommon = 2
rare = 3
epic = 4
legendary = 5

# About attribute.price: price of the item, called values are at the very top of this file.

# About attribute.use_time: positive [int]s give items the corresponding amount of use times.
#   * Everytime an item is used, its value is updated as current value minus 1.
#   * Once 0 item cant be used anymore.
#   * -1 gives an infinite amount of use times.

# About attribute.active: True means item is active, False means item is passive.


class Item:
    desc = ""
    buy = ""
    rarity = 1
    price = 0
    use_time = 0
    itemid = 0
    activate = ""
    active = False
    def __init__(self, name):
        self.name = name


invis_cape = Item("Invisibility Cloak")
invis_cape.desc = ("A cloack that makes you invisible.\n"
                   "When used, splits the local threat level in two\n"
                   "\n"
                   "(-50% local threat.).")
invis_cape.buy = f"You imagine how easily you could've gotten away with stealing this instead."
invis_cape.rarity = epic
invis_cape.price = costly
invis_cape.use_time = 1
invis_cape.active = True
#[local threat]/2 when used
def invis(self):
    gv.local_threat[gv.current_airport] = gv.local_threat[gv.current_airport] // 2
    return "The cape made you harder to track! (Decreased local threat by 50%)"
invis_cape.activate = invis.__get__(invis_cape,Item)



lottery_fake = Item("Falsified Lottery Coupon")
lottery_fake.desc = ("With your skills- I mean luck, you modify-\n"
                "*ahem* you SOMEHOW manage to get a lottery coupon with the winning numbers!\n"
                "Lucky you!\n"
                "\n"
                "- Gives between 1 000€ and 3 000€, but increases local threat by 3 000 per use.")
lottery_fake.buy = f""
lottery_fake.rarity = rare
lottery_fake.price = expensive
lottery_fake.use_time = 1
lottery_fake.active = True
lottery_fake.type = True
#Gives 1000-3000€, threat up by 3 000 no matter the outcome.
def lotteryfake(self):
    money = random.randint(1000, 3000)
    gv.local_threat[gv.current_airport] += 3000 - (gv.player_luck // 100)
    gv.player_money += money
    return f"You managed to get {money}€, but now you are in trouble!"
lottery_fake.activate = lotteryfake.__get__(lottery_fake,Item)



lottery_coupon = Item("Legit Lottery Coupon")
lottery_coupon.desc = (f"An actually legit 100% real lottery coupon that's not gonna get you in trouble!\n"
                       f"May not give you a lot though...\n"
                       f"But theres a chance to get up to 10 000€! Statistically guaranteed after 10 000 coupons!!\n"
                       f"\n"
                       f"- 50% nothing,\n"
                       f"- ranging from 20% to 5% theres a chance to get from 1€ to 2000€,\n"
                       f"- 0.01% chance to get the jackpot of 10 000€)")
lottery_coupon.buy = "Surely this one's the one to make you rich! "
lottery_coupon.rarity = common
lottery_coupon.price = cheap
lottery_coupon.use_time = 1
lottery_coupon.active = True
#50% chance to get nothing, 20% for 10-50€, 10% for 50-100€, 10% for 100-500€
# 5% for 500€-700€, 3% for 700€-1000, 1.99% for 1000-2000€, 0.01% 10 000€
def lotterystart(self):
    lottery = random.randint(0, 10000) + (gv.player_luck // 100)
    if lottery <= 5000:
        money = 0
    elif 5000 < lottery < 7000:
        money = random.randint(1, 5)
    elif 7000 < lottery < 8000:
        money = random.randint(5, 10)
    elif 8000 < lottery < 9000:
        money = random.randint(10, 50)
    elif 9000 < lottery < 9500:
        money = random.randint(50, 100)
    elif 9500 < lottery < 9800:
        money = random.randint(100, 500)
    elif 9800 < lottery < 9999:
        money = random.randint(500, 2000)
    else:
        money = 10000
    return f"Congratulations! You got {money}€ from the lottery!"
    gv.player_money += money
lottery_coupon.activate = lotterystart.__get__(lottery_coupon,Item)



luck_cookie = Item("Fortune Cookie")
luck_cookie.desc = ("A traditional chinese cookie that tells your fortune!\n"
                    "\n"
                    "+ luck")
luck_cookie.buy = ""
luck_cookie.rarity = uncommon
luck_cookie.price = cheap
luck_cookie.use_time = 1
luck_cookie.active = True
#Increases luck, there's a small chance to decrease it instead
def fortune(self):
    chance = random.randint(1, 6)
    if chance == 1:
        gv.player_luck += 10
        luck = 10
    else:
        gv.player_luck -= 10
        luck = -10
    return f"You read the fortune from the cookie and got {luck} luck!"
luck_cookie.activate = fortune.__get__(luck_cookie, Item)



energydrink = Item("ES :DDD")
energydrink.desc= (f"EbinSip the iconic energy drink.\n"
                   f"\n"
                   f"When consumed:\n"
                   f"- +4 time units")
energydrink.buy = "Ebin :DD"
energydrink.rarity = rare
energydrink.price = average
energydrink.use_time = 1
energydrink.active = True
#pärisemää :D
def addenergy(self):
    addtime = 4
    gv.time_units += addtime
    return (f"You chug the energy drink and feel energized.\n"
          f"(Gained {addtime} time units)\n"
          f"You feel like you could do a wheelie with any vehicle.")
energydrink.activate = addenergy.__get__(energydrink, Item)



snow_globe = Item("Snow globe")
snow_globe.desc = ("A Snow globe suvenier.\n"
                   "Snow falls when you shake it, its fun to look at idk.\n"
                   "\n"
                   "+ 100 score")
snow_globe.buy = ""
snow_globe.rarity = epic
snow_globe.price = average
snow_globe.use_time = -1
snow_globe.active = True
#score
def shakeglobe(self):
    gv.current_score += 500
    return (f"You gave the snowglobe a good shake and \n"
            f"watched as the artificial snow in the globe fell.")
snow_globe.activate =shakeglobe.__get__(snow_globe, Item)



arcade_ticket = Item("Arcade ticket")
arcade_ticket.desc = ("A ticket to the arcade where you can play games and have fun!\n"
                      "\n"
                      "+ 100 score")
arcade_ticket.buy = ""
arcade_ticket.rarity = rare
arcade_ticket.price = very_cheap
arcade_ticket.use_time = 1
arcade_ticket.active = True
#scoreeeeeeeeeee
def arcade(self):
    gv.current_score += 100
    return f"You visit a local arcade to play some games and have some fun! Yippee!"
arcade_ticket.activate = arcade.__get__(arcade,Item)



s_rabbit_paw = Item("Space-rabbit Foot")
s_rabbit_paw.desc = ("Straight from the vast prairies of space.\n"
                     "\n"
                     "+ luck")
s_rabbit_paw.buy = ""
s_rabbit_paw.rarity = epic
s_rabbit_paw.price = expensive
s_rabbit_paw.use_time = -1
s_rabbit_paw.active = False
#Adds a certain % buff to luck.
def rabbitluck(self):
    luck = random.randint(0, 20)
    gv.player_luck += luck
    return f"The rabbit's paw gives you +{luck} luck!"
s_rabbit_paw.activate = rabbitluck.__get__(s_rabbit_paw,Item)



janitor = Item("Janitors Clothes")
janitor.desc = ("Allows you to disguise yourself as a janitor and work for some money.\n"
                "\n"
                "- Increases income from [job]:'Clean the Airport' by 30€")
janitor.buy = ""
janitor.rarity = uncommon
janitor.price = costly
janitor.use_time = -1
janitor.active = False
#Under "Work", gives like 20€



flightmaster = Item("Flight-masters Clothes")
flightmaster.desc = ("Allows you to disguise your self as a flight master\n"
                     "and earn money while flying. Due to you not knowing how to fly however,\n"
                     "there is a slight chance you'll fall out of the sky.\n"
                     "\n"
                     "+ 200€ from the next flight\n"
                     "- 0.1% chance to die on the next flight.%")
flightmaster.buy = ""
flightmaster.rarity = epic
flightmaster.price = expensive
flightmaster.use_time = -1
flightmaster.active = False
#Under "Work", gives like 100€



bulletvest = Item("Bulletproof Vest")
bulletvest.desc = ("Allows you to take more hits.\n"
                   "\n"
                   "(Saves your life in some cases)")
bulletvest.buy = (f"The cashier gives you bombastic side eye and is probably thinking:\n"
                  f"'What'd you need that for?' You respond by giving the cashier back the bombastic side eye\n"
                  f"for selling such things in the first place.")
bulletvest.rarity = epic
bulletvest.price = expensive
bulletvest.use_time = 1
bulletvest.active = False
#gives the player +50 health(once that is added, for now just protects you in national_hero event)



tonnin_seteli = Item("A coffee and a cookie")
tonnin_seteli.desc = ("Wasn't this suppose to cost just 2€?\n"
                      "That was 1k € you gave, right? There is no way it wasn't 1k €...\n"
                      "But where's the change then? They couldn't possibly miss-calculate it, right?\n"
                      "They did give change back from it but it was so little...\n"
                      "Are you absolutely sure it was 1k € you gave? That was 1k €... \n"
                      "\n"
                      "\x1b[3m'Se oli tonnin seteli… Enks mä antanu tonnin setelin?'\x1b[0m")
tonnin_seteli.buy = (f"\x1b[3mYou find that 1000€ bill is the smallest you have so you decide to give it.\n"
                     f"The cashier gives very little change and then faces back to you.\n"
                     f"Although now he is just staring off into space with a blank expression on his face.\n"
                     f"You start to question if you actually gave 1000€ or not and try to ask several times\n"
                     f"where the rest of the change is but you get no response. The cashier is like a statue.\n"
                     f"It's like his consciousness had left this plane of existence. You wave your arm in front of him,\n"
                     f"but its no use. The money is gone now. No way to get it back.\n"
                     f"Are you really certain it was actually 1000€ that you gave? \x1b[0m")
tonnin_seteli.rarity = legendary
tonnin_seteli.price = very_cheap  # Se oli tonnin seteli...
tonnin_seteli.use_time = -1
tonnin_seteli.active = False
def tonni(self):
    return (f"You ponder at the purchase. It cost you 1000€...\n"
          f"You've forgotten what the price was suppose to even be, why didn't the cashier give back any change?\n"
          f"Was it actually 1000€? Is this some special coffee? Or some caviar cookie?\n"
          f"Now you are questioning if you actually gave 1000€ for it or not...\n"
          f"You don't even feel like eating this...")
tonnin_seteli.activate = tonni.__get__(tonnin_seteli,Item)
#Does absolutely nothing, reference to 'Kummeli'



warhead = Item("Unstable Nuclear Warhead")
warhead.desc = ("A Nuclear Warhead. Obviously no one wants to arrest a man with an armed bomb.\n"
                "Due to its unstable nature however, there is a small chance it will detonate.\n"
                "\n"
                "\x1b[3mOh and by the way, don't ask how you are allowed onto ANY planes with THIS...\x1b[0m\n"
                "\n"
                "- Local threat stays at 0"
                "- -5% global threat"
                "- every turn, 5% chance to roll a D20. If it lands on 1 the warhead detonates ending the game.")
warhead.buy = "You can't believe you got this for free, it feels too good to be true."
warhead.rarity = legendary
warhead.price = free  # it's free!
warhead.use_time = -1
warhead.active = True
#Local threat stays at 0, global threat grows by -5%
#On start of a turn, theres ~1-5% to print= "The nuclear warhead is shaking!"
#Then game throws a d20= if 2-20 = print "Nothing happened...", if 1 = "Game over"
def checkstability():
    stabilitycheck = random.randint(0, 10)
    if stabilitycheck <= 1:
        print()
        print("The warhead became less stable! You can hear it ticking!")
        time.sleep(1.5)
        print("\x1b[3mTick tock.\x1b[0m")
        time.sleep(1.5)
        print("\x1b[3mTick tock.\x1b[0m")
        time.sleep(1.5)
        print("\x1b[3mTick tock.\x1b[0m")
        time.sleep(1.5)
        blowup = random.randint(1, 20)
        if blowup == 1:
            print()
            print("The warhead detonates, evaporating you and the current airport in the blast.")
            die = True
            return die
        else:
            print("The warhead falls silent again...")
    gv.local_threat[gv.current_airport] = 0
    gv.global_threat -= int(gv.global_threat * 0.05)
warhead.activate = checkstability.__get__(warhead,Item)
def nucelearexplosion(self):
    gv.global_threat = 100000000000000


kerosene = Item("Jetfuel")
kerosene.desc = ("Can't melt steel beams.\n"
                 "\n"
                 "-doesn't do anything, yet\n"
                 "no, you cannot drink it.")
kerosene.buy = "KEROSENE!"
kerosene.rarity = rare
kerosene.price = costly
kerosene.use_time = 1
kerosene.active = True



flight_membership = Item("AirPremium membership")
flight_membership.desc = (f"Membership for\x1b[3m the\x1b[0m airline. Yes, the only one you are using.\n"
                          f"\x1b[3mIncludes a seat in the first class.\x1b[0m\n"
                          f"\n"
                          f"-30% ticket price on each flight.")
flight_membership.buy = ""
flight_membership.rarity = epic
flight_membership.price = very_expensive
flight_membership.use_time= -1
flight_membership.active = False



firearm = Item("Gun")
firearm.desc = ("Its a gun.\n"
                "\n"
                "-increases income from [job]: 'rob' by ~25%"
                "-can be used as a 'negotiator' in some cases.")
firearm.buy = "Freedom dispenser acquired."
firearm.rarity = rare
firearm.price = expensive
firearm.use_time = -1
firearm.active = False



gun_mag = Item("Loaded magazine")
gun_mag.desc = ("A mag for a gun. Filled with bullets.\n"
                "\n"
                "-needs a 'Gun' to be used.")
gun_mag.buy = "Dispensable freedom acquired."
gun_mag.rarity = rare
gun_mag.price = costly
gun_mag.use_time = 1
gun_mag.active = False



#these are the lists of items that the game uses
shop_items = [invis_cape, lottery_fake, lottery_coupon, luck_cookie, janitor, energydrink, tonnin_seteli, bulletvest, arcade_ticket, snow_globe, firearm, gun_mag]
qawason_items = [invis_cape, lottery_fake, lottery_coupon, luck_cookie, s_rabbit_paw, energydrink, bulletvest, warhead]
all_items = [invis_cape, lottery_fake, lottery_coupon, luck_cookie, energydrink, snow_globe, arcade_ticket, s_rabbit_paw, janitor, flightmaster, bulletvest, tonnin_seteli, warhead, kerosene, flight_membership, firearm, gun_mag]