#!/usr/bin/env python3
"""
End-Effector Pose Publisher Node
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import tf2_ros
from tf2_ros import LookupException, ExtrapolationException, ConnectivityException


class PosePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.get_logger().info('PosePublisher started.')

        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)

        self._publisher = self.create_publisher(PoseStamped, '/end_effector_pose', 10)

        self._timer = self.create_timer(0.1, self._publish_pose)  # 10 Hz

    def _publish_pose(self):
        try:
            trans = self._tf_buffer.lookup_transform(
                'world',
                'end_effector',
                rclpy.time.Time()
            )

            msg = PoseStamped()
            msg.header = trans.header

            msg.pose.position.x = trans.transform.translation.x
            msg.pose.position.y = trans.transform.translation.y
            msg.pose.position.z = trans.transform.translation.z

            msg.pose.orientation = trans.transform.rotation

            self._publisher.publish(msg)

        except (LookupException, ExtrapolationException, ConnectivityException) as e:
            self.get_logger().warn(f'TF not available yet: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = PosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()