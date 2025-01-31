import abc
import typing

import numpy
from scipy.spatial.distance import cdist

SCIPY_METRICS = typing.Literal[
    "braycurtis",
    "canberra",
    "chebyshev",
    "cityblock",
    "correlation",
    "cosine",
    "dice",
    "directed_hausdorff",
    "euclidean",
    "hamming",
    "jaccard",
    "jensenshannon",
    "kulsinski",
    "kulczynski1",
    "mahalanobis",
    "matching",
    "minkowski",
    "rogerstanimoto",
    "russellrao",
    "seuclidean",
    "sokalmichener",
    "sokalsneath",
    "sqeuclidean",
    "yule",
]


class Metric(abc.ABC):
    """This represents a general distance metric for computing distances
    between data points. Mathematically, this is a distance function, `f`,
    which obeys the following properties:
        - scalar-valued: `f(x, y)` is a Real number for all `x` and `y`
        - non-negativity: `f(x, y)` >= 0 for all `x` and `y`
        - identity: `f(x, y)` = 0 iff `x` = `y`
        - symmetry: `f(x, y)` = `f(y, x)`
        - triangle inequality (optional): `f(x, y)` <= `f(x, z)` + `f(z, y)`
          for all `x`, `y` and `z`.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: "Metric") -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    @abc.abstractmethod
    def one_to_one(self, left: typing.Any, right: typing.Any) -> float:
        """`left` and `right` are each a single data instance. Compute the
        distance between the two.
        """
        pass

    @abc.abstractmethod
    def one_to_many(self, left: typing.Any, right: typing.Any) -> numpy.ndarray:
        """`left` is a single instance and `right` is multiple instances.
        Compute a 1d array of distances from `left` to instances in `right`.
        """
        pass

    @abc.abstractmethod
    def many_to_many(self, left: typing.Any, right: typing.Any) -> numpy.ndarray:
        """`left` and `right` are both multiple instances. Compute a 2d array
        of distances from each instance in `left` to each instance in `right`.
        """
        pass

    @abc.abstractmethod
    def pairwise(self, instances: typing.Any) -> numpy.ndarray:
        """Compute a 2d array of distances among each pair in `instances`."""
        pass


class ScipyMetric(Metric):
    """See scipy.spatial.distance.cdist
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html.
    """

    def __init__(self, name: SCIPY_METRICS) -> None:
        if name not in typing.get_args(SCIPY_METRICS):
            msg = f"`name` must be one of {SCIPY_METRICS}. Got {name} instead"
            raise ValueError(
                msg,
            )
        super().__init__(name)

    def one_to_one(self, left: numpy.ndarray, right: numpy.ndarray, **kwargs) -> float:
        left = left[None, :]
        right = right[None, :]
        return float(self.many_to_many(left, right, **kwargs).squeeze())

    def one_to_many(
        self,
        left: numpy.ndarray,
        right: numpy.ndarray,
        **kwargs,
    ) -> numpy.ndarray:
        left = left[None, :]
        return self.many_to_many(left, right, **kwargs)[0]

    def many_to_many(
        self,
        left: numpy.ndarray,
        right: numpy.ndarray,
        **kwargs,
    ) -> numpy.ndarray:
        return cdist(left, right, metric=self.name, **kwargs)  # type: ignore

    def pairwise(self, instances: numpy.ndarray, **kwargs) -> numpy.ndarray:
        return self.many_to_many(instances, instances, **kwargs)


__all__ = [
    "SCIPY_METRICS",
    "Metric",
    "ScipyMetric",
]
