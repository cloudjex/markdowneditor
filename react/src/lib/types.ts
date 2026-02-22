// Response
export interface APIResponse<T> {
  status: number;
  headers: Headers;
  body: T;
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

// Object
export interface IdToken {
  id_token: string;
};

export interface User {
  email: string;
  password: string;
  groups: [
    {
      group_id: string,
      role: string
    }
  ];
  options: {
    enabled: boolean;
    otp: string;
  }
};

export interface Group {
  group_id: string;
  group_name: string;
};

export interface Node {
  group_id: string;
  node_id: string;
  label: string;
  text: string;
  children_ids: string[];
};

export interface Tree {
  node_id: string;
  label: string;
  children: Tree[];
};
