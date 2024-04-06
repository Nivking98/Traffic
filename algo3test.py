import math


cars = 20
busses= 2
trucks = 1
motorcycles = 0
lanes =3
camera = "A1A2"
cycle = 1

def algo3(lanes, cars, busses, trucks, motorcycles,camera,cycle):
    print("Time based Algo")
    if camera == "A1A2":
        A1A2_avg_ttc = {
            "car" : 3.87,
            "bus" : 5.00,
            "truck" : 6.08,
            "motorcycle" : 2.29
        }

        A1A2_sum = math.floor(cars*A1A2_avg_ttc["car"] + busses*A1A2_avg_ttc["bus"] + trucks*A1A2_avg_ttc["truck"] + motorcycles*A1A2_avg_ttc["motorcycle"])
        GST = A1A2_sum//(lanes+1)


    if camera == "B1B2":
        B1B2_avg_ttc = {
            "car" : 3.01,
            "bus" : 3.87,
            "truck" : 4.71,
            "motorcycle" : 1.75
        }

        B1B2_sum = math.floor(cars*B1B2_avg_ttc["car"] + busses*B1B2_avg_ttc["bus"] + trucks*B1B2_avg_ttc["truck"] + motorcycles*B1B2_avg_ttc["motorcycle"])
        GST = B1B2_sum//(lanes+1)

    print("Time for side: " ,  GST , "s")
    return GST

algo3(lanes, cars, busses, trucks, motorcycles,camera,cycle)