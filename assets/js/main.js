/* J.P. Fernando & Sons — site behaviour. No dependencies. */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canHover = window.matchMedia("(hover: hover)").matches;
  var CONTACT = { email: "jpfernandoandsons287@gmail.com", phone: "+94 11 243 5634" };

  function $(s, root) { return (root || document).querySelector(s); }
  function $$(s, root) { return Array.prototype.slice.call((root || document).querySelectorAll(s)); }

  /* ---------- opened straight from disk (double-clicked) ----------
     Online, folder links like "about-us/" load index.html automatically.
     From disk they would show a folder listing, so point them at index.html. */
  if (location.protocol === "file:") {
    $$("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (/^(https?:|mailto:|tel:|#)/.test(h)) return;
      var m = h.match(/^([^?#]*)(.*)$/);
      if (m[1] === "" || m[1] === "./") m[1] = "./";
      if (/\/$/.test(m[1])) a.setAttribute("href", m[1] + "index.html" + m[2]);
    });
  }

  /* ---------- storage (guarded: private mode can throw) ---------- */
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- years in trade (computed, never hard-coded) ---------- */
  var FOUNDED = 1953;
  var years = new Date().getFullYear() - FOUNDED;
  $$("[data-years]").forEach(function (el) {
    if (el.hasAttribute("data-count")) el.setAttribute("data-count", years); else el.textContent = years;
  });

  /* ==========================================================
     Header: solid after scroll, hide on scroll down
     ========================================================== */
  var hdr = $(".hdr");
  var mbar = $(".mbar");
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (hdr) {
      hdr.classList.toggle("is-solid", y > 40);
      if (!doc.classList.contains("menu-open")) hdr.classList.toggle("is-hidden", y > 400 && y > lastY + 4 && !hdr.querySelector(".is-open"));
      if (y < lastY - 4) hdr.classList.remove("is-hidden");
    }
    if (mbar) mbar.classList.toggle("show", y > 500);
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- quick-access bar: staggered slide-in ---------- */
  var qbar = $(".qbar");
  if (qbar) {
    $$("li", qbar).forEach(function (li, i) { li.style.setProperty("--n", i); });
    requestAnimationFrame(function () { qbar.classList.add("is-in"); });
  }

  /* ---------- mega menu ---------- */
  $$(".nav__item").forEach(function (item) {
    var btn = item.querySelector("button");
    var closeT;
    function open() { clearTimeout(closeT); item.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); }
    function close() { item.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }
    btn.addEventListener("click", function () { item.classList.contains("is-open") ? close() : open(); });
    if (canHover) {
      item.addEventListener("mouseenter", open);
      item.addEventListener("mouseleave", function () { closeT = setTimeout(close, 180); });
    }
    item.addEventListener("keydown", function (e) { if (e.key === "Escape") { close(); btn.focus(); } });
    item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) close(); });
  });

  /* ---------- mobile drawer ---------- */
  var burger = $(".burger");
  var drawer = $(".drawer");
  if (burger && drawer) {
    burger.addEventListener("click", function () {
      var open = !doc.classList.contains("menu-open");
      doc.classList.toggle("menu-open", open);
      burger.setAttribute("aria-expanded", String(open));
      drawer.setAttribute("aria-hidden", String(!open));
      drawer.inert = !open;
      document.body.style.overflow = open ? "hidden" : "";
      if (open) hdr.classList.remove("is-hidden");
    });
    drawer.inert = true;
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && doc.classList.contains("menu-open")) burger.click(); });
  }

  /* ==========================================================
     Reveal on scroll + split headings
     ========================================================== */
  $$("[data-split]").forEach(function (el) {
    var i = 0;
    function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement("span"); w.className = "w";
            var s = document.createElement("span"); s.textContent = part; s.style.setProperty("--i", i++);
            w.appendChild(s); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") { walk(n); }
      });
    }
    walk(el);
    el.classList.add("split");
  });

  var revealEls = $$("[data-reveal], [data-split], .era, [data-count]");
  // A fully clipped element never registers as intersecting, so watch its parent instead
  $$("[data-clip]").forEach(function (el) { el.parentElement.setAttribute("data-clip-host", ""); });
  revealEls = revealEls.concat($$("[data-clip-host]"));
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        $$(":scope > [data-clip]", en.target).forEach(function (c) { c.classList.add("in"); });
        if (en.target.hasAttribute("data-count")) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.concat($$("[data-clip]")).forEach(function (el) { el.classList.add("in"); if (el.hasAttribute("data-count")) el.textContent = el.getAttribute("data-count"); });
  }

  function countUp(el) {
    var end = parseInt(el.getAttribute("data-count"), 10);
    var start = parseInt(el.getAttribute("data-from") || "0", 10);
    var t0 = null, dur = 1600;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(start + (end - start) * e);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ==========================================================
     Living net — hero canvas (verlet simulation of a hung net)
     ========================================================== */
  var netWrap = $(".hero__net");
  if (netWrap) initNet(netWrap);

  function initNet(wrap) {
    var canvas = document.createElement("canvas");
    canvas.setAttribute("aria-hidden", "true");
    wrap.appendChild(canvas);
    var ctx = canvas.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W, H, nodes, links, cols, rows, S, start = performance.now();
    var mouse = { x: -9999, y: -9999 };
    var running = false, visible = true, raf;

    function build() {
      var r = wrap.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      S = W < 600 ? 30 : 38;
      var h = S * 0.62;
      cols = Math.ceil(W / S) + 2;
      rows = Math.ceil(H / h);
      nodes = []; links = [];
      for (var y = 0; y < rows; y++) {
        for (var x = 0; x < cols; x++) {
          var px = x * S + (y % 2 ? S / 2 : 0) - S;
          var py = 26 + y * h;
          nodes.push({ x: px, y: py, ox: px, oy: py, px: px, py: py, pin: y === 0, row: y });
        }
      }
      function id(x, y) { return y * cols + x; }
      for (y = 0; y < rows - 1; y++) {
        for (x = 0; x < cols; x++) {
          var a = id(x, y);
          var l = y % 2 ? x : x - 1, rr = y % 2 ? x + 1 : x;
          if (l >= 0) links.push(link(a, id(l, y + 1)));
          if (rr < cols) links.push(link(a, id(rr, y + 1)));
        }
      }
    }
    function link(a, b) {
      var A = nodes[a], B = nodes[b];
      return { a: A, b: B, len: Math.hypot(A.x - B.x, A.y - B.y) };
    }

    function sim(t) {
      var wind = Math.sin(t / 1700) * 0.05 + Math.sin(t / 630) * 0.02;
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        if (n.pin) continue;
        var vx = (n.x - n.px) * 0.96, vy = (n.y - n.py) * 0.96;
        n.px = n.x; n.py = n.y;
        n.x += vx + wind * (n.row / rows); n.y += vy + 0.12;
        var dx = n.x - mouse.x, dy = n.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 9000) { var d = Math.sqrt(d2) || 1, f = (95 - d) / 95 * 2.2; n.x += dx / d * f; n.y += dy / d * f; }
      }
      for (var k = 0; k < 3; k++) {
        for (var j = 0; j < links.length; j++) {
          var L = links[j], ddx = L.b.x - L.a.x, ddy = L.b.y - L.a.y;
          var dist = Math.sqrt(ddx * ddx + ddy * ddy) || 1;
          if (dist <= L.len) continue; // net twine only resists stretching
          var diff = (dist - L.len) / dist * 0.5;
          if (!L.a.pin) { L.a.x += ddx * diff; L.a.y += ddy * diff; }
          if (!L.b.pin) { L.b.x -= ddx * diff; L.b.y -= ddy * diff; }
        }
      }
    }

    function draw(t) {
      ctx.clearRect(0, 0, W, H);
      var reveal = reduceMotion ? rows : Math.min(rows, ((t - start) / 1400) * rows);
      ctx.lineWidth = 1;
      for (var r = 0; r < rows - 1; r++) {
        if (r > reveal) break;
        var fade = Math.max(0, 1 - r / (rows * 0.92));
        ctx.strokeStyle = "rgba(11,26,43," + (0.34 * fade * Math.min(1, reveal - r)).toFixed(3) + ")";
        ctx.beginPath();
        for (var j = 0; j < links.length; j++) {
          var L = links[j];
          if (L.a.row !== r) continue;
          ctx.moveTo(L.a.x, L.a.y); ctx.lineTo(L.b.x, L.b.y);
        }
        ctx.stroke();
      }
      // headrope + floats
      ctx.strokeStyle = "rgba(11,26,43,.75)"; ctx.lineWidth = 2.2;
      ctx.beginPath(); ctx.moveTo(0, 26); ctx.lineTo(W, 26); ctx.stroke();
      for (var c = 1; c < cols; c += 3) {
        var n = nodes[c];
        ctx.fillStyle = "#e4572e";
        ctx.beginPath(); ctx.ellipse(n.x, 26, 12, 8, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "rgba(255,255,255,.35)";
        ctx.beginPath(); ctx.ellipse(n.x - 4, 23, 4, 2.2, 0, 0, Math.PI * 2); ctx.fill();
      }
    }

    function loop(t) {
      sim(t); draw(t);
      if (running) raf = requestAnimationFrame(loop);
    }
    function play() { if (!running && visible && !reduceMotion) { running = true; raf = requestAnimationFrame(loop); } }
    function pause() { running = false; cancelAnimationFrame(raf); }

    build();
    if (reduceMotion) { for (var i = 0; i < 240; i++) sim(0); draw(performance.now()); }
    else play();

    window.addEventListener("pointermove", function (e) {
      var r = canvas.getBoundingClientRect();
      mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    }, { passive: true });
    document.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
    var rt;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { build(); if (reduceMotion) { for (var i = 0; i < 240; i++) sim(0); draw(performance.now()); } }, 200);
    });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? play() : pause(); }).observe(wrap);
    }
    document.addEventListener("visibilitychange", function () { document.hidden ? pause() : play(); });
  }

  /* ==========================================================
     Category explorer (home)
     ========================================================== */
  var explorer = $(".explorer");
  if (explorer) {
    var items = $$(".explorer__item", explorer);
    var imgs = $$(".explorer__img", explorer);
    function activate(key) {
      items.forEach(function (it) { it.classList.toggle("is-active", it.dataset.key === key); });
      imgs.forEach(function (im) { im.classList.toggle("is-active", im.dataset.key === key); });
    }
    items.forEach(function (it) {
      var a = it.querySelector("a");
      it.addEventListener("mouseenter", function () { activate(it.dataset.key); });
      a.addEventListener("focus", function () { activate(it.dataset.key); });
      if (!canHover) {
        a.addEventListener("click", function (e) {
          if (!it.classList.contains("is-active")) { e.preventDefault(); activate(it.dataset.key); }
        });
      }
    });
    if (items[0]) activate(items[0].dataset.key);
  }

  /* ==========================================================
     Products hub filter
     ========================================================== */
  var filters = $$(".filter");
  if (filters.length) {
    filters.forEach(function (f) {
      f.addEventListener("click", function () {
        var g = f.dataset.filter;
        filters.forEach(function (x) { x.setAttribute("aria-pressed", String(x === f)); });
        $$(".hub .card").forEach(function (c) {
          var show = g === "all" || (c.dataset.group || "").split(" ").indexOf(g) > -1;
          c.classList.toggle("is-hidden", !show);
        });
      });
    });
  }

  /* ==========================================================
     Rope timeline (about) — rope draws as you scroll
     ========================================================== */
  var tl = $(".timeline");
  if (tl) {
    var paths = $$(".timeline__rope path", tl);
    function sizeRope() {
      var h = tl.offsetHeight;
      var d = "M12 0";
      for (var y = 0; y < h; y += 40) d += " Q " + (y / 40 % 2 ? 20 : 4) + " " + (y + 20) + " 12 " + (y + 40);
      paths.forEach(function (p) { p.setAttribute("d", d); });
      var svg = $(".timeline__rope svg", tl);
      svg.setAttribute("viewBox", "0 0 24 " + h);
      var len = paths[0].getTotalLength();
      paths[0].style.strokeDasharray = len; paths[0].dataset.len = len;
      updateRope();
    }
    function updateRope() {
      var r = tl.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, (window.innerHeight * 0.65 - r.top) / r.height));
      var len = +paths[0].dataset.len;
      paths[0].style.strokeDashoffset = reduceMotion ? 0 : len * (1 - p);
    }
    sizeRope();
    window.addEventListener("scroll", updateRope, { passive: true });
    window.addEventListener("resize", sizeRope);
  }

  /* ---------- gallery filmstrip arrows ---------- */
  $$(".gallery-wrap").forEach(function (w) {
    var strip = $(".gallery", w);
    var btns = $$(".gnav", w);
    function update() {
      var max = strip.scrollWidth - strip.clientWidth - 2;
      btns[0].disabled = strip.scrollLeft <= 2;
      btns[1].disabled = strip.scrollLeft >= max;
      $(".gallery-nav", w).hidden = max <= 0;
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        strip.scrollBy({ left: +b.dataset.dir * strip.clientWidth * 0.8, behavior: reduceMotion ? "auto" : "smooth" });
      });
    });
    strip.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    window.addEventListener("load", update);
    update();
  });

  /* ==========================================================
     Gallery lightbox
     ========================================================== */
  var lb = $(".lightbox");
  if (lb && typeof lb.showModal === "function") {
    $$(".gallery__item").forEach(function (g) {
      g.addEventListener("click", function () {
        var img = g.querySelector("img");
        $("img", lb).src = img.dataset.full || img.src;
        $("img", lb).alt = img.alt;
        $("p", lb).textContent = img.alt;
        lb.showModal();
      });
      g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); g.click(); } });
    });
    $(".lightbox__close", lb).addEventListener("click", function () { lb.close(); });
    lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
  }

  /* ==========================================================
     Open-now indicator (Colombo time, UTC+5:30)
     ========================================================== */
  $$(".open-now").forEach(function (el) {
    var now = new Date();
    var col = new Date(now.getTime() + (now.getTimezoneOffset() + 330) * 60000);
    var d = col.getDay(), m = col.getHours() * 60 + col.getMinutes();
    var open = (d >= 1 && d <= 5 && m >= 540 && m < 1020) || (d === 6 && m >= 540 && m < 780);
    el.classList.toggle("is-open", open);
    el.textContent = open ? "Open now in Colombo" : "Closed now — enquiries answered next working day";
  });

  /* ==========================================================
     Enquiry list
     ========================================================== */
  var KEY = "jpfs-enquiry";
  var list = store.get(KEY, []);
  var toast = $(".toast");
  var toastT;

  function saveList() { store.set(KEY, list); renderList(); }
  function inList(id) { return list.some(function (x) { return x.id === id; }); }
  function renderList() {
    $$(".qbtn__count").forEach(function (c) { c.textContent = list.length; c.setAttribute("data-count", list.length); });
    $$(".add-btn").forEach(function (b) {
      var on = inList(b.dataset.id);
      b.setAttribute("aria-pressed", String(on));
      var t = b.querySelector(".add-btn__t");
      if (t) t.textContent = on ? "In enquiry list" : (b.dataset.label || "Add to enquiry");
    });
    $$(".form__list").forEach(function (box) {
      var ul = box.querySelector("ul");
      ul.innerHTML = "";
      list.forEach(function (x) {
        var li = document.createElement("li");
        li.textContent = x.name;
        var rm = document.createElement("button");
        rm.type = "button"; rm.setAttribute("aria-label", "Remove " + x.name); rm.textContent = "×";
        rm.addEventListener("click", function () { list = list.filter(function (y) { return y.id !== x.id; }); saveList(); });
        li.appendChild(rm); ul.appendChild(li);
      });
      box.classList.toggle("show", list.length > 0);
    });
  }
  function showToast(msg, href) {
    if (!toast) return;
    toast.querySelector("span").textContent = msg;
    var a = toast.querySelector("a");
    if (href) { a.href = href; a.hidden = false; } else a.hidden = true;
    toast.classList.add("show");
    clearTimeout(toastT);
    toastT = setTimeout(function () { toast.classList.remove("show"); }, 3800);
  }
  $$(".add-btn").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      var id = b.dataset.id;
      if (inList(id)) {
        list = list.filter(function (x) { return x.id !== id; });
        showToast(b.dataset.name + " removed from your enquiry list");
      } else {
        list.push({ id: id, name: b.dataset.name });
        showToast(b.dataset.name + " added to your enquiry list", b.dataset.contact);
        $$(".qbtn").forEach(function (q) { q.classList.remove("bump"); void q.offsetWidth; q.classList.add("bump"); });
      }
      saveList();
    });
  });
  renderList();

  /* ==========================================================
     Enquiry forms
     Sends via a form endpoint when one is configured in data-endpoint;
     otherwise opens the visitor's email app with the enquiry written out.
     ========================================================== */
  $$("form[data-enquiry]").forEach(function (form) {
    var status = form.querySelector(".form__status");
    var preset = new URLSearchParams(location.search).get("product");
    var sel = form.querySelector("[name=interest]");
    if (preset && sel) { $$("option", sel).forEach(function (o) { if (o.value === preset) sel.value = preset; }); }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fd = new FormData(form);
      if (list.length) fd.set("enquiry_list", list.map(function (x) { return x.name; }).join(", "));
      var lines = [];
      var labels = { buyer: "I am", name: "Name", company: "Company / organisation", phone: "Phone", email: "Email", interest: "Product interest", enquiry_list: "Products on my list", quantity: "Quantity / sizes", message: "Message" };
      Object.keys(labels).forEach(function (k) { var v = fd.get(k); if (v) lines.push(labels[k] + ": " + v); });
      var body = lines.join("\n");
      var endpoint = form.getAttribute("data-endpoint");

      if (endpoint) {
        // Hidden honeypot: people never see it, spam bots fill it in
        if (fd.get("botcheck")) return;
        fd.delete("botcheck");
        var key = form.getAttribute("data-access-key");
        if (key) fd.set("access_key", key); // Web3Forms
        fd.set("subject", "Website enquiry from " + (fd.get("name") || "visitor") + (fd.get("interest") ? " — " + fd.get("interest") : ""));
        fd.set("from_name", "jpfernandoandsons.com");
        if (fd.get("email")) { fd.set("replyto", fd.get("email")); fd.set("_replyto", fd.get("email")); }
        var btn = form.querySelector("[type=submit]");
        btn.disabled = true;
        fetch(endpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
          .then(function (r) {
            return r.json().catch(function () { return {}; }).then(function (data) {
              // Web3Forms reports failures as success:false in the body
              if (!r.ok || data.success === false) throw new Error(data.message || r.status);
            });
          })
          .then(function () {
            setStatus("Thank you — your enquiry has been sent. We reply during business hours (Mon–Fri 9:00–17:00, Sat 9:00–13:00).");
            form.reset(); list = []; saveList();
          })
          .catch(function () { setStatus("Sorry, the enquiry could not be sent. Please email " + CONTACT.email + " or call " + CONTACT.phone + "."); })
          .then(function () { btn.disabled = false; });
        return;
      }

      var subject = "Enquiry from " + (fd.get("name") || "website") + (fd.get("interest") ? " — " + fd.get("interest") : "");
      var href = "mailto:" + CONTACT.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body + "\n\n(Sent from jpfernandoandsons.com)");
      window.location.href = href;
      setStatus("Your email app should now open with this enquiry written out — just press send. If nothing opened, copy the text below and email it to " + CONTACT.email + ", or call " + CONTACT.phone + ".", body);
    });

    function setStatus(msg, copyText) {
      if (!status) return;
      status.innerHTML = "";
      var p = document.createElement("p"); p.style.margin = "0"; p.textContent = msg; status.appendChild(p);
      if (copyText) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "link-arrow"; b.style.marginTop = "10px"; b.textContent = "Copy enquiry text";
        b.addEventListener("click", function () {
          (navigator.clipboard ? navigator.clipboard.writeText(copyText) : Promise.reject())
            .then(function () { b.textContent = "Copied"; })
            .catch(function () { b.textContent = "Copy failed — select the text manually"; });
        });
        status.appendChild(b);
      }
      status.classList.add("show");
      status.setAttribute("tabindex", "-1");
      status.focus({ preventScroll: false });
    }
  });
})();
