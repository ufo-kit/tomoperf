import argparse
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
    handle = lprecmods.lpTransform.lpTransform(args.width, args.num_projections, args.num_slices, 'hamming', True)

    if args.prepare:
        handle.precompute()
    else:
        handle.initcmem()
        frec = handle.adj(R, args.width / 2 - 4)


if __name__ == '__main__':
    main()
