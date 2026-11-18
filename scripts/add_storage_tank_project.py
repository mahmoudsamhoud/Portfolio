"""Build the Storage Tank Design Tool portfolio entry from the supplied revision."""
from pathlib import Path
from html import escape
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/projects/Pr05-Storage-Tank-Design-Tool'
SOURCE = Path('E:/ENPPI/StorageTankDesignTool/Rev.03/Storage_Tank_Design_Tool_API650.html')
APP = SOURCE.name
OUT.mkdir(exist_ok=True)
shutil.copy2(SOURCE, OUT / APP)

# Original editorial artwork, explicitly distinguished from an application capture.
(OUT/'tank-overview.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" role="img" aria-labelledby="title desc">
<title id="title">Storage Tank Design Tool</title><desc id="desc">Portfolio illustration of a storage tank elevation and plan, not a design drawing or application screenshot.</desc>
<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#254052" stroke-width=".7"/></pattern></defs>
<rect width="1440" height="900" fill="#101e2d"/><rect width="1440" height="900" fill="url(#grid)"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="80" y="90" fill="#6dd6cf" font-size="22" letter-spacing="4">STATIC EQUIPMENT / ENGINEERING SOFTWARE</text>
<text x="80" y="166" fill="#f0f6fa" font-size="54" font-weight="700">Storage Tank Design Tool</text><text x="82" y="212" fill="#a9bdce" font-size="25">Design inputs. Calculation checks. Drawing outputs.</text>
<g fill="none" stroke="#8bc9d8" stroke-width="3"><path d="M170 405L475 320L780 405V710H170Z"/><path d="M170 466H780M170 527H780M170 588H780M170 649H780" stroke="#527b90"/><path d="M145 715H805M475 320V710"/><path d="M170 445H780" stroke="#67d7cc" stroke-dasharray="10 8"/><path d="M130 405V710M119 405H141M119 710H141M170 752H780M170 740V764M780 740V764"/><circle cx="1100" cy="530" r="157"/><circle cx="1100" cy="530" r="146" stroke="#527b90"/><path d="M920 530H1280M1100 350V710" stroke="#527b90" stroke-dasharray="9 8"/><path d="M1257 530H1305V555H1260M770 625H820V655H780"/></g>
<text x="360" y="798" fill="#a9bdce" font-size="21">TANK ELEVATION</text><text x="1040" y="748" fill="#a9bdce" font-size="21">PLAN VIEW</text>
<text x="80" y="860" fill="#6dd6cf" font-size="18">API 650 · 13th Edition basis</text><text x="895" y="860" fill="#a9bdce" font-size="16">PROJECT ILLUSTRATION · NOT TO SCALE</text></g></svg>''',encoding='utf-8')

def figure():
    return '<figure><a href="tank-overview.svg"><img src="tank-overview.svg" width="1440" height="900" alt="Storage tank elevation and plan: portfolio illustration, not an application screenshot" loading="lazy"></a><figcaption>Project illustration. The application generates its own drawing from the entered design data. Select to enlarge.</figcaption></figure>'

def page(title, body, summary=False):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} | Mahmoud Samhoud</title><meta name="description" content="A browser-based storage tank design workflow with calculation checks, nozzle reinforcement, drawings and reports."><script src="../../js/theme-init.js"></script><link rel="icon" href="../../img/favicon.png"><link rel="stylesheet" href="../../css/main.css?v=gallery-20261118"><link rel="stylesheet" href="../../css/project-report.css"></head>
<body class="project-report"><a class="skip-link" href="#content">Skip to project</a><header class="case-nav"><a class="case-brand" href="../../../index.html">MS<span> / Engineering portfolio</span></a><nav aria-label="Project navigation"><a href="../../../index.html#portfolio">All projects</a><a href="{'work-05.html' if summary else 'summary.html'}">{'Full report' if summary else 'Project summary'}</a></nav></header><main id="content">{body}</main><footer class="case-footer"><p>Hesham Fouad &amp; Mahmoud Samhoud <span> / Static equipment engineering</span></p><a href="../../../index.html#portfolio">Back to selected work</a></footer><script src="../../js/main.js?v=gallery-20261118"></script></body></html>'''

hero=f'''<section class="case-hero"><p class="case-kicker">Static equipment / Engineering software / Rev.03</p><h1>Storage Tank Design Tool<span>From design basis<br>to calculation and drawing.</span></h1><p class="case-lead">A standalone browser application that brings tank configuration, engineering checks, nozzle reinforcement and documentation into one workflow.</p><div class="case-tags"><span>API 650 · 13th Edition basis</span><span>HTML / CSS / JavaScript</span><span>SI &amp; US Customary</span></div><div class="case-actions"><a class="case-button" href="{APP}">Open design tool</a><a href="#overview">Explore the project</a></div></section>'''
credits='<p>Developed by <strong>Eng. Hesham Fouad and Eng. Mahmoud Samhoud</strong>, Static Equipment Engineers, Pressure Vessels Department – ENPPI, as credited in the supplied application.</p>'
sections=[
('overview','One design basis, connected outputs', '<p>Storage-tank design involves related decisions about geometry, liquid levels, materials, loads, plate thicknesses and structural details. This tool connects those inputs to a calculation summary, a detailed report, a data sheet and a general-arrangement sketch.</p>'+credits+'<p>The supplied revision identifies its calculation basis as API 650, 13th Edition, March 2020. This project page describes the implementation; it does not certify code compliance.</p>'),
('workflow','A guided engineering workflow','''<ol class="steps"><li><h3>Establish the project</h3><p>Enter document identifiers and engineering metadata, choose SI or US Customary units, or use the ITSdesign report reader to populate supported inputs.</p></li><li><h3>Define the tank</h3><p>Set dimensions, shell courses, liquid levels, specific gravity, pressures, temperature, material family, roof arrangement and environmental loads.</p></li><li><h3>Develop the details</h3><p>Configure bottom plates, compression-ring details, roof supports, stiffening rings, anchorage and nozzles.</p></li><li><h3>Review calculations and notes</h3><p>Inspect required versus provided values, clause references, check status and applicability notes. Review failures before exporting results.</p></li><li><h3>Prepare deliverables</h3><p>Generate the sketch, review the calculation report and data sheet, then save project data or export the required output.</p></li></ol>'''),
('scope','Calculation coverage in the supplied source','''<div class="table-wrap"><table><thead><tr><th>Area</th><th>Implemented workflow</th></tr></thead><tbody><tr><td>Shell</td><td>1-foot and variable-design-point methods, course thicknesses, corrosion allowances, material properties and applicability notes.</td></tr><tr><td>Bottom and roof</td><td>Bottom and annular plates; supported and self-supporting roof configurations; compression-ring details; floating-roof inputs.</td></tr><tr><td>Environmental loads</td><td>Wind and stiffening-ring checks, seismic options, anchorage, and internal/external pressure checks.</td></tr><tr><td>Materials</td><td>Carbon steel, austenitic stainless steel, duplex stainless steel and aluminium selections, with material-family and temperature handling.</td></tr><tr><td>Nozzles</td><td>Shell and roof nozzle inputs, reinforcement-area calculations and nozzle information for the drawing.</td></tr></tbody></table></div><p>Available settings depend on the selected tank configuration. The source includes notes and checks for combinations outside the implemented method’s scope.</p>'''),
('outputs','Reports and drawings from the same inputs','''<ul class="feature-list"><li><strong>Calculation report.</strong> Project title block, engineering sections, equations, clause references, check status and design notes, with browser print/PDF output.</li><li><strong>Data sheet.</strong> HTML and Excel outputs, including a tank sketch.</li><li><strong>General arrangement.</strong> Elevation, plan, liquid levels, internals, stair arrangement, nozzle schedule and compression-ring detail, controlled through drawing settings.</li><li><strong>Drawing exports.</strong> SVG, PNG, DXF and an AutoCAD 2000 DWG writer are implemented in the supplied file.</li><li><strong>Project continuity.</strong> Save/open controls, browser-local persistence and migration logic for older saved states.</li></ul>'''),
('implementation','A portable browser application','''<p>The application is packaged in one HTML file with embedded styling, JavaScript and supporting library code. No external script or stylesheet tags are required by the supplied file.</p><p>The source separates material and calculation functions, sketch geometry and export writers, report generation, input schemas, and interface state. The seven main tabs are General Information, Design Data, Tank Configuration, Tank Design, Shell Nozzle Reinforcement, Tank Sketch and Print Preview.</p><p>This portfolio includes an unchanged copy of Rev.03. The report describes the tool without reproducing its full source.</p>'''),
('review','Review status and engineering use','''<p>Portfolio integration checks cover the copied file, JavaScript syntax and local page links. They do not independently validate the engineering formulas, exported drawings or every configuration.</p><p>The application itself states that results need independent verification before use on project deliverables. Its stated scope does not include other code editions, API 653 or API 620; a method or edition should not be inferred from the availability of an import reader.</p>''')]
toc='<aside class="case-toc"><p>IN THIS PROJECT</p><nav aria-label="Report sections">'+''.join(f'<a href="#{key}">{escape(title)}</a>' for key,title,_ in sections)+'</nav></aside>'
body=hero+figure()+'<div class="case-layout">'+toc+'<article>'+''.join(f'<section class="case-section" id="{key}"><h2>{title}</h2>{text}</section>' for key,title,text in sections)+'</article></div>'
(OUT/'work-05.html').write_text(page('Storage Tank Design Tool — Full report',body),encoding='utf-8')
summary=hero+figure()+'<section class="case-section" id="overview"><h2>Project at a glance</h2>'+sections[0][2]+'</section><section class="case-section"><h2>From inputs to deliverables</h2>'+sections[3][2]+f'<div class="case-actions"><a class="case-button" href="work-05.html">Read the full report</a></div></section>'
(OUT/'summary.html').write_text(page('Storage Tank Design Tool — Summary',summary,True),encoding='utf-8')
(OUT/'README.md').write_text(f'''# Storage Tank Design Tool — API 650

Portfolio copy of the supplied Rev.03 application.

Developed by Eng. Hesham Fouad & Eng. Mahmoud Samhoud, Static Equipment Engineers, Pressure Vessels Department – ENPPI.

## Files
- `{APP}`: unchanged, standalone application. Open in a modern browser.
- `summary.html`: portfolio summary.
- `work-05.html`: complete portfolio report.
- `tank-overview.svg`: original portfolio illustration, not a UI screenshot or design drawing.

The report pages use shared assets in the parent portfolio. The application itself is self-contained.

## Scope
The source identifies API 650, 13th Edition (March 2020) as its design basis. Features include SI/USC units, tank configuration, shell/roof/bottom calculations, wind/seismic and anchorage checks, nozzle reinforcement, a report reader, drawing exports and Excel/print output.

Results require independent engineering verification before project use. Portfolio integration is not engineering certification. The GitHub repository has not yet been created.
''',encoding='utf-8')

p=ROOT/'index.html'; html=p.read_text(encoding='utf-8')
prefix='assets/projects/'+OUT.name+'/'
card=f'''<div class="col-lg-4 col-md-6 portfolio-item isotope-item filter-engineering-software filter-static-equipment" data-project="project-tank" role="button" tabindex="0" aria-haspopup="dialog" aria-controls="project-tank">
<img loading="lazy" decoding="async" src="{prefix}tank-overview.svg" class="img-fluid" alt="Storage Tank Design Tool — illustrated tank elevation and plan" />
<div class="portfolio-info"><span class="project-index">05 / STATIC EQUIPMENT</span><h4>Storage Tank Design Tool<i class="bi bi-arrow-up-right" aria-hidden="true"></i></h4><p>Tank configuration, engineering checks and drawing outputs in one browser application.</p><span class="project-open">Explore project</span></div></div>
'''
if 'data-project="project-tank"' not in html:
    marker='            </div>\n            <!-- End Portfolio Container -->'
    assert marker in html
    html=html.replace(marker,card+marker,1)
modal=f'''<div class="modal" id="project-tank" role="dialog" aria-modal="true" aria-labelledby="project-tank-title" tabindex="-1"><div class="modal-content"><button type="button" class="close-modal" aria-label="Close project">&times;</button>
<div class="project-header"><h2 id="project-tank-title">Storage Tank Design Tool — API 650</h2><div class="project-meta"><span>Static Equipment</span><span>Engineering Software</span><span>JavaScript</span></div></div>
<div class="project-body"><div class="project-description"><h3>Project Overview</h3><p>A standalone browser tool that connects storage-tank design inputs with engineering checks, nozzle reinforcement, reports and drawing exports.</p><h3>Engineering Workflow</h3><ul><li>SI and US Customary inputs with material and roof selections</li><li>Shell, bottom, roof, wind, seismic and anchorage calculations</li><li>Clause-referenced check summaries and design notes</li><li>Excel data sheets, print/PDF reports and drawing exports</li></ul><h3>Development</h3>{credits}<div class="project-gallery"><h3>Project Illustration</h3><div class="gallery-grid"><a href="{prefix}tank-overview.svg"><img src="{prefix}tank-overview.svg" class="gallery-img" alt="Storage tank elevation and plan illustration, not an application screenshot" loading="lazy" /></a></div></div></div>
<div class="project-details"><h3>Project Details</h3><div class="detail-item"><h4>Design Basis</h4><p>API 650, 13th Edition (March 2020), as stated in the application</p></div><div class="detail-item"><h4>Tools Used</h4><p>HTML, CSS, JavaScript, SVG and browser-based exports</p></div><div class="detail-item"><h4>Revision</h4><p>Rev.03 · Standalone HTML application</p></div><div class="detail-item"><h4>Documentation</h4><p>Workflow, implemented features, outputs and review status.</p><a class="view-report-btn" href="{prefix}work-05.html">View Full Report</a></div></div></div></div></div>
'''
if 'id="project-tank"' not in html: html=html.replace('      <!-- Project Modals -->','      <!-- Project Modals -->\n'+modal,1)
p.write_text(html,encoding='utf-8')
print('Created',OUT)
