"""Exercise actual Tk callbacks and render supplied data. Keeps the UI open."""
from pathlib import Path
from unittest.mock import patch
import numpy as np
from Orbit import OrbitApp

app = OrbitApp()
source = Path('E:/GP/Python/2202Apr/Orbit')
out = Path(__file__).parent/'validation'
out.mkdir(exist_ok=True)
with patch('Orbit.filedialog.askopenfilename', return_value=str(source/'OrbitData.xlsx')):
    app.open_file()
app.run_analysis()
app.update()
assert app.result is not None
assert app.result['metrics']['sample_rate_hz'] == 6400
with patch('Orbit.filedialog.asksaveasfilename', return_value=str(out/'ui_export.csv')), patch('Orbit.messagebox.askyesno', return_value=True):
    app.save_data()
assert (out/'ui_export.report.json').exists()
np.testing.assert_array_equal(np.loadtxt(out/'ui_export.csv', delimiter=',', skiprows=1)[:, 3:5], app.result['filtered'])
app.fc.set('25')
assert app.result is None
assert str(app.export['state']) == 'disabled'
with patch('Orbit.filedialog.askopenfilename', return_value=str(source/'OrbitData.csv')):
    app.open_file()
with patch('Orbit.messagebox.showerror') as error:
    app.run_analysis()
    assert error.called and app.result is None
app.override.set(True)
app.fc.set('24.97')
app.run_analysis()
assert app.result is not None
app.override.set(False)
with patch('Orbit.filedialog.askopenfilename', return_value=str(source/'orbit_data.csv')):
    app.open_file()
app.run_analysis()
assert app.result is not None
with patch('Orbit.filedialog.askopenfilename', return_value=str(source/'OrbitData.xlsx')):
    app.open_file()
app.run_analysis()
app.figure.savefig(out/'verified_orbits.png', dpi=150)
app.update()
print('UI smoke passed: CSV/XLSX selection, analysis, error, override, stale-state prevention, export, plot.', flush=True)
app.mainloop()
