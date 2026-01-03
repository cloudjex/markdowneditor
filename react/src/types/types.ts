export interface APIResponse {
  status: number;
  headers: Headers;
  body: unknown;
};

export interface TreeNode {
  id: string;
  label: string;
  children: TreeNode[];
};

export interface SigninForm {
  email: string;
  password: string;
};

export interface SignupForm {
  email: string;
  password: string;
  password_confirm: string;
};
