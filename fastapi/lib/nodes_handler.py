from lib.dynamodb_client import DynamoDBClient
from models.node import Node


class NodesHandler:
    def __init__(self, group_id: str):
        self._db_client = DynamoDBClient()
        self._group_id = group_id
        self._node_map = {n.node_id: n for n in self._db_client.get_nodes(group_id)}

    def tree(self, nid: str) -> dict:
        node = self._node_map[nid]
        return {
            "node_id": node.node_id,
            "label": node.label,
            "children": [self.tree(child_id) for child_id in node.children_ids],
        }

    def get_root(self) -> Node:
        # all node ids
        all_ids = set(self._node_map.keys())

        # node ids (node have parent node)
        child_ids = set()
        for node in self._node_map.values():
            child_ids.update(node.children_ids)

        root_ids = all_ids - child_ids
        root_id = next(iter(root_ids))
        return self._node_map[root_id]

    def get_parent(self, node_id: str) -> Node | None:
        for node in self._node_map.values():
            if node_id in node.children_ids:
                return node
        else:
            return None

    def children_ids_recursive(self, node_id: str) -> list[Node]:
        ret = []

        def dfs(node_id: str):
            node = self._node_map[node_id]
            for child_id in node.children_ids:
                ret.append(self._node_map[child_id])
                dfs(child_id)

        dfs(node_id)
        return ret
