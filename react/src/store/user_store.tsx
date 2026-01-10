import { create } from "zustand";
import { persist } from "zustand/middleware";

import type { NodeTree } from "../types/types";

interface UserState {
  email: string;
  password: string;
  id_token: string;
  node_tree: NodeTree | null;

  /* eslint-disable no-unused-vars */
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  setIdToken: (id_token: string) => void;
  setNodeTree: (node_tree: NodeTree | null) => void;

  resetUserState: () => void;
}

const userStore = create<UserState>()(
  persist((set) => ({
    email: "",
    password: "",
    id_token: "",
    node_tree: null,

    setEmail: (email: string): void => { set({ email }); },
    setPassword: (password: string): void => { set({ password }); },
    setIdToken: (id_token: string): void => { set({ id_token }); },
    setNodeTree: (node_tree: NodeTree | null): void => { set({ node_tree }); },

    resetUserState: () => set({
      email: "",
      password: "",
      id_token: "",
      node_tree: null,
    }),
  }),
    { name: "user-store", }
  )
);

export default userStore;
