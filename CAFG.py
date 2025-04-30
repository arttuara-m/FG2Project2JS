import mysql.connector
import EventHandler

conn = mysql.connector.connect(
    host="localhost",
    user="surviver",
    password="123",
    database="flight_game",
    charset="latin1",
    collation="latin1_swedish_ci",
)


print("___________________________________________________________________________")
print(
    "You're an extraterrestial alien, one who was flying carefree with your UFO. You just enjoyed exploring the inky black space."
)
print(
    "But a critical system failure sent your vessel spiraling out of control, tearing through the sky like a fallen meteor."
)
print(
    "You landed in Earth, a world inhabited by strange bipeds who have built a civilization. You decide to shapeshift into this strange form."
)
print(
    "With no possible way to return to the galaxy, you decide to blend in, become a tourist. Grab a hawaiian shirt that tourists wear."
)
print(
    "But be careful. The governments of all countries have been informed of an extraterrestial creature roaming around the world."
)
print(
    "Still, you decide to fly around to see the wonders of Earth. Just try to not get killed!"
)
print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
print()

EventHandler.turnhandler()
