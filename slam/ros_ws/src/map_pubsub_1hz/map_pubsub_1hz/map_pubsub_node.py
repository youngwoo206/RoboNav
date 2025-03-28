#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import time

class PointCloudThrottler(Node):
    def __init__(self):
        super().__init__('pointcloud_throttler')
        # Create a subscription to the original pointcloud topic
        self.subscription = self.create_subscription(
            PointCloud2,
            '/husky3/sensors/lidar3d_0/points',
            self.pointcloud_callback,
            10)  # Queue size of 10
            
        # Create a publisher for the throttled pointcloud
        self.publisher = self.create_publisher(
            PointCloud2,
            '/throttled_pointcloud',
            10)  # Queue size of 10
            
        # Initialize timer for our desired publish rate (1 Hz)
        self.timer = self.create_timer(10, self.timer_callback)
        
        # Variable to store the most recent pointcloud
        self.latest_pointcloud = None
        
        # Flag to track if we have a new pointcloud since last publish
        self.new_data = False
        
        self.get_logger().info('PointCloud throttler node initialized')

    def pointcloud_callback(self, msg):
        # Store the incoming pointcloud
        self.latest_pointcloud = msg
        self.new_data = True

    def timer_callback(self):
        # Check if we have received any pointcloud data
        if self.latest_pointcloud is not None and self.new_data:
            # Publish the most recent pointcloud
            self.publisher.publish(self.latest_pointcloud)
            self.get_logger().debug('Published throttled pointcloud')
            
            # Reset the new data flag
            self.new_data = False

def main(args=None):
    rclpy.init(args=args)
    
    throttler = PointCloudThrottler()
    
    try:
        rclpy.spin(throttler)
    except KeyboardInterrupt:
        pass
    finally:
        throttler.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
