import { create } from "zustand";
import { persist } from "zustand/middleware";

import type { Tree, UserGroup } from "@/src/lib/types";


interface UserState {
  email: string;
  password: string;
  id_token: string;
  user_groups: UserGroup[];
  tree: Tree;
  preview_text: string,

  /* eslint-disable no-unused-vars */
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  setIdToken: (id_token: string) => void;
  setUserGroups: (user_groups: UserGroup[]) => void;
  setTree: (tree: Tree) => void;
  setPreviewText: (preview_text: string) => void;

  resetUserState: () => void;
}

const userStore = create<UserState>()(
  persist((set) => ({
    email: "",
    password: "",
    id_token: "",
    user_groups: [],
    tree: { children: [], node_id: "", label: "" },
    preview_text: "",

    setEmail: (email: string): void => { set({ email }); },
    setPassword: (password: string): void => { set({ password }); },
    setIdToken: (id_token: string): void => { set({ id_token }); },
    setUserGroups: (user_groups: UserGroup[]): void => { set({ user_groups }); },
    setTree: (tree: Tree): void => { set({ tree: tree }); },
    setPreviewText: (preview_text: string): void => { set({ preview_text }); },

    resetUserState: () => set({
      email: "",
      password: "",
      id_token: "",
      user_groups: [],
      tree: { children: [], node_id: "", label: "" },
    }),
  }),
    { name: "user-store", }
  )
);

export default userStore;
