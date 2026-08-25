# -*- coding: utf-8 -*-
"""E-Tile Mosaic static site generator — Foshan mosaic factory export site."""
import os, re, glob, html
import fitz

OUT = 'G:/mosaic-site'
IMG = os.path.join(OUT, 'images')
TODAY = '2026-08-21'
DOMAIN = 'https://etile-mosaic.com'

SITE_NAME = 'E-Tile Mosaic'
COMPANY = 'Foshan E-Tile Building Material Co., Ltd.'
BRAND = 'FengFu Mosaic'

# ---------- idempotent fix: crystal pool PDFs had colliding prefixes ----------
def ensure_crystal_pool():
    d = os.path.join(IMG, 'crystal-pool')
    cur = sorted([f for f in os.listdir(d) if f.endswith('.jpg') and not f.endswith('_hi.jpg')])
    if len(cur) < 16:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
        src_dir = 'G:/mosaicwebsite/网页图片/水晶马赛克crystal mosaic/泳池马赛克 crystal pool mosaic'
        def render(pdf, prefix, maxp):
            doc = fitz.open(os.path.join(src_dir, pdf))
            n = min(doc.page_count, maxp)
            for i in range(n):
                pg = doc[i]
                zoom = 1100 / pg.rect.width
                pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
                pix.save(os.path.join(d, f'{prefix}_{i+1:02d}.jpg'), jpg_quality=82)
            doc.close()
        render('pool mosaic 1.pdf', 'crystal_pool_a', 10)
        render('pool mosaic 2.pdf', 'crystal_pool_b', 8)
ensure_crystal_pool()

# ---------- image inventory ----------
def imgs(subdir):
    d = os.path.join(IMG, subdir)
    files = sorted([f for f in os.listdir(d) if f.endswith('.jpg') and not f.endswith('_hi.jpg')])
    return files

def hi_name(fn):
    return fn[:-4] + '_hi.jpg'

# ---------- category meta ----------
CATS = [
    dict(slug='glass-mosaics', title='Glass Mosaics', en='GLASS MOSAICS',
         desc='Fused glass mosaic series — ice flower, gold line, hot-melt, hexagon, diamond, cloud and more. 10 series, 100+ designs.',
         img='images/hero/card_glass.jpg', count='10 Series'),
    dict(slug='ceramic-mosaics', title='Ceramic Mosaics', en='CERAMIC MOSAICS',
         desc='Glazed ceramic mosaic sheets in 44 styles — matt, glossy and textured surfaces for walls, floors and pools.',
         img='images/hero/card_ceramic.jpg', count='44 Styles'),
    dict(slug='crystal-mosaics', title='Crystal Mosaics', en='CRYSTAL MOSAICS',
         desc='Iridium crystal glass mosaics with rainbow shimmer — 4mm and 6mm thick sheets plus crystal pool mosaic ranges.',
         img='images/hero/card_crystal.jpg', count='72+ Designs'),
    dict(slug='marble-mosaics', title='Marble Mosaics', en='MARBLE MOSAICS',
         desc='Natural marble mosaic flooring medallions and waterjet-cut patterns for luxury lobbies, bathrooms and feature walls.',
         img='images/hero/card_marble.jpg', count='2 Series'),
    dict(slug='handcut-murals', title='Handcut Mosaic Murals', en='HANDCUT MURALS',
         desc='Handcrafted mosaic mural backsplashes — artisan cut and assembled by skilled craftsmen. Bespoke art for your space.',
         img='images/hero/card_handcut.jpg', count='16 Murals'),
    dict(slug='pool-patterns', title='Custom Pool Patterns', en='CUSTOM POOL PATTERNS',
         desc='14 years of swimming pool mosaic pattern design & fabrication. Custom designs from your image or our library.',
         img='images/hero/card_pool.jpg', count='14 Years'),
]

# ---------- glass series meta ----------
GLASS_SERIES = [
    ('glass_iceflower',   'Ice Flower Series',      '冰花系列',   'Frosted ice-flower texture glass mosaic with soft, luminous surface.'),

    ('glass_goldline',    'Gold Line Series',       '金线系列',   'Transparent glass mosaic accented with real gold-tone line details.'),
    ('glass_nosand_rainbow','No-Sand & Rainbow Series','无沙+七彩系列','Smooth no-sand glass tiles plus vibrant rainbow colour range.'),
    ('glass_hotmelt_nosand','Hot-Melt No-Sand Series','热熔无沙系列','Hot-melt fused glass, smooth glossy finish, no sand backing.'),
    ('glass_hotmelt_sand','Hot-Melt Sand Series',   '热熔有沙系列', 'Hot-melt fused glass with sand texture — anti-slip for wet areas.'),
    ('glass_shimmer',     'Shimmer Series',         '幻彩系列',   'Colour-shifting iridescent glass mosaic that shimmers in the light.'),
    ('glass_cloud',       'Pure Cloud Series',      '纯云彩系列', 'Soft cloud-effect translucent glass, 54-page colour library.'),
    ('glass_icejade',     'Ice Jade Series',        '10-15冰瓷玉系列','Ice-jade porcelain glass, 10–15mm mixed sizes, premium depth.'),
    ('glass_diamond',     'Diamond Series',         '菱形系列',   'Diamond-shaped glass mosaic tiles for dynamic geometric patterns.'),
    ('glass_hexagon',     'Hexagon Series',         '六角系列',   'Hexagonal glass mosaic, honeycomb patterns, 2023 collection.'),
]

# ---------- helpers ----------
def esc(s): return html.escape(str(s), quote=True)

def img_card(subdir, fn, title, cat):
    hi = fn[:-4] + '_hi.jpg'
    if not os.path.exists(os.path.join(IMG, subdir, hi)):
        hi = fn  # PDF-rendered cards have no _hi twin; card itself is 1100px
    return (f'<div class="product-card" data-title="{esc(title)}" data-cat="{esc(cat)}" data-hi="images/{subdir}/{hi}">'
            f'<div class="p-thumb"><img src="images/{subdir}/{fn}" alt="{esc(title)}" loading="lazy">'
            f'<span class="zoom">🔍 View</span></div>'
            f'<div class="p-body"><h4>{esc(title)}</h4><span>{esc(cat)}</span></div></div>')

def grid_of(subdir, files, cat, title_fn):
    return '<div class="grid">' + ''.join(img_card(subdir, f, title_fn(f), cat) for f in files) + '</div>'

def num_of(f):
    """Trailing number from filename stem (glass_iceflower_01.jpg -> 1)."""
    m = re.search(r'_(\d+)$', f[:-4])
    return int(m.group(1)) if m else 0

def cer_title(f): return 'Ceramic Mosaic Style %02d' % num_of(f)
def mf_title(f): return 'Marble Flooring Design %02d' % num_of(f)
def mw_title(f): return 'Marble Waterjet Design %02d' % num_of(f)
def hc_title(f): return 'Handcut Mosaic Mural %02d' % num_of(f)
def pp_title(f): return 'Custom Pool Mosaic Pattern %02d' % num_of(f)
def c6_title(f): return 'Iridium Crystal 6mm — %02d' % num_of(f)
def cp_title(f): return 'Crystal Pool Mosaic — %02d' % num_of(f)
def c4_title(f):
    code = re.search(r'_(\w+)$', f[:-4]).group(1)
    return 'Iridium Crystal 4mm — %s' % code

# ---------- page skeleton ----------
def page(title, desc, content, active, og_img='images/hero/banner1.jpg'):
    canonical = f'{DOMAIN}/{title.lower().replace(" ","-")}.html'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | {COMPANY}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)} | Foshan Mosaic Factory China">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230d1b2a'/%3E%3Cpath d='M4 4h8v8H4zM12 4h8v8h-8zM20 4h8v8h-8zM4 12h8v8H4zM12 12h8v8h-8zM20 12h8v8h-8zM4 20h8v8H4zM12 20h8v8h-8zM20 20h8v8h-8z' fill='%23c9a227'/%3E%3C/svg%3E">
<link rel="stylesheet" href="css/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html">
      <div class="brand-mark"></div>
      <div class="brand-name">{BRAND}<em>Foshan E-Tile · Mosaic</em></div>
    </a>
    <button class="nav-toggle" aria-label="Menu">☰</button>
    <nav class="main-nav">
      <a href="index.html"{' class="active"' if active=='index' else ''}>Home</a>
      <a href="products.html"{' class="active"' if active=='products' else ''}>Products</a>
      <a href="glass-mosaics.html"{' class="active"' if active=='glass' else ''}>Glass</a>
      <a href="ceramic-mosaics.html"{' class="active"' if active=='ceramic' else ''}>Ceramic</a>
      <a href="crystal-mosaics.html"{' class="active"' if active=='crystal' else ''}>Crystal</a>
      <a href="marble-mosaics.html"{' class="active"' if active=='marble' else ''}>Marble</a>
      <a href="handcut-murals.html"{' class="active"' if active=='handcut' else ''}>Handcut</a>
      <a href="pool-patterns.html"{' class="active"' if active=='pool' else ''}>Pool</a>
      <a href="about.html"{' class="active"' if active=='about' else ''}>About</a>
      <a href="contact.html"{' class="active"' if active=='contact' else ''}>Contact</a>
      <a class="nav-cta" href="contact.html">Get a Quote</a>
    </nav>
  </div>
</header>
{content}
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>{BRAND}</h4>
        <p>{COMPANY}</p>
        <p>14+ years of mosaic R&amp;D and production. Swimming pool mosaic patterns, engineering murals, garden landscape and KTV art mosaic for worldwide projects.</p>
      </div>
      <div>
        <h4>Products</h4>
        <ul>
          <li><a href="glass-mosaics.html">Glass Mosaics</a></li>
          <li><a href="ceramic-mosaics.html">Ceramic Mosaics</a></li>
          <li><a href="crystal-mosaics.html">Crystal Mosaics</a></li>
          <li><a href="marble-mosaics.html">Marble Mosaics</a></li>
          <li><a href="handcut-murals.html">Handcut Murals</a></li>
          <li><a href="pool-patterns.html">Custom Pool Patterns</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="about.html#case">Case Study</a></li>
          <li><a href="products.html#downloads">Catalogues</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <p>📍 Foshan, Guangdong, China</p>
        <p>✉️ sales@etile-mosaic.com</p>
        <p>💬 WhatsApp: +86 138 0000 0000</p>
        <p>🕐 Mon–Sat 8:30–18:00 (GMT+8)</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> {COMPANY}. All rights reserved.</span>
      <span>{BRAND} — Premium Mosaic Manufacturer &amp; Exporter</span>
    </div>
  </div>
</footer>
<div class="lightbox" id="lightbox">
  <button class="lb-close" aria-label="Close">✕</button>
  <button class="lb-nav lb-prev" aria-label="Previous">‹</button>
  <img class="lb-img" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="">
  <button class="lb-nav lb-next" aria-label="Next">›</button>
  <div class="lb-info"><span><b class="lb-title"></b> · <span class="lb-cat"></span></span><a class="lb-quote" href="contact.html">Request Quote</a></div>
</div>
<script src="js/main.js"></script>
</body>
</html>'''

def page_hero(title, sub, crumb):
    return f'''<section class="page-hero"><div class="container">
  <div class="crumb">{crumb}</div>
  <h1>{title}</h1>
  <p>{sub}</p>
</div></section>'''

# ---------- footer of generator ----------
def cat_card(c):
    return f'''<a class="cat-card" href="{c["slug"]}.html">
  <div class="thumb"><img src="{c["img"]}" alt="{esc(c["title"])}" loading="lazy"></div>
  <span class="arrow">→</span>
  <div class="body"><h3>{c["title"]}</h3><p>{esc(c["desc"])}</p><span class="count">{c["count"]} · Explore →</span></div>
</a>'''

pages = []
def save(name, content):
    p = os.path.join(OUT, name)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    pages.append(name)
    print(f'  ✓ {name} ({len(content)//1024} KB)')

# =====================================================================
# 1. HOME
# =====================================================================
home = f'''
<section class="hero">
  <div class="hero-slides">
    <div class="hero-slide active" style="background-image:url('images/hero/banner1.jpg')"></div>
    <div class="hero-slide" style="background-image:url('images/hero/banner2.jpg')"></div>
    <div class="hero-slide" style="background-image:url('images/hero/banner3.jpg')"></div>
    <div class="hero-slide" style="background-image:url('images/hero/banner4.jpg')"></div>
  </div>
  <div class="container">
    <div class="hero-content">
      <span class="hero-kicker">Foshan Mosaic Factory · Since 2010</span>
      <h1>Premium Mosaic Tiles &amp;<br><span>Custom Pool Art</span> for Global Projects</h1>
      <p>{COMPANY} designs and manufactures glass, ceramic, crystal, marble and handcut mosaic — from architectural surfaces to 14-year-proven swimming pool mosaic patterns.</p>
      <div class="hero-actions">
        <a class="btn btn-gold" href="products.html">Browse Products</a>
        <a class="btn btn-ghost" href="contact.html">Get a Free Quote</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><b>14<i>+</i></b><span>Years of Mosaic Making</span></div>
        <div class="stat"><b>6</b><span>Product Lines</span></div>
        <div class="stat"><b>450<i>+</i></b><span>Designs &amp; Colours</span></div>
        <div class="stat"><b>30<i>+</i></b><span>Export Countries</span></div>
      </div>
    </div>
  </div>
  <div class="hero-dots">
    <button class="hero-dot active" aria-label="Slide 1"></button>
    <button class="hero-dot" aria-label="Slide 2"></button>
    <button class="hero-dot" aria-label="Slide 3"></button>
    <button class="hero-dot" aria-label="Slide 4"></button>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head">
      <div class="kicker">Our Products</div>
      <h2>Six Complete Mosaic Product Lines</h2>
      <p>From classic glass and marble to iridescent crystal and handcrafted murals — everything produced in our own Foshan factory.</p>
    </div>
    <div class="cat-grid">
      {''.join(cat_card(c) for c in CATS)}
    </div>
  </div>
</section>

<section class="section" style="background:var(--bg-2)">
  <div class="container">
    <div class="sec-head">
      <div class="kicker">Why E-Tile</div>
      <h2>A Factory That Delivers, Not Just Sells</h2>
    </div>
    <div class="feature-grid">
      <div class="feature"><div class="icon">🏭</div><h3>In-House Factory</h3><p>Own production lines for glass, ceramic, crystal, marble and handcut mosaic — direct factory pricing and full process control.</p></div>
      <div class="feature"><div class="icon">🎨</div><h3>Professional Design Team</h3><p>In-house mosaic designers handle full project design, custom pattern development and large-site artistic schemes independently.</p></div>
      <div class="feature"><div class="icon">✅</div><h3>Strict Quality Control</h3><p>Mature production guarantee system with multi-stage inspection — quality up to standard, delivery on time.</p></div>
      <div class="feature"><div class="icon">🚢</div><h3>Export Experience</h3><p>14 years serving international property brands and engineering projects with safe packaging and punctual shipping.</p></div>
    </div>
  </div>
</section>

<section class="section" id="case">
  <div class="container">
    <div class="case-grid">
      <div class="img-wrap"><img src="images/hero/case_mural.jpg" alt="Chengdu Metro handcut mosaic mural project" loading="lazy"></div>
      <div>
        <div class="kicker" style="color:var(--gold);font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px">Signature Project</div>
        <h3>Chengdu Metro — "Mamen River Dragon" Mural</h3>
        <p>Our handcrafted mosaic mural at Chengdu Metro Institute of Technology Station reproduces the Late Jurassic "Mamen River Dragon" scene with the unique craft of manual mosaic inlay. The station has become a popular photo spot for young visitors.</p>
        <p>From detail iteration during production to full-quality evaluation and size-split installation — our team manages the entire artistic scheme for large construction sites.</p>
        <div class="tag-row">
          <span class="tag">Handcut Mosaic Mural</span>
          <span class="tag">Public Transport Project</span>
          <span class="tag">Full Custom Design</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--bg-2)">
  <div class="container">
    <div class="sec-head">
      <div class="kicker">Factory Tour</div>
      <h2>See Our Ceramic Mosaic Line in Action</h2>
    </div>
    <div class="video-wrap" style="max-width:860px;margin:0 auto">
      <video controls poster="images/hero/hero_ceramic_video.jpg" preload="none">
        <source src="videos/ceramic-showroom.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Planning a Pool, Hotel or Mosaic Art Project?</h2>
    <p>Send us your design or dimensions — our design team will reply within 24 hours with a custom mosaic scheme and factory-direct quotation.</p>
    <a class="btn btn-gold" href="contact.html">Start Your Project →</a>
  </div>
</section>
'''
save('index.html', page('Home', 'Foshan mosaic factory — glass, ceramic, crystal, marble and handcut mosaic tiles plus custom swimming pool mosaic patterns. 14 years of factory-direct production.', home, 'index'))

# =====================================================================
# 2. PRODUCTS overview
# =====================================================================
dl_items = [
    ('glass-hexagon-catalog.pdf', 'Glass Hexagon Catalog'),
    ('glass-ice-jade-catalog.pdf', 'Glass Ice Jade Catalog'),
    ('glass-cloud-series-catalog.pdf', 'Glass Cloud Series'),
    ('marble-waterjet-catalog.pdf', 'Marble Waterjet Series'),
    ('marble-flooring-catalog.pdf', 'Marble Flooring Series'),
    ('crystal-pool-mosaic-1.pdf', 'Crystal Pool Mosaic I'),
    ('crystal-pool-mosaic-2.pdf', 'Crystal Pool Mosaic II'),
    ('crystal-mosaic-catalogue.pdf', 'Crystal Mosaic Catalogue'),
    ('customized-pool-mosaic-2026.pdf', '2026 Custom Pool Mosaic'),
]
dl_html = '<div class="downloads">' + ''.join(
    f'<a class="dl-card" href="downloads/{esc(fn)}" target="_blank"><div class="pdf-ic">PDF</div><div><b>{esc(name)}</b><span>Download catalogue</span></div></a>'
    for fn, name in dl_items) + '</div>'

products = page_hero('All Products', 'Six complete mosaic lines from one Foshan factory — browse by category or download our PDF catalogues.', 'HOME / PRODUCTS') + f'''
<section class="section">
  <div class="container">
    <div class="cat-grid">
      {''.join(cat_card(c) for c in CATS)}
    </div>
  </div>
</section>
<section class="section" style="background:var(--bg-2)" id="downloads">
  <div class="container">
    <div class="sec-head">
      <div class="kicker">Catalogues</div>
      <h2>Download PDF Catalogues</h2>
      <p>Full product series in original factory PDF format — ready for your project team.</p>
    </div>
    {dl_html}
  </div>
</section>
'''
save('products.html', page('Products', 'Browse all mosaic product categories — glass, ceramic, crystal, marble, handcut murals and custom pool patterns with downloadable PDF catalogues.', products, 'products'))

# =====================================================================
# 3. GLASS MOSAICS
# =====================================================================
glass_files = imgs('glass')
glass_by_series = {}
for f in glass_files:
    key = re.sub(r'_\d+$', '', f[:-4])
    glass_by_series.setdefault(key, []).append(f)

glass_secs = []
for key, en_name, cn, desc in GLASS_SERIES:
    files = glass_by_series.get(key, [])
    if not files:
        continue
    n = len(files)
    def glass_title(f, en=en_name): return '%s — Design %02d' % (en, num_of(f))
    glass_secs.append(f'''<div class="series" id="{key}">
  <div class="series-head">
    <div><h2>{en_name} <small>{cn} · {n} designs</small></h2></div>
    <span class="series-en">{cn}</span>
  </div>
  <p style="color:var(--text-2);margin-bottom:18px;max-width:760px">{desc}</p>
  {grid_of('glass', files, 'Glass Mosaic', glass_title)}
</div>''')

glass_page = page_hero('Glass Mosaics', 'Ten fused-glass mosaic series — ice flower, gold line, hot-melt, hexagon, diamond, cloud, shimmer and more. 100+ designs for walls, pools, facades and feature panels.', 'HOME / PRODUCTS / GLASS MOSAICS') + f'''
<section class="section">
  <div class="container">
    {''.join(glass_secs)}
    <div class="cta-band" style="border-radius:var(--radius)">
      <h2>Need a Custom Glass Mosaic?</h2>
      <p>Custom colours, sizes and patterns available — tell us your project.</p>
      <a class="btn btn-gold" href="contact.html">Request a Quote</a>
    </div>
  </div>
</section>
'''
save('glass-mosaics.html', page('Glass Mosaics', 'Fused glass mosaic series from Foshan factory — ice flower, gold line, hot-melt, hexagon, diamond, cloud and shimmer glass mosaic tiles.', glass_page, 'glass', 'images/glass/glass_goldline_01.jpg'))

# =====================================================================
# 4. CERAMIC MOSAICS
# =====================================================================
cer_files = imgs('ceramic')
cer_grid = grid_of('ceramic', cer_files, 'Ceramic Mosaic', cer_title)
ceramic_page = page_hero('Ceramic Mosaics', '44 glazed ceramic mosaic styles — matt, glossy and textured surfaces. Durable, easy-clean and colourfast for walls, floors, swimming pools and commercial spaces.', 'HOME / PRODUCTS / CERAMIC MOSAICS') + f'''
<section class="section">
  <div class="container">
    {cer_grid}
  </div>
</section>
<section class="section" style="background:var(--bg-2)">
  <div class="container">
    <div class="sec-head"><div class="kicker">Showroom</div><h2>Ceramic Mosaic Collection — Video</h2></div>
    <div class="video-wrap" style="max-width:860px;margin:0 auto">
      <video controls poster="images/hero/hero_ceramic_video.jpg" preload="none">
        <source src="videos/ceramic-showroom.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
  </div>
</section>
'''
save('ceramic-mosaics.html', page('Ceramic Mosaics', 'Glazed ceramic mosaic sheets in 44 styles from Foshan factory — matt, glossy, textured ceramic mosaic tiles for walls, floors and pools.', ceramic_page, 'ceramic', 'images/ceramic/ceramic_01.jpg'))

# =====================================================================
# 5. CRYSTAL MOSAICS
# =====================================================================
c4_files = imgs('crystal-4mm')
c6_files = imgs('crystal-6mm')
cp_files = imgs('crystal-pool')

crystal_page = page_hero('Crystal Mosaics', 'Iridescent crystal glass mosaics with a rainbow shimmer — 4mm and 6mm iridium series plus dedicated crystal pool mosaic ranges.', 'HOME / PRODUCTS / CRYSTAL MOSAICS') + f'''
<section class="section">
  <div class="container">
    <div class="filter-bar">
      <button class="filter-btn active" data-filter="all">All</button>
      <button class="filter-btn" data-filter="4mm Iridium">4mm Iridium</button>
      <button class="filter-btn" data-filter="6mm Iridium">6mm Iridium</button>
      <button class="filter-btn" data-filter="Crystal Pool">Crystal Pool</button>
    </div>
    <div class="grid">
      {''.join(img_card('crystal-4mm', f, c4_title(f), '4mm Iridium') for f in c4_files)}
      {''.join(img_card('crystal-6mm', f, c6_title(f), '6mm Iridium') for f in c6_files)}
      {''.join(img_card('crystal-pool', f, cp_title(f), 'Crystal Pool') for f in cp_files)}
    </div>
  </div>
</section>
'''
save('crystal-mosaics.html', page('Crystal Mosaics', 'Iridescent crystal glass mosaic — 4mm and 6mm iridium series and crystal pool mosaic ranges from Foshan factory.', crystal_page, 'crystal', 'images/crystal-4mm/c4_FF7001.jpg'))

# =====================================================================
# 6. MARBLE MOSAICS
# =====================================================================
mf_files = imgs('marble-flooring')
mw_files = imgs('marble-waterjet')

marble_page = page_hero('Marble Mosaics', 'Natural marble mosaic flooring medallions and waterjet-cut patterns — precision cut from real stone for luxury lobbies, bathrooms and feature floors.', 'HOME / PRODUCTS / MARBLE MOSAICS') + f'''
<section class="section">
  <div class="container">
    <div class="series" id="flooring">
      <div class="series-head"><div><h2>Flooring Series <small>地花系列 · {len(mf_files)} designs</small></h2></div><span class="series-en">Flooring Medallions</span></div>
      <p style="color:var(--text-2);margin-bottom:18px;max-width:760px">Classic marble flooring medallions and borders — radial and floral compositions for grand entrance halls and luxury interiors.</p>
      {grid_of('marble-flooring', mf_files, 'Marble Flooring', mf_title)}
    </div>
    <div class="series" id="waterjet">
      <div class="series-head"><div><h2>Waterjet Series <small>水刀系列 · {len(mw_files)} designs</small></h2></div><span class="series-en">Waterjet Cut Patterns</span></div>
      <p style="color:var(--text-2);margin-bottom:18px;max-width:760px">CNC waterjet-cut natural stone patterns — intricate geometric and floral designs with sharp, precise edges.</p>
      {grid_of('marble-waterjet', mw_files, 'Marble Waterjet', mw_title)}
    </div>
  </div>
</section>
'''
save('marble-mosaics.html', page('Marble Mosaics', 'Natural marble mosaic flooring medallions and waterjet-cut patterns from Foshan factory — luxury stone mosaics for lobbies and bathrooms.', marble_page, 'marble', 'images/marble-waterjet/marble_waterjet_01.jpg'))

# =====================================================================
# 7. HANDCUT MURALS
# =====================================================================
hc_files = imgs('handcut')
handcut_page = page_hero('Handcut Mosaic Murals', 'Artisan handcut mosaic mural backsplashes — every tessera placed by skilled craftsmen to create bespoke art for kitchens, bathrooms and feature walls.', 'HOME / PRODUCTS / HANDCUT MURALS') + f'''
<section class="section">
  <div class="container">
    <div class="sec-head left"><div class="kicker">Bespoke Art</div><h2>Handcut Mosaic Mural Collection</h2><p>Each mural is hand-cut and assembled piece by piece. Custom designs, sizes and colour palettes available — send us your artwork.</p></div>
    {grid_of('handcut', hc_files, 'Handcut Mural', hc_title)}
    <div class="cta-band" style="border-radius:var(--radius);margin-top:56px">
      <h2>Commission a Custom Mural</h2>
      <p>Send your image or idea — our designers will create a mosaic mural plan with quotation.</p>
      <a class="btn btn-gold" href="contact.html">Commission a Mural</a>
    </div>
  </div>
</section>
'''
save('handcut-murals.html', page('Handcut Mosaic Murals', 'Artisan handcut mosaic mural backsplashes by Foshan factory — bespoke handcrafted mosaic art for kitchens and feature walls.', handcut_page, 'handcut', 'images/handcut/handcut_01.jpg'))

# =====================================================================
# 8. POOL PATTERNS
# =====================================================================
pp_files = imgs('pool-patterns')
pool_page = page_hero('Custom Pool Patterns', '14 years of swimming pool mosaic pattern design and fabrication. Choose from our pattern library or let our design team create a full custom scheme from your image.', 'HOME / PRODUCTS / CUSTOM POOL PATTERNS') + f'''
<section class="section">
  <div class="container">
    <div class="feature-grid" style="margin-bottom:48px">
      <div class="feature"><div class="icon">🎨</div><h3>Full Scheme Design</h3><p>Professional design team handles entire pool mosaic scheme creation — from concept to production.</p></div>
      <div class="feature"><div class="icon">📐</div><h3>From Your Image</h3><p>Send us a picture, logo or pattern — we turn it into a precise mosaic layout with colour plan.</p></div>
      <div class="feature"><div class="icon">🗺️</div><h3>Rich Pattern Library</h3><p>Extensive in-house library of pool art patterns for quick, proven design selection.</p></div>
      <div class="feature"><div class="icon">⏱️</div><h3>On-Time Delivery</h3><p>14 years of pool puzzle production — stable quality and punctual delivery for engineering projects.</p></div>
    </div>
    {grid_of('pool-patterns', pp_files, 'Pool Pattern', pp_title)}
    <div class="cta-band" style="border-radius:var(--radius);margin-top:56px">
      <h2>Design Your Pool Mosaic</h2>
      <p>Send your pool dimensions and design idea — free custom scheme and quotation within 24 hours.</p>
      <a class="btn btn-gold" href="contact.html">Get Free Design</a>
    </div>
  </div>
</section>
'''
save('pool-patterns.html', page('Custom Pool Patterns', 'Custom swimming pool mosaic patterns from Foshan factory — 14 years of pool mosaic design and fabrication, custom schemes from your image.', pool_page, 'pool', 'images/pool-patterns/pool_2026_11.jpg'))

# =====================================================================
# 9. ABOUT
# =====================================================================
about = page_hero('About Us', 'A Foshan mosaic factory built on design capability, production discipline and 14 years of export experience.', 'HOME / ABOUT') + f'''
<section class="section">
  <div class="container">
    <div class="about-grid">
      <div>
        <h3>Who We Are</h3>
        <p><b>{COMPANY}</b> (brand: {BRAND}) focuses on the R&amp;D and production of mosaic. Our products are widely used in indoor and outdoor swimming pools, garden landscapes, KTV hotels and other space decoration.</p>
        <p>With advanced design ideas, reasonable budget quotation, excellent manufacturing technology and high-quality service, we customize swimming pool mosaic, engineering mosaic mural and landscape mosaic for every customer.</p>
        <p>The company has a professional team of mosaic designers who can independently complete large-scale construction-site mosaic artistic design. With a mature production guarantee system, we ensure quality up to standard and delivery on time.</p>
        <h3>Our Capabilities</h3>
        <ul>
          <li>Swimming pool mosaic pattern design &amp; fabrication — 14 years</li>
          <li>Custom mosaic mural &amp; large-scale engineering art</li>
          <li>Garden landscape &amp; KTV art mosaic</li>
          <li>Glass / ceramic / crystal / marble mosaic production lines</li>
          <li>Full-scheme design from your image (来图定制设计)</li>
          <li>Size-split, numbered packing and safe wooden-crate export</li>
        </ul>
      </div>
      <div>
        <div class="img-wrap" style="border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)"><img src="images/hero/about_pool.jpg" alt="Crystal pool mosaic factory production" loading="lazy"></div>
        <h3 style="font-size:20px;margin-top:26px">Our Process</h3>
        <div class="steps">
          <div class="step"><div class="num">01</div><h4>Design</h4><p>Scheme creation or from-your-image pattern design with colour plan.</p></div>
          <div class="step"><div class="num">02</div><h4>Production</h4><p>Material selection, cutting and assembly with continuous detail iteration.</p></div>
          <div class="step"><div class="num">03</div><h4>QC</h4><p>Overall effect evaluation and adjustment, design-confirmed before finishing.</p></div>
          <div class="step"><div class="num">04</div><h4>Delivery</h4><p>Split into installable sizes, numbered and packed into safe wooden crates.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--bg-2)" id="case">
  <div class="container">
    <div class="case-grid">
      <div class="img-wrap"><img src="images/hero/case_mural.jpg" alt="Chengdu Metro mural — handcut mosaic reproduction" loading="lazy"></div>
      <div>
        <div class="kicker" style="color:var(--gold);font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;margin-bottom:10px">Case Study</div>
        <h3>Chengdu Metro Institute of Technology Station</h3>
        <p>Located in the "Mamen River Dragon" relic circle, the station's full mural reproduces the Late Jurassic living scene of the Mamen River Dragon using hand-inlaid mosaic and the dreamy texture of mosaic itself.</p>
        <p>During production we repeatedly adjusted details of the dragon image and communicated closely with the design institute. The finished artwork was evaluated as a whole, confirmed by the design institute, then split into installation-friendly sizes and packed in safe wooden crates.</p>
        <p>Today the station is a popular photo spot for young visitors — a benchmark of our large-scale mural capability.</p>
        <div class="tag-row"><span class="tag">Handcut Mosaic</span><span class="tag">Engineering Mural</span><span class="tag">Public Art</span></div>
      </div>
    </div>
  </div>
</section>
<section class="stats-band">
  <div class="container">
    <div class="inner">
      <div><b>14+</b><span>Years in Business</span></div>
      <div><b>100%</b><span>In-House Production</span></div>
      <div><b>24h</b><span>Quote Response</span></div>
      <div><b>30+</b><span>Export Countries</span></div>
    </div>
  </div>
</section>
<section class="cta-band">
  <div class="container">
    <h2>Let's Build Your Mosaic Project</h2>
    <p>Talk to our design team about your pool, mural or architectural mosaic needs.</p>
    <a class="btn btn-gold" href="contact.html">Contact Us →</a>
  </div>
</section>
'''
save('about.html', page('About Us', 'About Foshan E-Tile Building Material Co., Ltd. — FengFu Mosaic, 14 years of mosaic R&D, pool pattern design, murals and export production.', about, 'about', 'images/hero/about_pool.jpg'))

# =====================================================================
# 10. CONTACT
# =====================================================================
contact = page_hero('Contact Us', 'Send us your project details — design, dimensions and quantity. Our team replies within 24 hours with a scheme and quotation.', 'HOME / CONTACT') + f'''
<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div>
        <div class="contact-card">
          <h3>🏢 Company</h3>
          <p class="big">{COMPANY}</p>
          <p>{BRAND} — Pool Mosaic · Engineering Mural · Landscape &amp; KTV Mosaic</p>
        </div>
        <div class="contact-card">
          <h3>📍 Address</h3>
          <p>Foshan, Guangdong Province, China</p>
          <p style="font-size:13px">(Exact factory address provided on request)</p>
        </div>
        <div class="contact-card">
          <h3>✉️ Email</h3>
          <p class="big">sales@etile-mosaic.com</p>
          <p>Reply within 24 hours</p>
        </div>
        <div class="contact-card">
          <h3>💬 WhatsApp</h3>
          <p class="big">+86 138 0000 0000</p>
          <p>WeChat available for China-based partners</p>
        </div>
        <div class="contact-card">
          <h3>🕐 Working Hours</h3>
          <p>Monday – Saturday · 8:30 – 18:00 (GMT+8)</p>
        </div>
      </div>
      <div>
        <div class="form-wrap">
          <h3>Send Your Inquiry</h3>
          <form id="contact-form" data-formspree-id="xvgkrvbd" method="post" novalidate>
            <div class="form-row">
              <div class="form-group"><label>Your Name *</label><input type="text" name="name" required placeholder="John Smith"></div>
              <div class="form-group"><label>Company</label><input type="text" name="company" placeholder="Company Ltd."></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label>Email *</label><input type="email" name="email" required placeholder="you@company.com"></div>
              <div class="form-group"><label>WhatsApp / Phone</label><input type="text" name="phone" placeholder="+86 ..."></div>
            </div>
            <div class="form-group"><label>Product of Interest</label>
              <select name="product" id="cf-product">
                <option value="">— Select a category —</option>
                <option>Glass Mosaics</option>
                <option>Ceramic Mosaics</option>
                <option>Crystal Mosaics</option>
                <option>Marble Mosaics</option>
                <option>Handcut Mosaic Murals</option>
                <option>Custom Pool Patterns</option>
                <option>Other / Custom Design</option>
              </select>
            </div>
            <div class="form-group"><label>Message *</label><textarea name="message" required placeholder="Project type, dimensions (m), quantity, target country, design reference…"></textarea></div>
            <button class="btn btn-gold" type="submit" style="width:100%;justify-content:center">Send Inquiry →</button>
            <p class="form-note">By submitting, you agree to be contacted about your inquiry. Your data is never shared.</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>
'''
save('contact.html', page('Contact Us', 'Contact Foshan E-Tile Building Material Co., Ltd. — send your mosaic project inquiry for a free quotation within 24 hours.', contact, 'contact'))

# =====================================================================
# SEO files
# =====================================================================
urls = [
    ('index.html', '1.0', 'weekly'),
    ('products.html', '0.9', 'weekly'),
    ('glass-mosaics.html', '0.9', 'weekly'),
    ('ceramic-mosaics.html', '0.9', 'weekly'),
    ('crystal-mosaics.html', '0.9', 'weekly'),
    ('marble-mosaics.html', '0.9', 'weekly'),
    ('handcut-murals.html', '0.9', 'weekly'),
    ('pool-patterns.html', '0.9', 'weekly'),
    ('about.html', '0.6', 'monthly'),
    ('contact.html', '0.7', 'monthly'),
]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url>\n    <loc>{DOMAIN}/{fn}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n'
    for fn, pr, cf in urls) + '</urlset>\n'
with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap)
print('  ✓ sitemap.xml')

robots = f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n'
with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots)
print('  ✓ robots.txt')

print(f'\nDONE — {len(pages)} pages generated')
