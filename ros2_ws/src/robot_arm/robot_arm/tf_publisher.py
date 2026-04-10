#!/usr/bin/env python3
"""
TF Publisher Node
"""

import rclpy
from rclpy.node import Node
import tf2_ros
from geometry_msgs.msg import TransformStamped
import math


class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.get_logger().info('TFPublisher started.')

        self._br = tf2_ros.TransformBroadcaster(self)
        self._static_br = tf2_ros.StaticTransformBroadcaster(self)

        self._t = 0.0
        self._timer = self.create_timer(0.02, self._broadcast)  # 50 Hz

        self._publish_static()

    def _publish_static(self):
        transforms = []

        # world -> base_link
        t = TransformStamped()
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'
        t.transform.rotation.w = 1.0
        transforms.append(t)

        # link1 -> link2
        t = TransformStamped()
        t.header.frame_id = 'link1'
        t.child_frame_id = 'link2'
        t.transform.translation.x = 0.3
        t.transform.rotation.w = 1.0
        transforms.append(t)

        # link2 -> end_effector
        t = TransformStamped()
        t.header.frame_id = 'link2'
        t.child_frame_id = 'end_effector'
        t.transform.translation.x = 0.2
        t.transform.rotation.w = 1.0
        transforms.append(t)

        self._static_br.sendTransform(transforms)

    def _broadcast(self):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'link1'

        # 45° amplitude, 0.5 Hz
        angle = 0.785 * math.sin(2 * math.pi * 0.5 * self._t)

        t.transform.rotation.z = math.sin(angle / 2.0)
        t.transform.rotation.w = math.cos(angle / 2.0)

        self._br.sendTransform(t)

        self._t += 0.02


def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()