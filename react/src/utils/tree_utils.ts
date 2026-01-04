import type { Tree } from '../types/types';

export default {
  get_node,
  get_parent_node_id,
  get_parent_node_ids,
};

function get_node(tree: Tree, node_id: string): Tree | null {
  let parts = node_id.split("/");
  parts = parts.filter((part) => part && part !== "Nodes");

  let current: Tree = tree;
  for (const part of parts) {
    const next = current.children.find((child: Tree) => child.label === part);
    if (!next) {
      return null;
    };

    current = next;
  }

  return current;
};

function get_parent_node_id(node_id: string): string {
  const parts = node_id.split("/").filter(Boolean);
  const parentParts = parts.slice(0, -1);
  return "/" + parentParts.join("/");
};

function get_parent_node_ids(node_id: string): string[] {
  const parts = node_id.split("/").filter(Boolean);
  if (parts.length <= 1) return [];

  const parentIds: string[] = [];
  for (let i = 1; i < parts.length; i++) {
    parentIds.push("/" + parts.slice(0, i).join("/"));
  }

  return parentIds;
};
