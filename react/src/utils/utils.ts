export default {
  requests,
  get_url_node_id,
  get_node,
  get_parent_node_id,
  get_parent_node_ids,
  insert_node,
  delete_tree_node,
  is_valid_new_node,
};

type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

interface APIResponse<T = unknown> {
  status: number;
  headers: Headers;
  body: T;
}

async function requests(
  url: string,
  method: HTTPMethod,
  headers: Record<string, string>,
  params: Record<string, string>
): Promise<APIResponse> {
  if (!headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  console.group("API Request");
  console.log(`[${method}]: ${url}`);
  console.log({ url, method, headers, params });

  let detail: RequestInit;

  if (method === "GET" || method === "DELETE") {
    detail = {
      method,
      headers,
    };
    url = `${url}?${new URLSearchParams(params)}`;
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

interface TreeNode {
  id: string;
  label: string;
  children?: TreeNode[];
}

function get_url_node_id(): string {
  const params = new URLSearchParams(location.search);
  const node_id = params.get("node_id");
  if (!node_id) {
    throw new Error(`can't find node_id`);
  };
  return node_id;
}

function get_node(tree: TreeNode, node_id: string): TreeNode {
  let parts = node_id.split("/");
  parts = parts.filter((part) => part && part !== "Folder");

  let current: TreeNode = tree;
  for (const part of parts) {
    if (!Array.isArray(current.children)) {
      throw new Error(`current not have children: node_id=${node_id}`);
    };

    const next = current.children.find((child: TreeNode) => child.label === part);
    if (!next) {
      throw new Error(`can't find next: node_id=${node_id}`);
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

function insert_node(tree: TreeNode, insert_node: TreeNode): TreeNode {
  const parent_id = get_parent_node_id(insert_node.id);
  const parent = get_node(tree, parent_id);

  parent.children = parent.children ?? [];
  parent.children.push(insert_node);
  return tree;
}

function delete_tree_node(tree: TreeNode, target_id: string): TreeNode {
  const parent_id = get_parent_node_id(target_id);
  const parent = get_node(tree, parent_id);
  if (!parent.children) {
      throw new Error(`can't find children: target_id=${target_id}`);
  };

  parent.children = parent.children.filter((child) => child.id !== target_id);
  return tree;
}

function is_valid_new_node(tree: TreeNode, insert_node: TreeNode): boolean {
  if (!insert_node.id || !insert_node.label) {
    return false;
  };

  const parent_id = get_parent_node_id(insert_node.id);
  const parent = get_node(tree, parent_id);
  const siblings = parent.children ?? [];
  return !siblings.some((child) => child.label === insert_node.label);
}
