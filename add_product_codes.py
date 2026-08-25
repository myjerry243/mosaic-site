# -*- coding: utf-8 -*-
"""马赛克网站: 产品图片标注原厂编号。
有编号 → 图片左上角金色徽标 + h4 标题下 "No. XXXX"
无编号 → 图片左上角灰色 "Effect" 徽标 + h4 下 "Effect Image"
先备份 HTML 到 backup_html/ 再修改。"""
import json, os, re, shutil, glob

BASE = r'G:\mosaic-site'
MAP = json.load(open(os.path.join(BASE, 'code_final_map.json'), encoding='utf-8'))

# 产品页（含 product-card 的）
PAGES = ['glass-mosaics.html', 'ceramic-mosaics.html', 'crystal-mosaics.html',
         'marble-mosaics.html', 'handcut-murals.html', 'pool-patterns.html']

BK = os.path.join(BASE, 'backup_html')
os.makedirs(BK, exist_ok=True)

# 备份
for p in PAGES:
    src = os.path.join(BASE, p)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(BK, p))
print("HTML 已备份到 backup_html/")

def process_card(card_html):
    """给单个 product-card 块加编号标注。返回修改后的块。"""
    m = re.search(r'<img src="([^"]+)"', card_html)
    if not m:
        return card_html
    src = m.group(1)
    # 归一化路径: 'images/...' 开头
    if not src.startswith('images/'):
        return card_html
    code = MAP.get(src, '')
    has_code = bool(code and code.strip())
    label = code.strip() if has_code else 'Effect'

    # 1. p-thumb 内 img 后加徽标（在 </div> 前、zoom span 后）
    badge = f'<span class="code-badge{"" if has_code else " effect"}">{label}</span>'
    if 'code-badge' not in card_html:
        # 插到 <img ...> 之后（zoom 之前）
        card_html = re.sub(r'(<img[^>]*>)', r'\1' + badge, card_html, count=1)

    # 2. h4 标题后加 p-code（若无）
    if '.p-code' not in card_html:
        code_span = (f'<span class="p-code">No. {label}</span>' if has_code
                     else '<span class="p-code effect">Effect Image</span>')
        # 在 <h4>...</h4> 内追加
        card_html = re.sub(r'(<h4>[^<]*)</h4>', r'\1' + code_span + r'</h4>', card_html, count=1)
    return card_html

stats = {'cards': 0, 'with_code': 0, 'effect': 0, 'skip': 0}
for p in PAGES:
    path = os.path.join(BASE, p)
    if not os.path.exists(path):
        print(f"MISS {p}")
        continue
    html = open(path, encoding='utf-8').read()
    # 按 product-card 块处理
    def repl(m):
        stats['cards'] += 1
        return process_card(m.group(0))
    new_html, n = re.subn(r'<div class="product-card".*?</div>\s*</div>', repl, html, flags=re.S)
    # 统计（在 repl 里已累计 cards；with_code/effect 需从结果里数）
    new_html = new_html
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    n_code = new_html.count('code-badge">')
    n_eff = new_html.count('code-badge effect')
    print(f"{p}: 卡片块={n} 有编号徽标={n_code} 效果图徽标={n_eff}")
    stats['with_code'] += n_code
    stats['effect'] += n_eff

print(f"\n总计: 卡片={stats['cards']} 编号={stats['with_code']} 效果图={stats['effect']}")
