import math
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from robot_interfaces.msg import FoodState, FoodStateArray


class Kurban:
    def __init__(self, name: str, x: float, y: float):
        self.name: str = name
        self.pose: Pose = Pose()
        self.pose.x = x
        self.pose.y = y


class KurbanSpawner(Node):
    def __init__(self):
        super().__init__("kurban_spawner")
        self.kurbanlar: list[Kurban] = []
        self.kurban_isim_sayaci = 0

        self.kurban_pubber = self.create_publisher(FoodStateArray, "food_turtle_poses", 10)
        self.create_subscription(String, "killed_foods", self.oldurulen_cb, 10)
        self.spawn_client = self.create_client(Spawn, "spawn")

        while not self.spawn_client.wait_for_service(0.5):
            self.get_logger().warn("spawn servisi bekleniyor")

        self.create_timer(1.3, self.kontrol_kurban_yaratma)
        self.create_timer(0.1, self.kurbanlari_yayinla)




    def call_spawn(self, isim: str, x: float, y: float):
        istek = Spawn.Request()
        istek.name = isim
        istek.x = x
        istek.y = y
        istek.theta = random.uniform(0.0, 2 * math.pi)
        self.spawn_client.call_async(istek)




    def kontrol_kurban_yaratma(self):
        if len(self.kurbanlar) >= 5:
            return

        self.kurban_isim_sayaci += 1
        isim = f"kurban{self.kurban_isim_sayaci}"
        x = random.uniform(1.0, 10.0)
        y = random.uniform(1.0, 10.0)

        self.call_spawn(isim, x, y)
        self.kurbanlar.append(Kurban(isim, x, y))




    def kurbanlari_yayinla(self):
        mesaj = FoodStateArray()
        mesaj.header.stamp = self.get_clock().now().to_msg()
        for kurban in self.kurbanlar:
            food = FoodState()
            food.name = kurban.name
            food.pose.position.x = kurban.pose.x
            food.pose.position.y = kurban.pose.y
            mesaj.foods.append(food)
        self.kurban_pubber.publish(mesaj)

    def oldurulen_cb(self, msg: String):
        self.kurbanlar = [k for k in self.kurbanlar if k.name != msg.data]


def main():
    rclpy.init()
    node = KurbanSpawner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
