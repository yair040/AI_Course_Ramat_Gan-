import numpy as np
import matplotlib.pyplot as plt

# 1. Create sinusoidal signal x with 10 cycles
cycles = 10
samples_per_cycle = 200
total_samples = cycles * samples_per_cycle

# Create time vector: 10 cycles, each cycle is 2*pi
t = np.linspace(0, cycles * 2 * np.pi, total_samples)

# Create sine signal with amplitude -1 to +1
x = np.sin(t)

# 2. Create h vector - 30 samples around the peak
# Find the peak in the first cycle (occurs at pi/2)
peak_index = samples_per_cycle // 4  # Peak occurs at quarter cycle

# Extract 30 samples centered around the peak (15 before, peak, 14 after)
half_window = 15
h_start = peak_index - half_window
h_end = peak_index + half_window
h = x[h_start:h_end + 1]  # 30 samples including the peak

# Flip h for proper convolution (template matching)
h_flipped = np.flip(h)

# 3. Run convolution between x and h
# Using 'same' mode to keep output same size as x
output = np.convolve(x, h_flipped, mode='same')

# Find peak locations in the convolution output
# Peaks should occur approximately every 200 samples
threshold = np.max(output) * 0.9  # 90% of maximum
peak_locations = []
for i in range(1, len(output) - 1):
    if output[i] > output[i-1] and output[i] > output[i+1] and output[i] > threshold:
        peak_locations.append(i)

# Remove duplicate detections (peaks within 100 samples of each other)
filtered_peaks = []
for peak in peak_locations:
    if not filtered_peaks or peak - filtered_peaks[-1] > 100:
        filtered_peaks.append(peak)

print(f"Number of detected peaks: {len(filtered_peaks)}")
print(f"Peak locations (sample indices): {filtered_peaks}")

# 4. Draw the graphs
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

# Plot 1: Original sinusoidal signal
ax1.plot(t, x, 'b-', linewidth=1.5, label='Sine signal')
ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax1.set_xlabel('Time (radians)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Original Sinusoidal Signal (10 cycles)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Plot 2: Template h used for convolution
t_h = np.linspace(0, len(h) / samples_per_cycle * 2 * np.pi, len(h))
ax2.plot(t_h, h, 'r-', linewidth=2, marker='o', markersize=3, label='Template (h)')
ax2.set_xlabel('Time (radians)')
ax2.set_ylabel('Amplitude')
ax2.set_title('Template Signal (30 samples around peak)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Plot 3: Convolution output with detected peaks
ax3.plot(t, output, 'g-', linewidth=1.5, label='Convolution output')
ax3.plot(t[filtered_peaks], output[filtered_peaks], 'ro', markersize=10, 
         label=f'Detected peaks ({len(filtered_peaks)})', zorder=5)
ax3.axhline(y=threshold, color='orange', linestyle='--', alpha=0.5, 
            label='Detection threshold')
ax3.set_xlabel('Time (radians)')
ax3.set_ylabel('Convolution Response')
ax3.set_title('Peak Detection Output (Convolution Result)')
ax3.grid(True, alpha=0.3)
ax3.legend()

plt.tight_layout()
plt.show()

# Print summary
print(f"\nSummary:")
print(f"Total samples: {total_samples}")
print(f"Samples per cycle: {samples_per_cycle}")
print(f"Template length: {len(h)} samples")
print(f"Expected peak spacing: ~{samples_per_cycle} samples")
print(f"Actual peak spacings: {[filtered_peaks[i+1] - filtered_peaks[i] for i in range(len(filtered_peaks)-1)]}")