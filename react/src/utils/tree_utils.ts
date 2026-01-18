import type { NodeTree } from '../types/types';

export default {
  get_node,
  get_parent_node,
  get_parent_node_ids,
  get_children_ids,
};

function get_node(node_tree: NodeTree, node_id: string): NodeTree | null {
  function recursive(node: NodeTree): NodeTree | null {
    if (node.id === node_id) {
      return node;
    }
    for (const child of node.children) {
      const result = recursive(child);
      if (result !== null) {
        return result;
      }
    }
    return null;
  }

  return recursive(node_tree);
}

function get_parent_node_ids(node_tree: NodeTree, node_id: string): string[] {
  const result: string[] = [];
  let current_id = node_id;

  if (node_tree.id == current_id) {
    return result;
  }

  while (true) {
    const parent = get_parent_node(node_tree, current_id);
    if (parent) {
      result.push(parent.id);
      current_id = parent.id;
      if (parent.id === node_tree.id) {
        break;
      }
    } else {
      break;
    }
  }

  return result.reverse();
}

function get_parent_node(node_tree: NodeTree, node_id: string): NodeTree | null {
  function find_parent(node: NodeTree): NodeTree | null {
    for (const child of node.children) {
      if (child.id === node_id) {
        return node;
      }
      const result = find_parent(child);
      if (result !== null) {
        return result;
      }
    }
    return null;
  }

  return find_parent(node_tree);
}

function get_children_ids(node_tree: NodeTree, node_id: string): string[] {
  const target = get_node(node_tree, node_id);
  const result: string[] = [];
  if (!target) {
    return result;
  }

  function collect(node: NodeTree) {
    for (const child of node.children) {
      result.push(child.id);
      collect(child);
    }
  }

  collect(target);
  return result;
}
