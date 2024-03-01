This program has been designed and implemented to track the state of an object over time, where that object is a vehicle traveling on a highway. The program uses measurement data from two independent sources: the odometry of 
the vehicle and the vision system that analyzes the road. 
The parameters of the state vector, namely X (position relative to the center of the road), alpha (directional angle calculated relative to the road axis) and V (vehicle speed), are estimated using the Kalman
filter algorithm implemented in the program. The user can customize the filtering parameters, and the system automatically converts the transition model and outputs, entered by the user, into the corresponding variables used by the filter.
The models of transitions (state succession) and outputs (state projection onto observations) have been precisely defined for this application domain, providing an accurate representation of vehicle behavior on the road.
To test the effectiveness of the program, sequences of disturbed measurement data were generated for different types of driving, such as straight ahead, curved driving, lane changes, acceleration and braking. The program 
estimates the vehicle's state vector at successive moments in time, presenting the user with graphs of the state parameters estimated and included in the simulated observations.
Numerous tests of the program's performance for different types of driving and different levels of interference were also conducted to verify its effectiveness and accuracy under a variety of road conditions.
The program was written in such a way that its functionality could be easily extended to include additional algorithms and problems.
