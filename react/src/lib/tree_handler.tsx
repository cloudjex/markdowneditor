import type { Tree } from '@/src/lib/types';


class TreeHandler {
  private tree: Tree;

  constructor(tree: Tree) {
    this.tree = tree;
  }

  getNode(nodeId: string, node: Tree = this.tree): Tree | null {
    if (node.node_id === nodeId) {
      return node;
    }

    for (const child of node.children) {
      const found = this.getNode(nodeId, child);
      if (found) return found;
    }

    return null;
  }

  getParentNode(nodeId: string, node: Tree = this.tree): Tree | null {
    for (const child of node.children) {
      if (child.node_id === nodeId) {
        return node;
      }
      const parent = this.getParentNode(nodeId, child);
      if (parent !== null) {
        return parent;
      }
    }
    return null;
  };

  getParentNodeIds(nodeId: string): string[] {
    const result: string[] = [];
    let currentId = nodeId;

    if (this.tree.node_id === currentId) {
      return result;
    }

    while (true) {
      const parent = this.getParentNode(currentId);
      if (parent) {
        currentId = parent.node_id;
        result.push(currentId);
        if (this.tree.node_id === currentId) {
          break;
        }
      } else {
        break;
      }
    }

    return result.reverse();
  }

  getChildrenIds(nodeId: string): string[] {
    const target = this.getNode(nodeId);
    const result: string[] = [];
    if (!target) {
      return result;
    }

    function collect(node: Tree) {
      for (const child of node.children) {
        result.push(child.node_id);
        collect(child);
      }
    };

    collect(target);
    return result;
  }

  moveNodeList(current_node_id: string): Record<string, string>[] {
    const list: Record<string, string>[] = [];

    function dfs(node: Tree, parentLabel: string | null) {
      if (node.node_id === current_node_id) {
        return;
      }

      const fullLabel = parentLabel ? `${parentLabel} / ${node.label}` : node.label;
      list.push({ node_id: node.node_id, label: fullLabel });

      if (node.children) {
        for (const child of node.children) {
          dfs(child, fullLabel);
        }
      }
    }

    dfs(this.tree, null);
    return list;
  }
}

export default TreeHandler;
