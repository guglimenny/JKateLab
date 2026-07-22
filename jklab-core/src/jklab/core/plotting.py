# ==========================================================
# plotting.py
#
# Basic plotting utilities.
#
# ==========================================================

import typing as tp
import numpy as np
import matplotlib.pyplot as plt

from . import exceptions as mex

# ==========================================================
# FIGURE SIZE DEFAULTS
# ==========================================================

RECT_WIDTH_SCALE = 8
RECT_HEIGHT_SCALE = 6

SQUARE_SCALE = 6

# ==========================================================
# STYLE DEFAULTS
# ==========================================================

LABEL_FONTSIZE = 20
TITLE_FONTSIZE = 22
TITLE_FONTSIZE_LARGE = 26
LEGEND_FONTSIZE = 16

DEFAULT_LINESTYLE = "-"
DEFAULT_LINEWIDTH = 2

DEFAULT_MARKER = ""

DEFAULT_MARKER_EDGECOLOR = "black"
DEFAULT_MARKER_EDGEWIDTH = 1

DEFAULT_MARKERSIZE = 8

TICK_FONTSIZE = 10

# ==========================================================
# INTERNAL UTILITIES
# ==========================================================

def _to_list(
    obj: tp.Any
) -> list:
    """
    Convert a single object to a one-element list.

    Lists and tuples are returned unchanged.
    """

    if isinstance(obj, (list, tuple)):
        return list(obj)

    return [obj]


def _expand_list(
    value: tp.Any,
    n: int,
    default: tp.Any = None
) -> list:
    """
    Expand a scalar value to a list of length n.

    Parameters
    ----------
    value : object
        Scalar or list-like value.

    n : int
        Desired output length.

    default : object, optional
        Default value used when value is None.

    Returns
    -------
    list
        List of length n.
    """

    if value is None:
        return [default] * n

    if isinstance(value, (list, tuple, np.ndarray)):

        if len(value) != n:
            mex.raise_error(
                error_type="value",
                module_name="plotting",
                function_name="_expand_list",
                message="Expected n values, got len(value)",
                n=n,
                nvalue=len(value)
            )

        return list(value)

    return [value] * n


def _expand_multiple_list(
    n: int,
    **kwargs
) -> dict:
    """
    Expand multiple plotting arguments to lists of
    length n.

    Parameters
    ----------
    n : int
        Number of curves.

    **kwargs
        Arguments passed as:

            name=(value, default)

    Returns
    -------
    dict
        Dictionary containing expanded arguments.
    """

    expanded = {}

    for key, (value, default) in kwargs.items():

        expanded[key] = _expand_list(
            value,
            n,
            default=default
        )

    return expanded

# ==========================================================
# TICKS
# ==========================================================

def _set_ticks(
    ax,
    xscale="linear",
    yscale="linear",

    xtick_step=None,
    ytick_step=None,

    xtick_values=None,
    ytick_values=None,

    xtick_labels=None,
    ytick_labels=None
):
    """
    Configure axis ticks.

    Tick precedence is:

    1. Explicit tick values (xtick_values / ytick_values)
    2. Automatic tick generation from tick step
       (xtick_step / ytick_step)
    3. Matplotlib defaults

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Target axes.

    xscale : {"linear", "log"}, optional
        X-axis scale.

    yscale : {"linear", "log"}, optional
        Y-axis scale.

    xtick_step : float or None, optional
        Tick spacing used to automatically generate
        x-axis ticks for linear scales.

    ytick_step : float or None, optional
        Tick spacing used to automatically generate
        y-axis ticks for linear scales.

    xtick_values : array-like or None, optional
        Explicit x-axis tick positions. If provided,
        they take precedence over xtick_step.

    ytick_values : array-like or None, optional
        Explicit y-axis tick positions. If provided,
        they take precedence over ytick_step.

    xtick_labels : array-like or None, optional
        Labels associated with xtick_values.
        If None, matplotlib default labels are used.

    ytick_labels : array-like or None, optional
        Labels associated with ytick_values.
        If None, matplotlib default labels are used.

    Returns
    -------
    None
    """

    # ======================================================
    # X-axis ticks
    # ======================================================
    if xtick_values is not None:

        if xtick_labels is None:

            ax.set_xticks(
                xtick_values
            )

        else:

            ax.set_xticks(
                xtick_values,
                labels=xtick_labels
            )

    elif (
        xtick_step is not None
        and xscale == "linear"
    ):

        xmin, xmax = ax.get_xlim()

        start = (
            np.floor(xmin / xtick_step)
            * xtick_step
        )

        stop = (
            np.ceil(xmax / xtick_step)
            * xtick_step
        )

        ax.set_xticks(
            np.arange(
                start,
                stop + xtick_step,
                xtick_step
            )
        )

    # ======================================================
    # Y-axis ticks
    # ======================================================
    if ytick_values is not None:

        if ytick_labels is None:

            ax.set_yticks(
                ytick_values
            )

        else:

            ax.set_yticks(
                ytick_values,
                labels=ytick_labels
            )

    elif (
        ytick_step is not None
        and yscale == "linear"
    ):

        ymin, ymax = ax.get_ylim()

        start = (
            np.floor(ymin / ytick_step)
            * ytick_step
        )

        stop = (
            np.ceil(ymax / ytick_step)
            * ytick_step
        )

        ax.set_yticks(
            np.arange(
                start,
                stop + ytick_step,
                ytick_step
            )
        )

    return None

# ==========================================================
# FIGURE SIZE
# ==========================================================

def get_figsize(
    nrows: int = 1,
    ncols: int = 1,
    shape: str = "rect",
    rect_width_scale: float = RECT_WIDTH_SCALE,
    rect_height_scale: float = RECT_HEIGHT_SCALE,
    square_scale: float = SQUARE_SCALE
) -> tuple[float, float]:
    """
    Compute figure size for a subplot grid.
    """

    if shape == "rect":

        return (
            ncols * rect_width_scale,
            nrows * rect_height_scale
        )

    if shape == "square":

        return (
            ncols * square_scale,
            nrows * square_scale
        )

    mex.raise_error(
        error_type="value",
        module_name="plotting",
        function_name="get_figsize",
        message=("Unknown figure shape."
                 "Expected 'rect' or 'square'"),
        shape=shape
    )

# ==========================================================
# LINE PLOTS
# ==========================================================

def plot_line(
    xdata_list,
    ydata_list,
    yerr_list=None,
    mask_list=None,
    label_list=None,

    color_list=None,
    linestyle_list=None,
    linewidth_list=None,
    marker_list=None,
    marker_size_list=None,
    marker_edgecolor_list=None,
    marker_edgewidth_list=None,

    figsize=None,
    figshape="rect",

    xscale="linear",
    yscale="linear",

    xlim=None,
    ylim=None,

    xlabel="",
    ylabel="",
    title="",

    legend_fontsize=LEGEND_FONTSIZE,
    xlabel_fontsize=LABEL_FONTSIZE,
    ylabel_fontsize=LABEL_FONTSIZE,
    title_fontsize=TITLE_FONTSIZE,

    xtick_step=None,
    ytick_step=None,
    xtick_values=None,
    ytick_values=None,
    xtick_labels=None,
    ytick_labels=None,
    xtick_fontsize=TICK_FONTSIZE,
    ytick_fontsize=TICK_FONTSIZE,

    show_legend=True,
    legend_loc="best",
    show_legend_frame=True,
    reverse_legend=False,
    wrap_title=False,

    tight_layout=True,
    savefig=None,
    show=True
) -> tuple:
    
    """
    Plot one or more line datasets.

    Parameters
    ----------
    xdata_list : array-like or list of array-like
        X-axis data.

    ydata_list : array-like or list of array-like
        Y-axis data.

    yerr_list : array-like, list of array-like, or None, optional
        Error bars associated with each curve.

    mask_list : array-like, list of array-like, or None, optional
        Boolean masks used to select plotted data points.

    label_list : str, list of str, or None, optional
        Curve labels used in the legend.

    color_list : str, list of str, or None, optional
        Curve colors.

    linestyle_list : str, list of str, or None, optional
        Line styles.

    linewidth_list : float, list of float, or None, optional
        Line widths.

    marker_list : str, list of str, or None, optional
        Marker styles.

    marker_size_list : float, list of float, or None, optional
        Marker sizes.

    marker_edgecolor_list : str, list of str, or None, optional
        Marker edge colors.

    marker_edgewidth_list : float, list of float, or None, optional
        Marker edge widths.

    figsize : tuple, optional
        Figure size passed to matplotlib.

    xscale : {"linear", "log"}, optional
        X-axis scale.

    yscale : {"linear", "log"}, optional
        Y-axis scale.

    xlim : tuple or None, optional
        X-axis limits.

    ylim : tuple or None, optional
        Y-axis limits.

    xlabel : str, optional
        X-axis label.

    ylabel : str, optional
        Y-axis label.

    title : str, optional
        Figure title.

    legend_fontsize : float, optional
        Legend font size.

    xlabel_fontsize : float, optional
        X-axis label font size.

    ylabel_fontsize : float, optional
        Y-axis label font size.

    title_fontsize : float, optional
        Figure title font size.

    xtick_step : float or None, optional
        Tick spacing for a linear X axis.

    ytick_step : float or None, optional
        Tick spacing for a linear Y axis.

    xtick_fontsize : float, optional
        X-axis tick-label font size.

    ytick_fontsize : float, optional
        Y-axis tick-label font size.

    show_legend : bool, optional
        If True, display the legend whenever at least one
        curve label is provided.

    legend_loc : str, optional
        Legend location passed to matplotlib.

    show_legend_frame : bool, optional
        If True, display the legend frame.

    reverse_legend : bool, optional
        If True, legend labels are displayed in reverse
        order.

    wrap_title : bool, optional
        If True, wrap long titles automatically.

    tight_layout : bool, optional
        If True, apply matplotlib tight_layout().

    savefig : str or pathlib.Path, optional
        Output path used to save the figure.

    show : bool, optional
        If True, display the figure using matplotlib.

    Returns
    -------
    tuple
        (fig, ax) matplotlib figure and axes objects.

    Notes
    -----
    All curve-specific arguments support either:

    - a single value applied to all curves;
    - a list containing one value per curve.

    If show=False, the figure is automatically closed to
    prevent notebook auto-rendering while still allowing
    (fig, ax) to be returned.
    """

    # === Curve data ===
    xdata_list = _to_list(xdata_list)
    ydata_list = _to_list(ydata_list)

    ncurves = len(ydata_list)

    if len(xdata_list) != ncurves:
        mex.raise_error(
            error_type="value",
            module_name="plotting",
            function_name="plot_line",
            message=("xdata_list and ydata_list must "
                     "contain the same number of curves"),
            nxcurves=len(xdata_list),
            nycurves=len(ydata_list)
        )

    plot_args = _expand_multiple_list(
        ncurves,

        yerr_list=(yerr_list, None),
        mask_list=(mask_list, slice(None)),

        label_list=(label_list, None),
        color_list=(color_list, None),

        linestyle_list=(
            linestyle_list,
            DEFAULT_LINESTYLE
        ),

        linewidth_list=(
            linewidth_list,
            DEFAULT_LINEWIDTH
        ),

        marker_list=(
            marker_list,
            DEFAULT_MARKER
        ),

        marker_size_list=(
            marker_size_list,
            DEFAULT_MARKERSIZE
        ),

        marker_edgecolor_list=(
            marker_edgecolor_list,
            DEFAULT_MARKER_EDGECOLOR
        ),

        marker_edgewidth_list=(
            marker_edgewidth_list,
            DEFAULT_MARKER_EDGEWIDTH
        )
    )

    yerr_list = plot_args["yerr_list"]
    mask_list = plot_args["mask_list"]

    label_list = plot_args["label_list"]
    color_list = plot_args["color_list"]

    linestyle_list = plot_args["linestyle_list"]
    linewidth_list = plot_args["linewidth_list"]

    marker_list = plot_args["marker_list"]
    marker_size_list = plot_args["marker_size_list"]

    marker_edgecolor_list = plot_args["marker_edgecolor_list"]
    marker_edgewidth_list = plot_args["marker_edgewidth_list"]

    # === Figure ===
    if figsize is None:
        figsize = get_figsize(shape=figshape)

    # === Axes ===
    fig, ax = plt.subplots(
        figsize=figsize
    )

    for (
        xdata,
        ydata,
        yerr,
        mask,
        label,
        color,
        linestyle,
        linewidth,
        marker,
        marker_size,
        marker_edgecolor,
        marker_edgewidth
    ) in zip(
        xdata_list,
        ydata_list,
        yerr_list,
        mask_list,
        label_list,
        color_list,
        linestyle_list,
        linewidth_list,
        marker_list,
        marker_size_list,
        marker_edgecolor_list,
        marker_edgewidth_list
    ):

        if yerr is None:

            ax.plot(
                xdata[mask],
                ydata[mask],
                label=label,
                color=color,
                linestyle=linestyle,
                linewidth=linewidth,
                marker=marker,
                markersize=marker_size,
                markeredgecolor=marker_edgecolor,
                markeredgewidth=marker_edgewidth,
            )

        else:

            ax.errorbar(
                xdata[mask],
                ydata[mask],
                yerr[mask],
                label=label,
                color=color,
                linestyle=linestyle,
                linewidth=linewidth,
                marker=marker,
                markersize=marker_size,
                markeredgecolor=marker_edgecolor,
                markeredgewidth=marker_edgewidth,
            )

    # === Axis scale ===
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    # === Axis lim ===
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # === Axis label ===
    ax.set_xlabel(
        xlabel,
        fontsize=xlabel_fontsize
    )

    ax.set_ylabel(
        ylabel,
        fontsize=ylabel_fontsize
    )

    # === Title ===
    ax.set_title(
        title,
        fontsize=title_fontsize,
        wrap=wrap_title
    )

    # === Legend ===
    if (
        show_legend
        and any(
            label is not None
            for label in label_list
        )
    ):
        ax.legend(
            fontsize=legend_fontsize,
            loc=legend_loc,
            frameon=show_legend_frame,
            reverse=reverse_legend
        )

    # === Ticks ===
    _set_ticks(
        ax=ax,
        xscale=xscale,
        yscale=yscale,
        xtick_step=xtick_step,
        ytick_step=ytick_step,
        xtick_values=xtick_values,
        ytick_values=ytick_values,
        xtick_labels=xtick_labels,
        ytick_labels=ytick_labels
    )

    ax.tick_params(
        axis="x",
        labelsize=xtick_fontsize
    )

    ax.tick_params(
        axis="y",
        labelsize=ytick_fontsize
    )

    # === Tight layout ===
    if tight_layout:
        fig.tight_layout()

    # === Savefig ===
    if savefig is not None:

        fig.savefig(
            savefig,
            bbox_inches="tight"
        )

    # === Show and close ===
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax

# ==========================================================
# CBAR HELPER FUNCTIONS
# ==========================================================

def _handle_cbar_range(
    data,
    cbar_min=None,
    cbar_max=None,
    symmetric_cbar=False
) -> tuple:
    """
    Determine colorbar limits.

    Parameters
    ----------
    data : array-like
        Grid data.

    cbar_min : float or None, optional
        Lower colorbar limit.

    cbar_max : float or None, optional
        Upper colorbar limit.

    symmetric_cbar : bool, optional
        If True, enforce symmetric colorbar limits
        around zero.

    Returns
    -------
    tuple
        (cbar_min, cbar_max)

    Notes
    -----
    If symmetric_cbar is True:

        cbar_min = -cbar_max

    whenever one of the two limits is omitted.

    Raises
    ------
    ValueError
        If data contains NaN values.

    ValueError
        If symmetric_cbar=True and both
        cbar_min and cbar_max are specified.
    """

    data = np.asarray(data)

    if np.isnan(data).any():
        mex.raise_error(
            error_type="value",
            module_name="plotting",
            function_name="_handle_cbar_range",
            message="Grid data contains NaN values"
        )

    if not symmetric_cbar:

        if cbar_min is None:
            cbar_min = np.min(data)

        if cbar_max is None:
            cbar_max = np.max(data)

    else:

        if (
            cbar_min is not None
            and cbar_max is not None
        ):    
            mex.raise_error(
                error_type="value",
                module_name="plotting",
                function_name="_handle_cbar_range",
                message=("Can't specify both cbar_min and "
                         "cbar_max if symmetric_cbar=True"),
                cbar_min=cbar_min,
                cbar_max=cbar_max,
                symmetric_cbar=symmetric_cbar
            )

        if cbar_min is None and cbar_max is None:

            cbar_max = np.max(
                np.abs(data)
            )

            cbar_min = -cbar_max

        elif cbar_min is None:

            cbar_min = -cbar_max

        elif cbar_max is None:

            cbar_max = -cbar_min

    return cbar_min, cbar_max


def _handle_cbar_range_list(
    data_list,
    cbar_min_list=None,
    cbar_max_list=None,
    symmetric_cbar_list=False,
    global_cbar_range=False
) -> list[tuple[float, float]]:

    ncbar = len(data_list)

    if global_cbar_range:
        
        global_min, global_max = _handle_cbar_range(
            data=data_list,
            cbar_min=cbar_min_list,
            cbar_max=cbar_max_list,
            symmetric_cbar=symmetric_cbar_list
        )

        cbar_list = [(global_min, global_max)] * len(data_list)

    else:

        cbar_args = _expand_multiple_list(
            ncbar,
            cbar_min_list=(cbar_min_list, None),
            cbar_max_list=(cbar_max_list, None),
            symmetric_cbar_list=(symmetric_cbar_list, None)
        )

        cbar_min_list = cbar_args["cbar_min_list"]
        cbar_max_list = cbar_args["cbar_max_list"]
        symmetric_cbar_list = cbar_args["symmetric_cbar_list"]

        cbar_list = [
            _handle_cbar_range(
                data,
                cbar_min=cbar_min,
                cbar_max=cbar_max,
                symmetric_cbar=symmetric_cbar
            )
            for data, cbar_min, cbar_max, symmetric_cbar in
            zip(
                data_list, 
                cbar_min_list, 
                cbar_max_list, 
                symmetric_cbar_list
            )
        ]

    return cbar_list

# ==========================================================
# IMSHOW PLOTS
# ==========================================================

def plot_imshow(
    image_data,

    image_cmap=None,
    cbar_min=None,
    cbar_max=None,
    symmetric_cbar=False,
    cbar_label="",
    cbar_location="right",
    cbar_label_fontsize=LABEL_FONTSIZE,
    cbar_tick_fontsize=TICK_FONTSIZE,

    figsize=None,
    figshape="square",
    image_origin="upper",

    xlim=None,
    ylim=None,

    xlabel="",
    ylabel="",
    title="",

    xlabel_fontsize=LABEL_FONTSIZE,
    ylabel_fontsize=LABEL_FONTSIZE,
    title_fontsize=TITLE_FONTSIZE,

    xtick_step=None,
    ytick_step=None,
    xtick_values=None,
    ytick_values=None,
    xtick_labels=None,
    ytick_labels=None,
    xtick_fontsize=TICK_FONTSIZE,
    ytick_fontsize=TICK_FONTSIZE,

    wrap_title=False,

    tight_layout=True,
    savefig=None,
    show=True
) -> tuple:
    """
    Plot a two-dimensional grid using imshow.

    Parameters
    ----------
    im_data : array-like
        imshow() grid values.

    im_cmap : matplotlib colormap, optional
        Colormap used for rendering.

    cbar_min, cbar_max : float or None, optional
        Colorbar limits.

    symmetric_cbar : bool, optional
        If True, use symmetric colorbar limits
        around zero.

    cbar_label : str, optional
        Colorbar label.

    cbar_location : str, optional
        Colorbar location passed to matplotlib.

    figsize : tuple, optional
        Figure size.

    figshape : str, optional
        Figure-shape preset used by get_figsize().

    im_origin : str or None, optional
        Origin argument passed to imshow().

    xlim, ylim : tuple or None, optional
        Axis limits.

    xlabel, ylabel, title : str, optional
        Axis labels and title.

    xtick_step, ytick_step : float or None, optional
        Automatic tick spacing.

    xtick_values, ytick_values : array-like or None, optional
        Explicit tick positions.

    xtick_labels, ytick_labels : array-like or None, optional
        Explicit tick labels.

    savefig : str or pathlib.Path, optional
        Output file.

    show : bool, optional
        If True, display the figure.

    Returns
    -------
    tuple
        (fig, ax)
    """

    # === Colorbar range ===
    cbar_min, cbar_max = _handle_cbar_range(
        image_data,
        cbar_min=cbar_min,
        cbar_max=cbar_max,
        symmetric_cbar=symmetric_cbar
    )

    # === Figure ===
    if figsize is None:
        figsize = get_figsize(
            shape=figshape
        )

    # === Axes ===
    fig, ax = plt.subplots(
        figsize=figsize
    )

    # === Image ===
    im = ax.imshow(
        image_data,
        cmap=image_cmap,
        vmin=cbar_min,
        vmax=cbar_max,
        origin=image_origin
    )

    # === Colorbar ===
    cbar = fig.colorbar(
        im,
        ax=ax,
        location=cbar_location
    )

    cbar.set_label(
        cbar_label,
        fontsize=cbar_label_fontsize
    )

    cbar.ax.tick_params(
        labelsize=cbar_tick_fontsize
    )

    # === Axis limits ===
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # === Labels ===
    ax.set_xlabel(
        xlabel,
        fontsize=xlabel_fontsize
    )

    ax.set_ylabel(
        ylabel,
        fontsize=ylabel_fontsize
    )

    # === Title ===
    ax.set_title(
        title,
        fontsize=title_fontsize,
        wrap=wrap_title
    )

    # === Ticks ===
    _set_ticks(
        ax=ax,
        xscale="linear",
        yscale="linear",
        xtick_step=xtick_step,
        ytick_step=ytick_step,
        xtick_values=xtick_values,
        ytick_values=ytick_values,
        xtick_labels=xtick_labels,
        ytick_labels=ytick_labels
    )

    ax.tick_params(
        axis="x",
        labelsize=xtick_fontsize
    )

    ax.tick_params(
        axis="y",
        labelsize=ytick_fontsize
    )

    # === Layout ===
    if tight_layout:
        fig.tight_layout()

    # === Save figure ===
    if savefig is not None:

        fig.savefig(
            savefig,
            bbox_inches="tight"
        )

    # === Show / close ===
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax

# ==========================================================
# GRID PLOTS
# ==========================================================

def plot_imshow_grid(
    image_data_list,
    nrows,
    ncols,

    subtitle_list=None,
    row_header_list=None,
    col_header_list=None,

    image_cmap=None,
    cbar_min_list=None,
    cbar_max_list=None,
    symmetric_cbar_list=False,
    cbar_location="right",
    global_cbar_range=False,

    figsize=None,
    figshape="square",
    constrained_layout=True,
    image_origin="upper",

    xlabel="",
    ylabel="",
    title="",

    subtitle_fontsize=TITLE_FONTSIZE,
    row_header_fontsize=TITLE_FONTSIZE_LARGE,
    col_header_fontsize=TITLE_FONTSIZE,
    xlabel_fontsize=LABEL_FONTSIZE,
    ylabel_fontsize=LABEL_FONTSIZE,
    title_fontsize=TITLE_FONTSIZE_LARGE,

    wrap_title=False,
    savefig=None,
    show=True
) -> tuple:
    
    nplots = nrows * ncols

    image_data_list = np.asarray(image_data_list)
    nimages = len(image_data_list)
    
    # === Validation ===
    if nimages < 1:
        mex.raise_error(
            error_type="value",
            module_name="plotting",
            function_name="plot_imshow_grid",
            message="image_data_list is empty",
            nplots=nimages
        )

    if nplots < nimages:
        mex.raise_error(
            error_type="value",
            module_name="plotting",
            function_name="plot_imshow_grid",
            message=("Grid is too small for the requested "
                     "number of images"),
            nimages=nimages,
            nplots=nplots,
            nrows=nrows,
            ncols=ncols,
        )

    if subtitle_list is not None:

        nlabels = len(subtitle_list)

        if nlabels == 0:
            mex.raise_error(
                error_type="value",
                module_name="plotting",
                function_name="plot_imshow_grid",
                message="subtitle_list is empty",
                nlabels=nlabels
            )

        if nlabels > nimages:
            mex.raise_error(
                error_type="value",
                module_name="plotting",
                function_name="plot_imshow_grid",
                message=("the grid has more "
                         "labels then plots"),
                nplots=nimages,
                nlabels=nlabels
            )

    # === Cbar list ===
    cbar_list = _handle_cbar_range_list(
        data_list=image_data_list,
        cbar_min_list=cbar_min_list,
        cbar_max_list=cbar_max_list,
        symmetric_cbar_list=symmetric_cbar_list,
        global_cbar_range=global_cbar_range
    )

    # === Figure ===
    if figsize is None:
        figsize = get_figsize(
            nrows=nrows,
            ncols=ncols,
            shape=figshape
        )

    # === Axes ===
    fig, axs = plt.subplots(
        nrows,
        ncols,
        figsize=figsize,
        constrained_layout=constrained_layout
    )

    axs = np.atleast_1d(axs).ravel()

    # === Grid ===
    for (
        image_idx, 
        image_data
    ) in enumerate(image_data_list):

        ax = axs[image_idx]

        cbar_min, cbar_max = cbar_list[image_idx]

        im = ax.imshow(
            image_data,
            cmap=image_cmap,
            vmin=cbar_min,
            vmax=cbar_max,
            origin=image_origin,
        )

        # === Colorbar ===
        cbar = fig.colorbar(
            im,
            ax=ax,
            location=cbar_location,
        )

        # === Labels ===
        if subtitle_list is not None:

            label = subtitle_list[image_idx % nlabels]
            ax.set_title(
                label,
                fontsize=subtitle_fontsize
            )

        row_idx = image_idx // ncols
        col_idx = image_idx % ncols

        # left side
        if row_header_list is not None and col_idx == 0:
            ax.text(
                -0.1, 0.5,
                row_header_list[image_idx // ncols],
                transform=ax.transAxes,
                ha="right",
                va="center",
                rotation=90,
                fontsize=row_header_fontsize
            )

        # top
        if col_header_list is not None and row_idx == 0:
            ax.set_title(
                col_header_list[col_idx],
                fontsize=col_header_fontsize
            )

        # === Axis label ===
        ax.set_xlabel(
            xlabel,
            fontsize=xlabel_fontsize
        )

        ax.set_ylabel(
            ylabel,
            fontsize=ylabel_fontsize
        )

    # === Title ===
    fig.suptitle(
        title,
        fontsize=title_fontsize,
        wrap=wrap_title
    )
    
    # === Close unused subplots ===
    if nplots > nimages:
        for ax in axs[nimages:]:
            fig.delaxes(ax)

    # === Save figure ===
    if savefig is not None:

        fig.savefig(
            savefig,
            bbox_inches="tight"
        )

    # === Show / close ===
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax