import sys
import os
import subprocess
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from system_integrations.Fragrance_Dispenser_API_pi import Fragrance_Dispenser_The_Machine
from system_integrations.bmp_generater import calculate_bmp
from backend_communication.services.OrderManager import OrderManager
from backend_communication.models.Perfume import Perfume, Food
from time import sleep

order_manager = OrderManager()
remocon = Fragrance_Dispenser_The_Machine('/dev/ttyACM0', '/dev/usb/lp0')
remocon.system_go_home()

# sleep(30)
while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Checking for new orders...")
    order = order_manager.process_next_order()
    if order:
        print("New order found:")
        perfume_enum = order['perfume']
        food_enum = order['food']
        userName = order['customerName']
        try:
            foodNo = list(Food).index(Food(food_enum))
            remocon.execute_once(foodNo)
            calculate_bmp([perfume_enum,perfume_enum,food_enum,food_enum], userName)
            # 使用 sudo 执行另一个 Python 文件
            subprocess.run(['sudo', 'python3', '/home/ubuntu/fragrance_dispenser/system_integrations/printer_main.py'], check=True)
            waiting_secs = (foodNo + 1) * 3
            sleep(waiting_secs)
            order_manager.complete_order(order['task_id'])
        except ValueError:
            print(f"Invalid perfume value: {perfume_enum}")
    sleep(3)
