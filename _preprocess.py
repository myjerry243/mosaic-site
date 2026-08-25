# -*- coding: utf-8 -*-
"""Mosaic site image preprocessing: PDF page renders + product photo resize/organize."""
import os, shutil, sys
import fitz
from PIL import Image

SRC = 'G:/mosaicwebsite/网页图片'
OUT = 'G:/mosaic-site'
CARD_W = 700      # card thumbnail max width
FULL_W = 1600     # lightbox/detail max width
PDF_PAGES = 14    # max pages rendered per PDF series

def render_pdf(pdf_path, outdir, prefix, max_pages=PDF_PAGES, width=1100):
    """Render first N pages of a PDF to JPEG."""
    doc = fitz.open(pdf_path)
    n = min(doc.page_count, max_pages)
    os.makedirs(outdir, exist_ok=True)
    saved = []
    for i in range(n):
        pg = doc[i]
        zoom = width / pg.rect.width
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        fn = f'{prefix}_{i+1:02d}.jpg'
        pix.save(os.path.join(outdir, fn), jpg_quality=82)
        saved.append(fn)
    doc.close()
    return saved

def process_image(src, outdir, prefix, card_w=CARD_W, full_w=FULL_W):
    """Copy+resize a product photo into card + hi versions."""
    im = Image.open(src)
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        im = bg
    elif im.mode != 'RGB':
        im = im.convert('RGB')
    w, h = im.size
    os.makedirs(outdir, exist_ok=True)
    def scale(im, mw):
        if im.size[0] > mw:
            return im.resize((mw, int(im.size[1] * mw / im.size[0])), Image.LANCZOS)
        return im
    im2 = scale(im, card_w)
    im2.save(os.path.join(outdir, f'{prefix}.jpg'), 'JPEG', quality=82)
    im3 = scale(im, full_w)
    im3.save(os.path.join(outdir, f'{prefix}_hi.jpg'), 'JPEG', quality=88)
    return f'{prefix}.jpg', f'{prefix}_hi.jpg'

log = []
def L(msg):
    log.append(msg)
    print(msg)

# ---------- 1. Glass mosaics PDF series ----------
glass_map = [
    ('冰花系列.pdf',                 'glass_iceflower'),
    ('金线系列.pdf',                 'glass_goldline'),
    ('无沙+七彩系列.pdf',             'glass_nosand_rainbow'),
    ('热熔无沙系列.pdf',              'glass_hotmelt_nosand'),
    ('热熔有沙系列.pdf',              'glass_hotmelt_sand'),
    ('幻彩系列.pdf',                 'glass_shimmer'),
    ('纯云彩系列.pdf',               'glass_cloud'),
    ('10-15冰瓷玉系列 2023.pdf',     'glass_icejade'),
    ('菱形PDF.pdf',                  'glass_diamond'),
    ('hexegon mosaic PDF  2023.pdf', 'glass_hexagon'),
]
glass_dir = os.path.join(SRC, '玻璃马赛克glass mosaics')
for fname, prefix in glass_map:
    p = os.path.join(glass_dir, fname)
    if os.path.exists(p):
        n = render_pdf(p, os.path.join(OUT, 'images/glass'), prefix)
        L(f'glass {prefix}: {len(n)} pages')

# ---------- 2. Marble mosaics PDFs ----------
marble_dir = os.path.join(SRC, '大理石马赛克 marble mosaics')
render_pdf(os.path.join(marble_dir, '地花系列flooring Series.pdf'),
           os.path.join(OUT, 'images/marble-flooring'), 'marble_flooring')
L('marble flooring done')
render_pdf(os.path.join(marble_dir, '水刀系列waterjet series.pdf'),
           os.path.join(OUT, 'images/marble-waterjet'), 'marble_waterjet')
L('marble waterjet done')

# ---------- 3. Crystal pool PDFs ----------
cpool_dir = os.path.join(SRC, '水晶马赛克crystal mosaic/泳池马赛克 crystal pool mosaic')
render_pdf(os.path.join(cpool_dir, 'pool mosaic 1.pdf'),
           os.path.join(OUT, 'images/crystal-pool'), 'crystal_pool', max_pages=10)
render_pdf(os.path.join(cpool_dir, 'pool mosaic 2.pdf'),
           os.path.join(OUT, 'images/crystal-pool'), 'crystal_pool', max_pages=8)
L('crystal pool done')

# ---------- 4. Customized pool patterns PDF ----------
pool_dir = os.path.join(SRC, '泳池拼图customized pool patterns')
render_pdf(os.path.join(pool_dir, '2026 customized pool mosaic .pdf'),
           os.path.join(OUT, 'images/pool-patterns'), 'pool_2026', max_pages=16)
L('pool patterns done')

# ---------- 5. Ceramic PNGs ----------
cer_dir = os.path.join(SRC, '陶瓷马赛克ceramic mosaics')
files = sorted([f for f in os.listdir(cer_dir) if f.lower().endswith('.png')])
for i, f in enumerate(files, 1):
    process_image(os.path.join(cer_dir, f), os.path.join(OUT, 'images/ceramic'), f'ceramic_{i:02d}')
L(f'ceramic: {len(files)} images')

# ---------- 6. Crystal 4mm iridium PNGs ----------
c4_dir = os.path.join(SRC, '水晶马赛克crystal mosaic/4厘幻彩 4mm thick irridium series')
files = sorted([f for f in os.listdir(c4_dir) if f.lower().endswith('.png')])
for f in files:
    stem = os.path.splitext(f)[0]
    process_image(os.path.join(c4_dir, f), os.path.join(OUT, 'images/crystal-4mm'), f'c4_{stem}')
L(f'crystal 4mm: {len(files)} images')

# ---------- 7. Crystal 6mm iridium PNGs ----------
c6_dir = os.path.join(SRC, '水晶马赛克crystal mosaic/6厘幻彩6mm thick irridium series')
files = sorted([f for f in os.listdir(c6_dir) if f.lower().endswith('.png')])
for f in files:
    stem = os.path.splitext(f)[0]
    process_image(os.path.join(c6_dir, f), os.path.join(OUT, 'images/crystal-6mm'), f'c6_{stem}')
L(f'crystal 6mm: {len(files)} images')

# ---------- 8. Handcut murals ----------
hc_dir = os.path.join(SRC, '剪画handcut mosaic mural/handcut mosaic backsplashes')
files = sorted([f for f in os.listdir(hc_dir) if f.lower().endswith(('.png', '.jpg'))])
for i, f in enumerate(files, 1):
    process_image(os.path.join(hc_dir, f), os.path.join(OUT, 'images/handcut'), f'handcut_{i:02d}')
L(f'handcut: {len(files)} images')

# ---------- 9. Hero images (best picks) ----------
def pick_hero():
    hero_dir = os.path.join(OUT, 'images/hero')
    os.makedirs(hero_dir, exist_ok=True)
    # pool pattern cover page (page 11-12 usually has pool art patterns)
    doc = fitz.open(os.path.join(pool_dir, '2026 customized pool mosaic .pdf'))
    for idx in [10, 11]:
        pg = doc[idx]
        zoom = 1600 / pg.rect.width
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        pix.save(os.path.join(hero_dir, f'hero_pool_{idx+1}.jpg'), jpg_quality=85)
    doc.close()
    # glass cover (hexagon, has company logo on cover)
    doc = fitz.open(os.path.join(glass_dir, 'hexegon mosaic PDF  2023.pdf'))
    pg = doc[0]
    zoom = 1600 / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    pix.save(os.path.join(hero_dir, 'hero_hexagon_cover.jpg'), jpg_quality=85)
    doc.close()
    # crystal pool cover
    doc = fitz.open(os.path.join(cpool_dir, 'pool mosaic 1.pdf'))
    pg = doc[0]
    zoom = 1600 / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    pix.save(os.path.join(hero_dir, 'hero_crystal_pool.jpg'), jpg_quality=85)
    doc.close()
    L('hero images done')
pick_hero()

# ---------- 10. Copy videos + catalog PDFs to downloads ----------
vid_dir = os.path.join(OUT, 'videos')
os.makedirs(vid_dir, exist_ok=True)
src_mp4 = os.path.join(cer_dir, '8月21日.mp4')
if os.path.exists(src_mp4):
    shutil.copy2(src_mp4, os.path.join(vid_dir, 'ceramic-showroom.mp4'))
    L('video copied')

dl_dir = os.path.join(OUT, 'downloads')
os.makedirs(dl_dir, exist_ok=True)
dl_src = [
    (os.path.join(glass_dir, 'hexegon mosaic PDF  2023.pdf'), 'glass-hexagon-catalog.pdf'),
    (os.path.join(glass_dir, '10-15冰瓷玉系列 2023.pdf'), 'glass-ice-jade-catalog.pdf'),
    (os.path.join(glass_dir, '纯云彩系列.pdf'), 'glass-cloud-series-catalog.pdf'),
    (os.path.join(marble_dir, '水刀系列waterjet series.pdf'), 'marble-waterjet-catalog.pdf'),
    (os.path.join(marble_dir, '地花系列flooring Series.pdf'), 'marble-flooring-catalog.pdf'),
    (os.path.join(cpool_dir, 'pool mosaic 1.pdf'), 'crystal-pool-mosaic-1.pdf'),
    (os.path.join(cpool_dir, 'pool mosaic 2.pdf'), 'crystal-pool-mosaic-2.pdf'),
    (os.path.join(SRC, '水晶马赛克crystal mosaic/crystal mosaic catalogue(2).pdf'), 'crystal-mosaic-catalogue.pdf'),
    (os.path.join(pool_dir, '2026 customized pool mosaic .pdf'), 'customized-pool-mosaic-2026.pdf'),
]
for src, dst in dl_src:
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(dl_dir, dst))
L(f'downloads: {len(dl_src)} PDFs')

# ---------- summary ----------
total = 0
for root, dirs, files in os.walk(os.path.join(OUT, 'images')):
    total += len([f for f in files if f.endswith('.jpg')])
L(f'TOTAL images: {total}')
print('DONE')
