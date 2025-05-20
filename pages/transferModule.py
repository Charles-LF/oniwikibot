from mwclient import Site

# 全局常量定义
MODULE_NAMESPACE_ID = 828
TARGET_MODULE_PREFIXES = ['Data', 'I18n']


def parse_module_title(page_name: str, namespace_prefix: str) -> str:
    """从完整页面名称中解析出模块标题。"""
    if page_name.startswith(namespace_prefix + ':'):
        return page_name[len(namespace_prefix) + 1:]
    return ''


def fetch_modules_to_process(site: Site, module_prefixes: list[str]) -> list[str]:
    """根据给定站点和前缀列表获取需要处理的模块。"""
    modules_to_process = []
    module_namespace_prefix = site.namespaces[MODULE_NAMESPACE_ID]
    for page in site.allpages(namespace=MODULE_NAMESPACE_ID):
        module_title = parse_module_title(page.name, module_namespace_prefix)
        if module_title and any(module_title.startswith(prefix) for prefix in module_prefixes):
            if module_title not in modules_to_process:
                modules_to_process.append(module_title)
    return modules_to_process


def sync_module(module_name: str, old_site: Site, new_site: Site) -> None:
    """同步单个模块从旧站点到新站点。"""
    full_module_name = f"Module:{module_name}"
    new_text = new_site.pages[full_module_name].text()
    old_text = old_site.pages[full_module_name].text()
    if old_text != new_text:
        edit_response = new_site.pages[full_module_name].edit(text=old_text, summary="原站模块同步")
        print(f"模块 {module_name} 同步完成: {edit_response}")


def trans_module(old_site: Site, new_site: Site) -> None:
    """
    将指定模块从旧站点转移到新站点。
    """
    modules = fetch_modules_to_process(old_site, TARGET_MODULE_PREFIXES)
    for module in modules:
        sync_module(module, old_site, new_site)
