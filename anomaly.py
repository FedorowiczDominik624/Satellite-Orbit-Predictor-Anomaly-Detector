import math

def compute_position_residual(
    pos_a: tuple[float, float, float],
    pos_b: tuple[float, float, float],
) -> float:
    """Compute the scalar Euclidean distance between two 3D position vectors.

    Both positions must be in the same reference frame (e.g., ECI Cartesian, km).
    Returns the magnitude of the error vector |pos_b - pos_a|.
    """
    dx = (pos_b[0] - pos_a[0])
    dy = (pos_b[1] - pos_a[1])
    dz = (pos_b[2] - pos_a[2])

    d = math.sqrt(dx**2 + dy**2 + dz**2)

    return d

if __name__ == "__main__":
    pos_a = (7000, 0, 0)
    pos_b = (7000, 3, 4)
    residual = compute_position_residual(pos_a, pos_b)
    print(f"Predicted Position: {pos_a}")
    print(f"Observed Positions: {pos_b}")
    print(f"Residual Position: {residual:.1f} km")