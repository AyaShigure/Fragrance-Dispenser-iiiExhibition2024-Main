import os
import json
from pathlib import Path
from datetime import datetime
import time
from typing import Optional, List, Dict, Any
from ..models.Perfume import Perfume, Food
from ..models.PrintStatus import PrintStatus

class OrderManager:
    def __init__(self, order_file: str = "order.json", status_file: str = "status.json"):
        printer_dir = self.init_printer_directory()
        self.order_file = os.path.join(printer_dir, order_file)
        self.status_file = os.path.join(printer_dir, status_file)
        
    def init_printer_directory(self):
        # 获取用户主目录
        user_home = str(Path.home())
        printer_dir = os.path.join(user_home, "Perfume_Printer")

        # 创建 .Perfume_Printer 目录（如果不存在）
        if not os.path.exists(printer_dir):
            os.makedirs(printer_dir)

        # 只在文件不存在时创建新文件
        order_file = os.path.join(printer_dir, "order.json")
        status_file = os.path.join(printer_dir, "status.json")
        
        for file_path in [order_file, status_file]:
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)

        return printer_dir

    def _read_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _write_json_file(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_latest_order(self) -> Optional[Dict[str, Any]]:
        orders = self._read_json_file(self.order_file)
        if not orders:
            return None
        # 按时间戳排序，返回最新的订单
        return max(orders, key=lambda x: x['task_id'])

    def _is_any_order_printing(self) -> bool:
        status_list = self._read_json_file(self.status_file)
        return any(status['status'] == PrintStatus.PRINTING for status in status_list)

    def _add_status_record(self, task_id: int, status: PrintStatus) -> None:
        status_list = self._read_json_file(self.status_file)
        status_record = {
            "task_id": task_id,
            "status": status,
            "task_start": time.time()
        }
        status_list.append(status_record)
        self._write_json_file(self.status_file, status_list)

    def process_next_order(self) -> Optional[Dict[str, Any]]:
        # 如果有正在处理的订单，返回None
        if self._is_any_order_printing():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] There is an order being printed.")
            return None

        # 获取最新订单
        latest_order = self._get_latest_order()
        if not latest_order:
            return None

        # 检查订单是否已经在状态列表中
        status_list = self._read_json_file(self.status_file)
        if any(status['task_id'] == latest_order['task_id'] for status in status_list):
            return None

        # 验证订单中的perfume和food是否有效
        try:
            Perfume(latest_order['perfume'])
            Food(latest_order['food'])
        except ValueError:
            return None

        # 添加新的状态记录
        self._add_status_record(latest_order['task_id'], PrintStatus.PRINTING)
        
        return latest_order

    def complete_order(self, task_id: int) -> None:
        status_list = self._read_json_file(self.status_file)
        for status in status_list:
            if status['task_id'] == task_id and status['status'] == PrintStatus.PRINTING:
                status['status'] = PrintStatus.COMPLETED
                status['task_end'] = time.time()  # 添加任务完成时间戳
                break
        self._write_json_file(self.status_file, status_list) 