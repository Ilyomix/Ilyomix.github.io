/* Ilyes Abd-Lillah — site behaviour. Works without GSAP; GSAP adds the motion when motion is allowed. */
(function () {
  var d = document, root = d.documentElement, lang = root.lang || 'en';

  /* Local time in Toulouse */
  var fmt = new Intl.DateTimeFormat(lang === 'fr' ? 'fr-FR' : 'en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Paris' });
  function tick() { var t = fmt.format(new Date()); d.querySelectorAll('[data-time]').forEach(function (n) { n.textContent = t; }); }
  tick(); setInterval(tick, 15000);

  /* Years of experience, since September 2017 */
  var now = new Date(), years = now.getFullYear() - 2017 - (now < new Date(now.getFullYear(), 8, 1) ? 1 : 0);
  d.querySelectorAll('[data-years]').forEach(function (n) { n.textContent = years; });

  /* Theme toggle, remembered */
  var toggle = d.querySelector('[data-theme-toggle]'), meta = d.querySelector('meta[name=theme-color]');
  function syncToggle() {
    if (!toggle) return;
    var light = root.getAttribute('data-theme') === 'light';
    var label = toggle.getAttribute(light ? 'data-label-dark' : 'data-label-light');
    toggle.setAttribute('aria-label', label); toggle.setAttribute('title', label);
  }
  if (toggle) {
    syncToggle();
    toggle.addEventListener('click', function () {
      var light = root.getAttribute('data-theme') !== 'light';
      if (light) root.setAttribute('data-theme', 'light'); else root.removeAttribute('data-theme');
      if (meta) meta.setAttribute('content', light ? '#f3f2ee' : '#0b0c0f');
      try { localStorage.setItem('theme', light ? 'light' : 'dark'); } catch (e) {}
      syncToggle();
    });
  }

  /* Language choice, remembered */
  d.querySelectorAll('[data-lang]').forEach(function (a) {
    a.addEventListener('click', function () { try { localStorage.setItem('lang', a.getAttribute('data-lang')); } catch (e) {} });
  });

  /* The header shows where I am only while no section on screen already says it */
  var place = d.querySelector('.header-place'), sayers = d.querySelectorAll('[data-place]');
  if (place && 'IntersectionObserver' in window) {
    var seen = [];
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var i = seen.indexOf(e.target);
        if (e.isIntersecting && i < 0) seen.push(e.target);
        if (!e.isIntersecting && i > -1) seen.splice(i, 1);
      });
      place.classList.toggle('is-shown', seen.length === 0);
    }, { rootMargin: '-64px 0px 0px 0px' });
    sayers.forEach(function (el) { io.observe(el); });
    if (!sayers.length) place.classList.add('is-shown');
  } else if (place) place.classList.add('is-shown');

  /* Header state */
  var header = d.querySelector('.site-header');
  function onScroll() { header.classList.toggle('is-scrolled', scrollY > 8); }
  onScroll(); addEventListener('scroll', onScroll, { passive: true });

  /* Numbers, formatted for the page language */
  var nf = new Intl.NumberFormat(lang === 'fr' ? 'fr-FR' : 'en-US');
  function fmtNum(v) { return nf.format(Math.round(v)).replace(/\u202f/g, '\u00a0'); }

  /* Cadran downloads, live. The build baked in the latest figure; the Cadran API gives the current one. */
  var live = d.querySelector('[data-live="downloads"]');
  if (live && window.fetch) {
    var busy = false;
    var poll = function () {
      if (busy || d.hidden) return;
      busy = true;
      fetch('https://cadranapp.com/api/download-count', { cache: 'no-store' })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) {
          var n = Math.round(+j.downloadCount);
          if (!(n > 0)) return;
          live.setAttribute('data-count', n);
          var tag = live.parentNode.querySelector('.live'); if (tag) tag.hidden = false;
          if (live.__countTo) live.__countTo(n);
          else if (!live.__waiting) live.textContent = fmtNum(n) + (live.getAttribute('data-suffix') || '');
        })
        .catch(function () {})
        .then(function () { busy = false; });
    };
    poll(); setInterval(poll, 30000);
    d.addEventListener('visibilitychange', poll);
  }

  /* ---------- Motion ---------- */
  function noMotion() { root.classList.remove('anim'); root.classList.add('no-anim'); }
  if (!root.classList.contains('motion-ok')) { noMotion(); return; }
  function load(src) { return new Promise(function (ok, ko) { var s = d.createElement('script'); s.src = src; s.async = false; s.onload = ok; s.onerror = ko; d.head.appendChild(s); }); }
  requestAnimationFrame(function () { setTimeout(function () {
    Promise.all([load('/assets/js/gsap.min.js'), load('/assets/js/ScrollTrigger.min.js')]).then(motion, noMotion);
  }, 0); });

  function motion() {
  var gsap = window.gsap, ST = window.ScrollTrigger;
  if (!gsap || !ST) { noMotion(); return; }
  window.__gsapOn = true;
  gsap.registerPlugin(ST);
  var q = function (s, c) { return gsap.utils.toArray(s, c); };
  var fine = matchMedia('(pointer: fine)').matches;

  /* Hero intro */
  var intro = gsap.timeline({ defaults: { ease: 'expo.out' } });
  intro
    .to('.hero-title .line > span', { yPercent: 0, y: 0, duration: 1.35, stagger: 0.085 }, 0.05)
    .fromTo('.portrait-card', { scale: 1.045, y: 10 }, { scale: 1, y: 0, duration: 1.8 }, 0)
    .fromTo('.portrait-halo', { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 2 }, 0.1)
    .fromTo('.hero-copy > *', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 1, stagger: 0.08 }, 0.5)
    .to('.chip', { opacity: 1, duration: 0.8, stagger: 0.12 }, 0.9)
    .fromTo('.hero-lights', { opacity: 0 }, { opacity: 1, duration: 2.2, ease: 'power2.out' }, 0);

  /* Lights drift, only while their section is on screen */
  q('.lights').forEach(function (group) {
    var tl = gsap.timeline({ paused: true });
    q('i:not(.pl)', group).forEach(function (el) {
      tl.to(el, { x: gsap.utils.random(-70, 70), y: gsap.utils.random(-50, 50), scale: gsap.utils.random(0.88, 1.18),
        duration: gsap.utils.random(8, 15), ease: 'sine.inOut', yoyo: true, repeat: -1 }, 0);
    });
    ST.create({ trigger: group.parentElement, start: 'top bottom', end: 'bottom top', onToggle: function (s) { s.isActive ? tl.play() : tl.pause(); } });
    if (!group.classList.contains('hero-lights') && !group.classList.contains('stage-lights')) {
      gsap.fromTo(group, { yPercent: -10 }, { yPercent: 10, ease: 'none', scrollTrigger: { trigger: group.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    }
  });

  /* Pointer: a light follows the cursor in the hero, the portrait tilts a little */
  if (fine) {
    var hero = d.querySelector('.hero'), pl = d.querySelector('.hero-lights .pl'), card = d.querySelector('.portrait-card');
    if (hero && pl) {
      var px = gsap.quickTo(pl, 'x', { duration: 1.4, ease: 'power3' }), py = gsap.quickTo(pl, 'y', { duration: 1.4, ease: 'power3' });
      var rx = card && gsap.quickTo(card, 'rotationX', { duration: 0.9, ease: 'power3' }), ry = card && gsap.quickTo(card, 'rotationY', { duration: 0.9, ease: 'power3' });
      if (card) gsap.set(card, { transformPerspective: 1000 });
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect();
        px(e.clientX - r.left - r.width / 2); py(e.clientY - r.top - r.height / 2);
        if (card) {
          var c = card.getBoundingClientRect(), nx = (e.clientX - (c.left + c.width / 2)) / r.width, ny = (e.clientY - (c.top + c.height / 2)) / r.height;
          ry(gsap.utils.clamp(-7, 7, nx * 14)); rx(gsap.utils.clamp(-6, 6, -ny * 12));
        }
      });
      hero.addEventListener('pointerleave', function () { if (card) { rx(0); ry(0); } });
    }
  }

  /* Screens power on one after the other: the backlight glows, then the picture comes up */
  function screensOn() {
    var tl = gsap.timeline({ paused: true });
    ['.dev-display', '.dev-mbp', '.dev-mba', '.dev-phone.p1', '.dev-phone.p2'].forEach(function (sel, i) {
      var off = d.querySelector(sel + ' .screen-off'), t = i * 0.14;
      if (!off) return;
      tl.to(off, { backgroundColor: '#17191f', duration: 0.14, ease: 'power1.in' }, t)
        .to(off, { opacity: 0, duration: 0.6, ease: 'power2.out' }, t + 0.12);
    });
    return tl;
  }

  /* Stage: the desk assembles, then the screens and the lights come on */
  var mm = gsap.matchMedia();
  mm.add({ wide: '(min-width: 900px)', narrow: '(max-width: 899px)' }, function (ctx) {
    if (ctx.conditions.wide) {
      gsap.timeline({ scrollTrigger: { trigger: '.stage', start: 'top 85%', end: 'top top', scrub: 0.9 } })
        .from('.stage-head > *', { y: 40, opacity: 0, stagger: 0.08 }, 0)
        .from('.set .dev-display', { yPercent: 22, scale: 0.9, opacity: 0 }, 0)
        .from('.set .dev-mbp', { xPercent: -28, yPercent: 14, opacity: 0 }, 0.08)
        .from('.set .dev-mba', { xPercent: 28, yPercent: 14, opacity: 0 }, 0.08)
        .from('.set .dev-phone', { yPercent: 50, opacity: 0, stagger: 0.07 }, 0.2);
      gsap.timeline({ scrollTrigger: { trigger: '.stage', start: 'top top', end: '+=110%', scrub: 0.8, pin: '.stage-pin', anticipatePin: 1 } })
        .fromTo('.stage-lights', { opacity: 0 }, { opacity: 1, duration: 1 }, 0)
        .fromTo('.spot', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0)
        .from('.legend a', { y: 24, opacity: 0, stagger: 0.08, duration: 0.3 }, 0.7)
        .to({}, { duration: 0.2 });
      /* A screen is either off or on: never a half-lit veil that the scroll position leaves behind */
      var on = screensOn();
      ST.create({ trigger: '.stage', start: 'top -12%', onEnter: function () { on.play(); }, onLeaveBack: function () { on.reverse(); } });
    } else {
      gsap.set('.stage-lights, .spot', { opacity: 0 });
      var onN = screensOn();
      gsap.timeline({ scrollTrigger: { trigger: '.set', start: 'top 70%', once: true, onEnter: function () { onN.play(); } } })
        .to('.stage-lights, .spot', { opacity: 1, duration: 1.4, ease: 'power2.out' }, 0);
    }
  });

  /* Reel: endless rows that speed up with the scroll */
  var reels = q('.reel-row').map(function (row) {
    var dir = row.getAttribute('data-dir') === '-1' ? -1 : 1;
    var tl = gsap.fromTo(row, { xPercent: dir === 1 ? 0 : -50 }, { xPercent: dir === 1 ? -50 : 0, ease: 'none', duration: 60, repeat: -1, paused: true });
    return tl;
  });
  if (reels.length) {
    ST.create({
      trigger: '.faces', start: 'top bottom', end: 'bottom top',
      onToggle: function (s) { reels.forEach(function (t) { s.isActive ? t.play() : t.pause(); }); },
      onUpdate: function (s) {
        var v = Math.min(Math.abs(s.getVelocity()) / 250, 6);
        reels.forEach(function (t) { gsap.to(t, { timeScale: 1 + v, duration: 0.25, overwrite: true, onComplete: function () { gsap.to(t, { timeScale: 1, duration: 1.2, ease: 'power2.out' }); } }); });
      }
    });
    q('.reel-row').forEach(function (row) {
      row.addEventListener('pointerenter', function () { reels.forEach(function (t) { gsap.to(t, { timeScale: 0.15, duration: 0.6 }); }); });
      row.addEventListener('pointerleave', function () { reels.forEach(function (t) { gsap.to(t, { timeScale: 1, duration: 0.8 }); }); });
    });
  }

  /* Reveals */
  ST.batch('[data-reveal]', {
    start: 'top 88%', once: true,
    onEnter: function (batch) { gsap.fromTo(batch, { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 1.15, ease: 'expo.out', stagger: 0.08, overwrite: true }); }
  });

  /* Parallax on product media */
  q('[data-speed]').forEach(function (el) {
    var s = parseFloat(el.getAttribute('data-speed')) || 1;
    gsap.fromTo(el, { y: 60 * s }, { y: -60 * s, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* Counters */
  q('[data-count]').forEach(function (el) {
    var suffix = el.getAttribute('data-suffix') || '', o = { v: 0 };
    var draw = function () { el.textContent = fmtNum(o.v) + suffix; };
    el.__waiting = true; el.textContent = '0' + suffix;
    ST.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () {
      el.__waiting = false;
      gsap.to(o, { v: parseFloat(el.getAttribute('data-count')) || 0, duration: 1.8, ease: 'power3.out', onUpdate: draw });
      el.__countTo = function (n) { gsap.to(o, { v: n, duration: 1.2, ease: 'power2.out', onUpdate: draw, overwrite: true }); };
    } });
  });

  addEventListener('load', function () { ST.refresh(); });
  if (d.readyState === 'complete') ST.refresh();
  }
})();
