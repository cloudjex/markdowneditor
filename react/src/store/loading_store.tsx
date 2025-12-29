import { create } from "zustand";
import { persist } from "zustand/middleware";

interface LoadingState {
  loading_stack: number;

  /* eslint-disable no-unused-vars */
  setLoading: (loading: boolean) => void;

  resetLoadingState: () => void;
}

const loadingState = create<LoadingState>()(
  persist(
    (set) => ({
      loading_stack: 0,

      setLoading: (loading: boolean) => {set((state) => {
          const stack = loading
            ? state.loading_stack + 1
            : state.loading_stack - 1;

          return { loading_stack: stack };
        });
      },
      resetLoadingState: () => set({
        loading_stack: 0
      }),
    }),
    { name: "loading-store" }
  )
);

export default loadingState;
