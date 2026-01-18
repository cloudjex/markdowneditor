// Response
export interface BaseAPIResponse<T> {
  status: number;
  headers: Headers;
  body: T;
};

export interface SigninResponse {
  email: string;
  id_token: string;
  options: {
    enabled: boolean;
  }
};

export interface TreeResponse {
  node_tree: NodeTree;
};

export interface TreeOperateResponse {
  node_tree: NodeTree;
  id: string,
};

export interface NodeResponse {
  node: Node
};

// Object
export interface Node {
  id: string;
  email: string;
  text: string;
};

export interface NodeTree {
  id: string;
  label: string;
  children: NodeTree[];
};

// Form
export interface SigninForm {
  email: string;
  password: string;
};

export interface SignupForm {
  email: string;
  password: string;
  password_confirm: string;
};
