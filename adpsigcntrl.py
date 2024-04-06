#Built from scratch
import cv2
import numpy as np
from ultralytics import YOLO
import time
#import pygame
import math
'''import csv
import os'''

#notes: fix A1A2: 2,3,4 
            #B1B2: 
            #C: 2,3,5
            #D: 1,2,3,4

ROI_coords = { 
    "A1A2": {
        "1": {
            "x1": 130,
            "y1": 365,
            "x2": 1100,
            "y2": 955
        },
        "2": {
            "x1": 130,
            "y1": 365,
            "x2": 1077,
            "y2": 955
        },
        "3": {
            "x1": 288,
            "y1": 446,
            "x2": 1010,
            "y2": 1057
        },
        "4": {
            "x1": 248,
            "y1": 478,
            "x2": 1031,
            "y2": 1057
        },
        "5": {
            "x1": 296,
            "y1": 358,
            "x2": 1079,
            "y2": 1077
        },
         "6": {
            "x1": 194,
            "y1": 389,
            "x2": 1102,
            "y2": 1078
        },
        },
    "C": {
        "1": {
            "x1": 0,
            "y1": 520,
            "x2": 1005,
            "y2": 1055
        },
        "2": {
            "x1": 0,
            "y1": 456,
            "x2": 1455,
            "y2": 1055
        },
        "3": {
            "x1": 99,
            "y1": 699,
            "x2": 1078,
            "y2": 1587
        },
        "4": {
            "x1": 0,
            "y1": 567,
            "x2": 1078,
            "y2": 1202
        },
        "5": {
            "x1": 0,
            "y1": 825,
            "x2": 546,
            "y2": 1329
        },
         "6": {
            "x1": 75,
            "y1": 195,
            "x2": 1080,
            "y2": 871
        },
    },
    "D": {
        "1": {
            "x1": 358,
            "y1": 382,
            "x2": 1076,
            "y2": 1221
        },
        "2": {
            "x1": 156,
            "y1": 619,
            "x2": 1080,
            "y2": 1200
        },
        "3": {
            "x1": 350,
            "y1": 336,
            "x2": 1076,
            "y2": 952
        },
        "4": {
            "x1": 336,
            "y1": 435,
            "x2": 1075,
            "y2": 973
        },
        "5": {
            "x1": 549,
            "y1": 106,
            "x2": 1077,
            "y2": 730
        },
         "6": {
            "x1": 0,
            "y1": 500,
            "x2": 1080,
            "y2": 1890
        }
    },
    "B1B2": { 
        "1": {
            "x1": 0,
            "y1": 0,
            "x2": 1920,
            "y2": 1080
        },
        "2": {
            "x1": 0,
            "y1": 0,
            "x2": 1920,
            "y2": 1080
        },
        "3": {
            "x1": 0,
            "y1": 0,
            "x2": 1920,
            "y2": 1080
        },
        "4": {
            "x1": 0,
            "y1": 0,
            "x2": 1920,
            "y2": 1080
        },
        "5": {
            "x1": 0,
            "y1": 0,
            "x2": 1920,
            "y2": 1080
        },
         "6": {
            "x1": 0,
            "y1": 0,
            "x2": 1920,
            "y2": 1080
        },
    }
}

##lanes per intersection side: should be constant as it is done manually however:
#If OpenCV is used to determine number of lanes in real time image this can be updated in another iteration of this project:
noOfLanes = {
    "A1A2": {
        "1": 4,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4,
        "6": 4,
        },
    "C": {
        "1": 1,
        "2": 1,
        "3": 1,
        "4": 1,
        "5": 1,
        "6": 1,
    },
    "D": {
        "1": 1,
        "2": 1,
        "3": 1,
        "4": 1,
        "5": 1,
        "6": 1,
    },
    "B1B2": {
        "1": 3,
        "2": 3,
        "3": 3,
        "4": 3,
        "5": 3,
        "6": 3,
    }
}

#Max Green Signal Time in seconds
Max_times ={
    "A1A2": 20,
    "C": 8,
    "D": 8,
    "B1B2": 20 
}
#Scaled speeds from m/s to pixels/s - to be updated accurately but placed here for future simulation
Avg_speeds = {
    "car" : 4,
    "bus" : 6,
    "truck" : 7,
    "motorcycle" : 2
}

#Colors for bounding boxes
colors = {
    'car': (255, 0, 255),  # Purple
    'bus': (255, 0, 0),    # Blue
    'truck': (0, 255, 0),  # Green
    'motorcycle': (255, 255, 255),  # White
}

#Avg acceleration of each vehicle in m/s^2
Veh_avgAccel = {
    "car" : 3.33,
    "bus" : 2,
    "truck" : 1.67,
    "motorcycle" : 6.87
}

#Actual Cycle Times - Preset as Fixed but Altered as the Algorithm Progresses for Adaptive Signal Control
cycle_times = {
     "A1A2": 10,
    "C": 4,
    "D": 4,
    "B1B2": 10 
    }

#Datasets for Iteration and Testing
objects = ["car", 'bus', 'truck', 'motorcycle']
Cameras= ["A1A2" , "C", "D", "B1B2"] 
cycles = ["1"] #Can be Altered to add cycles 1-6 Optionally 7 and 8 which was image processed(Image Processing Code developed using GPT and not reproduced in this REPO) to show Night time and Rain Blur Effects on YOLO Algorithm

'''TESTING with User Input:

#Slicing To Get Limited Phases:
Cameras_set = ["A1A2", "C", "D", "B1B2"]

# List with only "A1A2"
slice = input("Choose phases to simulate between 1-4: ")
Cameras_ = Cameras_set[:slice]


#Manipulating Number of Cycles to Simulate:
user_input = input("Enter the new end number for the cycle between 1 - 6 : ")
end_cycle = ((int(user_input))%9) + 1 # End number

# Creating the cycle list using range function
cycle = list(range(start_cycle, end_cycle))

# Show the cycles relating to 1-6 .png
print("cycle list:", cycle)

'''

image_dir ="C:\\GitHub Repositories\\Traffic\\"
#C:\Users\Nivan\Desktop\Traffic\A1A2\1.png
#C:\GitHub Repositories\Traffic\A1A2\1.png
space = "\\"
png = ".png"

def controller():
    #Loop through all the images taken from camera: (logical order A1A2(1) -> "B1B2(1) -> ... -> A1A2(2) -> ...")
    for cycle in cycles:
            for camera in Cameras:
                image_files = f"{image_dir}{camera}{space}{cycle}{png}"
                #image_files = "C:\\Users\\Nivan\\Desktop\\Traffic\\A1A2\\1.png"
                image = cv2.imread(image_files)
                if image is None:
                    print(f"Error loading image: {image_files}")
                #print(image_files)
                #Extract ROI from Manual Database:
                x1 = ROI_coords[camera][cycle]["x1"]
                y1 = ROI_coords[camera][cycle]["y1"]
                x2 = ROI_coords[camera][cycle]["x2"]
                y2 = ROI_coords[camera][cycle]["y2"]
                #Apply ROI on the local image files:
                #print(x1,y1,x2,y2)
                roi = image[int(y1):int(y2), int(x1):int(x2)]
                #scaled_roi = cv2.resize(roi, (800, 600))
                ''' cv2.imshow(f'ROI - {camera} {cycle}', scaled_roi)
                cv2.waitKey(0)
                cv2.destroyAllWindows()'''
                #Run model on the ROI (Area on road the system wants to detect vehicles) image:
                detect_vehicles(roi,camera,cycle)

def detect_vehicles(roi,camera,cycle):
    #vehicle count dictionary
    vehicle_counts = {
    'car': 0,
    'bus': 0,
    'truck': 0,
    'motorcycle': 0
    }
    #Pretrained Model
    model = YOLO("yolov8n.pt") 
    #Run Model on ROI
    results = model.predict(roi)
    result = results[0]
    box = result.boxes[0]
    #
    len(result.boxes)
    for box in result.boxes:
        class_id = result.names[box.cls[0].item()] #
        cords = box.xyxy[0].tolist() #
        cords = [round(x) for x in cords] #
        conf = round(box.conf[0].item(), 2) #
        '''print("Object type:", class_id)
        print("Coordinates:", cords)
        print("Probability:", conf)
        print("++++++++++++++++")'''
        #Place bounding box and count objects if the are [car,bus,truck,motorcycle]
        if class_id in vehicle_counts:
            vehicle_counts[class_id] += 1 
            cv2.rectangle(roi, (cords[0], cords[1]), (cords[2], cords[3]), colors[class_id], 2) #
            cv2.putText(roi, f"{class_id} {conf}", (cords[0], cords[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[class_id], 2) #
    # Place vehicle count on Image
    y_offset = 15
    for vehicle_type, count in vehicle_counts.items():
        text = f"{vehicle_type}: {count}" #
        cv2.putText(roi, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[vehicle_type], 2) #
        y_offset += 30  # Move to the next line for the next vehicle type

    scaled_roi = cv2.resize(roi, (800, 600))

    # Display the ROI with bounding boxes
    cv2.imshow('Detected Vehicles', scaled_roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Chose between adaptive signal timing algo2 or algo3 or move to fixed time/no time before traffic light simulation is run per cycle to get time results
    data_to_algo(vehicle_counts,camera,cycle)


def data_to_algo(vehicle_counts,camera,cycle):
     # Initialize a dictionary to store the data (empty dict then append but test code first)

    #COUNTS FROM CAMERA BASED SENSOR
    lanes = noOfLanes[camera][cycle]
    cars = vehicle_counts["car"]
    busses = vehicle_counts["bus"]
    trucks = vehicle_counts["truck"]
    motorcycles = vehicle_counts["motorcycle"]
    total_vehicles = cars + busses + trucks + motorcycles

    #PRINT COUNTS ON TERMINAL
    print("cycle", cycle, "intersection side: ", camera)
    print("Lane#: ", lanes)
    print("car count: ", cars)
    print("bus count: ", busses)
    print("truck count: ", trucks)
    print("motorcycle counts: ", motorcycles)

    #SEMI-ACTUATED ADAPTIVE CONTROL OF PASEA INTERSECTION: Weights or GST passed on from here to Sim
    if camera == "A1A2" or camera == "B1B2" : 
        choice = input("Type 1: fixed time or 2: algo2 or 3: algo3: ")
        if choice == "1":
            cycle_times[camera] = fixed_time(camera,cycle)
        elif choice == "2":
            cycle_times[camera] = algo2(lanes, total_vehicles, camera,cycle)
        else: 
            cycle_times[camera] = algo3(lanes, cars, busses, trucks, motorcycles,camera,cycle)
    elif (camera == "C" or camera == "D") and total_vehicles != 0:
        cycle_times[camera] = fixed_time(camera,cycle)
    else:
        cycle_times[camera] = no_time(camera, cycle)
    #Run Simulation After Last Phase of the Cycle
    if camera == "B1B2":
        traffic_light_simulation(cycle_times)

#skip side "C" or "D" if no vehicles present (none of the cases show this but it is possible in real world scenario) 
#weight = 0 
def no_time(camera, cycle):
    print("no time")
    weight = 0
    time = weight * Max_times[camera]
    print("time: ", time, "s")
    return time
    #calculate_green_time(camera, cycle, time)

#fixed time automatically allocated to "C" and "D" if cars present by choice for remaining
# weight fixed at 0.5
def fixed_time(camera, cycle):
    print("fixed time")
    weight = 0.5
    time = weight * Max_times[camera]
    print("time: ", time, "s")
    return time
    #calculate_green_time(camera, cycle, weight)

#Density based Algortihm - weights for A1A2 B1B2 2D[total_vehicles,lanes]
#weight scale 0-1 how is the densities appreciated: exponential or linear(linear here) determine by difference in weight values
#weight categorization - 4 Quantization steps
def algo2(lanes, total_vehicles,camera,cycle):
    print("Density based Algo")

    if camera == "A1A2":
        densityA = total_vehicles//lanes
        print(densityA)
        categoryA = {
            "low" : 4,
            "medium" : 6,
            "high" : 8
        }
        if densityA < categoryA["low"]:
            weight = 0.25
        elif densityA > categoryA["low"] and densityA < categoryA["medium"]:
            weight = 0.5
        elif densityA > categoryA["medium"] and densityA < categoryA["high"]:
            weight = 0.75
        else:
            weight = 1

    elif camera == "B1B2":
        densityB = total_vehicles//lanes
        categoryB = {
            "low" : 2,
            "medium" : 3,
            "high" : 5
        }
        if densityB < categoryB["low"]:
            weight = 0.25
        elif densityB > categoryB["low"] and densityB < categoryB["medium"]:
            weight = 0.5
        elif densityB > categoryB["medium"] and densityB < categoryB["high"]:
            weight = 0.75
        else:
            weight = 1

    time = weight * Max_times[camera]
    print("time: " , time, "s")
    return time
    #Density categorization: truck,bus,car,bike : bigger vehicle*number more density in queue: more time (3D)
    #// lane# -> higher density (higher weight category)
    #Time is int so at all times ensure time is int and not float hence why // used and specific max times and categorized weights used
    #calculate_green_time(camera, cycle, weight)

#Time based Algorithm - weights for A1A2 B1B2 3D [total_veh_type,lanes,avgtime] with summation
#weight categorization
#equation of motion queuelength = 0.5 * avgaccel * t² 
#Example calc for avg_timetocross, t = sqrt((2*queuelength)/avgaccel).
#Weight = sum(veh_type * avg_timetocross)/#lanes+1
#A1A2_queuelength = 50
#B1B2_queuelength = 30
#returns the time itself which may surpass the orignal maxGT for A and B to allow for more complexity in design to meet the needs of the current traffic situation
#Based on equation limitting factors must be established to ensure this value isn't too high but priority should always go to highways over minor streets
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

    print("time: " , GST, "s")
    return GST
    
    # faster vehicle less time to cross lights -> less time for side (mehirs algo)
    #avg speed
    #calculate_green_time(camera, cycle, weight)

def traffic_light_simulation(cycle_times): 
#display time
        
    for light, duration in [('A1 A2', cycle_times["A1A2"]), ('C', cycle_times["C"]), ('D', cycle_times["D"]), ('B1 B2', cycle_times["B1B2"])]:
        print(f"Light {light} is green for {int(duration)} seconds.")
        for remaining in range(int(duration), 0, -1):
            print(f"{remaining} seconds remaining")
            time.sleep(1)  # Simulate the green light duration
        print("Cycle Complete")
        
      


controller()

