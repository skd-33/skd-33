import json, os, urllib.request as ur
U = "skd-33"
C, BG, CARD, LINE, G1 = "#ff9f43", "#120a14", "#1a0f1c", "#5a3a2a", "#ff4d6d"
LO, HI = "#4a1d3a", "#ffb347"
F = 'font-family="monospace"'
os.makedirs("assets", exist_ok=True)

def get(p):
    r = ur.Request("https://api.github.com/" + p, headers={"Authorization": "Bearer " + os.environ.get("GITHUB_TOKEN", "")})
    return json.load(ur.urlopen(r))
user, repos = get(f"users/{U}"), get(f"users/{U}/repos?per_page=100")
stars = sum(r["stargazers_count"] for r in repos)

def w(name, s): open(f"assets/{name}.svg", "w", encoding="utf-8").write(s)

def svg(wd, h, body, bg=True):
    r = f'<rect width="{wd}" height="{h}" fill="{BG}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{wd}" height="{h}">{r}{body}</svg>'

def card(cw, h, rows):
    b = f'<polygon points="1,1 {cw-15},1 {cw-1},15 {cw-1},{h-1} 1,{h-1}" fill="{CARD}" stroke="{C}"/>'
    b += f'<path d="M{cw-15},1 L{cw-1},15" stroke="{C}" stroke-width="3"/>'
    y = 28
    for t, s, c, bold in rows:
        wt = ' font-weight="bold"' if bold else ""
        b += f'<text x="14" y="{y}" fill="{c}" {F} font-size="{s}"{wt}>{t}</text>'
        y += s + 10
    return svg(cw, h, b)

def section(name, n):
    return svg(800, 50, f'<text x="10" y="30" fill="{C}" {F} font-size="24" font-weight="bold">~/{name}</text>'
               f'<text x="790" y="30" fill="#887" {F} font-size="14" text-anchor="end">// {n:02d}</text>'
               f'<rect x="10" y="40" width="780" height="1" fill="{LINE}"/><rect x="10" y="39" width="100" height="3" fill="{C}"/>')

# header
t = "SOURABH KUMAR DUBEY"
g = lambda dx, c: f'<text x="{30+dx}" y="90" fill="{c}" {F} font-size="40" font-weight="bold">{t}</text>'
lines = ["CSE student · competitive programmer",
         "C / C++ / Python · computer vision · networks",
         f'building things at <tspan fill="{C}" font-weight="bold">skd-33</tspan>']
w("header", svg(800, 245,
    f'<rect width="800" height="245" fill="none" stroke="{C}" stroke-width="2"/>'
    f'<text x="30" y="35" fill="#2ecc40" {F} font-size="14">$ whoami</text>'
    + g(-3, G1) + g(3, C) + g(0, "#fff4e8")
    + "".join(f'<text x="30" y="{130+i*25}" fill="#bba" {F} font-size="16"><tspan fill="{C}">&gt;&gt;</tspan> {l}</text>'
              for i, l in enumerate(lines))
    + f'<text x="30" y="222" fill="#2ecc40" {F} font-size="16">$</text>'
    + '<rect x="46" y="208" width="9" height="17" fill="#2ecc40">'
      '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect>'))

for i, n in enumerate(["links", "stats", "city", "projects", "stack"], 1):
    w(f"sec-{n}", section(n, i))

# links
for f, n, h in [("leetcode", "LeetCode", "skd-33"), ("codeforces", "Codeforces", "sourabhkumardubey200"), ("github", "GitHub", "skd-33"), ("x", "X", "skd_33"), ("dev", "DEV", "ab_33")]:
    w(f"link-{f}", card(160, 80, [(n, 16, C, True), ("@" + h[:18], 11, "#998", False)]))

# stats
for k, (lab, v) in {"stars": ("TOTAL STARS", stars), "repos": ("REPOS", user["public_repos"]),
                    "followers": ("FOLLOWERS", user["followers"]), "following": ("FOLLOWING", user["following"])}.items():
    w(f"stat-{k}", card(200, 90, [(lab, 12, "#a98", False), (str(v), 30, C, True)]))

# projects: (file, title, line1, line2, stack)
projects = [
    ("buildfolio", "BuildFolio", "Portfolio builder made", "as a gift for a friend.", "Web"),
    ("dpi", "Deep Packet Inspection", "Network traffic inspection system", "in C++. Currently building it.", "C++ · Networks · In progress"),
("vision", "Obstacle Detection", "College team project: obstacle alerts", "for the visually impaired. I was a part.", "YOLO · PyTorch · Team project"),
    ("chess", "Chess Square Game", "Guess the square from", "the board coordinates.", "Python"),
]
for f, tt, a1, b1, s in projects:
    w(f"card-{f}", card(400, 130, [(tt, 18, C, True), (a1, 13, "#bba", False), (b1, 13, "#bba", False), (s, 12, "#a98", False)]))

# stack
rows = [("Languages", "C, C++, Python"), ("AI / CV", "PyTorch, YOLO, Ultralytics"), ("Web", "Three.js"), ("Tools", "Git")]
w("stack", svg(800, 130, "".join(
    f'<text x="20" y="{30+i*30}" fill="{C}" {F} font-size="15" font-weight="bold">{a1}</text>'
    f'<text x="170" y="{30+i*30}" fill="#bba" {F} font-size="15">{b1}</text>' for i, (a1, b1) in enumerate(rows))))

w("footer", svg(800, 50, f'<text x="10" y="30" fill="#2ecc40" {F} font-size="14">$ Connection closed.</text>'))

# contribution city
# contribution city
import random, datetime
random.seed(7)
def mix(a, b, t):
    a, b = [tuple(int(x[i:i+2], 16) for i in (1, 3, 5)) for x in (a, b)]
    return "#%02x%02x%02x" % tuple(int(p + (q - p) * t) for p, q in zip(a, b))

q = '{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}' % U
tok = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN", "")
req = ur.Request("https://api.github.com/graphql", json.dumps({"query": q}).encode(), {"Authorization": "Bearer " + tok})
cal = json.load(ur.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]

N, a, b, ox, oy, A, B = 19, 10, 5, 400, 110, 7, 3.5
days = [(d["date"], d["contributionCount"]) for wk in cal["weeks"] for d in wk["contributionDays"]][-N * N:][::-1]
cells = sorted(((x, y) for x in range(N) for y in range(N)), key=lambda p: (p[0] - 9) ** 2 + (p[1] - 9) ** 2)
grid = {c: (days[k] if k < len(days) else ("", 0)) for k, c in enumerate(cells)}
mx = max(c for _, c in days) or 1
best = max(days, key=lambda d: d[1])
bd = datetime.datetime.strptime(best[0], "%Y-%m-%d").strftime("%b %d") if best[0] else "-"

def poly(pts, fill):
    return '<polygon points="%s" fill="%s"/>' % (" ".join("%s,%s" % p for p in pts), fill)

out = "".join(f'<circle cx="{random.randint(0,800)}" cy="{random.randint(0,200)}" r="{random.choice([.6,.9,1.2])}" fill="#fff4e8" opacity="{random.choice([.3,.5,.8])}"/>' for _ in range(70))
out += f'<circle cx="90" cy="70" r="18" fill="#fff4e8"/><circle cx="99" cy="64" r="16" fill="{BG}"/>'
out += poly([(ox, oy - b - 6), (ox + N * a + 12, oy + (N - 1) * b), (ox, oy + (2 * N - 1) * b + 6), (ox - N * a - 12, oy + (N - 1) * b)], "#241a2a")
for (gx, gy), (_, c) in sorted(grid.items(), key=lambda kv: kv[0][0] + kv[0][1]):
    cx, cy = ox + (gx - gy) * a, oy + (gx + gy) * b
    if not c:
        if random.random() < .5:
            out += f'<circle cx="{cx}" cy="{cy-3}" r="3.2" fill="#2f9e5b"/><circle cx="{cx-1}" cy="{cy-4}" r="1.8" fill="#4fcf80"/>'
        continue
    h = 6 + 64 * (c / mx) ** 0.6
    col = mix(LO, HI, (c / mx) ** 0.6)
    L, R, P = mix(col, "#000000", .35), mix(col, "#000000", .55), mix(col, "#ffffff", .15)
    out += (poly([(cx - A, cy - h), (cx, cy - h + 2 * B), (cx, cy + 2 * B), (cx - A, cy)], L)
          + poly([(cx + A, cy - h), (cx, cy - h + 2 * B), (cx, cy + 2 * B), (cx + A, cy)], R)
          + poly([(cx, cy - h - B), (cx + A, cy - h), (cx, cy - h + B), (cx - A, cy - h)], P))
    for yy in range(5, int(h) - 2, 6):
        for u in (.3, .7):
            if random.random() < .4:
                out += f'<rect x="{cx-A+A*u:.1f}" y="{cy-h+2*B*u+yy:.1f}" width="1.6" height="1.8" fill="#ffd479"/>'
            if random.random() < .3:
                out += f'<rect x="{cx+A*u:.1f}" y="{cy-h+2*B-2*B*u+yy:.1f}" width="1.6" height="1.8" fill="#ffd479"/>'

txt = lambda y, s: f'<text x="785" y="{y}" fill="#bba" {F} font-size="13" text-anchor="end">{s}</text>'
out += (f'<text x="14" y="26" fill="#2ecc40" {F} font-size="14">$ render-city --blocks <tspan fill="#887"># last 365 days, downtown is latest</tspan></text>'
        + txt(70, f'<tspan fill="{G1}" font-weight="bold">{cal["totalContributions"]}</tspan> contributions')
        + txt(92, f'<tspan fill="{G1}" font-weight="bold">{user["public_repos"]}</tspan> repos')
        + txt(114, f'busiest day <tspan fill="#fff4e8" font-weight="bold">{bd} · {best[1]}</tspan>')
        + f'<text x="14" y="362" fill="#887" {F} font-size="12">quiet</text>'
        + "".join(f'<rect x="{55+i*16}" y="351" width="12" height="12" fill="{mix(LO, HI, i/4)}"/>' for i in range(5))
        + f'<text x="142" y="362" fill="#887" {F} font-size="12">skyscraper</text>')
w("contribution-city", svg(800, 380, out))