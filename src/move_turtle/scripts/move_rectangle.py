#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from math import radians

def move_turtle_in_rectangle():
    # Initialize the ROS node
    rospy.init_node('move_turtle_rectangle_node', anonymous=True)
    
    # Create a publisher to send velocity commands to the turtle
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    # Define the rate at which the loop will run (10 Hz)
    rate = rospy.Rate(10)
    
    # Create a Twist message to set linear and angular velocity
    vel_msg = Twist()

    # Set linear velocity (forward motion)
    vel_msg.linear.x = 1.0  # Adjust speed as necessary
    vel_msg.linear.y = 0.0
    vel_msg.linear.z = 0.0
    
    # Set angular velocity (rotation for turning)
    vel_msg.angular.x = 0.0
    vel_msg.angular.y = 0.0
    vel_msg.angular.z = 0.0

    # Define the dimensions of the rectangle
    rectangle_length = 5.0  # Length of the rectangle (meters)
    rectangle_width = 3.0   # Width of the rectangle (meters)

    rospy.loginfo("Moving the turtle in a rectangular path...")

    # Move in the rectangular path (4 sides)
    for _ in range(2):  # Two full sides of the rectangle (we repeat it)
        # Move forward for the length of the rectangle
        move_straight(velocity_publisher, vel_msg, rectangle_length, rate)
        
        # Turn 90 degrees to make the corner
        turn_90_degrees(velocity_publisher, rate)
        
        # Move forward for the width of the rectangle
        move_straight(velocity_publisher, vel_msg, rectangle_width, rate)
        
        # Turn 90 degrees again to make another corner
        turn_90_degrees(velocity_publisher, rate)

    rospy.loginfo("Rectangle path completed.")

def move_straight(publisher, vel_msg, distance, rate):
    # Move the turtle straight for the specified distance
    # We are moving at a constant linear speed, so we compute the time to travel the distance
    vel_msg.linear.x = 1.0  # Set forward speed (adjust as necessary)
    
    # Time to travel the given distance (distance = speed * time)
    duration = distance / vel_msg.linear.x
    start_time = rospy.Time.now()
    
    rospy.loginfo(f"Moving straight for {distance} meters.")
    
    # Move until the desired distance is covered
    while rospy.Time.now() - start_time < rospy.Duration(duration):
        publisher.publish(vel_msg)
        rate.sleep()

    # Stop the turtle after moving the desired distance
    vel_msg.linear.x = 0.0
    publisher.publish(vel_msg)

def turn_90_degrees(publisher, rate):
    # Set angular velocity to rotate 90 degrees (pi/2 radians)
    vel_msg = Twist()
    vel_msg.angular.z = 1.0  # Angular velocity for turning (radians per second)
    
    # The time it will take to turn 90 degrees (angle = angular velocity * time)
    turn_duration = 1.57 / vel_msg.angular.z  # 1.57 radians = 90 degrees
    
    rospy.loginfo("Turning 90 degrees.")
    
    # Rotate until the turtle has turned 90 degrees
    start_time = rospy.Time.now()
    while rospy.Time.now() - start_time < rospy.Duration(turn_duration):
        publisher.publish(vel_msg)
        rate.sleep()

    # Stop the rotation after the turn is complete
    vel_msg.angular.z = 0.0
    publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        # Call the function to move the turtle in a rectangular path
        move_turtle_in_rectangle()
    except rospy.ROSInterruptException:
        pass

