"""Validated shaft-orbit input and zero-phase band-pass processing.

Times are seconds, X/Y share the user's displacement unit. No probe geometry
or tachometer reference is inferred from these three columns.
"""
from pathlib import Path
import csv
import numpy as np
from scipy import signal


def sheet_names(path):
    from openpyxl import load_workbook
    with Path(path).open('rb') as stream:
        book = load_workbook(stream, read_only=True, data_only=True)
        try:
            return book.sheetnames
        finally:
            book.close()


def load_data(path, sheet=None):
    """Read exactly three columns, optional one-row text header, blank rows OK.

    Reject partially empty/non-numeric rows; never sort, fill, or drop samples.
    Timestamp validation occurs separately so an explicit clock override works.
    """
    path = Path(path)
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as stream:
            sample = stream.read(8192)
            stream.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            except csv.Error:
                dialect = csv.excel
            rows = list(csv.reader(stream, dialect))
    elif path.suffix.lower() == '.xlsx':
        from openpyxl import load_workbook
        book = load_workbook(path, read_only=True, data_only=True)
        try:
            rows = list(book[sheet or book.sheetnames[0]].values)
        finally:
            book.close()
    else:
        raise ValueError('Choose a .csv or .xlsx file.')
    data, notes = [], []
    blank = lambda v: v is None or (isinstance(v, str) and not v.strip())
    first = True
    for line, row in enumerate(rows, 1):
        if all(blank(v) for v in row):
            continue
        if len(row) != 3:
            raise ValueError(f'Row {line}: expected exactly 3 columns: time, X, Y.')
        try:
            if any(blank(v) or isinstance(v, bool) for v in row):
                raise ValueError()
            values = [float(v) for v in row]
        except (ValueError, TypeError):
            # Only a complete nonnumeric text row can be a header.
            def label(v):
                if not isinstance(v, str) or not v.strip():
                    return False
                try:
                    float(v)
                    return False
                except ValueError:
                    return v.strip().lower() not in {'nan', 'inf', '-inf', 'infinity'}
            if first and all(label(v) for v in row):
                notes.append(f'Header: {", ".join(row)}')
                first = False
                continue
            raise ValueError(f'Row {line}: all three cells must be finite numbers.') from None
        if not np.isfinite(values).all():
            raise ValueError(f'Row {line}: NaN and infinity are not valid samples.')
        data.append(values)
        first = False
    array = np.asarray(data, dtype=float)
    if len(array) < 16:
        raise ValueError('At least 16 numeric samples are required.')
    if np.array_equal(array[0], [0, 0, 0]):
        notes.append('First row is (0, 0, 0). Retained as recorded; verify whether it is a real sample.')
    return array, notes


def signal_stats(t):
    t = np.asarray(t, dtype=float)
    if t.ndim != 1 or len(t) < 2 or not np.isfinite(t).all():
        raise ValueError('Time must contain at least two finite samples.')
    steps = np.diff(t)
    if np.any(steps <= 0):
        raise ValueError('Timestamps repeat or go backward. Use the original XLSX or explicitly override the sample rate.')
    dt = (t[-1] - t[0]) / (len(t) - 1)
    # Permit at most 1% interval rounding, not gaps or clock jumps.
    if np.max(np.abs(steps - dt)) > max(dt * .01, 1e-12):
        raise ValueError('Time spacing varies by more than 1%. Use a verified uniform source or sample-rate override.')
    fs = 1.0 / dt
    return fs, dt, fs / len(t), len(t) * dt


def filter_design(lowcut, highcut, fs, fc, order=2):
    if not np.isfinite([lowcut, highcut, fs, fc]).all():
        raise ValueError('Frequencies must be finite numbers.')
    if not 0 < lowcut < fc < highcut < fs / 2:
        raise ValueError('Require 0 < low cutoff < 1x frequency < high cutoff < sample rate / 2.')
    if int(order) != order or not 1 <= order <= 6:
        raise ValueError('Filter order must be an integer from 1 to 6.')
    sos = signal.butter(int(order), [lowcut, highcut], btype='bandpass', fs=fs, output='sos')
    poles = signal.sos2zpk(sos)[1]
    # Conservative decay guard: largest pole decays to 0.1% amplitude.
    guard = int(np.ceil(np.log(.001) / np.log(np.max(np.abs(poles)))))
    return sos, guard


def oneX_filter(data, lowcut, highcut, fs, fc, order=2):
    values = np.asarray(data, dtype=float)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError('Signal must be a finite one-dimensional array.')
    sos, guard = filter_design(lowcut, highcut, fs, fc, order)
    if len(values) <= 2 * guard + int(np.ceil(fs / fc)) + 1:
        raise ValueError(f'Record too short for this band. Need more than {(2*guard+fs/fc)/fs:.2f} s; widen the band or record longer.')
    return signal.sosfiltfilt(sos, signal.detrend(values), padlen=guard)


def single_orbit(x, y, fs, fc):
    x, y = np.asarray(x), np.asarray(y)
    if not np.isfinite([fs, fc]).all() or not 0 < fc < fs / 2:
        raise ValueError('Require 0 < 1x frequency < sample rate / 2.')
    span = fs / fc
    if x.ndim != 1 or x.shape != y.shape or len(x) < int(np.ceil(span)) + 1:
        raise ValueError('Matching X/Y signals must contain a full revolution.')
    start = (len(x) - 1 - span) / 2
    positions = np.linspace(start, start + span, int(np.ceil(span)) + 1)
    return (np.interp(positions, np.arange(len(x)), x),
            np.interp(positions, np.arange(len(y)), y))


def analyze(data, fc=24.97, low=22., high=28., order=2, sample_rate=None):
    data = np.asarray(data, dtype=float)
    if data.ndim != 2 or data.shape[1] != 3 or len(data) < 16 or not np.isfinite(data).all():
        raise ValueError('Input must be a finite N by 3 table with at least 16 rows.')
    t = data[:, 0].copy()
    notes = []
    if sample_rate is not None:
        if not np.isfinite(sample_rate) or sample_rate <= 0:
            raise ValueError('Sample-rate override must be finite and positive.')
        t = t[0] + np.arange(len(t)) / sample_rate
        notes.append(f'Timestamps reconstructed in original row order at {sample_rate:g} Hz by explicit override.')
    fs, dt, df, tw = signal_stats(t)
    _, guard = filter_design(low, high, fs, fc, order)
    xy = np.column_stack([oneX_filter(data[:, i], low, high, fs, fc, order) for i in (1, 2)])
    valid = np.zeros(len(t), dtype=bool)
    valid[guard:-guard] = True
    ox, oy = single_orbit(xy[valid, 0], xy[valid, 1], fs, fc)
    freqs, psd = signal.periodogram(data[:, 1:], fs=fs, window='hann', detrend='linear', axis=0)
    peaks = freqs[1:][np.argmax(psd[1:], axis=0)]
    rms = np.sqrt(np.mean(xy[valid]**2, axis=0))
    pp = np.ptp(xy[valid], axis=0)
    if np.any((peaks < low) | (peaks > high)):
        notes.append('A dominant spectral peak is outside the selected band. Confirm shaft speed independently.')
    notes.append('One revolution is a time slice at the entered speed, not a tachometer-synchronized orbit.')
    metrics = dict(samples=len(t), sample_rate_hz=fs, dt_s=dt, fft_bin_hz=df,
                   sample_span_s=t[-1]-t[0], fft_record_s=tw, frequency_hz=fc,
                   low_hz=low, high_hz=high, order=int(order), edge_guard_s=guard/fs,
                   valid_samples=int(valid.sum()), x_rms=float(rms[0]), y_rms=float(rms[1]),
                   x_peak_to_peak=float(pp[0]), y_peak_to_peak=float(pp[1]),
                   x_dominant_hz=float(peaks[0]), y_dominant_hz=float(peaks[1]))
    return dict(time=t, raw=data[:, 1:], filtered=xy, valid=valid, orbit=np.column_stack([ox, oy]),
                freqs=freqs, psd=psd, metrics=metrics, notes=notes)


def export_csv(path, result):
    """Export full precision and mark filter-edge samples explicitly."""
    table = np.column_stack([result['time'], result['raw'], result['filtered'], result['valid']])
    np.savetxt(path, table, delimiter=',', comments='', fmt=['%.17g']*5+['%d'],
               header='time_s,x_raw,y_raw,x_bandpass,y_bandpass,valid_interior')
