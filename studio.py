#!/usr/bin/env python3
"""
AI Content Studio - 自动化内容代运营系统
"""

import os
import json
import time
import asyncio
import hashlib
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

ORDERS_FILE = "orders.json"
CONFIG_FILE = "config.json"
OUTPUT_DIR = "output"


class ContentStudio:
    def __init__(self):
        self.orders = self.load_orders()
        self.config = self.load_config()

    def load_orders(self):
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"orders": [], "counter": 0}

    def save_orders(self):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=2)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "price": 99,
            "notification_url": os.getenv("NOTIFICATION_URL", ""),
            "admin_wx": "",
        }

    def create_order_id(self):
        self.orders["counter"] += 1
        order_id = f"ORD{self.orders['counter']:06d}"
        self.save_orders()
        return order_id

    def generate_content(self, topic, platform, count):
        """根据需求生成内容"""

        templates = {
            "小红书": [
                "救命！{emotion}！{keyword}终于有救了！\n\n求你们快去试！\n\n# {topic} #干货分享",
                "{pain}的姐妹集合！\n\n我是怎么搞定{kw}的...\n\n方法在评论区👇\n\n# {topic} #必看",
                "后悔没早知道！{kw}这样做才对\n\n花了我3个月总结的经验\n\n# {topic} #收藏",
                "哭了！{emotion}！{kw}也太简单了吧\n\n以前的白做了\n\n# {topic} #教程",
                "{pain}十年总结！这些雷区千万别踩\n\n第3个90%的人都错了\n\n# {topic} #避坑",
            ],
            "抖音": [
                "【标题】{emotion}！关于{kw}的秘密\n\n【开场】关注我，带你了解更多{kw}干货\n\n【正文】很多人不知道，{pain}的时候...其实只要这样做就可以...\n\n【结尾】觉得有用点个赞，关注我下期更精彩\n\n#{topic} #干货",
            ],
            "知乎": [
                "作为一个{kw}的老手，我来分享下我的经验：\n\n**1、先了解自己的{pain}**\n\n**2、选择对的方法**\n\n**3、坚持才是王道**\n\n以上是我的真实经验，有问题评论区见！\n\n#{topic} #经验分享",
            ],
            "微博": [
                "{emotion}！{kw}终于有救了！\n\n花了我3个月总结的经验，求你们快去试！\n\n# {topic} #",
            ],
        }

        keywords = [
            "平价",
            "敏感肌",
            "保湿",
            "美白",
            "抗老",
            "痘痘",
            "毛孔",
            "黄黑皮",
            "早C晚A",
            "刷酸",
        ]
        pain_points = [
            "脸干",
            "长痘",
            "毛孔粗",
            "肤色暗沉",
            "黑头",
            "出油",
            "过敏",
            "细纹",
        ]
        emotions = ["崩溃", "哭了", "终于", "感动", "惊喜", "后悔", "激动", "破防"]

        contents = []
        platform_templates = templates.get(platform, templates["小红书"])

        for i in range(count):
            template = random.choice(platform_templates)
            content = template.format(
                emotion=random.choice(emotions),
                keyword=random.choice(keywords),
                kw=random.choice(keywords),
                pain=random.choice(pain_points),
                topic=topic,
            )
            contents.append(
                {
                    "id": i + 1,
                    "content": content,
                    "created_at": datetime.now().isoformat(),
                }
            )

        return contents

    def create_order(self, topic, platform, count, customer_info):
        """创建新订单"""
        order_id = self.create_order_id()

        order = {
            "order_id": order_id,
            "topic": topic,
            "platform": platform,
            "count": count,
            "customer_info": customer_info,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "content": None,
            "completed_at": None,
        }

        self.orders["orders"].append(order)
        self.save_orders()

        return order

    def process_order(self, order_id):
        """处理订单：生成内容"""
        order = None
        for o in self.orders["orders"]:
            if o["order_id"] == order_id:
                order = o
                break

        if not order:
            return {"error": "Order not found"}

        if order["status"] == "completed":
            return {"error": "Order already completed"}

        contents = self.generate_content(
            order["topic"], order["platform"], order["count"]
        )

        order["content"] = contents
        order["status"] = "completed"
        order["completed_at"] = datetime.now().isoformat()

        self.save_orders()

        self.notify_admin(order)

        return {
            "status": "success",
            "order_id": order_id,
            "content_count": len(contents),
        }

    def notify_admin(self, order):
        """通知管理员"""
        if self.config.get("notification_url"):
            try:
                import requests

                data = {
                    "text": f"🎉 新订单完成！\n\n订单号: {order['order_id']}\n主题: {order['topic']}\n平台: {order['platform']}\n数量: {order['count']}条\n客户: {order.get('customer_info', 'N/A')}"
                }
                requests.post(self.config["notification_url"], json=data, timeout=10)
            except:
                pass

    def get_pending_orders(self):
        """获取待处理订单"""
        return [o for o in self.orders["orders"] if o["status"] == "pending"]

    def get_completed_orders(self):
        """获取已完成订单"""
        return [o for o in self.orders["orders"] if o["status"] == "completed"]

    def auto_process(self):
        """自动处理所有待处理订单"""
        pending = self.get_pending_orders()
        results = []

        for order in pending:
            result = self.process_order(order["order_id"])
            results.append(result)

        return results

    def get_order_content(self, order_id):
        """获取订单内容"""
        for o in self.orders["orders"]:
            if o["order_id"] == order_id:
                return o.get("content", [])
        return []

    def export_content(self, order_id, format="text"):
        """导出内容"""
        contents = self.get_order_content(order_id)
        if not contents:
            return ""

        if format == "json":
            return json.dumps(contents, ensure_ascii=False, indent=2)

        text = f"=== 订单 {order_id} 内容 ===\n\n"
        for c in contents:
            text += f"--- 第{c['id']}条 ---\n"
            text += c["content"] + "\n\n"

        return text


def main():
    import sys

    studio = ContentStudio()

    if len(sys.argv) < 2:
        print("""
=== AI Content Studio ===

用法:
  python studio.py create <主题> <平台> <数量> [客户信息]
  python studio.py process <订单号>
  python studio.py auto
  python studio.py list
  python studio.py export <订单号>
  python studio.py stats

示例:
  python studio.py create "美妆护肤" "小红书" 10 "微信ID"
  python studio.py process ORD000001
  python studio.py auto
  python studio.py list
  python studio.py export ORD000001
""")
        return

    command = sys.argv[1]

    if command == "create":
        topic = sys.argv[2] if len(sys.argv) > 2 else "通用"
        platform = sys.argv[3] if len(sys.argv) > 3 else "小红书"
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        customer_info = sys.argv[5] if len(sys.argv) > 5 else ""

        order = studio.create_order(topic, platform, count, customer_info)
        print(f"✅ 订单已创建: {order['order_id']}")
        print(f"   主题: {topic}")
        print(f"   平台: {platform}")
        print(f"   数量: {count}条")

    elif command == "process":
        order_id = sys.argv[2] if len(sys.argv) > 2 else ""
        result = studio.process_order(order_id)
        if result.get("error"):
            print(f"❌ 错误: {result['error']}")
        else:
            print(f"✅ 订单已完成: {order_id}")
            print(f"   生成内容: {result['content_count']}条")

    elif command == "auto":
        results = studio.auto_process()
        print(f"✅ 自动处理完成，共 {len(results)} 个订单")

    elif command == "list":
        print("\n=== 待处理订单 ===")
        pending = studio.get_pending_orders()
        for o in pending:
            print(f"{o['order_id']} | {o['topic']} | {o['platform']} | {o['count']}条")

        print("\n=== 已完成订单 ===")
        completed = studio.get_completed_orders()
        for o in completed:
            print(
                f"{o['order_id']} | {o['topic']} | {o['platform']} | {o['count']}条 | {o['completed_at'][:19]}"
            )

    elif command == "export":
        order_id = sys.argv[2] if len(sys.argv) > 2 else ""
        content = studio.export_content(order_id)
        print(content)

    elif command == "stats":
        all_orders = studio.orders["orders"]
        completed = len([o for o in all_orders if o["status"] == "completed"])
        pending = len([o for o in all_orders if o["status"] == "pending"])

        print(f"""
=== 运营统计 ===

总订单数: {len(all_orders)}
已完成: {completed}
待处理: {pending}

收入预估: ¥{completed * studio.config["price"]}
""")


if __name__ == "__main__":
    main()
