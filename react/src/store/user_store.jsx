import { create } from "zustand";
import { persist } from 'zustand/middleware';

const userStore = create(persist((set) => ({
  // user info
  email: "",
  password: "",
  id_token: "",
  tree: {},

  setEmail: (email) => set({ email: email }),
  setPassword: (password) => set({ password: password }),
  setIdToken: (id_token) => set({ id_token: id_token }),
  setTree: (tree) => set({ tree: tree }),

  reset: () => set({
    email: "",
    password: "",
    id_token: "",
    tree: {},
  }),

}), {
  name: "user-store"
}));

export default userStore;