#!/usr/bin/env python3
"""
Content Factory - 批量内容生成器
支持：小红书笔记、抖音脚本、知乎问答、微博文案
"""

import json
import random
from datetime import datetime
from pathlib import Path

TOPICS = {
    "美妆护肤": {
        "keywords": [
            "敏感肌",
            "平价",
            "保湿",
            "美白",
            "抗老",
            "痘痘",
            "毛孔",
            "黄黑皮",
            "早C晚A",
            "刷酸",
        ],
        "pain_points": [
            "脸干",
            "长痘",
            "毛孔粗",
            "肤色暗沉",
            "黑头",
            "出油",
            "过敏",
            "细纹",
        ],
        "emotions": ["崩溃", "哭了", "终于", "感动", "惊喜", "后悔", "激动", "破防"],
    },
    "母婴育儿": {
        "keywords": [
            "辅食",
            "早教",
            "睡整觉",
            "DHA",
            "纸尿裤",
            "奶粉",
            "宝宝湿疹",
            "疫苗",
        ],
        "pain_points": ["哭闹", "不睡觉", "不吃奶", "发烧", "咳嗽", "湿疹", "红屁股"],
        "emotions": ["焦虑", "崩溃", "心疼", "终于轻松", "感动", "后悔"],
    },
    "家居生活": {
        "keywords": ["收纳", "清洁", "除醛", "出租屋", "改造", "收纳神器", "清洁剂"],
        "pain_points": ["太乱", "没时间", "不会整理", "味道大", "甲醛", "打扫累"],
        "emotions": ["舒服", "治愈", "解压", "满足", "骄傲", "惊艳"],
    },
    "职场成长": {
        "keywords": ["面试", "简历", "升职", "加薪", "职场人际", "副业", "搞钱"],
        "pain_points": ["被裁", "工资低", "不会说话", "没方向", "迷茫", "加班"],
        "emotions": ["焦虑", "干货", "终于", "血泪教训", "避坑", "分享"],
    },
}


def generate_xiaohongshu(topic, count=10):
    """生成小红书笔记文案"""
    topic_data = TOPICS.get(topic, TOPICS["美妆护肤"])
    results = []

    templates = [
        "救命！{emotion}！{keyword}终于有救了！\n\n求你们快去试！\n\n# {topic} #干货分享",
        "{pain_point}的姐妹集合！\n\n我是怎么搞定{kw}的...\n\n方法在评论区👇\n\n# {topic} #必看",
        "后悔没早知道！{kw}这样做才对\n\n花了我3个月总结的经验\n\n# {topic} #收藏",
        "哭了！{emotion}！{kw}也太简单了吧\n\n以前的白做了\n\n# {topic} #教程",
        "{pain_point}十年总结！这些雷区千万别踩\n\n第3个90%的人都错了\n\n# {topic} #避坑",
        "花了3000块买来的教训！\n\n{kw}到底怎么选？\n\n# {topic} #测评#红黑榜",
        "答应我！有{kw}一定要试试这个！\n\n我不允许你不知道\n\n# {topic} #好物推荐",
        "从{pain_point}到完美，我做对了这3件事\n\n# {topic} #经验分享#成长",
    ]

    for i in range(count):
        template = random.choice(templates)
        content = template.format(
            emotion=random.choice(topic_data["emotions"]),
            keyword=random.choice(topic_data["keywords"]),
            kw=random.choice(topic_data["keywords"]),
            pain_point=random.choice(topic_data["pain_points"]),
            topic=topic,
        )
        results.append(
            {
                "type": "xiaohongshu",
                "topic": topic,
                "content": content,
                "hashtags": [f"#{topic}", "#干货分享", "#必看"],
            }
        )

    return results


def generate_douyin_script(topic, count=10):
    """生成抖音短视频脚本"""
    topic_data = TOPICS.get(topic, TOPICS["美妆护肤"])
    results = []

    for i in range(count):
        hook = random.choice(
            [
                "90%的人都不知道！",
                "这个秘密，一般人我不告诉他",
                "女生必看！",
                "答应我，一定要看完！",
                "这个技巧，我后悔知道太晚",
            ]
        )

        script = f"""【标题】{hook}关于{random.choice(topic_data["keywords"])}的秘密

【开场】3秒
关注我，带你了解更多{random.choice(topic_data["keywords"])}干货

【正文】45秒
很多人不知道，{random.choice(topic_data["pain_points"])}的时候...
其实只要这样做就可以...

{"".join([f"第一点，{random.choice(topic_data['keywords'])}... " for _ in range(2)])}

【结尾】
觉得有用的话，点个赞再走
关注我，下期更精彩

#{topic} #干货 #知识分享"""

        results.append(
            {
                "type": "douyin",
                "topic": topic,
                "script": script,
                "duration": "60秒",
                "hook": hook,
            }
        )

    return results


def generate_zhihu_answer(topic, count=5):
    """生成知乎问答"""
    topic_data = TOPICS.get(topic, TOPICS["美妆护肤"])
    results = []

    questions = [
        f"如何{random.choice(topic_data['keywords'])}？",
        f"{random.choice(topic_data['keywords'])}有什么推荐？",
        f"怎么样才能{random.choice(topic_data['keywords'])}？",
    ]

    for i, q in enumerate(questions[:count]):
        answer = f"""作为一个{random.choice(topic_data["keywords"])}的老手，我来分享下我的经验：

**1、先了解自己的{random.choice(topic_data["pain_points"])}**

很多人不知道，{random.choice(topic_data["keywords"])}之前，先要搞明白自己的问题在哪。

**2、选择对的产品**

我用过几十款，踩过的坑：
- 某牌：{random.choice(topic_data["keywords"])}一般般
- 某牌：真的好用！
- 某牌：{random.choice(topic_data["pain_points"])}别买

**3、坚持才是王道**

{"".join([f"{i + 1}. {random.choice(topic_data['keywords'])}需要坚持 " for i in range(3)])}

以上是我的真实经验，有问题评论区见！

# {topic} #经验分享"""

        results.append(
            {"type": "zhihu", "question": q, "answer": answer, "topic": topic}
        )

    return results


def generate_all(topic, xiaohongshu_count=20, douyin_count=10, zhihu_count=5):
    """生成所有类型的内容"""
    return {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "xiaohongshu": generate_xiaohongshu(topic, xiaohongshu_count),
        "douyin": generate_douyin_script(topic, douyin_count),
        "zhihu": generate_zhihu_answer(topic, zhihu_count),
        "total": xiaohongshu_count + douyin_count + zhihu_count,
    }


def save_results(results, topic):
    """保存结果"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    filename = f"output/{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return filename


def main():
    topics = list(TOPICS.keys())

    for topic in topics:
        print(f"\n{'=' * 50}")
        print(f"正在生成 {topic} 相关内容...")

        results = generate_all(
            topic, xiaohongshu_count=20, douyin_count=10, zhihu_count=5
        )

        filename = save_results(results, topic)
        print(f"✅ 已生成 {results['total']} 条内容")
        print(f"📁 保存至: {filename}")

        print(f"\n【小红书示例】")
        if results["xiaohongshu"]:
            print(results["xiaohongshu"][0]["content"][:200] + "...")

        print(f"\n【抖音脚本示例】")
        if results["douyin"]:
            print(results["douyin"][0]["script"][:200] + "...")


if __name__ == "__main__":
    main()
