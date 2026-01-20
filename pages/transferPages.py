import datetime
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from mwclient import Site
from img.img import transferImg

# --- 常量定义 ---
CROSS_SITE_LINK_REGEX = r'\[\[(en|ru|pt-br):[^\]]*\]\]'
DEV_NAMESPACE_PREFIX = "Dev:"
MODULE_NAMESPACE_PREFIX = "Module:Dev/"
IGNORED_PAGES = ["教程", "MediaWiki:Common.css"]
IMAGE_NAMESPACE_ID = 6


# 线程锁，保证控制台输出不乱序
print_lock = threading.Lock()

def safe_print(message):
    with print_lock:
        print(message)


# --- 工具函数 ---
def clean_page_text(page_text: str) -> str:
    """清理页面文本中的跨站链接"""
    return re.sub(CROSS_SITE_LINK_REGEX, "", page_text)

def convert_dev_namespace(page_text: str) -> str:
    """将 Dev: 命名空间转换为 Module:Dev/"""
    return page_text.replace(DEV_NAMESPACE_PREFIX, MODULE_NAMESPACE_PREFIX)

def process_image(old_site: Site, new_site: Site, title: str):
    """处理图片页面的传输"""
    if "File:" in title:
        try:
            transferImg(oldSite=old_site, newSite=new_site, fileName=title)
            return True
        except Exception as e:
            safe_print(f"图片 {title} 传输失败: {e}")
    return False



# --- 核心更新逻辑 ---
def update_single_page(old_site: Site, new_site: Site, title: str, user: str):
    try:
        # 1. 抓取旧站内容
        old_page = old_site.pages[title]
        raw_text = old_page.text()
        
        # 2. 处理文本
        processed_text = convert_dev_namespace(clean_page_text(raw_text))
        
        # 3. 抓取新站内容并比对
        new_page = new_site.pages[title]
        if processed_text != new_page.text():
            new_page.edit(
                text=processed_text,
                summary=f'原站点 {title} 由 {user} 更改, 自动同步 (Multi-threaded)'
            )
            safe_print(f"已更新: {title}")
        else:
            safe_print(f"无变化: {title}")
    except Exception as e:
        safe_print(f"处理页面 {title} 时出错: {e}")

# --- 主调用函数 ---
def update_pages(old_site: Site, new_site: Site, max_workers=5):
    """增量同步：多线程版"""
    now = datetime.datetime.now()
    three_hours_ago = now - datetime.timedelta(hours=3)
    end_time = int(three_hours_ago.timestamp())
    
    safe_print(f"开始多线程同步，时间窗口: {three_hours_ago} 至今")

    changes_list_old = old_site.get(
        action="query",
        list="recentchanges",
        rcstart="now",
        rcend=end_time,
        rcdir="older",
        rcprop="user|title"
    )
    pages = changes_list_old["query"]["recentchanges"]
    
    processed_titles = set()
    tasks = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in pages:
            title = page["title"]
            if title in IGNORED_PAGES or title in processed_titles:
                continue
            
            # 图像特殊处理
            if "File:" in title:
                process_image(old_site, new_site, title)
                processed_titles.add(title)
                continue

            # 提交线程任务
            tasks.append(executor.submit(update_single_page, old_site, new_site, title, page["user"]))
            processed_titles.add(title)

        # 等待结果
        for future in as_completed(tasks):
            future.result()
    
    safe_print("增量同步完成")

def transfer_all_pages(old_site: Site, new_site: Site, max_workers=10):
    """全量同步：多线程版"""
    old_page_list = {page.name for page in old_site.allpages(generator=True)}
    new_page_list = {page.name for page in new_site.allpages(generator=True)}
    pages_to_transfer = sorted(list(old_page_list - new_page_list))

    if not pages_to_transfer:
        safe_print("没有需要全量转移的页面")
        return

    safe_print(f"发现 {len(pages_to_transfer)} 个缺失页面，准备转移...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(update_single_page, old_site, new_site, name, "Charles手动触发"): name for name in pages_to_transfer}
        for future in as_completed(futures):
            future.result()

    safe_print("全量转移完成")
