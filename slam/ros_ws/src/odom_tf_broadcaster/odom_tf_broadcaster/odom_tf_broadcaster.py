#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import TransformStamped
import message_filters
import tf2_ros
from tf2_ros import TransformBroadcaster

class OdomTFBroadcaster(Node):
    def __init__(self):
        super().__init__('odom_tf_broadcaster')

        # Create subscribers with message filters
        self.odom_sub = message_filters.Subscriber(
            self, Odometry, '/husky3/platform/odom')
        self.pointcloud_sub = message_filters.Subscriber(
            self, PointCloud2, '/husky3/sensors/lidar3d_0/points')

        # Time synchronizer that pairs messages based on timestamps
        # The parameters (10) is the queue size
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [self.odom_sub, self.pointcloud_sub], 10, 0.1)  # 0.1 sec tolerance
        self.ts.registerCallback(self.sync_callback)
        
        # TF broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        self.get_logger().info("Odom-PointCloud synchronizer initialized")

    def sync_callback(self, odom_msg, pointcloud_msg):
        # Create a transform from odom data but with pointcloud timestamp
        tf_stamped = TransformStamped()
        
        # Use the timestamp from the pointcloud
        tf_stamped.header.stamp = pointcloud_msg.header.stamp
        tf_stamped.header.frame_id = 'odom'  # Adjust as needed for your system
        tf_stamped.child_frame_id = 'base_link'  # Adjust as needed
        
        # Copy position data from odometry
        tf_stamped.transform.translation.x = odom_msg.pose.pose.position.x
        tf_stamped.transform.translation.y = odom_msg.pose.pose.position.y
        tf_stamped.transform.translation.z = odom_msg.pose.pose.position.z
        
        # Copy orientation data from odometry
        tf_stamped.transform.rotation = odom_msg.pose.pose.orientation
        
        # Broadcast the transform
        self.tf_broadcaster.sendTransform(tf_stamped)
        
        self.get_logger().debug(f"Published synchronized transform with timestamp: {pointcloud_msg.header.stamp.sec}.{pointcloud_msg.header.stamp.nanosec}")

def main(args=None):
    rclpy.init(args=args)
    node = OdomTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

