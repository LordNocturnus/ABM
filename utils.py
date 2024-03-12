"""
Two prime numbers are used to encode both the x and y coordinate into a single integer
"""
import numpy.typing as npt  # type: ignore
import numpy as np
#import numba as nb # type: ignore

PRIMEX = 461

PRIMEY = 463

DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0), (0, 0))
PRIMEDIRECTIONS = (-PRIMEY, PRIMEX, PRIMEY, -PRIMEX, 0)

RNG = np.random.default_rng(0)


#@nb.jit(nopython=True)  # type: ignore
def pos_to_prime(x: int | npt.NDArray[int], y: int | npt.NDArray[int]) -> int | npt.NDArray[int]:
    return x * PRIMEX + y * PRIMEY


#@nb.jit(nopython=True)  # type: ignore
def prime_to_pos(prime: int | npt.NDArray[int]) -> tuple[int, int] | tuple[npt.NDArray[int], npt.NDArray[int]]:
    y = (prime % PRIMEX) // (PRIMEY - PRIMEX)
    x = (prime - y * PRIMEY) // PRIMEX
    return x, y


if __name__ == "__main__":
    for x in range(230):
        for y in range(230):
            print(x, y)
            x_2, y_2 = prime_to_pos(pos_to_prime(x, y))
            assert x == x_2
            assert y == y_2
