import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d

from pathlib import Path

import fym


class Load:
    def __init__(self, ax, anchors):
        vertices = np.vstack(([0, 0, 0], *anchors))
        self.body = ax.plot_trisurf(*vertices.T)
        self.body._base = self.body._vec

    def set(self, pos, R):
        _vec = np.array([pos + R @ point for point in self.body._base[:3].T])
        self.body._vec = np.vstack((_vec.T, self.body._base[3]))


class Link:
    def __init__(self, ax, color="k", linewidth=1, **kwargs):
        self.body = art3d.Line3D(
            [], [], [], color=color, linewidth=linewidth, **kwargs)
        ax.add_artist(self.body)

    def set(self, start, end):
        self.body._verts3d = np.vstack((start, end)).T


class Quadrotor:
    def __init__(self, ax, body_diameter=0.315, rotor_radius=0.15):
        d = body_diameter

        # Body
        body_segs = np.array([
            [[d, 0, 0], [0, 0, 0]],
            [[-d, 0, 0], [0, 0, 0]],
            [[0, d, 0], [0, 0, 0]],
            [[0, -d, 0], [0, 0, 0]]
        ])
        colors = (
            (1, 0, 0, 1),
            (0, 0, 1, 1),
            (0, 0, 1, 1),
            (0, 0, 1, 1),
        )

        self.body = art3d.Line3DCollection(
            body_segs, colors=colors, linewidth=2)

        kwargs = dict(radius=rotor_radius, ec="k", fc="k", alpha=0.3)
        self.rotors = [
            Circle((d, 0), **kwargs),
            Circle((0, d), **kwargs),
            Circle((-d, 0), **kwargs),
            Circle((0, -d), **kwargs),
        ]

        ax.add_collection3d(self.body)
        for rotor in self.rotors:
            ax.add_patch(rotor)
            art3d.pathpatch_2d_to_3d(rotor, z=0)

        self.body._base = self.body._segments3d
        for rotor in self.rotors:
            rotor._segment3d = np.array(rotor._segment3d)
            rotor._center = np.array(rotor._center + (0,))
            rotor._base = rotor._segment3d

    def set(self, pos, R=np.eye(3)):
        # Rotate
        self.body._segments3d = np.array([
            R @ point
            for point in self.body._base.reshape(-1, 3)
        ]).reshape(self.body._base.shape)

        for rotor in self.rotors:
            rotor._segment3d = np.array([
                R @ point for point in rotor._base
            ])

        # Translate
        self.body._segments3d = self.body._segments3d + pos

        for rotor in self.rotors:
            rotor._segment3d = rotor._segment3d + pos


class FuncAnimation(matplotlib.animation.FuncAnimation):
    def __init__(self, fig, func=None, init_func=None, blit=True,
                 *args, **kwargs):
        self.fig = fig
        init_func = self.init_wrapper(init_func)
        func = self.func_wrapper(func)
        super().__init__(fig, func=func, init_func=init_func, blit=blit,
                         *args, **kwargs)

    def init_wrapper(self, init_func):
        def wrapper():
            if init_func is None:
                return

            self.iterable_of_artists = init_func() or []
            for ax in self.fig.axes:
                for name in ['collections', 'patches', 'lines',
                             'texts', 'artists', 'images']:
                    artist = getattr(ax, name)
                    for art in artist:
                        if art not in set(self.iterable_of_artists):
                            self.iterable_of_artists.append(art)

            return self.iterable_of_artists
        return wrapper

    def func_wrapper(self, func):
        def wrapper(frame):
            if func is None:
                return
            func(frame)
            return self.iterable_of_artists
        return wrapper

    def save(self, filename, writer="ffmpeg", *args, **kwargs):
        super().save(filename, writer=writer, *args, **kwargs)
