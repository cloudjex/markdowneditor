import type { Tree } from '@/src/lib/types';


class TreeHandler {
  private tree: Tree;

  constructor(tree: Tree) {
    this.tree = tree;
  }

  getNode(nodeId: string): Tree | null {
    const recursive = (node: Tree): Tree | null => {
      if (node.node_id === nodeId) {
        return node;
      }
      for (const child of node.children) {
        const result = recursive(child);
        if (result !== null) {
          return result;
        }
      }
      return null;
    };

    return recursive(this.tree);
  }

  getParentNode(nodeId: string): Tree | null {
    const findParent = (node: Tree): Tree | null => {
      for (const child of node.children) {
        if (child.node_id === nodeId) {
          return node;
        }
        const result = findParent(child);
        if (result !== null) {
          return result;
        }
      }
      return null;
    };

    return findParent(this.tree);
  }

  getParentNodeIds(nodeId: string): string[] {
    const result: string[] = [];
    let currentId = nodeId;

    if (this.tree.node_id === currentId) {
      return result;
    }

    while (true) {
      const parent = this.getParentNode(currentId);
      if (parent) {
        result.push(parent.node_id);
        currentId = parent.node_id;
        if (parent.node_id === this.tree.node_id) {
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

    const collect = (node: Tree) => {
      for (const child of node.children) {
        result.push(child.node_id);
        collect(child);
      }
    };

    collect(target);
    return result;
  }

  getNodeList(current_node_id: string): Record<string, string>[] {
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