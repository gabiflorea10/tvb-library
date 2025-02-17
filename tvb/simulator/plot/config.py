# -*- coding: utf-8 -*-

import os
import numpy as np
from datetime import datetime


class FiguresConfig(object):
    VERY_LARGE_SIZE = (40, 20)
    VERY_LARGE_PORTRAIT = (30, 50)
    SUPER_LARGE_SIZE = (80, 40)
    LARGE_SIZE = (20, 15)
    SMALL_SIZE = (15, 10)
    NOTEBOOK_SIZE = (10, 7)
    FIG_FORMAT = 'png'
    SAVE_FLAG = True
    SHOW_FLAG = False
    MOUSE_HOOVER = False
    MATPLOTLIB_BACKEND = "Agg"  # "Qt4Agg"
    FONTSIZE = 10
    WEIGHTS_NORM_PERCENT = 99
    MAX_SINGLE_VALUE = np.finfo("single").max
    MAX_INT_VALUE = np.iinfo(np.int64).max

    def __init__(self, out_base=None, separate_by_run=False):
        print(out_base)
        print(separate_by_run)
        """
        :param work_folder: Base folder where logs/figures/results should be kept
        :param separate_by_run: Set TRUE, when you want logs/results/figures to be in different files / each run
        """
        self._out_base = out_base or os.path.join(os.getcwd(), "outputs")
        self._separate_by_run = separate_by_run

    def largest_size(self):
        import sys
        if 'IPython' not in sys.modules:
            return self.LARGE_SIZE
        from IPython import get_ipython
        if getattr(get_ipython(), 'kernel', None) is not None:
            return self.NOTEBOOK_SIZE
        else:
            return self.LARGE_SIZE

    @property
    def FOLDER_LOGS(self):
        folder = os.path.join(self._out_base, "logs")
        if self._separate_by_run:
            folder = folder + datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M')
        if not (os.path.isdir(folder)):
            os.makedirs(folder)
        return folder

    @property
    def FOLDER_RES(self):
        folder = os.path.join(self._out_base, "res")
        if self._separate_by_run:
            folder = folder + datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M')
        if not (os.path.isdir(folder)):
            os.makedirs(folder)
        return folder

    @property
    def FOLDER_FIGURES(self):
        folder = os.path.join(self._out_base, "figs")
        if self._separate_by_run:
            folder = folder + datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M')
        if not (os.path.isdir(folder)):
            os.makedirs(folder)
        return folder


CONFIGURED = FiguresConfig()
