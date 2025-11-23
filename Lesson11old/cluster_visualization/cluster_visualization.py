"""
Cluster Visualization with Overlap
Author: Yair Levi
Date: October 15, 2025

Generates 3 clusters with normal distribution and visualizes them with boundaries.
Total: 6000 points (2000 per cluster, with 2000 being overlap shared across clusters)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.cluster import KMeans
import matplotlib.patches as mpatches

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
TOTAL_POINTS = 6000
POINTS_PER_CLUSTER = 2000
OVERLAP_POINTS = 2000
NON_OVERLAP_PER_CLUSTER = (POINTS_PER_CLUSTER - OVERLAP_POINTS) // 3  # 0 points
OVERLAP_PER_CLUSTER = OVERLAP_POINTS // 3  # ~667 points per cluster from overlap

print("=" * 80)
print("CLUSTER VISUALIZATION WITH NORMAL DISTRIBUTION")
print("Author: Yair Levi")
print("=" * 80)

# Cluster parameters (mean_x, mean_y, std_x, std_y)
cluster_params = [
    {
        'name': 'Cluster 1 (Red)',
        'mean': [2, 2],
        'std': [1.5, 1.0],
        'color': 'red',
        'alpha': 0.6
    },
    {
        'name': 'Cluster 2 (Green)',
        'mean': [8, 3],
        'std': [1.2, 1.8],
        'color': 'green',
        'alpha': 0.6
    },
    {
        'name': 'Cluster 3 (Blue)',
        'mean': [5, 8],
        'std': [2.0, 1.3],
        'color': 'blue',
        'alpha': 0.6
    }
]

print(f"\nGenerating {TOTAL_POINTS} points total:")
print(f"  - {POINTS_PER_CLUSTER} points per cluster (3 clusters)")
print(f"  - {OVERLAP_POINTS} points are overlap (shared across all clusters)")
print(f"  - Distribution: Each cluster gets {OVERLAP_PER_CLUSTER} overlap + {NON_OVERLAP_PER_CLUSTER} unique")
print("\nCluster Parameters:")

# Generate overlap points first (in the center region between clusters)
print(f"\nGenerating {OVERLAP_POINTS} overlapping points...")
overlap_center = [5, 4.5]  # Center point between all clusters
overlap_std = [2.5, 2.0]   # Large std to spread across clusters

overlap_x = np.random.normal(overlap_center[0], overlap_std[0], OVERLAP_POINTS)
overlap_y = np.random.normal(overlap_center[1], overlap_std[1], OVERLAP_POINTS)
overlap_points = np.column_stack([overlap_x, overlap_y])

# Split overlap points among clusters
overlap_per_cluster = OVERLAP_POINTS // 3
overlap_remainder = OVERLAP_POINTS % 3

# Calculate points per cluster
cluster_splits = [overlap_per_cluster] * 3
for i in range(overlap_remainder):
    cluster_splits[i] += 1

# Generate points for each cluster
all_points = []
all_labels = []
point_types = []  # Track if point is overlap or unique

start_idx = 0
for i, params in enumerate(cluster_params):
    print(f"\n{params['name']}:")
    print(f"  Mean: ({params['mean'][0]}, {params['mean'][1]})")
    print(f"  Std Dev: ({params['std'][0]}, {params['std'][1]})")
    
    # Get overlap points for this cluster
    end_idx = start_idx + cluster_splits[i]
    cluster_overlap = overlap_points[start_idx:end_idx]
    
    # Generate unique points for this cluster
    unique_count = POINTS_PER_CLUSTER - cluster_splits[i]
    x_unique = np.random.normal(params['mean'][0], params['std'][0], unique_count)
    y_unique = np.random.normal(params['mean'][1], params['std'][1], unique_count)
    unique_points = np.column_stack([x_unique, y_unique])
    
    print(f"  Points: {cluster_splits[i]} overlap + {unique_count} unique = {POINTS_PER_CLUSTER} total")
    
    # Combine overlap and unique points
    cluster_points = np.vstack([cluster_overlap, unique_points])
    all_points.append(cluster_points)
    
    # Label points
    all_labels.extend([i] * POINTS_PER_CLUSTER)
    point_types.extend(['overlap'] * cluster_splits[i] + ['unique'] * unique_count)
    
    start_idx = end_idx

# Concatenate all cluster points
all_points = np.vstack(all_points)

print(f"\n✓ Total points generated: {len(all_points)}")
print(f"  - Cluster 1: {POINTS_PER_CLUSTER} points")
print(f"  - Cluster 2: {POINTS_PER_CLUSTER} points")
print(f"  - Cluster 3: {POINTS_PER_CLUSTER} points")
print(f"  - Overlap points distributed across clusters: {OVERLAP_POINTS}")

# Convert to numpy arrays
all_labels = np.array(all_labels)
point_types = np.array(point_types)

# Verify total
assert len(all_points) == TOTAL_POINTS, f"Expected {TOTAL_POINTS} but got {len(all_points)}"
assert np.sum(point_types == 'overlap') == OVERLAP_POINTS, "Overlap count mismatch"

print("\n" + "=" * 80)
print("CREATING VISUALIZATION")
print("=" * 80)

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Cluster Visualization with Normal Distribution\nAuthor: Yair Levi', 
             fontsize=14, fontweight='bold')

# Plot 1: Original clusters with overlap highlighted
print("\nPlot 1: Original clusters with overlap region highlighted...")

# Plot unique points first
for i, params in enumerate(cluster_params):
    cluster_mask = all_labels == i
    unique_mask = (point_types == 'unique') & cluster_mask
    
    ax1.scatter(all_points[unique_mask, 0], all_points[unique_mask, 1], 
               c=params['color'], alpha=params['alpha'], 
               s=30, label=f"{params['name']} (unique)", 
               edgecolors='black', linewidth=0.3)

# Plot overlap points with distinct marker
overlap_mask = point_types == 'overlap'
ax1.scatter(all_points[overlap_mask, 0], all_points[overlap_mask, 1], 
           c='yellow', alpha=0.7, s=40, label='Overlap Points', 
           marker='*', edgecolors='black', linewidth=0.5)

# Draw ellipses for cluster boundaries (2 standard deviations)
print("Drawing cluster boundaries (2σ ellipses)...")
for i, params in enumerate(cluster_params):
    ellipse = Ellipse(xy=params['mean'], 
                     width=4*params['std'][0],   # 2 std deviations each side
                     height=4*params['std'][1],  # 2 std deviations each side
                     angle=0, 
                     edgecolor=params['color'], 
                     facecolor='none', 
                     linewidth=2, 
                     linestyle='--',
                     label=f'{params["name"]} Boundary (2σ)')
    ax1.add_patch(ellipse)

ax1.set_xlabel('X Coordinate', fontsize=11)
ax1.set_ylabel('Y Coordinate', fontsize=11)
ax1.set_title('Original Clusters with Overlap Points Highlighted', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_aspect('equal', adjustable='box')

# Plot 2: K-Means clustering result
print("\nPlot 2: K-Means clustering visualization...")
print("Running K-Means algorithm (k=3)...")

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
predicted_labels = kmeans.fit_predict(all_points)
centers = kmeans.cluster_centers_

print(f"✓ K-Means clustering complete")
print(f"  Cluster centers found at:")
for i, center in enumerate(centers):
    print(f"    Cluster {i+1}: ({center[0]:.2f}, {center[1]:.2f})")

# Define colors for K-Means clusters
kmeans_colors = ['red', 'green', 'blue']

# Plot K-Means results
for i in range(3):
    mask = predicted_labels == i
    ax2.scatter(all_points[mask, 0], all_points[mask, 1], 
               c=kmeans_colors[i], alpha=0.6, s=30, 
               label=f'Cluster {i+1}', edgecolors='black', linewidth=0.3)

# Highlight overlap points in K-Means result
ax2.scatter(all_points[overlap_mask, 0], all_points[overlap_mask, 1], 
           c='yellow', alpha=0.5, s=50, marker='*',
           edgecolors='black', linewidth=0.5, zorder=3)

# Plot cluster centers
ax2.scatter(centers[:, 0], centers[:, 1], 
           c='black', s=300, marker='X', 
           edgecolors='white', linewidth=2,
           label='Cluster Centers', zorder=5)

# Draw Voronoi-like boundaries (simple approach using decision boundaries)
print("Drawing decision boundaries...")

# Create a mesh to plot decision boundaries
x_min, x_max = all_points[:, 0].min() - 1, all_points[:, 0].max() + 1
y_min, y_max = all_points[:, 1].min() - 1, all_points[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                     np.linspace(y_min, y_max, 500))

# Predict cluster for each point in mesh
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot decision boundaries
ax2.contour(xx, yy, Z, levels=[0.5, 1.5], 
           colors='black', linewidths=2, linestyles='--', alpha=0.8)

ax2.set_xlabel('X Coordinate', fontsize=11)
ax2.set_ylabel('Y Coordinate', fontsize=11)
ax2.set_title('K-Means Clustering Result (k=3)', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal', adjustable='box')

# Add statistics text box
overlap_percentage = (OVERLAP_POINTS / TOTAL_POINTS) * 100
stats_text = f"""Statistics:
Total Points: {TOTAL_POINTS}
Points per Cluster: {POINTS_PER_CLUSTER}
Overlap Points: {OVERLAP_POINTS} ({overlap_percentage:.1f}%)
Unique Points: {TOTAL_POINTS - OVERLAP_POINTS}
"""
fig.text(0.02, 0.02, stats_text, fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
         verticalalignment='bottom')

plt.tight_layout(rect=[0, 0.05, 1, 0.96])

print("\n✓ Visualization complete")
print("\n" + "=" * 80)
print("SAVING FIGURE")
print("=" * 80)

# Save the figure
output_filename = 'cluster_visualization.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"\n✓ Figure saved as: {output_filename}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"  Total points: {TOTAL_POINTS}")
print(f"  Cluster 1: {POINTS_PER_CLUSTER} points")
print(f"  Cluster 2: {POINTS_PER_CLUSTER} points")
print(f"  Cluster 3: {POINTS_PER_CLUSTER} points")
print(f"  Overlapping: {OVERLAP_POINTS} points (shared across clusters)")
print(f"  Unique: {TOTAL_POINTS - OVERLAP_POINTS} points")

# Display the plot
print("\nDisplaying plot...")
plt.show()

print("\n✓ Program execution completed successfully")
print("\nAuthor: Yair Levi")