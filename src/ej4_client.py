#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from ej4.srv import Decision


class MoveClient(Node):

    def __init__(self):
        super().__init__('move_client')

        self.client = self.create_client(
            Decision,
            'move_robot')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando servicio...')

        self.req = Decision.Request()

    def send_request(self, mov, meters):

        self.req.mov = mov
        self.req.meters = meters

        future = self.client.call_async(self.req)

        rclpy.spin_until_future_complete(self, future)

        return future.result()


def main(args=None):

    rclpy.init(args=args)

    client = MoveClient()

    mov = input("Movimiento (L/R): ")
    meters = int(input("Distancia o angulo: "))

    response = client.send_request(mov, meters)

    print(f'Respuesta del servidor: {response.d}')

    rclpy.shutdown()


if __name__ == '__main__':
    main()