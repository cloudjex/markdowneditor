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
  tree: Tree;
};

export interface NodeResponse {
  node: {
    id: string;
    email: string;
    text: string;
  };
};

// Object
export interface Tree {
  id: string;
  label: string;
  children: Tree[];
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
