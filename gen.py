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
w("header", svg(800, 210,
    f'<rect width="800" height="210" fill="none" stroke="{C}" stroke-width="2"/>'
    f'<text x="30" y="35" fill="#2ecc40" {F} font-size="14">$ whoami</text>'
    + g(-3, G1) + g(3, C) + g(0, "#fff4e8")
    + "".join(f'<text x="30" y="{130+i*25}" fill="#bba" {F} font-size="16"><tspan fill="{C}">&gt;&gt;</tspan> {l}</text>'
              for i, l in enumerate(lines))))

for i, n in enumerate(["links", "stats", "city", "projects", "stack"], 1):
    w(f"sec-{n}", section(n, i))

# links
for f, n, h in [("leetcode", "LeetCode", "skd-33"), ("codeforces", "Codeforces", "sourabhkumardubey200"), ("github", "GitHub", "skd-33"), ("x", "X", "skd_33")]:
    w(f"link-{f}", card(160, 80, [(n, 16, C, True), ("@" + h[:18], 11, "#998", False)]))

# stats
for k, (lab, v) in {"stars": ("TOTAL STARS", stars), "repos": ("REPOS", user["public_repos"]),
                    "followers": ("FOLLOWERS", user["followers"]), "following": ("FOLLOWING", user["following"])}.items():
    w(f"stat-{k}", card(200, 90, [(lab, 12, "#a98", False), (str(v), 30, C, True)]))

# projects: (file, title, line1, line2, stack)
projects = [
    ("buildfolio", "BuildFolio", "Portfolio builder for", "friends. Hacktoberfest entry.", "DEV Challenge"),
    ("dpi", "Deep Packet Inspection", "Network traffic inspection", "system built in C++.", "C++ · Networks"),
    ("vision", "Obstacle Detection", "Smartphone obstacle alerts", "for the visually impaired.", "YOLO · PyTorch"),
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
def mix(a, b, t):
    a, b = [tuple(int(x[i:i+2], 16) for i in (1, 3, 5)) for x in (a, b)]
    return "#%02x%02x%02x" % tuple(int(p + (q - p) * t) for p, q in zip(a, b))

q = '{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount weekday}}}}}}' % U
tok = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN", "")
req = ur.Request("https://api.github.com/graphql", json.dumps({"query": q}).encode(), {"Authorization": "Bearer " + tok})
cal = json.load(ur.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]

tiles = [(i, d["weekday"], d["contributionCount"]) for i, wk in enumerate(cal["weeks"]) for d in wk["contributionDays"]]
mx = max(c for _, _, c in tiles) or 1
A, B, ox, oy = 9, 4.5, 70, 120
def poly(pts, fill):
    return '<polygon points="%s" fill="%s"/>' % (" ".join("%s,%s" % p for p in pts), fill)
out = ""
for i, j, c in sorted(tiles, key=lambda t: (t[0] + t[1], t[0])):
    cx, cy = ox + (i - j) * 10, oy + (i + j) * 5
    h = 2 + 80 * c / mx if c else 2
    col = mix(LO, HI, c / mx) if c else "#2a2030"
    L, R, P = mix(col, "#000000", .35), mix(col, "#000000", .55), mix(col, "#ffffff", .15)
    out += (poly([(cx - A, cy - h), (cx, cy - h + B * 2), (cx, cy + B * 2), (cx - A, cy)], L)
          + poly([(cx + A, cy - h), (cx, cy - h + B * 2), (cx, cy + B * 2), (cx + A, cy)], R)
          + poly([(cx, cy - h - B), (cx + A, cy - h), (cx, cy - h + B), (cx - A, cy - h)], P))
w("contribution-city", svg(660, 430, out + f'<text x="14" y="26" fill="{C}" {F} font-size="14">{cal["totalContributions"]} contributions in the last year</text>'))