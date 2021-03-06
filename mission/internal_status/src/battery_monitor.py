#!/usr/bin/env python

#python imports
import subprocess
import os

#ros imports
import rospy
from std_msgs.msg import Int32

class BatteryMonitor():
    def __init__(self):
        
        rospy.init_node("battery_monitor")

        # Settings
        self.path_to_voltage_meter = rospy.get_param("/battery/logging/path")
        self.interval = rospy.get_param("/battery/logging/interval")          # How often the battery level is checked and published

        # Thresholds
        self.critical_level = rospy.get_param("/battery/thresholds/critical")   # Minimum allowed value in millivolts
        self.warning_level = rospy.get_param("/battery/thresholds/warning")     # Warning threshold in millivolts
        
        # Publisher
        self.battery_level_pub = rospy.Publisher("/auv/battery_level", Int32, queue_size=1)

        # Main loop
        while not rospy.is_shutdown():

            self.getVoltage()
            self.battery_level_pub.publish(self.voltage)

            # Critical voltage level
            if self.voltage <= self.critical_level:
                for i in range(10):
                    rospy.logfatal(self.voltage)
                    rospy.sleep(0.5)
                os.system("sudo shutdown now")
                
            # Warning voltage level
            elif self.voltage <= self.warning_level:
                rospy.logwarn(self.voltage)

            else :
                rospy.loginfo(self.voltage)
            
            rospy.sleep(self.interval)
            


    def getVoltage(self):

        # Record output from voltage meter command, decode from bytes object to string, convert from string to integer
        self.voltage = int(subprocess.check_output(["cat", self.path_to_voltage_meter]).decode("utf-8"))


if __name__ == '__main__':

    BatteryMonitor()