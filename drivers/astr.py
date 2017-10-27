import argparse
import astra
import time
import numpy as np



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, required=True)
    parser.add_argument('--num-projections', type=int, required=True)
    parser.add_argument('--num-slices', type=int, required=True)

    args = parser.parse_args()
    angles = np.linspace(0, np.pi, args.num_projections, False, dtype=np.float64)

    vol_geom = astra.create_vol_geom(args.width, args.width, args.num_slices)
    proj_geom = astra.create_proj_geom('parallel3d', 1.0, 1.0, args.num_slices, args.width, angles)

    vid = astra.data3d.create('-vol', vol_geom)
    pid = astra.data3d.create('-proj3d', proj_geom, 0.0)

    config = astra.astra_dict('BP3D_CUDA')
    config['ProjectionDataId'] = pid
    config['ReconstructionDataId'] = vid

    aid = astra.algorithm.create(config)
    astra.algorithm.run(aid)


if __name__ == '__main__':
    main()
