# -*- coding: utf-8 -*-
"""全量 OCR 备份图，提取每张产品图的"原来的产品编号"。
备份图 = 清理前带水印原图，水印即原厂型号编号。
增量落盘 (done 清单 + jsonl)，断点续扫，防 SIGTERM。"""
import easyocr, cv2, numpy as np, os, sys, json, re, glob

BASE = r'G:\mosaic-site'
BK = os.path.join(BASE, 'images_backup_wm', 'images')
OUT = os.path.join(BASE, 'product_codes_ocr.jsonl')
DONE = os.path.join(BASE, 'product_codes_ocr_done.txt')

# 编号模式：字母+数字组合 (YC01/FC2/LSD1908/1902/A-12 等)
CODE_RE = re.compile(r'^[A-Za-z]{0,4}[-_]?\d{2,5}$')

def read_img(path):
    return cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)

def main():
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False, verbose=False)
    # 收集备份图
    files = []
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        files.extend(glob.glob(os.path.join(BK, '**', ext), recursive=True))
    files = sorted(files)
    print(f"备份图总数: {len(files)}", flush=True)

    done = set()
    if os.path.exists(DONE):
        done = set(l.strip() for l in open(DONE, encoding='utf-8') if l.strip())
    print(f"已完成: {len(done)}，续扫", flush=True)

    out_f = open(OUT, 'a', encoding='utf-8')
    done_f = open(DONE, 'a', encoding='utf-8')
    stats = {'done': len(done), 'with_code': 0, 'no_code': 0, 'fail': 0}

    for i, path in enumerate(files):
        rel = os.path.relpath(path, BK).replace('\\', '/')
        if rel in done:
            continue
        img = read_img(path)
        if img is None:
            stats['fail'] += 1
            done_f.write(rel + '\n'); done_f.flush()
            done.add(rel)
            continue
        try:
            res = reader.readtext(img)
            texts = [(round(t[2], 2), t[1].strip()) for t in res]
            # 提取高置信度编号 (conf>=0.3 且匹配编号模式) — 排除中文/句子
            codes = []
            for conf, txt in texts:
                if conf < 0.3:
                    continue
                # 去空白
                t = re.sub(r'\s+', '', txt)
                if CODE_RE.match(t):
                    codes.append({'code': t, 'conf': conf})
            # 按置信度排序去重
            seen = set()
            uniq = []
            for c in sorted(codes, key=lambda x: -x['conf']):
                if c['code'] not in seen:
                    seen.add(c['code'])
                    uniq.append(c)
            record = {'file': rel, 'codes': uniq[:4], 'all_texts': texts[:8]}
            out_f.write(json.dumps(record, ensure_ascii=False) + '\n'); out_f.flush()
            if uniq:
                stats['with_code'] += 1
            else:
                stats['no_code'] += 1
        except Exception as e:
            record = {'file': rel, 'error': str(e)[:100]}
            out_f.write(json.dumps(record, ensure_ascii=False) + '\n'); out_f.flush()
            stats['fail'] += 1
        done_f.write(rel + '\n'); done_f.flush()
        done.add(rel)
        stats['done'] += 1
        if (i + 1) % 20 == 0:
            print(f"进度 {i+1}/{len(files)} | {stats}", flush=True)

    out_f.close(); done_f.close()
    print(f"完成: {stats}", flush=True)

if __name__ == '__main__':
    main()
