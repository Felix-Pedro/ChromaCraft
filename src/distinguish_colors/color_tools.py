#%%
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import matplotlib.patches as patches
import time
import seaborn as sns



def rgb_to_hex(rgb_color):
    """
    Converts an RGB color tuple to its corresponding hexadecimal representation.

    Args:
        rgb_color (tuple): A tuple containing the red, green, and blue values of the color, each ranging from 0 to 1.

    Returns:
        str: The hexadecimal representation of the color, in the format "#RRGGBB".
    """
    if rgb_color[0] == '#':
        return rgb_color
    r, g, b = int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)



def color_difference(color1, color2):
    """
    Calculates the Euclidean distance between two RGB colors.

    Parameters:
    color1 (numpy.ndarray): An array representing the first RGB color.
    color2 (numpy.ndarray): An array representing the second RGB color.

    Returns:
    float: The Euclidean distance between the two colors.
    """
    return np.sqrt(np.sum((color1 - color2) ** 2))

def is_color_distinguishable(new_color, existing_colors, min_color_diff=0.2, max_color_diff=2, debug=False):
    """
    Check if a new color is distinguishable from a list of existing colors.

    Args:
        new_color (tuple): RGB values of the new color.
        existing_colors (list): List of tuples with RGB values of existing colors.
        min_color_diff (float, optional): Minimum color difference threshold. Defaults to 0.2.
        max_color_diff (int, optional): Maximum color difference threshold. Defaults to 2 (Imposible, no actual maximum).
        debug (bool, optional): Whether to show debug plots. Defaults to False.

    Returns:
        bool: True if the new color is distinguishable, False otherwise.
    """
    for ec in existing_colors:
        if color_difference(new_color, ec) < min_color_diff or color_difference(new_color, ec) > max_color_diff:
            if debug:
                plt.figure(figsize=(12, 4))

                # Plot the current color
                plt.subplot(1, 3, 1)
                plt.bar(0, 1, color=rgb_to_hex(new_color), edgecolor='k')
                plt.title('Current Color')

                # Plot the comparison color
                plt.subplot(1, 3, 2)
                plt.bar(0, 1, color=rgb_to_hex(ec), edgecolor='k')
                plt.title('Comparison Color')

                # Show numeric color difference
                plt.subplot(1, 3, 3)
                diff = color_difference(new_color, ec)
                plt.axis('off')
                plt.text(0.1, 0.5, f'Diff: {diff:.2f}', fontsize=12, verticalalignment='center')

                plt.tight_layout()
                plt.title('Not Approved', fontsize=16, color='red')
                plt.show()
                time.sleep(1)

            return False
        if debug:
            plt.figure(figsize=(12, 4))

            # Plot the current color
            plt.subplot(1, 3, 1)
            plt.bar(0, 1, color=rgb_to_hex(new_color), edgecolor='k')
            plt.title('Current Color')

            # Plot the comparison color
            plt.subplot(1, 3, 2)
            plt.bar(0, 1, color=rgb_to_hex(ec), edgecolor='k')
            plt.title('Comparison Color')

            # Show numeric color difference
            plt.subplot(1, 3, 3)
            diff = color_difference(new_color, ec)
            plt.axis('off')
            plt.text(0.1, 0.5, f'Diff: {diff:.2f}', fontsize=12, verticalalignment='center')

            plt.tight_layout()
            plt.title('Partial Approve', fontsize=16, color=rgb_to_hex((0.8, 0.6, 0.0)))
            plt.show()
            time.sleep(0.6)

    return True

def generate_distinguishable_colors(n, min_color_diff=0.2, max_color_diff=2, debug=False, hexa=False, colors=[], custom_color_fn=None, progress_bar=True):
    """
    Generate a list of n distinguishable colors.

    Args:
        n (int): The number of colors to generate.
        min_color_diff (float): The minimum difference between two colors, it is a number between 0 and sqrt(3). Default is 0.2.
        max_color_diff (float): The maximum difference between two colors. Default is 2 (imposible, no actual maximum).
        debug (bool): Whether to plot the current color. Default is False.
        hexa (bool): Whether to return the colors in hexadecimal format. Default is False.
        colors (list): A list of colors to start with. Default is an empty list.
        custom_color_fn (function): A function that generates a custom color. Default is None.
        progress_bar (bool): Whether to show a progress bar. Default is True.

    Returns:
        list: A list of n distinguishable colors.
    """
    assert 0 < min_color_diff <= 2, 'The minimum color difference must be in the range (0, 2]'
    
    if progress_bar:
        pbar = tqdm(total=n)
    else:
        pbar = None

    while len(colors) < n:
        if custom_color_fn:
            new_color = custom_color_fn()
        else:
            new_color = np.random.rand(3)  # Generate a random RGB color

        if is_color_distinguishable(new_color, colors, min_color_diff, max_color_diff, debug):
            colors.append(new_color)
            if debug: plot_current_color(new_color)
            if pbar:
                pbar.update(1)

    if pbar:
        pbar.close()

    if hexa:
        return list(map(rgb_to_hex, colors))
    return colors

def calculate_layout(num_colors, max_cols=6):
    num_cols = min(num_colors, max_cols)
    num_rows = (num_colors + num_cols - 1) // num_cols
    return num_rows, num_cols

def plot_color_palette(colors, label_colors=True, label_size=10):
    """
    Plots a color palette with the given colors.

    Args:
    - colors: list of colors to be plotted. Each color can be a string (e.g. 'red', '') or a tuple of RGB values (e.g. (1, 0, 0)).
    - label_colors: boolean indicating whether to label each color with its hex code. Alternatively, a list of labels can be provided.
    - label_size: font size for the color labels.

    Returns:
    - None
    """
    num_colors = len(colors)
    num_rows, num_cols = calculate_layout(num_colors)

    figsize = (num_cols * 1.5, num_rows * 1.5)
    spacing = 1.2

    fig, ax = plt.subplots(figsize=figsize)

    for i, color in enumerate(colors):
        row = i // num_cols
        col = i % num_cols

        x = col
        y = (num_rows - row - 1) * spacing
        if isinstance(color, (list,tuple)) :
            color = rgb_to_hex(color)
        ax.add_patch(patches.Rectangle((x, y), 1, 1, facecolor=color))

        if label_colors:
            label = rgb_to_hex(color) if isinstance(label_colors, bool) else label_colors[i]
            ax.text(x + 0.5, y + 1.05, label, ha='center', va='center', fontsize=label_size)

    ax.set_xlim(0, num_cols)
    ax.set_ylim(0, num_rows * spacing)
    ax.axis('off')
    plt.show()

def plot_current_color(new_color):
    plt.figure(figsize=(5, 4))

    plt.bar(0, 1, color=rgb_to_hex(new_color), edgecolor='k')
    plt.title('Current Color')

    plt.title('Approved', fontsize=16, color='green')
    plt.show()
    time.sleep(1)

if __name__ == '__main__':
    sns.set_style('whitegrid')
    n = 24  # Change this to the number of colors you want
    min_color_diff = 0.25  # Minimum color difference
    max_color_diff = 1.2   # Maximum color difference

    colors = generate_distinguishable_colors(n, min_color_diff, max_color_diff, debug=True, hexa=True)

    # Example of using custom labels:
    # label_colors = ['Red', 'Green', 'Blue', ...]  # Provide labels for each color
    # plot_color_palette(colors, label_colors=label_colors)

    plot_color_palette(colors)

# %%
