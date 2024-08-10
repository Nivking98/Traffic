The first 4 folders entitled "A1A2" , "B1B2" , "C" and "D" show images from 4 phases of an intersection located in Trindad and Tobago.
This is considered to be the first dataset for this project.
The Pasea_scale_model folder depicts an illustration of the intersection with number of lanes present on the horizontal and vertical roads.

Within this folder also lies code to read the intersectionj.png for future simulation using 2D kinematics to deduce results for traffic flow on this specific intersection.
"adpsigcntrl.py" - Main .py file which encompasses the code for the simulation of the traffic light. 
It allows user input for the Adaptive Algorithms Possible for "A1A2" and "B1B2".

The YOLOv8n.pt was utitilized for object detection as sensor input to the algorithms for adjusting signal light timings.
The outputs are the signal light timings for the 4 phases and the 6 cycles labeled as "1","2", ... ".png" in the dataset.

Run the adpsigcntrl.py to see the results.
You can also run the "Sim.py" to see the "intersectionj.png" read into the pygame library for testing and future simulation.

[ECNG 3020 Presentati.pdf](https://github.com/user-attachments/files/16570412/ECNG.3020.Presentati.pdf)
