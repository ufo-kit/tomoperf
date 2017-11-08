import os
import argparse
import shutil
import lprecmods.lpTransform
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--width', type=int, required=True)
    parser.add_argument('--num-projections', type=int, required=True)
    parser.add_argument('--num-slices', type=int, required=True)

    args = parser.parse_args()
    R = np.zeros((args.num_slices, args.width, args.num_projections), dtype=np.float32)
    handle = lprecmods.lpTransform.lpTransform(args.width, args.num_projections, args.num_slices, None, False)

    if args.prepare:
        # We cache the intermediate output for later use
        suffix = '{}-{}'.format(args.width, args.num_projections)
        padj_name = '/tmp/Padj-{}'.format(suffix)
        pfwd_name = '/tmp/Pfwd-{}'.format(suffix)
        pgl_name = '/tmp/Pgl-{}'.format(suffix)

        if os.path.exists(padj_name) and os.path.exists(pfwd_name) and os.path.exists(pgl_name):
            shutil.copyfile(padj_name, 'Padj')
            shutil.copyfile(pfwd_name, 'Pfwd')
            shutil.copyfile(pgl_name, 'Pgl')
        else:
            handle.precompute()
            shutil.copyfile('Padj', padj_name)
            shutil.copyfile('Pfwd', pfwd_name)
            shutil.copyfile('Pgl', pgl_name)
    else:
        handle.initcmem()
        frec = handle.adj(R, args.width / 2)


if __name__ == '__main__':
    main()
