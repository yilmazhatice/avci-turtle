# Turtlesim Avcı

ROS 2 ve Turtlesim ile yapılmış avcı kaplumbağa oyunu.
Ekranda rastgele kurbanlar doğar, avcı o an en yakın kurbanı kovalayıp yer.

## Paketler

| Paket | Açıklama |
|---|---|
| `robot_interfaces` | `FoodState` ve `FoodStateArray` mesajları (kurban adı ve konumu) |
| `turtle_spawner` | Kurbanları üretir, `/food_turtle_poses` topic'inde yayınlar, `/killed_foods` ile öldürülenleri listeden çıkarır |
| `turtle_controller` | Avcıyı en yakın kurbana sürer, `kill` servisiyle yer ve `/killed_foods` topic'ine bildirir |
| `robot_bringup` | Tüm sistemi tek komutla başlatan launch dosyası |

## Kurulum

```bash
source /opt/ros/jazzy/setup.bash
cd ~/turtlesim_big
colcon build
source install/setup.bash
```


Node'ları ayrı ayrı çalıştırmak için:

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_spawner food_turtle_spawner
ros2 run turtle_controller main_turtle_controller
```

## Ayarlar

| Değer | Yer | Açıklama |
|---|---|---|
| 1.3 sn | `food_turtle_spawner.py` | Kurban üretim aralığı |
| 5 | `food_turtle_spawner.py` | Ekrandaki en fazla kurban sayısı |
| 1.0 | `main_turtle_controller.py` | Avcının kurbanı yeme mesafesi |
