"""Reproduce the supplied-data audit. No source files are changed."""
import json
from pathlib import Path
import numpy as np
from Functions import load_data, analyze, export_csv


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    out = Path(__file__).parent / 'validation'
    out.mkdir(exist_ok=True)
    arrays = {}
    report = {}
    for name in ['orbit_data.csv', 'OrbitData.csv', 'OrbitData.xlsx']:
        data, notes = load_data(args.source / name)
        arrays[name] = data
        dt = np.diff(data[:, 0])
        record = dict(rows=len(data), first=data[0].tolist(), last=data[-1].tolist(),
                      nonincreasing_intervals=int(np.count_nonzero(dt <= 0)), notes=notes)
        try:
            record['metrics'] = analyze(data)['metrics']
        except ValueError as exc:
            record['rejected_reason'] = str(exc)
        report[name] = record
    excel = arrays['OrbitData.xlsx']
    exported = arrays['OrbitData.csv']
    compact = arrays['orbit_data.csv']
    np.testing.assert_allclose(excel[:, 1:], exported[:, 1:], rtol=0, atol=5e-5)
    np.testing.assert_array_equal(exported[1:, 1:], compact[:, 1:])
    fixed = analyze(exported, sample_rate=6400)
    reference = analyze(excel)
    np.testing.assert_allclose(fixed['filtered'], reference['filtered'], rtol=0, atol=5e-5)
    report['cross_checks'] = dict(xy_match_excel_csv_within_5e_minus_5=True, compact_xy_match_csv_after_first_row=True,
        maximum_csv_displacement_error=float(np.max(np.abs(excel[:, 1:]-exported[:, 1:]))),
        maximum_csv_timestamp_error_s=float(np.max(np.abs(excel[:, 0]-exported[:, 0]))),
        overridden_csv_matches_excel_output_within_5e_minus_5=True,
        maximum_filtered_difference=float(np.max(np.abs(fixed['filtered']-reference['filtered']))))
    export_csv(out/'verified_xlsx_output.csv', reference)
    (out/'supplied_data_audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
