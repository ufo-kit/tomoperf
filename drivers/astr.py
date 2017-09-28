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

    reco = np.zeros((args.width, args.width), dtype=np.float32)
    vol_geom = astra.create_vol_geom(args.width, args.width)
    vid = astra.data2d.link('-vol', vol_geom, reco)

    proj_geom = astra.create_proj_geom('parallel', 1.0, args.width, angles)
    pid = astra.create_projector('cuda', proj_geom, vol_geom)

    sino = np.zeros((args.num_projections, args.width), dtype=np.float32)
    sid = astra.data2d.link('-sino', proj_geom, sino)

    config = astra.astra_dict('FBP_CUDA')
    config['ProjectorId'] = pid
    config['ProjectionDataId'] = sid
    config['ReconstructionDataId'] = vid

    aid = astra.algorithm.create(config)

    for i in range(args.num_slices):
        astra.algorithm.run(aid)


if __name__ == '__main__':
    main()
