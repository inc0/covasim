"""
Compare current results to baseline
"""

import sciris as sc
import covasim as cv

baseline_filename = 'baseline.json'


def test_baseline():
    ''' Compare the current default sim against the saved baseline '''

    # Load existing baseline
    filepath = sc.makefilepath(filename=baseline_filename, folder=sc.thisdir(__file__))
    baseline = sc.loadjson(filepath)
    old = baseline['summary']

    # Calculate new baseline
    sim = cv.Sim(verbose=0)
    sim.run()
    new = sim.summary

    # Compare keys
    old_keys = set(old.keys())
    new_keys = set(new.keys())
    if old_keys != new_keys:
        errormsg = f"Keys don't match; old: {old_keys}; new: {new_keys}"
        raise KeyError(errormsg)

    mismatches = {}
    for key in old.keys():
        old_val = old[key]
        new_val = new[key]
        if old_val != new_val:
            mismatches[key] = {'old': old_val, 'new': new_val}

    if len(mismatches):
        errormsg = '\nThe following values have changed between old and new!\n'
        errormsg += 'Please rerun "update_baseline" if this is intentional.\n'
        for mkey,mval in mismatches.items():
            errormsg += f'{mkey}: old = {mval["old"]}, new = {mval["new"]}\n'
        raise ValueError(errormsg)
    else:
        print('Baseline matches')

    return new


if __name__ == '__main__':

    new = test_baseline()

    print('Done.')