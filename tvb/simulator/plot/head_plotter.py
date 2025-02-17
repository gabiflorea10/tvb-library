# coding=utf-8

from matplotlib import pyplot
import numpy
from tvb.simulator.plot.utils import compute_in_degree
from tvb.simulator.plot.base_plotter import BasePlotter
from tvb.datatypes.sensors import Sensors
from tvb.datatypes.projections import ProjectionMatrix


class HeadPlotter(BasePlotter):

    def __init__(self, config=None):
        super(HeadPlotter, self).__init__(config)

    def _plot_connectivity(self, connectivity, figure_name='Connectivity'):
        pyplot.figure(figure_name + str(connectivity.number_of_regions), self.config.VERY_LARGE_SIZE)
        axes = []
        axes.append(self.plot_regions2regions(connectivity.normalized_weights,
                                              connectivity.region_labels, 121, "normalised weights"))
        axes.append(self.plot_regions2regions(connectivity.tract_lengths,
                                              connectivity.region_labels, 122, "tract lengths"))
        self._save_figure(None, figure_name.replace(" ", "_").replace("\t", "_"))
        self._check_show()
        return pyplot.gcf(), tuple(axes)

    def _plot_connectivity_stats(self, connectivity, figsize=None, figure_name='HeadStats '):
        if not isinstance(figsize, (list, tuple)):
            figsize = self.config.VERY_LARGE_SIZE
        pyplot.figure("Head stats " + str(connectivity.number_of_regions), figsize=figsize)
        areas_flag = len(connectivity.areas) == len(connectivity.region_labels)
        axes = []
        axes.append(self.plot_vector(compute_in_degree(connectivity.normalized_weights), connectivity.region_labels,
                                     111 + 10 * areas_flag, "w in-degree"))
        if len(connectivity.areas) == len(connectivity.region_labels):
            axes.append(self.plot_vector(connectivity.areas, connectivity.region_labels, 122, "region areas"))
        self._save_figure(None, figure_name.replace(" ", "").replace("\t", ""))
        self._check_show()
        return pyplot.gcf(), tuple(axes)

    def _plot_sensors(self, sensors, projection, region_labels, count=1):
        figure, ax, cax = self._plot_projection(sensors, projection, region_labels,
                                                title= "%d - %s - Projection" % (count, sensors.sensors_type))
        count += 1
        return count, figure, ax, cax

    def _plot_projection(self, sensors, projection, region_labels, figure=None, title="Projection",
                         show_x_labels=True, show_y_labels=True, x_ticks=numpy.array([]), y_ticks=numpy.array([]),
                         figsize=None):
        if not isinstance(figsize, (list, tuple)):
            figsize = self.config.VERY_LARGE_SIZE
        if not (isinstance(figure, pyplot.Figure)):
            figure = pyplot.figure(title, figsize=figsize)
        ax, cax1 = self._plot_matrix(projection, sensors.labels, region_labels, 111, title,
                                     show_x_labels, show_y_labels, x_ticks, y_ticks)
        self._save_figure(None, title)
        self._check_show()
        return figure, ax, cax1

    def plot_head(self, connectivity, sensors, plot_stats=False, plot_sensors=True):
        output = []
        output.append(self._plot_connectivity(connectivity))
        if plot_stats:
            output.append(self._plot_connectivity_stats(connectivity))
        if plot_sensors:
            count = 1
            for s_type, sensors_set in sensors.items():
                for sensor, projection in sensors_set.items():
                    if isinstance(sensor, Sensors) and isinstance(projection, ProjectionMatrix):
                        count, figure, ax, cax = \
                            self._plot_sensors(sensor, projection.projection_data,
                                               connectivity.region_labels, count)
                        output.append((figure, ax, cax))
        return tuple(output)

    def plot_tvb_connectivity(self, connectivity, num="weights", order_by=None, plot_hinton=False, plot_tracts=True):
        """
        A 2D plot for visualizing the Connectivity.weights matrix
        """
        labels = connectivity.region_labels
        plot_title = connectivity.__class__.__name__

        if order_by is None:
            order = numpy.arange(connectivity.number_of_regions)
        else:
            order = numpy.argsort(order_by)
            if order.shape[0] != connectivity.number_of_regions:
                self.logger.error("Ordering vector doesn't have length number_of_regions")
                self.logger.error("Check ordering length and that connectivity is configured")
                return

        # Assumes order is shape (number_of_regions, )
        order_rows = order[:, numpy.newaxis]
        order_columns = order_rows.T

        if plot_hinton:
            from tvb.simulator.plot.tools import hinton_diagram
            weights_axes = hinton_diagram(connectivity.weights[order_rows, order_columns], num)
            weights_figure = None
        else:
            # weights matrix
            weights_figure = pyplot.figure(num="Connectivity weights", figsize=self.config.largest_size())
            weights_axes = weights_figure.gca()
            wimg = weights_axes.matshow(connectivity.weights[order_rows, order_columns])
            weights_figure.colorbar(wimg)

        weights_axes.set_title(plot_title)

        weights_axes.set_yticks(numpy.arange(connectivity.number_of_regions))
        weights_axes.set_yticklabels(list(labels[order]), fontsize=8)

        weights_axes.set_xticks(numpy.arange(connectivity.number_of_regions))
        weights_axes.set_xticklabels(list(labels[order]), fontsize=8, rotation=90)

        self._save_figure(weights_figure, plot_title)
        self._check_show()

        if plot_tracts:
            # tract lengths matrix
            tracts_figure = pyplot.figure(num="Tracts' lengths", figsize=self.config.largest_size())
            tracts_axes = tracts_figure.gca()
            timg = tracts_axes.matshow(connectivity.tract_lengths[order_rows, order_columns])
            tracts_axes.set_title("Tracts' lengths")
            tracts_figure.colorbar(timg)
            tracts_axes.set_yticks(numpy.arange(connectivity.number_of_regions))
            tracts_axes.set_yticklabels(list(labels[order]), fontsize=8)

            tracts_axes.set_xticks(numpy.arange(connectivity.number_of_regions))
            tracts_axes.set_xticklabels(list(labels[order]), fontsize=8, rotation=90)

            self._save_figure(tracts_figure)
            self._check_show()
            return weights_figure, weights_axes, tracts_figure, tracts_axes

        else:
            return weights_figure, weights_axes
