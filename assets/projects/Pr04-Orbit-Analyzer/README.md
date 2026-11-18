# Orbit Analyzer

A local Python desktop application for three-column shaft-displacement recordings.
The original files in `E:/GP/Python/2202Apr/Orbit` have not been modified.

## Run on this computer

Double-click **Start Orbit Analyzer.cmd** in this folder. The project has an
installed virtual environment. Maximize the window if you need more plot space.

1. Click **Open CSV / XLSX**. For the supplied recording, choose `OrbitData.xlsx`.
2. Select the worksheet if necessary. The supplied workbook uses `Sheet1`.
3. Enter shaft frequency in Hz, low/high cutoff frequencies, filter order and units.
   The defaults are 24.97 Hz, 22–28 Hz, order 2 and µm. The entered speed is retained
   from the original script; it is not a tachometer measurement extracted from the file.
4. Click **Analyze**. Review both **Orbits & spectrum** and **Data & validation**.
5. **Save plot** writes PNG or PDF. **Export CSV + report** writes the full sample
   table and an accompanying `.report.json` with settings, metrics and notes.

CSV/XLSX input must have exactly three columns in this order: time in seconds,
X displacement, Y displacement. A single text header row is optional. Both displacement
columns must use the same unit. Changing the unit label does not rescale the data.
Comma-, semicolon- and tab-delimited CSVs are supported. Blank rows are ignored;
partially blank rows, invalid cells and nonfinite numbers are rejected. Excel formulas
must have numeric cached results from a spreadsheet application.

**Override clock (Hz)** explicitly reconstructs time in the original row order.
Use it only when acquisition rate and uninterrupted sample ordering are known.
For the supplied `OrbitData.csv`, enable it at **6400 Hz**. Do not sort that file
by its corrupted timestamps. The application does not silently repair time.

## What the supplied data contains

Each row represents paired X/Y displacement samples. The adjacent instrument waveform
text file identifies MOTOR NDE BEARING (X11703–X11704), micrometres, a 6400 Hz
sample rate, and matching X/Y acquisition times of March 23, 2022, 10:27:54 AM.
Its 6400 Hz X/Y blocks match the workbook to floating-point precision (maximum
absolute discrepancy below 9e-16 µm). Other 800 Hz blocks in that text file are
separate recordings and are not inputs to this analysis.

| Input | Numeric rows | Timing and precision |
| --- | ---: | --- |
| OrbitData.xlsx | 32,769 | Uniform 6400 Hz; timestamps 0–5.12 s. Preferred reference. |
| OrbitData.csv | 32,769 | 12,898 nonincreasing intervals; timestamp error up to 0.005 s. Requires explicit clock override. |
| orbit_data.csv | 32,768 | Omits the first zero row and uses a 0.000156 s step, implying 6410.2564 Hz rather than 6400 Hz. |

The CSV displacement channels match each other after accounting for the first row.
Compared with Excel, CSV rounding changes some displacement values by up to
0.00004988 µm. The first `(0,0,0)` row is present in the instrument export as well
as the workbook; it is retained. There is no tachometer column or probe-angle metadata.

## Corrections and calculation method

- The original `bandstop` rejected the desired 1× band. The replacement uses a
  Butterworth **bandpass**, implemented with second-order sections.
- Removed the preceding low-pass filter at the shaft frequency, which attenuated
  the component being measured. Forward/backward filtering avoids phase delay.
- Sample interval is `(last_time - first_time)/(N - 1)`, with checks for monotonicity
  and uniformity. Record span is `(N - 1)*dt`; FFT record duration is `N*dt`, and
  FFT bin spacing is `fs/N`. These quantities are distinguished in the report.
- The original 24.95–25 Hz band is unsuitable for this short record. With the new
  order-2 design and edge criterion it requires more than approximately 124.5 s.
  The 22–28 Hz default is an explicit broader analysis band, not an exact single-tone extraction.
- Linear trends are removed from both channels. Filtering uses `sosfiltfilt` with
  a pole-decay-based padding interval. Samples within that interval at each edge
  are excluded from plotted filtered orbits and summary metrics.
- The central one-revolution view spans exactly `1/fc` seconds using interpolation.
  It is a time slice, not a synchronous average or a tachometer-referenced orbit.
- Plots have equal X/Y scaling and visible units. Invalid settings produce an error;
  changed settings clear old results and disable export until recalculation.

Forward/backward filtering squares the single-pass amplitude response. Thus the
specified Butterworth cutoff frequencies have approximately half-amplitude gain
after both passes. RMS and peak-to-peak values describe the retained frequency band.
The edge guard is a conservative heuristic based on pole decay to 0.1% amplitude,
not a universal bound on transient error. Physical orbit interpretation assumes
appropriately calibrated, synchronized displacement channels and suitable probe geometry.

Implementation references: [SciPy Butterworth design](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html)
and [SciPy forward/backward SOS filtering](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html).

## Verified results

For `OrbitData.xlsx`, defaults of 24.97 Hz and a 22–28 Hz order-2 band:

| Quantity | Value |
| --- | ---: |
| Sample rate | 6400 Hz |
| Sample span | 5.12 s |
| FFT bin spacing | 0.19530654 Hz |
| Raw dominant spectral bin, both channels | 24.99923708 Hz |
| Exclusion at each edge | 0.56671875 s |
| Valid interior samples | 25,515 |
| X filtered RMS | 2.56306744 µm |
| Y filtered RMS | 7.20873529 µm |
| X filtered peak-to-peak | 8.02011305 µm |
| Y filtered peak-to-peak | 20.90005668 µm |

The bin peak is not a precision speed measurement. The approximately 0.1953 Hz
bin spacing cannot independently confirm 24.97 Hz to two decimal places.

Validation completed:

- **12 automated tests passed.** Known synthetic X/Y sinusoids with offsets,
  linear drift and out-of-band interference were recovered within 0.5% relative
  RMS error. Independent sinusoidal projection checked amplitudes within 0.2%
  and phase coefficients within 0.005 displacement units.
- Checked malformed inputs, timestamp offsets, repeated/backward/irregular time,
  invalid cutoff/order, insufficient record duration, exact one-revolution length,
  explicit timing override and full-precision CSV export round-trip.
- Supplied-data audit passed. After reconstructing `OrbitData.csv` at 6400 Hz,
  its filtered output differs from the workbook result by at most 3.852e-7 µm.
- Actual Tk callback smoke tests passed for CSV/XLSX selection, worksheet selection,
  analysis, error reporting, override, stale-state prevention, exports and plot generation.
- Final visual inspection verified the maximized plots, axis labels, validation
  text, metrics and export controls on November 18, 2026.

These checks establish numerical behavior under the documented assumptions, not
independent sensor calibration or proof of a machinery diagnosis.

Artifacts in `validation/`:

- `supplied_data_audit.json`: machine-readable audit of the three inputs.
- `verified_xlsx_output.csv`: processed workbook samples. The `valid_interior`
  column is 1 for usable interior samples and 0 for excluded edge samples.
- `verified_orbits.png`: saved plot from the UI smoke test.
- `ui_export.csv` and `ui_export.report.json`: export round-trip verification.

## Install elsewhere and reproduce

Install Python 3.12 with Tcl/Tk, then run in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe Orbit.py
```

The virtual environment created on this computer is machine-specific. Recreate it
when moving the project. This machine's bundled Python needed a local copy of its
Tcl scripts inside `.venv/tcl`; the application detects that optional local copy.
Normal Python installations use their own Tcl/Tk installation.

To repeat numerical checks and the supplied-file audit:

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_orbit
.\.venv\Scripts\python.exe validate_supplied.py "E:/GP/Python/2202Apr/Orbit"
```

`Functions.py` owns loading, validation, filtering and export. `Orbit.py` owns the
desktop interface. `ui_smoke.py` is a development check using the supplied source
path; it exercises callbacks and leaves the application open.
