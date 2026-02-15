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

export interface UserGroup {
  group_name: string; role: string;
}

export interface User {
  email: string;
  password: string;
  groups: UserGroup[];
  options: {
    enabled: boolean;
    otp: string;
  }
};

export interface Node {
  node_id: string;
  label: string;
  user_group: string;
  text: string;
  children: string[],
};

export interface Tree {
  node_id: string;
  label: string;
  children: Tree[];
};
