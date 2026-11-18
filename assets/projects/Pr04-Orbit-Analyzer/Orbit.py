"""Desktop UI. Run `python Orbit.py`; importing this module opens no windows."""
from pathlib import Path
import json
import os
import sys
# Some packaged Python runtimes cannot source Tcl scripts inside WindowsApps.
# Use a local copy when supplied in this virtual environment; ordinary Python
# installations continue to use their own Tcl/Tk without configuration.
_local_tcl = Path(sys.prefix) / 'tcl'
if (_local_tcl / 'tcl8.6' / 'init.tcl').is_file():
    os.environ.setdefault('TCL_LIBRARY', str(_local_tcl / 'tcl8.6'))
    os.environ.setdefault('TK_LIBRARY', str(_local_tcl / 'tk8.6'))
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Functions import load_data, sheet_names, analyze, export_csv


class OrbitApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Orbit Analyzer | Shaft vibration')
        width = min(1320, self.winfo_screenwidth() - 50)
        height = min(870, self.winfo_screenheight() - 120)
        self.geometry(f'{width}x{height}+20+20')
        self.minsize(1000, 640)
        self.configure(bg='#edf2f7')
        self.result = None
        self.path = tk.StringVar()
        self.sheet = tk.StringVar()
        self.fc = tk.StringVar(value='24.97')
        self.low = tk.StringVar(value='22')
        self.high = tk.StringVar(value='28')
        self.order = tk.StringVar(value='2')
        self.override = tk.BooleanVar(value=False)
        self.rate = tk.StringVar(value='6400')
        self.unit = tk.StringVar(value='µm')
        self.status = tk.StringVar(value='Open a three-column file: time (seconds), X displacement, Y displacement.')
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#edf2f7')
        style.configure('TLabel', background='#edf2f7', foreground='#14283f', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=7)
        style.configure('Title.TLabel', font=('Segoe UI', 23, 'bold'))
        style.configure('Accent.TButton', background='#176b87', foreground='white')
        outer = ttk.Frame(self, padding=18)
        outer.pack(fill='both', expand=True)
        ttk.Label(outer, text='Orbit Analyzer', style='Title.TLabel').pack(anchor='w')
        ttk.Label(outer, text='Inspect shaft motion · isolate the 1× band · verify the recording').pack(anchor='w', pady=(0, 12))
        source = ttk.Frame(outer)
        source.pack(fill='x')
        ttk.Button(source, text='Open CSV / XLSX', command=self.open_file).pack(side='left')
        ttk.Entry(source, textvariable=self.path, state='readonly').pack(side='left', fill='x', expand=True, padx=10)
        ttk.Label(source, text='Sheet').pack(side='left')
        self.sheets = ttk.Combobox(source, textvariable=self.sheet, state='disabled', width=19)
        self.sheets.pack(side='left', padx=(6, 0))
        controls = ttk.Frame(outer, padding=(0, 12))
        controls.pack(fill='x')
        for label, variable, width in [('1× (Hz)', self.fc, 9), ('Low (Hz)', self.low, 8), ('High (Hz)', self.high, 8), ('Order', self.order, 4), ('Units', self.unit, 6)]:
            ttk.Label(controls, text=label).pack(side='left', padx=(0, 5))
            ttk.Entry(controls, textvariable=variable, width=width).pack(side='left', padx=(0, 13))
        ttk.Checkbutton(controls, text='Override clock (Hz)', variable=self.override).pack(side='left')
        ttk.Entry(controls, textvariable=self.rate, width=9).pack(side='left', padx=6)
        ttk.Button(controls, text='Analyze', style='Accent.TButton', command=self.run_analysis).pack(side='right')
        self.summary = ttk.Label(outer, text='No recording analyzed yet.', font=('Segoe UI', 11, 'bold'))
        self.summary.pack(anchor='w', pady=(2, 10))
        self.tabs = ttk.Notebook(outer)
        self.tabs.pack(fill='both', expand=True)
        chart = ttk.Frame(self.tabs)
        checks = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(chart, text=' Orbits & spectrum ')
        self.tabs.add(checks, text=' Data & validation ')
        self.figure = Figure(figsize=(12, 5.5), dpi=100, facecolor='#ffffff', layout='constrained')
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        NavigationToolbar2Tk(self.canvas, chart).update()
        self.detail = tk.Text(checks, wrap='word', font=('Consolas', 11), bg='white', fg='#14283f', relief='flat')
        scroll = ttk.Scrollbar(checks, command=self.detail.yview)
        scroll.pack(side='right', fill='y')
        self.detail.configure(yscrollcommand=scroll.set)
        self.detail.pack(fill='both', expand=True)
        self.detail.configure(state='disabled')
        bottom = ttk.Frame(outer, padding=(0, 10, 0, 0))
        bottom.pack(fill='x')
        self.export = ttk.Button(bottom, text='Export CSV + report', command=self.save_data, state='disabled')
        self.export.pack(side='right')
        self.save_plot = ttk.Button(bottom, text='Save plot', command=self.save_figure, state='disabled')
        self.save_plot.pack(side='right', padx=8)
        ttk.Label(bottom, textvariable=self.status, wraplength=800).pack(side='left', fill='x', expand=True)
        self.figure.text(.5, .5, 'Open a recording to explore its orbit', ha='center', color='#52677c', fontsize=17)
        self.canvas.draw()
        for variable in [self.path, self.sheet, self.fc, self.low, self.high, self.order, self.override, self.rate, self.unit]:
            variable.trace_add('write', self.invalidate)

    def invalidate(self, *_):
        self.result = None
        self.export.configure(state='disabled')
        self.save_plot.configure(state='disabled')
        self.summary.configure(text='Inputs changed. Analyze to refresh results.')
        self.status.set('Results are not current. Click Analyze.')
        self.figure.clear()
        self.figure.text(.5, .5, 'Click Analyze to calculate current inputs', ha='center', fontsize=16)
        self.canvas.draw_idle()
        self.set_detail('No current analysis. Click Analyze to validate these inputs.')

    def set_detail(self, text):
        self.detail.configure(state='normal')
        self.detail.delete('1.0', 'end')
        self.detail.insert('1.0', text)
        self.detail.configure(state='disabled')

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('Orbit data', '*.csv *.xlsx'), ('CSV', '*.csv'), ('Excel', '*.xlsx')])
        if not path:
            return
        self.path.set(path)
        self.sheet.set('')
        self.sheets.configure(values=[], state='disabled')
        try:
            if Path(path).suffix.lower() == '.xlsx':
                names = sheet_names(path)
                self.sheets.configure(values=names, state='readonly')
                self.sheet.set(names[0])
            self.status.set('File selected. Confirm frequency, displacement units and timing, then Analyze.')
        except Exception as exc:
            messagebox.showerror('Cannot open workbook', str(exc))

    def run_analysis(self):
        self.invalidate()
        try:
            if not self.path.get():
                raise ValueError('Open a CSV or XLSX file first.')
            data, source_notes = load_data(self.path.get(), self.sheet.get() or None)
            result = analyze(data, fc=float(self.fc.get()), low=float(self.low.get()), high=float(self.high.get()),
                             order=float(self.order.get()), sample_rate=float(self.rate.get()) if self.override.get() else None)
            result['notes'] = source_notes + result['notes']
            result['source'] = str(Path(self.path.get()).resolve())
            result['sheet'] = self.sheet.get() or None
            result['units'] = self.unit.get().strip() or 'input units'
            self.result = result
            self.draw_result()
            self.export.configure(state='normal')
            self.save_plot.configure(state='normal')
            self.status.set('Calculation complete. See Data & validation for assumptions and checks.')
        except Exception as exc:
            self.status.set('Analysis failed. Correct the input or settings and retry.')
            self.set_detail(str(exc))
            self.tabs.select(1)
            messagebox.showerror('Cannot analyze recording', str(exc))

    def draw_result(self):
        r = self.result
        m, mask, unit = r['metrics'], r['valid'], r['units']
        self.summary.configure(text=f"{m['samples']:,} samples     {m['sample_rate_hz']:,.3f} Hz     {m['sample_span_s']:.3f} s     Δf {m['fft_bin_hz']:.4f} Hz     1× {m['frequency_hz']:g} Hz")
        self.figure.clear()
        grid = self.figure.add_gridspec(2, 3, height_ratios=[1.6, 1])
        for i, (title, points) in enumerate([('Raw orbit', r['raw']), ('1× band · interior only', r['filtered'][mask]), ('One revolution · central slice', r['orbit'])]):
            ax = self.figure.add_subplot(grid[0, i])
            ax.plot(points[:, 0], points[:, 1], color=['#8192a3', '#176b87', '#d67737'][i], lw=.8)
            ax.set(title=title, xlabel=f'X ({unit})', ylabel=f'Y ({unit})')
            ax.set_aspect('equal', adjustable='datalim')
            ax.grid(alpha=.2)
            if i == 2:
                ax.plot(points[0, 0], points[0, 1], 'o', color='#d67737', ms=4)
                k = max(1, len(points)//8)
                ax.annotate('', xy=points[k], xytext=points[k-1], arrowprops=dict(arrowstyle='->', color='#14283f'))
        ax = self.figure.add_subplot(grid[1, :])
        for i, name in enumerate(['X', 'Y']):
            ax.semilogy(r['freqs'][1:], np.maximum(r['psd'][1:, i], np.finfo(float).tiny), label=name, lw=1)
        ax.axvspan(m['low_hz'], m['high_hz'], color='#176b87', alpha=.12, label='Pass band')
        ax.axvline(m['frequency_hz'], color='#d67737', ls='--', lw=1)
        ax.set(xlim=(0, min(m['sample_rate_hz']/2, max(100, m['high_hz']*3))), xlabel='Frequency (Hz)', ylabel=f'PSD ({unit}²/Hz)')
        ax.legend(loc='upper right', ncols=3)
        ax.grid(alpha=.2)
        self.canvas.draw()
        lines = ['INPUT CHECKS PASSED', 'Finite numeric samples; increasing and uniform effective time; valid frequency band;',
                 'enough data after filter-edge exclusion. These are numerical checks, not sensor calibration.', '',
                 f"Source: {r['source']}", f"Sheet: {r['sheet'] or '(CSV)'}", f"Displacement unit: {unit} (user supplied)", '',
                 'RESULTS — full valid interior, not just the one-revolution plot',
                 f"X RMS: {m['x_rms']:.6g} {unit}    Y RMS: {m['y_rms']:.6g} {unit}",
                 f"X peak-to-peak: {m['x_peak_to_peak']:.6g} {unit}    Y peak-to-peak: {m['y_peak_to_peak']:.6g} {unit}",
                 f"Raw spectral peak X: {m['x_dominant_hz']:.6g} Hz    Y: {m['y_dominant_hz']:.6g} Hz", '',
                 'METHOD', f"Linear detrend; Butterworth band-pass, order {m['order']} prototype; forward/backward SOS filtering.",
                 'Zero phase; squared magnitude response. Band limits are half-amplitude points after both passes.',
                 f"Excluded {m['edge_guard_s']:.4f} s at each end using pole decay to 0.1%; {m['valid_samples']:,} valid samples.",
                 'The edge guard is a conservative heuristic, not a universal error bound.',
                 'Raw orbit includes original offsets. Filtered orbit is detrended.',
                 'No probe-angle correction or tachometer phase is available in these inputs.', '', 'NOTES']
        lines.extend('• ' + note for note in r['notes'])
        lines.extend(['', 'FIRST FIVE INPUT ROWS (time, X, Y)', *[f'{t:.9g}, {x:.9g}, {y:.9g}' for t, (x, y) in zip(r['time'][:5], r['raw'][:5])]])
        self.set_detail('\n'.join(lines))
        self.tabs.select(0)

    def save_data(self):
        if self.result is None:
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='orbit_results.csv', filetypes=[('CSV', '*.csv')])
        if not path:
            return
        report_path = Path(path).with_suffix('.report.json')
        if report_path.exists() and not messagebox.askyesno('Replace report?', f'Replace {report_path.name}?'):
            return
        try:
            export_csv(path, self.result)
            report = {k: self.result[k] for k in ['source', 'sheet', 'units', 'metrics', 'notes']}
            report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
            self.status.set(f'Saved {Path(path).name} and {report_path.name}.')
        except Exception as exc:
            messagebox.showerror('Export failed', str(exc))

    def save_figure(self):
        if self.result is None:
            return
        path = filedialog.asksaveasfilename(defaultextension='.png', initialfile='orbit_plot.png', filetypes=[('PNG', '*.png'), ('PDF', '*.pdf')])
        if path:
            try:
                self.figure.savefig(path, dpi=180)
                self.status.set(f'Saved {Path(path).name}.')
            except Exception as exc:
                messagebox.showerror('Save failed', str(exc))


if __name__ == '__main__':
    OrbitApp().mainloop()
