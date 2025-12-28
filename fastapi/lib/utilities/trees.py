def find_node(node_id: str, tree: dict) -> dict | None:
    if tree.get("id") == node_id:
        return tree

    for child in tree.get("children", []):
        result = find_node(node_id, child)
        if result is not None:
            return result

    return None


def sort_tree(tree: dict) -> dict:
    if not tree or not isinstance(tree, dict):
        return tree

    def sort_key(child: dict) -> tuple[bool, str]:
        node_id: str = child.get("id", "")
        is_file = "children" not in child or not child.get("children")
        return (is_file, node_id)

    children = tree.get("children")
    if isinstance(children, list):
        children.sort(key=sort_key)
        for child in children:
            sort_tree(child)
        tree["children"] = children

    return tree


def find_children_ids(node_id: str, tree: dict) -> list[str]:
    target = find_node(node_id, tree)
    result = []
    if target is None:
        return result

    def collect(node):
        for child in node.get("children", []):
            result.append(child["id"])
            collect(child)

    collect(target)
    return result
