import matplotlib.pyplot as plt

from random_walk import RandomWalk

# Keep making new walks as long as the programm is active
while True:
    # Make a random walk
    rw = RandomWalk(1_000)     # number of walks argument
    rw.fill_walk_plot()

    # Plot the points in the walk
    plt.style.use('classic')
    fig, ax = plt.subplots(figsize =(16,9))
    point_numbers = range(rw.num_points)
    ax.plot(rw.x_values, rw.y_values, linewidth=1)

    # Emphasize starting and ending points
    ax.scatter(0,0, c = 'green', edgecolors='none', s = 100)
    ax.scatter(rw.x_values[-1], rw.y_values[-1], c='red', edgecolors='none', s=100)

    # # Remove axes
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)

    plt.show()

    keep_running = input("Make another walk? (y/n): ")
    if keep_running == 'n':
        break
