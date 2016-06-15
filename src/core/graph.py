"""
    Graphing methods used by EPANET and SWMM
    In this first draft, the two are separate below.
    Can merge in future when output APIs are harmonized or datasets are passed in instead of selection criteria.
"""

import matplotlib.pyplot as plt
from matplotlib import dates
import colorsys
import datetime
import numpy as np
# from Externals.epanet.outputapi.ENOutputWrapper import ENR_demand
ENR_demand = 0  # Avoid importing so SWMM does not depend on EPANET


class SWMM:
    """
        Graphing methods used by SWMM.
        parameter output is defined in Externals.swmm.outputapi.SMOutputWrapper as OutputObject
    """
    @staticmethod
    def plot_scatter(output, title,
                     object_type_label_x, object_id_x, attribute_name_x,
                     object_type_label_y, object_id_y, attribute_name_y,
                     start_index=0, num_steps=-1):
        """ Read the specified data from SWMM output and create a scatter plot.
            Args
            output: Externals.swmm.outputapi.SMOutputWrapper.OutputObject which has the output of interest open.
            title: Text to display as title of graph window
            object_type_label_x: type of object to use for x values: "Subcatchment", "Node", or "Link"
            object_id_x: identifier/name of the Subcatchment, Node, or Link to supply x values
            attribute_name_x: name from the AttributeNames list of SMO_subcatchment, SMO_node or SMO_link.
            object_type_label_y: "Subcatchment", "Node", or "Link"
            object_id_y: identifier/name of the Subcatchment, Node, or Link to supply y values
            attribute_name_y: name from the AttributeNames list of SMO_subcatchment, SMO_node or SMO_link.
            start_index: first model time step to include. Default = 0 (start at the first value)
            num_steps: number of model time steps to use. Default = -1 (end at the last value)
            """
        fig = plt.figure()
        # if num_steps < self.output.numPeriods:
        fig.canvas.set_window_title(title)
        plt.title(title)

        x_values, x_units = output.get_series_by_name(object_type_label_x,
                                                      object_id_x,
                                                      attribute_name_x,
                                                      start_index, num_steps)

        y_values, y_units = output.get_series_by_name(object_type_label_y,
                                                      object_id_y,
                                                      attribute_name_y,
                                                      start_index, num_steps)

        plt.scatter(x_values, y_values, s=15, alpha=0.5)

        if x_units:
            x_units = ' (' + x_units + ')'

        if y_units:
            y_units = ' (' + y_units + ')'

        plt.xlabel(object_type_label_x + ' ' + object_id_x + ' ' + attribute_name_x + x_units)
        plt.ylabel(object_type_label_y + ' ' + object_id_y + ' ' + attribute_name_y + y_units)

        plt.grid(True)
        plt.show()

    @staticmethod
    def plot_time(output, lines_list, elapsed_flag, start_index, num_steps):
        fig = plt.figure()
        title = "Time Series Plot"
        fig.canvas.set_window_title(title)
        plt.title(title)
        left_y_plot = fig.add_subplot(111)
        right_y_plot = None
        lines_plotted = []
        line_legends = []
        x_values = []
        for time_index in range(start_index, num_steps):
            elapsed_hours = output.elapsed_hours_at_index(time_index)
            if elapsed_flag:
                x_values.append(elapsed_hours)
            else:
                x_values.append(output.StartDate + datetime.timedelta(hours=elapsed_hours))
                left_y_plot.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))

        for line in lines_list:
            type_label, object_id, attribute, axis, legend_text = line.split(',', 4)
            legend_text = legend_text.strip('"')
            y_values, units = output.get_series_by_name(type_label, object_id, attribute, start_index, num_steps)
            if y_values:
                if axis == "Left":
                    plot_on = left_y_plot
                else:
                    if not right_y_plot:
                        right_y_plot = fig.add_subplot(111, sharex=left_y_plot, frameon=False)
                        right_y_plot.yaxis.set_label_position("right")
                        right_y_plot.yaxis.tick_right()  # Only show right-axis tics on right axis
                        left_y_plot.yaxis.tick_left()    # Only show left-axis tics on left axis
                    plot_on = right_y_plot

                color = colorsys.hsv_to_rgb(np.random.rand(), 1, 1)
                new_line = plot_on.plot(x_values, y_values, label=legend_text, c=color)[0]
                lines_plotted.append(new_line)
                line_legends.append(legend_text)
                old_label = plot_on.get_ylabel()
                if not old_label:
                    plot_on.set_ylabel(units)
                elif units not in old_label:
                    plot_on.set_ylabel(old_label + ', ' + units)

        # fig.suptitle("Time Series Plot")
        # plt.ylabel(parameter_label)
        if elapsed_flag:
            plt.xlabel("Time (hours)")
        else:
            plt.xlabel("Time")
            fig.autofmt_xdate()
        if not right_y_plot:
            plt.grid(True)  # Only show background grid if there is only a left Y axis
        plt.legend(lines_plotted, line_legends, loc="best")
        plt.show()


class EPANET:

    @staticmethod
    def plot_time(output, get_index, get_value, parameter_code, parameter_label, ids):
        fig = plt.figure()
        title = "Time Series Plot of " + parameter_label
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        for time_index in range(0, output.numPeriods):
            x_values.append(output.elapsed_hours_at_index(time_index))

        line_count = 0
        for each_id in ids:
            output_index = get_index(each_id)
            y_values = []
            for time_index in range(0, output.numPeriods):
                y_values.append(get_value(output_index, time_index, parameter_code))
            plt.plot(x_values, y_values, label=each_id)
            line_count += 1

        if line_count > 0:
            # fig.suptitle("Time Series Plot")
            plt.ylabel(parameter_label)
            plt.xlabel("Time (hours)")
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            plt.close()
            raise Exception("No lines were selected to graph")

    @staticmethod
    def update_profile(output, graph_ids, x_values, get_index, get_value, parameter_code, parameter_label, fig_number, time_index):
        if time_index >= 0:
            fig = plt.figure(fig_number)
            fig.clear()
            title = "Profile Plot of " + parameter_label + " at " + output.get_time_string(time_index)
            fig.canvas.set_window_title(title)
            plt.title(title)
            y_values = []
            min_y = 999.9

            for (graph_id, x_value) in zip(graph_ids, x_values):
                output_index = get_index(graph_id)
                y = get_value(output_index, time_index, parameter_code)
                if min_y == 999.9 or y < min_y:
                    min_y = y
                y_values.append(y)
                plt.annotate(
                    graph_id,
                    xy=(x_value, y), xytext=(0, 20),
                    textcoords='offset points', ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
                #, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

            plt.fill_between(x_values, y_values, min_y)

            plt.ylabel(parameter_label)
            plt.xlabel("Index")
            plt.grid(True)
            fig.canvas.draw()
            plt.show()

    @staticmethod
    def plot_freq(output, get_index, get_value, parameter_code, parameter_label, time_index, ids):
        if time_index < 0:
            raise Exception("Time index not selected, cannot plot frequency")
        count = len(ids)
        if count < 1:
            raise Exception("No items in list, cannot plot frequency")
        fig = plt.figure()
        title = "Distribution of " + parameter_label + " at " + output.get_time_string(time_index)
        fig.canvas.set_window_title(title)
        plt.title(title)
        percent = []
        values = []
        index = 0
        for each_id in ids:
            percent.append(index * 100 / count)
            index += 1
            output_index = get_index(each_id)
            values.append(get_value(output_index, time_index, parameter_code))

        values.sort()
        # Cumulative distributions:
        plt.plot(values, percent)  # From 0 to the number of data points-1
        # plt.step(values[::-1], np.arange(len(values)))  # From the number of data points-1 to 0

        plt.ylabel("Percent Less Than")
        plt.xlabel(parameter_label)
        plt.grid(True)
        plt.show()

    def plot_system_flow(output):
        if output.nodeCount < 1:
            raise Exception("No node results present in output, cannot plot system flow")
        fig = plt.figure()
        title = "System Flow Balance"
        fig.canvas.set_window_title(title)
        plt.title(title)
        x_values = []
        produced = []
        consumed = []
        for time_index in range(0, output.numPeriods):
            x_values.append(output.elapsed_hours_at_index(time_index))
            produced.append(0)
            consumed.append(0)

        for node_index in range(0, output.nodeCount - 1):
            node_flows = output.get_NodeSeries(node_index, ENR_demand)
            for time_index in range(0, output.numPeriods):
                flow = node_flows[time_index]
                if flow > 0:
                    consumed[time_index] += flow
                else:
                    produced[time_index] -= flow

        plt.plot(x_values, consumed, label="Consumed")
        plt.plot(x_values, produced, label="Produced")

        # fig.suptitle("Time Series Plot")
        plt.ylabel("Flow")
        plt.xlabel("Time (hours)")
        plt.grid(True)
        plt.legend()
        plt.show()
