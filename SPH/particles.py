"""
Defines the particle class and functionality
"""
import numpy as np
class Particle:
    _position: np.ndarray
    _velocity: np.ndarray
    _mass: float
    _smoothing_kernal: callable

    def __init__(self, position: list | np.ndarray, velocity: list | np.ndarray, mass: float, kernal: callable):
        self.position = position
        self.velocity = velocity
        self._mass = mass
        self._smoothing_kernal = kernal


    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, m: float):
        if not isinstance(m, float):
            try:
                m = float(m)
            except:
                raise ValueError(f"{m}, of type {type(m)} cannot be coerced into a floating point value")
        self._mass = m

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, pos: np.ndarray):
        if not isinstance(pos, np.ndarray):
            try:
                pos = np.asarray(pos)
            except:
                raise TypeError(f"{pos} is {type(pos)}, not a numpy array")
        if len(pos) != 2:
            raise ValueError(f"{pos} is not a 2D array, it is {len(pos)}D")
        if pos.dtype != np.float64:
            try:
                pos = pos.astype(np.float64)
            except:
                raise ValueError(f"{pos} does not contain np.float64 values")
        self._position = pos

    @property
    def velocity(self) -> np.ndarray:
        return self._velocity

    @velocity.setter
    def velocity(self, vel: np.ndarray):
        if not isinstance(vel, np.ndarray):
            try:
                vel = np.asarray(vel)
            except:
                raise TypeError(f"{vel} is {type(vel)}, not a numpy array")
        if len(vel) != 2:
            raise ValueError(f"{vel} is not a 2D array, it is {len(vel)}D")
        if vel.dtype != np.float64:
            try:
                vel = vel.astype(np.float64)
            except:
                raise ValueError(f"{vel} does not contain np.float64 values")
        self._velocity = vel

    def calc_density(self, distance):
        return self._smoothing_kernal(distance) * self._mass


