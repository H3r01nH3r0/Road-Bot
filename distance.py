from math import *

Aaltitude = 2000
Oppsite  = 20000

lat1 = 55.85107145860639
lat2 = 55.851450473354845
lon1 = 37.64691647073702
lon2 = 37.64720854841085

lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

dlon = lon2 - lon1
dlat = lat2 - lat1
a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
c = 2 * atan2(sqrt(a), sqrt(1-a))
Base = 6371 * c


Bearing =atan2(cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1), sin(lon2-lon1)*cos(lat2)) 

Bearing = degrees(Bearing)
print("")
print("")
print("--------------------")
print("Horizontal Distance:")
print(Base)
print("--------------------")
print("Bearing:")
print(Bearing)
print("--------------------")


Base2 = Base * 1000
distance = Base * 2 + Oppsite * 2 / 2
Caltitude = Oppsite - Aaltitude

a = Oppsite/Base
b = atan(a)
c = degrees(b)

distance = distance / 1000

print("The degree of vertical angle is:")
print(c)
print("--------------------")
print("The distance between the Balloon GPS and the Antenna GPS is:")
print(distance)
print("--------------------")
