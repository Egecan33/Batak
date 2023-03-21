import matplotlib.pyplot as plt
import numpy as np


def josephus_problem(num_seats, your_position):
    if num_seats == 1:
        return 0

    return (josephus_problem(num_seats - 1, your_position) + your_position) % num_seats


def visualize_josephus_problem(num_seats, safe_position):
    angle = 2 * np.pi / num_seats
    x = [np.cos(angle * i) for i in range(num_seats)]
    y = [np.sin(angle * i) for i in range(num_seats)]

    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, c="b", s=100)

    for i in range(num_seats):
        plt.text(
            x[i] * 1.1,
            y[i] * 1.1,
            str(i),
            fontsize=12,
            color="k",
            ha="center",
            va="center",
        )

    plt.text(x[safe_position], y[safe_position], "Safe", fontsize=12, color="r")
    plt.gca().set_aspect("equal", adjustable="box")

    plt.axis("off")
    plt.title(f"Josephus Problem: {num_seats} seats")
    plt.show()


if __name__ == "__main__":
    num_seats = 40
    your_position = 2

    safe_position = josephus_problem(num_seats, your_position)
    print(f"The safe position is: {safe_position}")

    visualize_josephus_problem(num_seats, safe_position)
