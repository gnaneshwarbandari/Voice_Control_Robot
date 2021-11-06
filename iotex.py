#!/usr/bin/env python3
import rospy
import wiotp.sdk.device
import time
import random
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

pub = None

myConfig = { 
    "identity": {
        "orgId": "gagtey",
        "typeId": "New",
        "deviceId":"12345"
    },
    "auth": {
        "token": "12345678"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    take_action(m)

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    if regions == "forward":
        state_description = 'case 1 - Moving Forward'
        linear_x = 0.6
        angular_z = 0
    elif regions == "stop":
        state_description = 'case 2 - Stopping...'
        linear_x = 0
        angular_z = 0.0
    elif regions == "left":
        state_description = 'case 3 - Turning Left'
        linear_x = 0
        angular_z = 0.6
    elif regions == "right":
        state_description = 'case 4 - Turning Right'
        linear_x = 0
        angular_z = -0.6
    elif regions == "backward":
        state_description = 'case 5 - Moving Backward'
        linear_x = -0.6
        angular_z = 0.0
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub
    
    rospy.init_node('voice_Control')
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    #sub = rospy.Subscriber('/mybot/laser/scan', LaserScan, clbk_laser)

    client.commandCallback = myCommandCallback

    rospy.spin()

if __name__ == '__main__':
    main()

client.disconnect()

    
