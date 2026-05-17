#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from ej4.srv import Decision

import time
import math


class MoveServer(Node):

    def __init__(self):
        super().__init__('move_server')

        self.srv = self.create_service(
            Decision,
            'move_robot',
            self.move_callback
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Servidor listo')

    def move_callback(self, request, response):

        twist = Twist()

        mov = request.mov
        meters = request.meters

        self.get_logger().info(
            f'Recibido -> mov: {mov}, meters: {meters}'
        )

        # VELOCIDADES
        linear_speed = 0.2
        angular_speed = 0.5

        # MOVIMIENTO LINEAL
        if mov == "L":

            distance = abs(meters)

            twist.linear.x = linear_speed

            duration = distance / linear_speed

            start = time.time()

            while (time.time() - start) < duration:
                self.cmd_pub.publish(twist)
                time.sleep(0.05)

            twist.linear.x = 0.0
            self.cmd_pub.publish(twist)

            response.d = meters

        # ROTACION
        elif mov == "R":

            angle_deg = abs(meters)
            angle_rad = math.radians(angle_deg)

            twist.angular.z = angular_speed

            duration = angle_rad / angular_speed

            start = time.time()

            while (time.time() - start) < duration:
                self.cmd_pub.publish(twist)
                time.sleep(0.05)

            twist.angular.z = 0.0
            self.cmd_pub.publish(twist)

            response.d = meters

        else:

            self.get_logger().error('Movimiento invalido')

            response.d = -1

        return response


def main(args=None):

    rclpy.init(args=args)

    node = MoveServer()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()