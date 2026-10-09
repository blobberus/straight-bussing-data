// Shuttle movement viewer: a time x stop ("stringline") chart of every bus trip on a chosen day and route,
// plus latest-arrival tables. Plain JS, no build; reads the files the sync workflow writes under data/.
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const getJSON = (u) => fetch(u, { cache: "no-cache" }).then((r) => (r.ok ? r.json() : Promise.reject(new Error(u + " " + r.status))));
  const getText = (u) => fetch(u, { cache: "no-cache" }).then((r) => (r.ok ? r.text() : Promise.reject(new Error(u + " " + r.status))));
  let idx = null, net = { routes: {}, stops: {}, route_stops: {} };

  /** Minimal RFC 4180 CSV parser -> array of objects. */
  function parseCSV(text) {
    const rows = [];
    let row = [], f = "", q = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
      else if (c === '"') q = true;
      else if (c === ",") { row.push(f); f = ""; }
      else if (c === "\n" || c === "\r") { if (c === "\r" && text[i + 1] === "\n") i++; row.push(f); rows.push(row); row = []; f = ""; }
      else f += c;
    }
    if (f || row.length) { row.push(f); rows.push(row); }
    const head = rows.shift() || [];
    return rows.filter((r) => r.length > 1).map((r) => Object.fromEntries(head.map((h, i) => [h, r[i] ?? ""])));
  }
  const clock = (epoch) => new Date(epoch * 1000).toLocaleTimeString("en-US", { timeZone: "America/Chicago", hour: "numeric", minute: "2-digit", second: "2-digit" });
  const hourOf = (epoch) => Number(new Date(epoch * 1000).toLocaleString("en-US", { timeZone: "America/Chicago", hour: "numeric", hour12: false })) % 24;
  const chip = (rid, name) => {
    const r = net.routes[rid] || {}, color = /^#[0-9a-f]{6}$/i.test(r.color || "") ? r.color : "#555555";
    const txt = /^#[0-9a-f]{6}$/i.test(r.text_color || "") ? r.text_color : "#ffffff";
    return `<span class="chip" style="background:${color};color:${txt}">${esc(r.short || name || rid)}</span>`;
  };

  function readHash() {
    const h = new URLSearchParams(location.hash.slice(1));
    return { day: h.get("day"), route: h.get("route") };
  }
  function fillDays() {
    const sel = $("day"), want = readHash().day;
    sel.innerHTML = idx.days.slice().reverse().map((d) => `<option value="${esc(d.day)}">${esc(d.day)} (${d.rows.toLocaleString()} arrivals)</option>`).join("");
    if (want && idx.days.some((d) => d.day === want)) sel.value = want;
  }
  function fillRoutes() {
    const d = idx.days.find((x) => x.day === $("day").value);
    const sel = $("route"), want = readHash().route;
    const list = d ? Object.entries(d.routes).sort((a, b) => b[1].rows - a[1].rows) : [];
    sel.innerHTML = list.map(([name, r]) => `<option value="${esc(name)}">${esc(name)} (${r.rows})</option>`).join("");
    if (want && list.some(([n]) => n === want)) sel.value = want;
  }

  function draw(rows, rid, routeName) {
    const order = (net.route_stops[rid] || []).slice();
    if (order.length > 2 && order[0] === order[order.length - 1]) order.pop();
    const maxIdx = Math.max(order.length - 1, ...rows.map((r) => Number(r.stop_index) || 0));
    const t0 = Math.min(...rows.map((r) => +r.epoch)), t1 = Math.max(...rows.map((r) => +r.epoch));
    const W = 1000, L = 150, R = 16, T = 18, rowH = 22, H = T + (maxIdx + 1) * rowH + 30;
    const x = (t) => L + ((t - t0) / Math.max(60, t1 - t0)) * (W - L - R), y = (i) => T + i * rowH + rowH / 2;
    const r = net.routes[rid] || {}, color = /^#[0-9a-f]{6}$/i.test(r.color || "") ? r.color : "#0066d6";
    let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">`;
    for (let i = 0; i <= maxIdx; i++) {
      const name = net.stops[order[i]]?.name || (i === order.length ? "(back at start)" : `stop ${i}`);
      svg += `<line class="grid" x1="${L}" x2="${W - R}" y1="${y(i)}" y2="${y(i)}"/><text class="axis" x="${L - 6}" y="${y(i) + 4}" text-anchor="end">${esc(name.length > 24 ? name.slice(0, 23) + "…" : name)}</text>`;
    }
    for (let t = Math.ceil(t0 / 3600) * 3600; t <= t1; t += 3600) {
      svg += `<line class="grid" x1="${x(t)}" x2="${x(t)}" y1="${T}" y2="${H - 26}"/><text class="axis" x="${x(t)}" y="${H - 10}" text-anchor="middle">${hourOf(t) % 12 || 12}${hourOf(t) < 12 ? "a" : "p"}</text>`;
    }
    const trips = new Map();
    for (const a of rows) { const k = a.trip_id + "|" + a.vehicle_id; (trips.get(k) || trips.set(k, []).get(k)).push(a); }
    let nSeg = 0;
    for (const list of trips.values()) {
      list.sort((a, b) => a.epoch - b.epoch);
      let seg = [];
      const flush = () => { if (seg.length > 1) { svg += `<polyline class="trip" stroke="${color}" points="${seg.map((p) => x(+p.epoch).toFixed(1) + "," + y(+p.stop_index).toFixed(1)).join(" ")}"/>`; nSeg++; } seg = []; };
      for (const a of list) {
        const prev = seg[seg.length - 1];
        if (prev && (+a.epoch - +prev.epoch > 1800 || +a.stop_index < +prev.stop_index)) flush();
        seg.push(a);
      }
      flush();
    }
    for (const a of rows) {
      svg += `<circle class="dot" cx="${x(+a.epoch).toFixed(1)}" cy="${y(+a.stop_index).toFixed(1)}" r="3" fill="${color}"><title>${esc(a.stop_name)} · ${esc(clock(+a.epoch))} · bus ${esc(a.vehicle_id)} · trip ${esc(a.trip_id)}</title></circle>`;
    }
    $("chart").innerHTML = svg + "</svg>";
    $("chartTitle").innerHTML = `${chip(rid, routeName)} ${esc(routeName)}: ${trips.size} bus trip${trips.size === 1 ? "" : "s"}`;
    const buses = new Set(rows.map((a) => a.vehicle_id)).size;
    $("stats").textContent = `${rows.length.toLocaleString()} arrivals · ${buses} bus${buses === 1 ? "" : "es"} · ${clock(t0)} to ${clock(t1)} (Chicago time)`;
  }

  function tableRows(rows, withRoute) {
    return rows.map((a) => `<tr><td>${esc(clock(+a.epoch))}</td>${withRoute ? `<td>${chip(a.route_id, a.route_name)} ${esc(a.route_name)}</td>` : ""}<td>${esc(a.stop_name)}</td><td>${esc(a.vehicle_id)}</td>${withRoute ? "" : `<td>${esc(a.trip_id)}</td><td>${a.segment_s ? esc(Math.round(a.segment_s)) + " s" : ""}</td>`}</tr>`).join("");
  }

  async function show() {
    const d = idx.days.find((x) => x.day === $("day").value), name = $("route").value, r = d?.routes[name];
    if (!r) { $("chart").innerHTML = "<p class='hint'>No data for this choice.</p>"; return; }
    history.replaceState(null, "", "#day=" + encodeURIComponent(d.day) + "&route=" + encodeURIComponent(name));
    $("csv").href = r.file;
    $("chart").innerHTML = "<p class='hint'>Loading&hellip;</p>";
    try {
      const rows = parseCSV(await getText(r.file)).filter((a) => a.epoch);
      draw(rows, r.route_id, name);
      $("routeTable").tBodies[0].innerHTML = tableRows(rows.slice(-50).reverse(), false);
    } catch (e) { $("chart").innerHTML = `<p class="hint">Couldn't load ${esc(r.file)}: ${esc(e.message)}</p>`; }
  }

  async function boot() {
    try {
      [idx, net.routes, net.stops, net.route_stops] = await Promise.all([getJSON("data/index.json"),
        getJSON("data/network/routes.json").catch(() => ({})), getJSON("data/network/stops.json").catch(() => ({})),
        getJSON("data/network/route_stops.json").catch(() => ({}))]);
    } catch (e) { $("meta").textContent = "No data yet: the first sync has not run."; return; }
    $("meta").textContent = `${idx.rows.toLocaleString()} arrivals over ${idx.days.length} service days · newest arrival ${idx.newest || "none"} (Chicago time) · last sync ${idx.synced} UTC · updates every 30 minutes`;
    fillDays(); fillRoutes(); show();
    $("day").addEventListener("change", () => { fillRoutes(); show(); });
    $("route").addEventListener("change", show);
    getText("data/latest.csv").then((t) => { $("latestTable").tBodies[0].innerHTML = tableRows(parseCSV(t).slice(-25).reverse(), true); }).catch(() => {});
  }
  boot();
})();
