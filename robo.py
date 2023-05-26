
import robomaster
from robomaster import robot


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    # 获取飞机电池电量信息
    tl_battery = tl_drone.battery
    battery_info = tl_battery.get_battery()
    print("Drone battery soc: {0}".format(battery_info))

    tl_drone.close()    