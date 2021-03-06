# -*- coding: utf-8 -*-
# =============================================================================
# Created on Sun Jul 21 15:29:19 2019
#
# @author: Brénainn Woodsend
#
#
# ScalarBar.py adds a scalar/color bar.
# Copyright (C) 2019  Brénainn Woodsend
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================

from builtins import super

import vtk
import numpy as np
import os
import sys
from pathlib2 import Path
from vtk.util.numpy_support import (
                                    numpy_to_vtk,
                                    numpy_to_vtkIdTypeArray,
                                    vtk_to_numpy,
                                    )

from vtkplotlib.plots.BasePlot import BasePlot



class ScalarBar(BasePlot):
    """Create a scalar bar. Also goes by the alias `colorbar`.

    :param plot: The plot with scalars to draw a scalarbar for.

    :param title: , defaults to ''.
    :type title: str, optional

    :param fig: The figure to plot into, can be None, defaults to vpl.gcf().
    :type fig: vpl.figure, vpl.QtFigure, optional


    :return: The scalarbar object.
    :rtype: vtkplotlib.plots.ScalarBar.ScalarBar


    The `plot` argument can be the output of any ``vpl.***`` command that takes
    `scalars` as an argument.

    """
    def __init__(self, plot, title="", fig="gcf"):

        super().__init__(fig)

        self.actor = vtk.vtkScalarBarActor()
        self.actor.SetTitle(title)

        self.actor.SetNumberOfLabels(6)

        self.lookup_table = plot.mapper.GetLookupTable()
        if self.lookup_table.GetTable().GetNumberOfTuples() == 0:
            # ForceBuild resets it as well as building it. Thus overwriting any
            # existing colormap. Only build if it has not already been built.
            self.lookup_table.ForceBuild()
        self.actor.SetLookupTable(self.lookup_table)


#        self.fig += self
        self.fig.renderer.AddActor2D(self.actor)
        self.fig.plots.add(self)



def test():
    from stl.mesh import Mesh
    import vtkplotlib as vpl

    mesh = Mesh.from_file(vpl.data.get_rabbit_stl())
    plot = vpl.mesh_plot(mesh, scalars=mesh.x)

    vpl.scalar_bar(plot)

    vpl.show()


if __name__ == "__main__":
    test()

