import { create } from "zustand";
import { persist } from "zustand/middleware";

import type { Tree as Tree } from "@/src/lib/types";


interface UserState {
  email: string;
  password: string;
  id_token: string;
  tree: Tree;
  preview_text: string,

  /* eslint-disable no-unused-vars */
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  setIdToken: (id_token: string) => void;
  setTree: (tree: Tree) => void;
  setPreviewText: (preview_text: string) => void;

  resetUserState: () => void;
}

const userStore = create<UserState>()(
  persist((set) => ({
    email: "",
    password: "",
    id_token: "",
    tree: { children: [], id: "", label: "" },
    preview_text: "",

    setEmail: (email: string): void => { set({ email }); },
    setPassword: (password: string): void => { set({ password }); },
    setIdToken: (id_token: string): void => { set({ id_token }); },
    setTree: (tree: Tree): void => { set({ tree: tree }); },
    setPreviewText: (preview_text: string): void => { set({ preview_text }); },

    resetUserState: () => set({
      email: "",
      password: "",
      id_token: "",
      tree: { children: [], id: "", label: "" },
    }),
  }),
    { name: "user-store", }
  )
);

export default userStore;
