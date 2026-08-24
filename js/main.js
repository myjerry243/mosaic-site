/* E-Tile Mosaic site scripts: nav, lightbox gallery, filters, contact form */
(function(){
  'use strict';

  /* ---------- hero slideshow ---------- */
  var slides = document.querySelectorAll('.hero-slide');
  var dots = document.querySelectorAll('.hero-dot');
  if (slides.length > 1) {
    var idx = 0;
    function go(i){
      slides[idx].classList.remove('active');
      if (dots[idx]) dots[idx].classList.remove('active');
      idx = (i + slides.length) % slides.length;
      slides[idx].classList.add('active');
      if (dots[idx]) dots[idx].classList.add('active');
    }
    setInterval(function(){ go(idx + 1); }, 6000);
    dots.forEach(function(d, i){ d.addEventListener('click', function(){ go(i); }); });
  }

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function(){ nav.classList.toggle('open'); });
    nav.addEventListener('click', function(e){
      if (e.target.tagName === 'A') nav.classList.remove('open');
    });
  }

  /* ---------- lightbox gallery ---------- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('.lb-img');
    var lbTitle = lb.querySelector('.lb-title');
    var lbCat = lb.querySelector('.lb-cat');
    var lbQuote = lb.querySelector('.lb-quote');
    var items = [];
    var cur = 0;

    function openAt(i){
      if (i < 0) i = items.length - 1;
      if (i >= items.length) i = 0;
      cur = i;
      var it = items[cur];
      lbImg.src = it.hi;
      lbImg.alt = it.title;
      if (lbTitle) lbTitle.textContent = it.title;
      if (lbCat) lbCat.textContent = it.cat;
      if (lbQuote) lbQuote.href = 'contact.html?product=' + encodeURIComponent(it.title);
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function close(){
      lb.classList.remove('open');
      document.body.style.overflow = '';
    }

    // collect all product cards
    var cards = document.querySelectorAll('.product-card');
    cards.forEach(function(card, idx){
      var img = card.querySelector('img');
      var hi = card.getAttribute('data-hi') || (img ? img.getAttribute('data-hi') : '');
      var title = card.getAttribute('data-title') || (img ? img.alt : ('Item ' + (idx+1)));
      var cat = card.getAttribute('data-cat') || '';
      items.push({hi: hi, title: title, cat: cat});
      card.addEventListener('click', function(){ openAt(idx); });
    });

    if (items.length > 0) {
      lb.querySelector('.lb-close').addEventListener('click', close);
      lb.querySelector('.lb-prev').addEventListener('click', function(e){ e.stopPropagation(); openAt(cur - 1); });
      lb.querySelector('.lb-next').addEventListener('click', function(e){ e.stopPropagation(); openAt(cur + 1); });
      lb.addEventListener('click', function(e){ if (e.target === lb) close(); });
      document.addEventListener('keydown', function(e){
        if (!lb.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') openAt(cur - 1);
        if (e.key === 'ArrowRight') openAt(cur + 1);
      });
    }
  }

  /* ---------- category filters ---------- */
  var filterBar = document.querySelector('.filter-bar');
  if (filterBar) {
    var buttons = filterBar.querySelectorAll('.filter-btn');
    var cards2 = document.querySelectorAll('.product-card');
    buttons.forEach(function(btn){
      btn.addEventListener('click', function(){
        buttons.forEach(function(b){ b.classList.remove('active'); });
        btn.classList.add('active');
        var f = btn.getAttribute('data-filter');
        cards2.forEach(function(card){
          var show = (f === 'all') || (card.getAttribute('data-cat') === f);
          card.style.display = show ? '' : 'none';
        });
      });
    });
    // auto-filter from URL ?cat=slug
    var params = new URLSearchParams(window.location.search);
    var catParam = params.get('cat');
    if (catParam) {
      var map = {
        '4mm-iridium':'4mm Iridium',
        '6mm-iridium':'6mm Iridium',
        'crystal-pool':'Crystal Pool'
      };
      var display = map[catParam] || catParam;
      var target = Array.prototype.find.call(buttons, function(b){ return b.getAttribute('data-filter') === display; });
      if (target) target.click();
    }
  }

  /* ---------- contact form (Formspree) ---------- */
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var id = form.getAttribute('data-formspree-id');
      if (!id) { alert('Form service not configured. Please email us directly.'); return; }
      var btn = form.querySelector('button[type=submit]');
      var orig = btn.textContent;
      btn.textContent = 'Sending…';
      btn.disabled = true;
      fetch('https://formspree.io/f/' + id, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function(r){
        if (r.ok) {
          form.innerHTML = '<div style="text-align:center;padding:36px 0"><h3 style="color:var(--navy);font-size:22px;margin-bottom:10px">✓ Thank you!</h3><p style="color:var(--text-2)">Your inquiry has been sent. Our team will reply within 24 hours.</p></div>';
        } else {
          throw new Error('bad response');
        }
      }).catch(function(){
        btn.textContent = orig;
        btn.disabled = false;
        alert('Network error — please email us directly or try again.');
      });
    });
    // prefill product from URL
    var params2 = new URLSearchParams(window.location.search);
    var prod = params2.get('product');
    if (prod) {
      var fld = document.getElementById('cf-product');
      if (fld) fld.value = prod;
    }
  }

  /* ---------- footer year ---------- */
  var yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- lazy image load-safe check (dev helper) ---------- */
  window.__imgBroken = function(){
    return Array.prototype.slice.call(document.images).filter(function(i){ return !i.complete || i.naturalWidth === 0; });
  };
})();
