import numpy as np
from src.distinguish_colors.color_tools import generate_distinguishable_colors, is_color_distinguishable

def test_generate_distinguishable_colors():
    # Test that the function generates the correct number of colors
    assert len(generate_distinguishable_colors(10)) == 10
    assert len(generate_distinguishable_colors(100,0.01)) == 100

    # Test that the function generates distinguishable colors
    colors = generate_distinguishable_colors(10)
    for i, color in enumerate(colors):
        for j, other_color in enumerate(colors):
            if i != j:
                assert is_color_distinguishable(color, [other_color])

    # Test that the function generates colors with the correct minimum difference
    colors = generate_distinguishable_colors(10, min_color_diff=0.5)
    for i, color in enumerate(colors):
        for j, other_color in enumerate(colors):
            if i != j:
                assert np.sqrt(np.sum((color - other_color) ** 2)) >= 0.5

    # Test that the function generates colors with the correct maximum difference
    colors = generate_distinguishable_colors(10, max_color_diff=1.5)
    for i, color in enumerate(colors):
        for j, other_color in enumerate(colors):
            if i != j:
                assert np.sqrt(np.sum((color - other_color) ** 2)) <= 1.5

def test_is_color_distinguishable():
    # Test that the function correctly identifies distinguishable colors
    assert is_color_distinguishable(np.array([1, 0, 0]), [np.array([0, 1, 0]), np.array([0, 0, 1])])
    assert is_color_distinguishable(np.array([0, 1, 0]), [np.array([1, 0, 0]), np.array([0, 0, 1])])
    assert is_color_distinguishable(np.array([0, 0, 1]), [np.array([1, 0, 0]), np.array([0, 1, 0])])

    # Test that the function correctly identifies indistinguishable colors
    assert not is_color_distinguishable(np.array([1, 0, 0]), [np.array([0.9, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])])
    assert not is_color_distinguishable(np.array([0, 1, 0]), [np.array([1, 0, 0]), np.array([0, 0.9, 0]), np.array([0, 0, 1])])
    assert not is_color_distinguishable(np.array([0, 0, 1]), [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 0.9])])