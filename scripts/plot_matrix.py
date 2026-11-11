import numpy as np
import matplotlib.pyplot as plt

def plot_row_vectors(filename, output_image="vector_plot.png"):
    # Read the matrix from the text file
    matrix = np.loadtxt(filename)
    
    # Ensure it's treated as a 2D array even if it's a single row
    if matrix.ndim == 1:
        matrix = matrix.reshape(1, -1)
        
    num_vectors, dimensions = matrix.shape
    
    plt.figure(figsize=(8, 8))
    
    # Handle 2D vectors (Arrow plot)
    if dimensions == 2:
        ax = plt.gca()
        colors = plt.get_cmap('tab10', num_vectors)        
        # Origin point for all vectors
        origin_x = np.zeros(num_vectors)
        origin_y = np.zeros(num_vectors)
        
        # Vector components
        U = matrix[:, 0]
        V = matrix[:, 1]
        
        # Plot arrows
        ax.quiver(origin_x, origin_y, U, V, angles='xy', scale_units='xy', scale=1, 
                  color=[colors(i) for i in range(num_vectors)])
        
        # Dynamically set axis limits based on the largest vector magnitude
        max_val = np.max(np.abs(matrix)) * 1.2
        ax.set_xlim([-max_val, max_val])
        ax.set_ylim([-max_val, max_val])
        
        # Add grid and axes
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal')
        plt.title('2D Vector Plot')
        
    # Handle >2D vectors (Line plot)
    else:
        for i, row in enumerate(matrix):
            plt.plot(row, marker='o', label=f'Vector {i+1}')
            
        plt.title(f'{dimensions}-Dimensional Vectors')
        plt.xlabel('Component Index')
        plt.ylabel('Magnitude')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='upper right')

    # Save the plot as an image file instead of displaying it
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    plt.close() # Free up memory
    print(f"Plot successfully saved as '{output_image}'")

# Run the function
if __name__ == "__main__":
    # Create a sample file for testing if it doesn't exist
    sample_data = "-0.942857 0.334701\n-0.213603 0.577802"
    with open("matrix.txt", "w") as f:
        f.write(sample_data)
        
    # Call the function and specify the output image name
    plot_row_vectors("matrix.txt", "my_vectors.png")
