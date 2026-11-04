"""
TRTL: Topological-Relativistic-Thermodynamic Learning
A Unified Physics-Grounded Machine Learning Framework
"""

__version__ = "1.0.0"
__author__ = "TRTL Research Consortium"

from .metric import RelativisticMetric
from .wave import WaveInterferenceLayer
from .thermo import ThermodynamicCrystallizer
from .spatial import SpatialBallTreeIndexer
from .classifier import TRTLClassifier
from .recourse import ThermodynamicRecourse

__all__ = [
    "RelativisticMetric",
    "WaveInterferenceLayer",
    "ThermodynamicCrystallizer",
    "SpatialBallTreeIndexer",
    "TRTLClassifier",
    "ThermodynamicRecourse",
]
