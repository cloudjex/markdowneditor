import { create } from "zustand";
import { persist } from "zustand/middleware";

import type { TreeNode } from "../types/types";

interface UserState {
  email: string;
  password: string;
  id_token: string;
  tree: TreeNode | null;

  /* eslint-disable no-unused-vars */
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  setIdToken: (id_token: string) => void;
  setTree: (tree: TreeNode | null) => void;

  resetUserState: () => void;
}

const userStore = create<UserState>()(
  persist((set) => ({
    email: "",
    password: "",
    id_token: "",
    tree: null,

    setEmail: (email: string): void => { set({ email }); },
    setPassword: (password: string): void => { set({ password }); },
    setIdToken: (id_token: string): void => { set({ id_token }); },
    setTree: (tree: TreeNode | null): void => { set({ tree }); },

    resetUserState: () => set({
      email: "",
      password: "",
      id_token: "",
      tree: null,
    }),
  }),
    { name: "user-store", }
  )
);

export default userStore;
