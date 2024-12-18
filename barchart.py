import matplotlib.pyplot as plt
import numpy as np
import argparse

# Read integers from the text file
def read_scores(file_path):
    with open(file_path, 'r') as file:
        scores = [int(line.strip()) for line in file]
    return scores

# Plot the distribution as a bar chart
def plot_score_distribution(scores, bin_size, max_bins):
    # Compute statistics
    average = np.mean(scores)
    median = np.median(scores)
    max = np.max(scores)
    min = np.min(scores)
    print(f"Average: {average:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Max: {max}")
    print(f"Min: {min}")

    # Create bins
    max_score = bin_size * max_bins
    bins = list(range(0, max_score + bin_size, bin_size))
    hist, bin_edges = np.histogram(scores, bins=bins)

    # Create the bar chart
    plt.bar(bin_edges[:-1], hist, width=bin_size, color='skyblue', edgecolor='black', align='edge')

    # Add vertical lines for average and median
    plt.axvline(average, color='red', linestyle='--', label=f'Average ({average:.2f})')
    plt.axvline(median, color='green', linestyle='--', label=f'Median ({median:.2f})')

    # Add labels and title
    plt.xlabel('Scores (binned)')
    plt.ylabel('Frequency')
    plt.title('Score Distribution')
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot score distribution from a text file.")
    parser.add_argument("file_path", type=str, help="Path to the text file containing scores.")
    parser.add_argument("--bin_size", type=int, default=100, help="Size of each bin (default: 100).")
    parser.add_argument("--max_bins", type=int, default=100, help="Maximum number of bins (default: 100).")

    args = parser.parse_args()

    try:
        scores = read_scores(args.file_path)
        plot_score_distribution(scores, args.bin_size, args.max_bins)
    except FileNotFoundError:
        print(f"Error: File '{args.file_path}' not found.")
    except ValueError:
        print("Error: File contains non-integer values.")
