import tempfile
import unittest
from pathlib import Path
import numpy as np
from Functions import analyze, load_data, signal_stats, oneX_filter, single_orbit, export_csv


class OrbitTests(unittest.TestCase):
    def setUp(self):
        self.fs = 1000.
        self.t = np.arange(10000) / self.fs
        self.x = 3*np.cos(2*np.pi*25*self.t)
        self.y = 2*np.sin(2*np.pi*25*self.t + .3)

    def test_timestamp_offset_and_off_by_one(self):
        fs, dt, df, tw = signal_stats(self.t + 123)
        np.testing.assert_allclose([fs, dt, df, tw], [1000, .001, .1, 10], rtol=1e-10)

    def test_known_orbit_amplitude_phase_and_interference(self):
        data = np.column_stack([self.t, self.x + 5 + .5*self.t + np.cos(2*np.pi*70*self.t),
                                self.y - 4 - .2*self.t + 2*np.sin(2*np.pi*80*self.t)])
        r = analyze(data, fc=25, low=22, high=28)
        mask = r['valid']
        truth = np.column_stack([self.x, self.y])[mask]
        relative_rms_error = np.sqrt(np.mean((r['filtered'][mask]-truth)**2, axis=0))/np.sqrt(np.mean(truth**2,axis=0))
        self.assertTrue(np.all(relative_rms_error < .005), relative_rms_error)
        # Independent sinusoidal projection verifies amplitude and relative phase.
        basis = np.column_stack([np.cos(2*np.pi*25*self.t[mask]), np.sin(2*np.pi*25*self.t[mask])])
        coeff = np.linalg.lstsq(basis, r['filtered'][mask], rcond=None)[0]
        np.testing.assert_allclose(np.linalg.norm(coeff, axis=0), [3, 2], rtol=.002)
        np.testing.assert_allclose(coeff[:, 1], [2*np.sin(.3), 2*np.cos(.3)], atol=.005)

    def test_reject_narrow_band(self):
        with self.assertRaisesRegex(ValueError, 'too short'):
            oneX_filter(self.x, 24.95, 25., 1000., 24.97)

    def test_bad_time(self):
        for bad in [np.array([0, 1, 1, 2]), np.array([0, 2, 1, 3]), np.array([0, 1, 2.2, 3])]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                signal_stats(bad)

    def test_invalid_band(self):
        for lo, hi, fc in [(26, 28, 25), (22, 500, 25), (0, 28, 25), (22, 28, float('nan'))]:
            with self.subTest(lo=lo, hi=hi), self.assertRaises(ValueError):
                oneX_filter(self.x, lo, hi, self.fs, fc)

    def test_bad_order(self):
        with self.assertRaises(ValueError):
            oneX_filter(self.x, 22, 28, self.fs, 25, 1.5)

    def test_override_is_explicit(self):
        data = np.column_stack([self.t[::-1], self.x, self.y])
        with self.assertRaises(ValueError):
            analyze(data)
        r = analyze(data, sample_rate=1000.)
        self.assertEqual(r['metrics']['sample_rate_hz'], 1000.)
        self.assertIn('reconstructed', r['notes'][0])

    def test_single_orbit_exact_duration(self):
        x, y = single_orbit(np.arange(2000.), np.arange(2000.)*2, 1000, 24.97)
        self.assertAlmostEqual(x[-1]-x[0], 1000/24.97)
        np.testing.assert_allclose(y, x*2)

    def test_short_orbit(self):
        with self.assertRaises(ValueError):
            single_orbit([1, 2], [1, 2], 1000, 25)

    def test_csv_bom_header_blank_and_semicolon(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'input.csv'
            path.write_text('\ufefftime;x;y\n' + '\n'.join(f'{i};1;2' for i in range(20))+'\n;;\n', encoding='utf-8')
            data, notes = load_data(path)
            self.assertEqual(data.shape, (20, 3))
            self.assertEqual(len(notes), 1)

    def test_reject_bad_cells(self):
        for bad in ['1,,2', '1,nan,2', '1,inf,2', '1,a,2', '1,2,3,4']:
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)/'input.csv'
                path.write_text('0,1,2\n'+bad+'\n'+'1,2,3\n'*20)
                with self.assertRaises(ValueError):
                    load_data(path)

    def test_export_roundtrip(self):
        r = analyze(np.column_stack([self.t, self.x, self.y]), fc=25)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'output.csv'
            export_csv(path, r)
            a = np.loadtxt(path, delimiter=',', skiprows=1)
            np.testing.assert_array_equal(a[:, 3:5], r['filtered'])
            np.testing.assert_array_equal(a[:, 5], r['valid'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
