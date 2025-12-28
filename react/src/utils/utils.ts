import type { APIResponse, TreeNode } from '../types/types';

export default {
  requests,
  get_node,
  get_parent_node_id,
  get_parent_node_ids,
  is_valid_new_node,
};

async function requests(
  url: string,
  method: string,
  headers: Record<string, string>,
  params: unknown
): Promise<APIResponse> {
  if (!headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  console.group("API Request");
  console.log(`[${method}]: ${url}`);
  console.log({ url, method, headers, params });

  let detail;
  if (method === "GET" || method === "DELETE") {
    detail = {
      method,
      headers,
    };
    url = `${url}?${new URLSearchParams(params as Record<string, string>)}`;
  } else {
    detail = {
      method,
      headers,
      body: JSON.stringify(params),
    };
  }

  const res = await fetch(url, detail);
  const result: APIResponse = {
    status: res.status,
    headers: res.headers,
    body: await res.json(),
  };

  console.log(result);
  console.groupEnd();
  return result;
}

function get_node(tree: TreeNode, node_id: string): TreeNode | null {
  let parts = node_id.split("/");
  parts = parts.filter((part) => part && part !== "Nodes");

  let current: TreeNode = tree;
  for (const part of parts) {
    const next = current.children.find((child: TreeNode) => child.label === part);
    if (!next) {
      return null;
    };

    current = next;
  }

  return current;
}

function get_parent_node_id(node_id: string): string {
  const parts = node_id.split("/").filter(Boolean);
  const parentParts = parts.slice(0, -1);
  return "/" + parentParts.join("/");
}

function get_parent_node_ids(node_id: string): string[] {
  const parts = node_id.split("/").filter(Boolean);
  if (parts.length <= 1) return [];

  const parentIds: string[] = [];
  for (let i = 1; i < parts.length; i++) {
    parentIds.push("/" + parts.slice(0, i).join("/"));
  }

  return parentIds;
}

function is_valid_new_node(tree: TreeNode, node_id: string): boolean {
  if (!node_id) {
    return false;
  };

  const parent_id = get_parent_node_id(node_id);
  const parent = get_node(tree, parent_id);

  if (!parent) {
    throw new Error(`parent is null`);
  };

  const siblings = parent.children;
  return !siblings.some((child) => child.label === node_id.split("/").pop());
}
