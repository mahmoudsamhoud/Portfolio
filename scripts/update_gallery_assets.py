from pathlib import Path
root = Path(__file__).resolve().parents[1]
paths = [root/'index.html', *root.glob('assets/projects/Pr04-Orbit-Analyzer/*.html')]
for p in paths:
    s = p.read_text(encoding='utf-8')
    s = s.replace('js/main.js"', 'js/main.js?v=gallery-20261118"')
    s = s.replace('css/main.css"', 'css/main.css?v=gallery-20261118"')
    p.write_text(s,encoding='utf-8')
p=root/'assets/projects/Pr04-Orbit-Analyzer/build_portfolio.py'
s=p.read_text(encoding='utf-8').replace('js/main.js"','js/main.js?v=gallery-20261118"').replace('css/main.css"','css/main.css?v=gallery-20261118"')
p.write_text(s,encoding='utf-8')
