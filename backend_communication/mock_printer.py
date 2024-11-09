import json
import time
import os

def mock_printer(printer_dir: str):
    # 确保 status.json 存在
    status_file = os.path.join(printer_dir, 'status.json')
    if not os.path.exists(status_file):
        with open(status_file, 'w') as f:
            json.dump([], f)

    while True:
        try:
            # 处理新订单
            process_new_order(printer_dir)
            
            # 读取状态文件
            status_file = os.path.join(printer_dir, 'status.json')
            with open(status_file, 'r') as f:
                status_list = json.load(f)
            
            # 更新超过5秒的任务状态
            current_time = time.time()
            for task in status_list:
                if task['status'] == 'PRINTING' and current_time - task['task_start'] > 5:
                    task['status'] = 'COMPLETED'
            
            # 保存状态
            with open(status_file, 'w') as f:
                json.dump(status_list, f, indent=2)
                
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    print("Mock printer started...")
    # 需要传入printer_dir参数
    printer_dir = "path/to/your/printer/dir"  
    mock_printer(printer_dir)