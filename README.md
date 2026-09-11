# Turtlesim Avcı

ROS 2 ve Turtlesim ile yapılmış avcı kaplumbağa oyunu.
Ekranda rastgele kurbanlar doğar, avcı o an en yakın kurbanı kovalayıp yer. 
Her 10 saniyede bir kurbanlar daha sık ve daha kalabalık doğar.


## Kurulum

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/turtlesim_big/src && cd ~/turtlesim_big/src
ros2 pkg create turtlesim_big --build-type ament_python --dependencies rclpy turtlesim geometry_msgs --node-name hunter
```

`hunter.py` kodunu `src/turtlesim_big/turtlesim_big/hunter.py` dosyasına yapıştır, sonra derle:

```bash
cd ~/turtlesim_big
colcon build
source install/setup.bash
```

## Çalıştırma

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
source ~/turtlesim_big/install/setup.bash
ros2 run turtlesim_big hunter
```

## Ayarlar

Zorluk, `hunter.py` dosyasının en üstündeki sabitlerle değiştirilebilir:


| `BASLANGIC_ARALIK` | 2.0 | İlk kurban üretim aralığı (sn) |
| `EN_KISA_ARALIK` | 0.3 | En hızlı üretim aralığı (sn) |
| `HIZLANMA_ORANI` | 0.85 | Her seviyede aralığın çarpıldığı oran |
| `SEVIYE_SURESI` | 10.0 | Seviye atlama süresi (sn) |
| `EN_FAZLA_KURBAN` | 25 | Ekrandaki en fazla kurban sayısı |
| `YAKALAMA_MESAFESI` | 0.8 | Avcının kurbanı yeme mesafesi |
