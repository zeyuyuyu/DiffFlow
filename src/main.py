import numpy as np

def calculate_differential_flow(input_data):
    """Calculates the differential flow between adjacent data points."""
    diff_flow = np.diff(input_data)
    return diff_flow

def main():
    # Example usage
    data = [10, 15, 12, 18, 20]
    result = calculate_differential_flow(data)
    print(f"Differential flow: {result}")

if __name__ == "__main__":
    main()