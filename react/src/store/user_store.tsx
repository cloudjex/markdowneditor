import { create } from "zustand";
import { persist } from "zustand/middleware";

import type { Tree, Group } from "@/src/lib/types";


interface UserState {
  email: string;
  password: string;
  idToken: string;
  groups: Group[];
  tree: Tree;
  previewText: string,

  /* eslint-disable no-unused-vars */
  setEmail: (email: string) => void;
  setPassword: (password: string) => void;
  setIdToken: (idToken: string) => void;
  setGroups: (groups: Group[]) => void;
  setTree: (tree: Tree) => void;
  setPreviewText: (previewText: string) => void;

  resetUserState: () => void;
}

const userStore = create<UserState>()(
  persist((set) => ({
    email: "",
    password: "",
    idToken: "",
    groups: [],
    tree: { children: [], node_id: "", label: "" },
    previewText: "",

    setEmail: (email: string): void => { set({ email }); },
    setPassword: (password: string): void => { set({ password }); },
    setIdToken: (idToken: string): void => { set({ idToken: idToken }); },
    setGroups: (groups: Group[]): void => { set({ groups: groups }); },
    setTree: (tree: Tree): void => { set({ tree: tree }); },
    setPreviewText: (previewText: string): void => { set({ previewText: previewText }); },

    resetUserState: () => set({
      email: "",
      password: "",
      idToken: "",
      groups: [],
      tree: { children: [], node_id: "", label: "" },
      previewText: "",
    }),
  }),
    { name: "user-store", }
  )
);

export default userStore;
