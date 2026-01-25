// Response
export interface APIResponse<T> {
  status: number;
  headers: Headers;
  body: T;
};

export interface SigninResponse {
  id_token: string;
};

// Object
export interface Node {
  id: string;
  email: string;
  text: string;
};

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
