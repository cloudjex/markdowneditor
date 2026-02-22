import { create } from "zustand";
import { persist } from "zustand/middleware";


interface LoadingState {
  loadingStack: number;

  /* eslint-disable no-unused-vars */
  setLoading: (loading: boolean) => void;

  resetLoadingState: () => void;
}

const loadingState = create<LoadingState>()(
  persist(
    (set) => ({
      loadingStack: 0,

      setLoading: (loading: boolean) => {set((state) => {
          const stack = loading
            ? state.loadingStack + 1
            : state.loadingStack - 1;

          return { loadingStack: stack };
        });
      },
      resetLoadingState: () => set({
        loadingStack: 0
      }),
    }),
    { name: "loading-store" }
  )
);

export default loadingState;
