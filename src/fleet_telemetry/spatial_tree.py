"""
2D KD-Tree for spatial fleet nearest-neighbor queries.
"""
import math
from typing import List, Optional, Tuple, Any

class KDNode:
    def __init__(self, point: Tuple[float, float], data: Any, left=None, right=None):
        self.point = point
        self.data = data
        self.left = left
        self.right = right

class SpatialKDTree:
    def __init__(self, items: List[Tuple[Tuple[float, float], Any]]):
        self.root = self._build(items, depth=0)

    def _build(self, items: list, depth: int) -> Optional[KDNode]:
        if not items:
            return None
        axis = depth % 2
        items.sort(key=lambda x: x[0][axis])
        mid = len(items) // 2
        return KDNode(
            point=items[mid][0],
            data=items[mid][1],
            left=self._build(items[:mid], depth + 1),
            right=self._build(items[mid + 1:], depth + 1)
        )

    def nearest(self, target: Tuple[float, float]) -> Optional[Tuple[Any, float]]:
        best = [None, float("inf")]
        def search(node: Optional[KDNode], depth: int):
            if node is None:
                return
            d = math.hypot(node.point[0] - target[0], node.point[1] - target[1])
            if d < best[1]:
                best[0] = node.data
                best[1] = d
            axis = depth % 2
            diff = target[axis] - node.point[axis]
            first = node.left if diff < 0 else node.right
            second = node.right if diff < 0 else node.left
            search(first, depth + 1)
            if abs(diff) < best[1]:
                search(second, depth + 1)
        search(self.root, 0)
        return best[0], best[1] if best[0] is not None else None
