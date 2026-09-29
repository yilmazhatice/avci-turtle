import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from robot_interfaces.msg import FoodStateArray


class Kurban:
    def __init__(self, name: str, x: float, y: float):
        self.name: str = name
        self.pose: Pose = Pose()
        self.pose.x = x
        self.pose.y = y


class Hunter(Node):
    def __init__(self):
        super().__init__("turtle_hunter")
        self.avci_pose: Pose = Pose()
        self.kurbanlar: list[Kurban] = []
        self.oldurulenler: set[str] = set()

        self.create_subscription(Pose, "turtle1/pose", self.pose_cb, 10)
        self.create_subscription(FoodStateArray, "food_turtle_poses", self.kurbanlar_cb, 10)
        self.cmd_vel_pubber = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.oldurulen_pubber = self.create_publisher(String, "killed_foods", 10)
        self.kill_client = self.create_client(Kill, "kill")

        while not self.kill_client.wait_for_service(0.5):
            self.get_logger().warn("kill servisi bekleniyor")



    def ana_dongu(self):
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)
            self.avlan()





    def avlan(self):
        self.kontrol_kurban_olum()
        hedef = self.hedef_sec()

        if hedef < 0:
            self.pub_cmd_vel(0.0, 0.0)
            return
        self.kovala(hedef)




    def call_kill(self, isim: str):
        istek = Kill.Request()
        istek.name = isim
        self.kill_client.call_async(istek)




    def kontrol_kurban_olum(self):
        oldurulecekler: list[Kurban] = []
        for i in range(len(self.kurbanlar)):
            mesafe = self.mesafe_hesapla(i)
            if mesafe < 1.0:
                oldurulecekler.append(self.kurbanlar[i])

        for oldurulecek in oldurulecekler:
            self.call_kill(oldurulecek.name)
            self.kurbanlar.remove(oldurulecek)
            self.oldurulen_yayinla(oldurulecek.name)




    def oldurulen_yayinla(self, isim: str):
        self.oldurulenler.add(isim)
        mesaj = String()
        mesaj.data = isim
        self.oldurulen_pubber.publish(mesaj)

    def kurbanlar_cb(self, msg: FoodStateArray):
        self.kurbanlar = [
            Kurban(food.name, food.pose.position.x, food.pose.position.y)
            for food in msg.foods
            if food.name not in self.oldurulenler
        ]




    def mesafe_hesapla(self, kurban_index: int) -> float:
        kurban = self.kurbanlar[kurban_index]
        x_farki = kurban.pose.x - self.avci_pose.x
        y_farki = kurban.pose.y - self.avci_pose.y
        return math.sqrt(x_farki ** 2 + y_farki ** 2)





    def aci_farki_hesapla(self, kurban_index: int) -> float:
        kurban = self.kurbanlar[kurban_index]
        x_farki = kurban.pose.x - self.avci_pose.x
        y_farki = kurban.pose.y - self.avci_pose.y

        kurban_aci = math.atan2(y_farki, x_farki)
        aci_farki = kurban_aci - self.avci_pose.theta


        if aci_farki > math.pi:
            aci_farki -= 2 * math.pi
        elif aci_farki < -math.pi:
            aci_farki += 2 * math.pi

        return aci_farki





    def hedef_sec(self) -> int:
        enyakin = 10000.0
        hedef = -1

        for i in range(len(self.kurbanlar)):
            mesafe = self.mesafe_hesapla(i)
            if mesafe < enyakin:
                hedef = i
                enyakin = mesafe

        return hedef




    def kovala(self, hedef_index: int):
        mesafe = self.mesafe_hesapla(hedef_index)
        aci_farki = self.aci_farki_hesapla(hedef_index)

        cizgisel_hiz = max(0.5, mesafe * 1.2)
        acisal_hiz = aci_farki * 3.0

        self.pub_cmd_vel(cizgisel_hiz, acisal_hiz)




    def pose_cb(self, msg: Pose):
        self.avci_pose = msg

    def pub_cmd_vel(self, cizgisel: float, acisal: float):
        mesaj = Twist()
        mesaj.linear.x = cizgisel
        mesaj.angular.z = acisal
        self.cmd_vel_pubber.publish(mesaj)


def main():
    rclpy.init()
    node = Hunter()
    try:
        node.ana_dongu()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()