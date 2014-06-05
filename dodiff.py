#!/usr/bin/env python

import subprocess


TODIFF_FORMAT = "chatservers/{0}.py"
TODIFF_NAMES = [
    'redent',
    'typedecoded',
    'typedecoded_2',
    'typedecoded_3',
    'typedecoded_4',
    'replace_main_store',
    'replace_main_store_2',
    'replace_main_store_3',
]
OUTPUT_EXT = 'udiff'

DIFFOPTS="-u"


def main():
    name_pairs = zip(TODIFF_NAMES[:-1], TODIFF_NAMES[1:])
    for left, right in name_pairs:
        outfile = 'diffs/{0}_to_{1}.{2}'.format(left, right, OUTPUT_EXT)
        left = TODIFF_FORMAT.format(left)
        right = TODIFF_FORMAT.format(right)
        print 'Writing to {0}'.format(outfile)
        with open(outfile, 'wb') as out:
            subprocess.call(['diff', DIFFOPTS, left, right], stdout=out)

if __name__ == '__main__':
    main()
