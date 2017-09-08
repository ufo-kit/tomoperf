import argparse
import tomopy
import logging
import numpy as np



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, required=True)
    parser.add_argument('--num-projections', type=int, required=True)
    parser.add_argument('--num-slices', type=int, required=True)
    parser.add_argument('--algorithm', type=str, choices=['gridrec', 'fbp'], required=True)

    args = parser.parse_args()
    data = np.zeros((args.num_slices, args.width, args.num_projections), dtype=np.float32)
    theta = tomopy.angles(args.num_projections)
    tomopy.recon(data, theta, algorithm=args.algorithm, sinogram_order=True,
                 num_gridx=args.width, num_gridy=args.width)


if __name__ == '__main__':
    main()
