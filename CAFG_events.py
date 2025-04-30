import random
import CAFG_variables as gv
import CAFG_items

class Event:
    desc = ""
    rarity = ""
    location = ""
    activate = ""
    def __init__(self,name):
        self.name = name

#decreases gv.local_threat by set amount or %
fox_fires = Event("Northern Lights")
fox_fires.desc = "Northern lights can be seen in the sky."
fox_fires.rarity = "Semi Harvinainen"
fox_fires.location = "country dependent"
def aurora(self):
    print("Their beaty has captured the attention of everyone.\n"
          "People are distracted and you feel more lucky.")
    addluck = random.randint(50, 100)
    print(f"You gained +{addluck} luck!")
    gv.player_luck += addluck
fox_fires.activate=aurora.__get__(fox_fires,Event)



#Sets gv.local_threat to 0 if successful
national_hero = Event("National Hero")
national_hero.desc = "A terror attack is about to happen at the airport!"
national_hero.rarity = "Harvinainen"
national_hero.location = "everywhere"
def terror(self):
    print("Quickly! De-escalate the sitsuation!")
    active = True
    tries = 3
    random_correct = random.randint(1, 4)
    while active:
        print("1 : Negotiate peacefully so no one gets hurt.\n"
              "2 : Give them a cookie, maybe they are just hungry!\n"
              "3 : Insult them and their mother.\n"
              "4 : Lie to them.\n"
              "5 : Go in guns blazing and shoot the bastards.")
        choise = input("Choose what to do:")

        # checks for valid input.
        if not choise.isdigit():
            print("Wrong input!")

        # Checks if player chose violence and happens to have a gun and ammo.
        elif int(choise) == 5:
            if CAFG_items.firearm in gv.player_items and CAFG_items.gun_mag in gv.player_items:
                print("You load your gun and  the terrorists. The locals see you as a hero!\n"
                      "(Local threaet set to 0)")
                gv.player_items.pop(gv.player_items.index(CAFG_items.gun_mag))
                gv.local_threat[gv.current_country] = 0
                active = False
            elif CAFG_items.firearm in gv.player_items:
                print("You dont have ammo!")
            else:
                print("You dont have a gun!")

        # If choice is correct, gives unique dialog based on what was chosen.
        elif int(choise) == random_correct:
            match choise:
                case 1:
                    print("With your intelligence and charisma, you calm the terrorists down.\n"
                          "")
                case 2:
                    print("You throw the terrorists a cookie and say 'You're not you when you are hungry.'.")
                case 3:
                    print("You successfully insult the terrorist")
                case 4:
                    print("You tell the terrorists that .")
            print("You managed to de-escalate the sitsuation! The locals see you as a hero!\n"
                  "(Local threat set to 0)")
            gv.local_threat[gv.current_country] = 0
            active = False
        else:
            tries -= 1
            print(f"Wrong choise! Try again! {tries} tries remaining!")
            if tries <= 0:
                print()
                if CAFG_items.bulletvest in gv.player_items:
                    print("The terrorists opened fire but your bulletproof vest saved you.\n"
                          "The terrorists left the airport.\n")
                    gv.player_items.pop(gv.player_items.index(CAFG_items.bulletvest))
                    active = False
                else:
                    print("Your 'negotiations' failed and the terrororists got you.")
                    die = True
                    return die
national_hero.activate=terror.__get__(national_hero,Event)



#Gives a random item
space_express = Event("Space Express")
space_express.desc = "Your Qawason express package has arrived! You wonder when you ordered this..."
space_express.rarity = "Harvinainen"
space_express.location = "everywhere"
def expressdelivery(self):
    qawason_random_item = random.randint(0, len(CAFG_items.qawason_items) - 1)
    print(f"You got one {CAFG_items.qawason_items[int(qawason_random_item)].name}!")
    gv.player_items.append(CAFG_items.qawason_items[int(qawason_random_item)])
space_express.activate=expressdelivery.__get__(space_express,Event)


used_events=[national_hero, space_express, fox_fires]