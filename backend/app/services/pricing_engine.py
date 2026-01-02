import json
import os
from typing import Dict, Any, List
from app.models.plan import PlanCode
from app.core.config import settings

class PricingEngine:
    def __init__(self):
        self.price_catalog = self._load_price_catalog()
    
    def _load_price_catalog(self) -> Dict[str, Any]:
        # Try multiple paths
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        catalog_path = os.path.join(base_dir, "app", "config", "price_catalog.json")
        if not os.path.exists(catalog_path):
            catalog_path = os.path.join(os.path.dirname(__file__), "..", "config", "price_catalog.json")
        if os.path.exists(catalog_path):
            with open(catalog_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default_catalog()
    
    def _default_catalog(self) -> Dict[str, Any]:
        return {
            "items": [
                {
                    "item_key": "robot_articulated_6dof",
                    "name_zhTW": "六軸關節式機器人",
                    "default_spec": "6軸，負載10kg，工作範圍1.5m",
                    "unit": "台",
                    "low": 800000,
                    "high": 1200000
                },
                {
                    "item_key": "robot_articulated_4dof",
                    "name_zhTW": "四軸關節式機器人",
                    "default_spec": "4軸，負載20kg，工作範圍1.2m",
                    "unit": "台",
                    "low": 600000,
                    "high": 900000
                },
                {
                    "item_key": "robot_gantry",
                    "name_zhTW": "龍門式機器人",
                    "default_spec": "XYZ三軸，負載50kg，行程2m x 1.5m",
                    "unit": "台",
                    "low": 1500000,
                    "high": 2200000
                },
                {
                    "item_key": "flip_station",
                    "name_zhTW": "翻轉站",
                    "default_spec": "氣動翻轉，負載30kg",
                    "unit": "站",
                    "low": 200000,
                    "high": 300000
                },
                {
                    "item_key": "vision_system",
                    "name_zhTW": "視覺系統",
                    "default_spec": "2D視覺，解析度1920x1080",
                    "unit": "套",
                    "low": 150000,
                    "high": 250000
                },
                {
                    "item_key": "eoat_gripper",
                    "name_zhTW": "夾爪",
                    "default_spec": "氣動夾爪，開合行程50mm",
                    "unit": "組",
                    "low": 50000,
                    "high": 80000
                },
                {
                    "item_key": "safety_fence",
                    "name_zhTW": "安全圍籬",
                    "default_spec": "標準型，高度2m",
                    "unit": "組",
                    "low": 100000,
                    "high": 150000
                },
                {
                    "item_key": "integration_engineering",
                    "name_zhTW": "整合工程",
                    "default_spec": "系統整合、程式開發、測試",
                    "unit": "項",
                    "low": 500000,
                    "high": 800000
                },
                {
                    "item_key": "installation_training",
                    "name_zhTW": "安裝與訓練",
                    "default_spec": "現場安裝、操作訓練",
                    "unit": "項",
                    "low": 200000,
                    "high": 300000
                }
            ],
            "modifiers": {
                "robot_count": {
                    "multiplier": 0.9
                },
                "vision_addon": {
                    "add": 150000
                },
                "safety_complexity": {
                    "small": 1.0,
                    "medium": 1.2,
                    "large": 1.5
                }
            }
        }
    
    def generate_plan_spec(self, plan_code: PlanCode, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate plan specification based on plan code and requirements"""
        if plan_code == PlanCode.P1:
            return {
                "name": "方案一：雙機器人 + 翻轉站",
                "assumptions": {
                    "robots": 2,
                    "robot_type": "articulated_6dof",
                    "flip_station": True,
                    "vision": False,
                    "scheduler": False
                }
            }
        elif plan_code == PlanCode.P2:
            return {
                "name": "方案二：單機器人 + 翻轉站 + 排程系統",
                "assumptions": {
                    "robots": 1,
                    "robot_type": "articulated_6dof",
                    "flip_station": True,
                    "vision": False,
                    "scheduler": True
                }
            }
        elif plan_code == PlanCode.P3:
            return {
                "name": "方案三：龍門式 + 研磨機器人 + 視覺系統",
                "assumptions": {
                    "robots": 1,
                    "robot_type": "gantry",
                    "flip_station": False,
                    "vision": True,
                    "scheduler": False
                }
            }
        return {"name": "", "assumptions": {}}
    
    def generate_quote_items(self, plan_code: PlanCode, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate quote items for a plan"""
        plan_spec = self.generate_plan_spec(plan_code, requirements)
        assumptions = plan_spec["assumptions"]
        items = []
        
        # Main equipment
        robot_count = assumptions.get("robots", 1)
        robot_type = assumptions.get("robot_type", "articulated_6dof")
        
        robot_item = self._get_catalog_item(f"robot_{robot_type}")
        if robot_item:
            for i in range(robot_count):
                items.append({
                    "category": "主要設備",
                    "item_name": robot_item["name_zhTW"],
                    "spec": robot_item["default_spec"],
                    "qty": 1.0,
                    "unit": robot_item["unit"],
                    "unit_price_low": robot_item["low"],
                    "unit_price_high": robot_item["high"],
                    "subtotal_low": robot_item["low"],
                    "subtotal_high": robot_item["high"]
                })
        
        # Flip station
        if assumptions.get("flip_station"):
            flip_item = self._get_catalog_item("flip_station")
            if flip_item:
                items.append({
                    "category": "工作站",
                    "item_name": flip_item["name_zhTW"],
                    "spec": flip_item["default_spec"],
                    "qty": 1.0,
                    "unit": flip_item["unit"],
                    "unit_price_low": flip_item["low"],
                    "unit_price_high": flip_item["high"],
                    "subtotal_low": flip_item["low"],
                    "subtotal_high": flip_item["high"]
                })
        
        # Vision system
        if assumptions.get("vision"):
            vision_item = self._get_catalog_item("vision_system")
            if vision_item:
                items.append({
                    "category": "主要設備",
                    "item_name": vision_item["name_zhTW"],
                    "spec": vision_item["default_spec"],
                    "qty": 1.0,
                    "unit": vision_item["unit"],
                    "unit_price_low": vision_item["low"],
                    "unit_price_high": vision_item["high"],
                    "subtotal_low": vision_item["low"],
                    "subtotal_high": vision_item["high"]
                })
        
        # EOAT
        eoat_item = self._get_catalog_item("eoat_gripper")
        if eoat_item:
            items.append({
                "category": "EOAT與治具",
                "item_name": eoat_item["name_zhTW"],
                "spec": eoat_item["default_spec"],
                "qty": robot_count,
                "unit": eoat_item["unit"],
                "unit_price_low": eoat_item["low"],
                "unit_price_high": eoat_item["high"],
                "subtotal_low": eoat_item["low"] * robot_count,
                "subtotal_high": eoat_item["high"] * robot_count
            })
        
        # Safety
        safety_item = self._get_catalog_item("safety_fence")
        if safety_item:
            items.append({
                "category": "安全設備",
                "item_name": safety_item["name_zhTW"],
                "spec": safety_item["default_spec"],
                "qty": 1.0,
                "unit": safety_item["unit"],
                "unit_price_low": safety_item["low"],
                "unit_price_high": safety_item["high"],
                "subtotal_low": safety_item["low"],
                "subtotal_high": safety_item["high"]
            })
        
        # Integration engineering
        integration_item = self._get_catalog_item("integration_engineering")
        if integration_item:
            items.append({
                "category": "整合工程",
                "item_name": integration_item["name_zhTW"],
                "spec": integration_item["default_spec"],
                "qty": 1.0,
                "unit": integration_item["unit"],
                "unit_price_low": integration_item["low"],
                "unit_price_high": integration_item["high"],
                "subtotal_low": integration_item["low"],
                "subtotal_high": integration_item["high"]
            })
        
        # Installation & training
        install_item = self._get_catalog_item("installation_training")
        if install_item:
            items.append({
                "category": "安裝與訓練",
                "item_name": install_item["name_zhTW"],
                "spec": install_item["default_spec"],
                "qty": 1.0,
                "unit": install_item["unit"],
                "unit_price_low": install_item["low"],
                "unit_price_high": install_item["high"],
                "subtotal_low": install_item["low"],
                "subtotal_high": install_item["high"]
            })
        
        return items
    
    def _get_catalog_item(self, item_key: str) -> Dict[str, Any]:
        for item in self.price_catalog.get("items", []):
            if item.get("item_key") == item_key:
                return item
        return None

