"""Publish selected analysis documentation from independent local project folders.

Run after each project's analysis.py: python scripts/build_vibration_portfolio.py
Raw recordings, source code, test data and Git metadata are never copied.
"""
from pathlib import Path
import argparse
import json
import shutil
from html import escape

PORTFOLIO = Path(__file__).resolve().parents[1]
PROJECTS = [
    ('Pr06-Blind-Press-Vibration', 'press', 'One recording. Six ways to investigate vibration.',
     'A single press recording connects time-domain statistics, frequency content, modulation, repetition and a circular waveform view.',
     'Circular Plot + Vip_Analysis + Waterfall'),
    ('Pr07-Bearing-Vibration', 'bearing', 'From a dense recording to inspectable evidence.',
     'A reproducible analysis of the supplied bearing waveform, bringing spectral, envelope, cepstral and time-varying views into one project.',
     'Vip_Analysis + Waterfall'),
    ('Pr08-Rotor-Spectral-Diagnostics', 'rotor', 'Two channels. A signed spectral perspective.',
     'Full-spectrum analysis and channel-mean trends share one paired displacement recording, with explicit timing and interpretation limits.',
     'FullSpectrum + SCP')]


def page(title, body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Mahmoud Samhoud</title><meta name="description" content="{escape(title)}: input grouping, reproducible numerical analysis and measured results.">
<script src="../../js/theme-init.js"></script><link rel="icon" href="../../img/favicon.png">
<link rel="stylesheet" href="../../vendor/bootstrap-icons/bootstrap-icons.css"><link rel="stylesheet" href="../../css/main.css?v=gallery-20261118"><link rel="stylesheet" href="../../css/project-report.css"><link rel="stylesheet" href="../../css/analysis-report.css">
</head><body class="project-report analysis-report"><a class="skip-link" href="#content">Skip to project</a>
<header class="case-nav"><a class="case-brand" href="../../../index.html">MS<span> / Engineering portfolio</span></a><nav aria-label="Project navigation"><a href="../../../index.html#portfolio">All projects</a><a href="summary.html">Summary</a><a href="report.html">Full report</a></nav></header>
<main id="content">{body}</main><footer class="case-footer"><p>Mahmoud Samhoud <span> / Vibration analysis</span></p><a href="../../../index.html#portfolio">Back to selected work</a></footer><script src="../../js/main.js?v=gallery-20261118"></script></body></html>'''


def figure(file, alt, caption):
    return f'<figure><a href="{file}" target="_blank" rel="noopener"><img src="{file}" alt="{escape(alt)}" loading="lazy" decoding="async"></a><figcaption>{caption} Select the plot to inspect the full-size image.</figcaption></figure>'


def build(project_root):
    cards, modals = [], []
    for folder, slug, tagline, intro, sources in PROJECTS:
        root = project_root / folder
        r = json.loads((root/'outputs/results.json').read_text(encoding='utf-8'))
        config = json.loads((root/'project.json').read_text(encoding='utf-8'))
        paired = config['kind'] == 'paired'
        dest = PORTFOLIO/'assets/projects'/folder
        dest.mkdir(parents=True, exist_ok=True)
        selected = ['analysis-overview.png', 'cover.png']
        if not paired:
            selected.append('waterfall.png')
        if config.get('circular'):
            selected.append('circular.png')
        for file in selected:
            shutil.copy2(root/'outputs'/file, dest/file)
        title = r['title']
        peak = r['x_peak_bin_hz']
        results = (f'The strongest non-DC X-channel bin is <strong>{peak:,.3f} Hz</strong>. '
                   f'True RMS is <strong>{r["x"]["rms"]:.4f}</strong> and peak-to-peak is <strong>{r["x"]["peak_to_peak"]:.4f}</strong>, both in recorded units.')
        if paired:
            results += (f' The Y channel also peaks at {r["y_peak_bin_hz"]:.3f} Hz. '
                f'The largest signed-spectrum bin is {r["signed_peak_bin_hz"]:.3f} Hz under the X + iY convention. '
                f'The Y mean of {r["y"]["mean"]:.4f} is retained in the mean trend rather than removed by filtering.')
        else:
            results += (f' The default-band envelope spectrum peaks at {r["envelope_peak_bin_hz"]:.3f} Hz. '
                f'The time–frequency analysis uses {r["waterfall_windows"]} overlapping windows, with {r["waterfall_bin_hz"]:.3f} Hz bin spacing.')
        limits = ('The CSV gives 6,410.256 Hz from its recorded timestamps. The earlier orbit project established a 6,400 Hz reference from a separate workbook. '
                  'These plots use the CSV clock; the runner allows an explicit override and records it in the result. '
                  'No speed channel or DC sensor calibration is supplied. Channel means cannot establish absolute shaft position or a speed-dependent centerline. '
                  'Positive and negative frequencies follow X + iY; identifying physical whirl direction also requires sensor orientation and the machine rotation convention.' if paired else
                  'Amplitude calibration, confirmed machine metadata and bearing geometry are not supplied. All amplitudes are in recorded units. '
                  'The 100–500 Hz envelope band is inherited from the original scripts and remains an exploratory choice. '
                  'A spectral peak, an elevated crest factor or the name outerfaultdata.txt alone does not establish a bearing fault. '
                  'Waterfall windows trade frequency resolution for time resolution; their bin spacing differs from the full-record FFT.')
        hero = f'''<section class="case-hero"><p class="case-kicker">Signal processing / Python / Dataset-led project</p><h1>{title}<span>{tagline}</span></h1><p class="case-lead">{intro}</p><div class="case-tags"><span>One input dataset</span><span>{'Signed spectrum' if paired else 'FFT · Envelope · Cepstrum'}</span><span>13 numerical checks passed</span></div><div class="case-actions"><a class="case-button" href="#results">Explore the results</a><a href="summary.html">Read the summary</a></div></section>'''
        stats = f'''<dl class="case-stats"><div><dt>{r['samples']:,}</dt><dd>input samples</dd></div><div><dt>{r['sample_rate_hz']:,.3f} Hz</dt><dd>rate from recorded timestamps</dd></div><div><dt>{r['sample_span_s']:.3f} s</dt><dd>first-to-last sample span</dd></div><div><dt>{r['fft_bin_hz']:.4f} Hz</dt><dd>full-record FFT bin spacing</dd></div></dl>'''
        methods = ('''<tr><td>Individual channel spectra</td><td>Remove each channel mean, apply a Hann window and correct coherent gain. Use one-sided peak-amplitude normalization.</td></tr>
<tr><td>Signed full spectrum</td><td>Transform the complex signal X + iY and retain both positive and negative frequencies. No one-sided doubling is applied.</td></tr>
<tr><td>Channel-mean trends</td><td>Average unfiltered X and Y values in non-overlapping 0.25-second blocks. Retain DC offsets and label by elapsed time, not invented RPM.</td></tr>''' if paired else '''<tr><td>Waveform and statistics</td><td>Use all samples for mean, true RMS, AC RMS, crest factor, Pearson kurtosis and peak-to-peak range.</td></tr>
<tr><td>Amplitude spectrum</td><td>Mean removal, Hann window, coherent-gain correction and frequency bins derived from the complete transform length.</td></tr>
<tr><td>Real cepstrum</td><td>Inverse real FFT of log magnitude with a finite floor. Quefrency reveals repetition structure; it is not a direct fault label.</td></tr>
<tr><td>Envelope and spectrum</td><td>Fourth-order Butterworth bandpass in second-order sections, forward/backward filtering, Hilbert magnitude and edge exclusion before the envelope FFT.</td></tr>
<tr><td>Waterfall and time–frequency map</td><td>Recompute each Hann-windowed segment with 50% overlap. Plot coherent-gain-corrected amplitude; the heatmap uses dB relative to one recorded unit.</td></tr>''')
        grouping = (f'The input <strong>{escape(r["input"])}</strong> appears in {sources}. SHA-256 comparison confirmed identical copies; '
                    'these analyses are grouped in one project and the repository stores one canonical recording. '
                    + ('The existing Orbit Analyzer remains separate and unchanged; this project adds only the non-orbit FullSpectrum and SCP work.' if paired else
                       'The press and bearing recordings have different contents, so each receives its own repository even though their analysis methods overlap.'))
        corrections = ('The original full-spectrum formula mixed squared amplitudes in its cross term, and the SCP script applied different filters to one recording while assigning RPM labels. '
                       'The maintained implementation uses the complex transform directly and replaces that pseudo-speed sweep with measured channel means. '
                       'Original scripts remain available in the standalone repository for traceability.' if paired else
                       'The original helpers treated standard deviation as RMS, used an incorrect peak-to-peak expression for same-sign data, and reused one envelope-spectrum segment. '
                       'The maintained runner separates RMS from AC RMS, corrects range and FFT normalization, validates timing, and recomputes each time window. '
                       'It also replaces incomplete interactive waterfall calls with a repeatable analysis of the same input.')
        extra = ''
        if not paired:
            extra += figure('waterfall.png', 'Waterfall spectra computed from the supplied recording', 'Selected segment spectra show how frequency content changes across the recording. Up to 28 windows are drawn for readability; all windows remain in the repository export.')
        if config.get('circular'):
            extra += '<h3>A circular view with an explicit speed assumption</h3><p>The inherited 1,200 RPM setting maps the first cycle onto angle. Radius is normalized amplitude plus 1.25, so negative amplitudes do not become misleading negative polar radii. The final point is not forced to match the first. This is a circular waveform, not shaft-orbit analysis.</p>'
            extra += figure('circular.png', 'Circular waveform at assumed 1200 RPM', 'The 1,200 RPM value is an assumption from the source script; no tachometer channel was supplied.')
        body = hero + figure('cover.png', f'{title}: selected measured spectrum', 'Generated from the supplied recording using the maintained analysis runner.') + stats + f'''
<div class="case-layout"><aside class="case-toc"><p>IN THIS PROJECT</p><nav aria-label="Report sections"><a href="#input">Input and grouping</a><a href="#method">Analysis workflow</a><a href="#results">Results and plots</a><a href="#validation">Numerical checks</a><a href="#limits">Interpretation limits</a></nav></aside><article>
<section class="case-section" id="input"><h2>One recording, one project.</h2><p>{grouping}</p><div class="case-note"><strong>Source folders:</strong> {sources}<br><strong>Input:</strong> {escape(r['input'])}<br><strong>Identity:</strong> <code class="file-hash">{r['sha256']}</code></div><p>Timestamps are finite and strictly increasing. Maximum interval deviation from the mean spacing is {r['timestamp_jitter_fraction']*100:.6f}%; the loader accepts up to 1% to accommodate decimal rounding.</p></section>
<section class="case-section" id="method"><h2>A repeatable analysis workflow.</h2><p>Load and validate the recording, derive the clock from sample intervals, compute each analysis, then export plots and numerical tables from the same run.</p><div class="table-wrap"><table><thead><tr><th>View</th><th>Method</th></tr></thead><tbody>{methods}</tbody></table></div><h3>What changed from the source scripts</h3><p>{corrections}</p></section>
<section class="case-section" id="results"><h2>Results from the supplied data.</h2><p>{results}</p>{figure('analysis-overview.png', title+' analysis panels', 'Full analysis overview. Frequency peaks are FFT-bin measurements, not fitted estimates or machine diagnoses. Dense waveform displays are thinned; numerical processing uses every sample.')}{extra}</section>
<section class="case-section" id="validation"><h2>Check the methods against known answers.</h2><p>All 13 numerical checks passed for the maintained runner. Coverage includes known-amplitude sine waves, DC and Nyquist handling, odd-length transforms, RMS and range, zero-signal statistics, envelope modulation recovery, opposite signed rotations, changing frequencies across waterfall windows, offset retention, BOM input and invalid data rejection.</p><p>The supplied dataset also completed an end-to-end run. Source-file hashes, generated results and the test transcript are retained in the independent project repository. These checks establish the tested numerical behavior; they do not establish a machine fault diagnosis.</p><h3>Reproducible outputs</h3><p>The Python project includes its recording, preserved originals, dependency versions, a Windows launcher, tests, CSV exports and a JSON run summary. This portfolio contains the report and selected figures only.</p></section>
<section class="case-section" id="limits"><h2>Keep interpretation tied to the evidence.</h2><p>{limits}</p><p>Methods follow the documented <a href="https://numpy.org/doc/stable/reference/routines.fft.html">NumPy FFT conventions</a> and <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html">SciPy analytic-signal definition</a>.</p></section></article></div>'''
        (dest/'report.html').write_text(page(title, body), encoding='utf-8')
        summary = f'''<section class="case-hero"><p class="case-kicker">Project summary / Signal processing</p><h1>{title}<span>{tagline}</span></h1><p class="case-lead">{intro}</p><div class="case-actions"><a class="case-button" href="report.html">Read the full report</a></div></section>{figure('cover.png', title, 'Actual results from the supplied recording.')}{stats}<div class="summary-grid"><section><h2>Input and approach</h2><p>{grouping}</p></section><section><h2>Measured results</h2><p>{results}</p></section><section><h2>Validation</h2><p>13 numerical checks passed, plus a completed run on the supplied recording. Source and input provenance stay with the independent repository.</p></section><section><h2>Interpretation</h2><p>{limits}</p></section></div>'''
        (dest/'summary.html').write_text(page(title+' — Summary', summary), encoding='utf-8')
        url = f'assets/projects/{folder}'
        number = folder[2:4]
        cards.append(f'''<div class="col-lg-4 col-md-6 portfolio-item isotope-item filter-engineering-software" data-project="project-{slug}" role="button" tabindex="0" aria-haspopup="dialog" aria-controls="project-{slug}"><img loading="lazy" decoding="async" src="{url}/cover.png" class="img-fluid" alt="{title}: measured spectrum"><div class="portfolio-info"><span class="project-index">{number} / ENGINEERING SOFTWARE</span><h4>{title}<i class="bi bi-arrow-up-right" aria-hidden="true"></i></h4><p>{intro}</p><span class="project-open">Explore project</span></div></div>''')
        modals.append(f'''<div class="modal" id="project-{slug}" role="dialog" aria-modal="true" aria-labelledby="project-{slug}-title" tabindex="-1"><div class="modal-content"><button type="button" class="close-modal" aria-label="Close project">&times;</button><div class="project-header"><h2 id="project-{slug}-title">{title}</h2><div class="project-meta"><span>Python</span><span>Vibration Analysis</span><span>NumPy / SciPy</span></div></div><div class="project-body"><div class="project-description"><h3>Project overview</h3><p>{intro}</p><h3>One input, connected analyses</h3><p>{grouping}</p><h3>Measured results</h3><p>{results}</p><div class="project-gallery"><a href="{url}/analysis-overview.png"><img class="gallery-img" src="{url}/cover.png" alt="{title} results" loading="lazy"></a></div></div><div class="project-details"><h3>Project details</h3><div class="detail-item"><h4>Dataset</h4><p>{r['samples']:,} samples · {r['sample_rate_hz']:,.3f} Hz</p></div><div class="detail-item"><h4>Validation</h4><p>13 numerical checks passed. Full recording processed.</p></div><div class="detail-item"><h4>Documentation</h4><p>Input grouping, method, results and limitations.</p><a class="view-report-btn" href="{url}/report.html">View Full Report</a></div></div></div></div></div>''')
    index = PORTFOLIO/'index.html'
    content = index.read_text(encoding='utf-8')
    import re
    content = re.sub(r'\s*<!-- VIBRATION CARDS START -->.*?<!-- VIBRATION CARDS END -->', '', content, flags=re.S)
    content = re.sub(r'\s*<!-- VIBRATION MODALS START -->.*?<!-- VIBRATION MODALS END -->', '', content, flags=re.S)
    marker = '            </div>\n            <!-- End Portfolio Container -->'
    assert content.count(marker) == 1
    content = content.replace(marker, '\n<!-- VIBRATION CARDS START -->\n'+'\n'.join(cards)+'\n<!-- VIBRATION CARDS END -->\n'+marker)
    content = content.replace('      <!-- Project Modals -->', '      <!-- Project Modals -->\n<!-- VIBRATION MODALS START -->\n'+'\n'.join(modals)+'\n<!-- VIBRATION MODALS END -->')
    index.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--projects-root', type=Path, default=Path('D:/Projects'))
    build(parser.parse_args().projects_root)
