export interface APIResponse {
  status: number;
  headers: Headers;
  body: unknown;
}

export interface TreeNode {
  id: string;
  label: string;
  children: TreeNode[];
}

export interface LoginForm {
  email: string;
  password: string;
};
