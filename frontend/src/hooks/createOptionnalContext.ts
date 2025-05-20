import { createContext, useContext } from "react";
export const createOptionalContext = <T>(displayName: string) => {
  const Context = createContext<T | undefined>(undefined);
  Context.displayName = displayName;
  function useOptionalContext(noThrow: true): T | undefined;
  function useOptionalContext(noThrow?: false): T;
  function useOptionalContext(noThrow?: boolean) {
    const value = useContext(Context);
    if (value === undefined && !noThrow) {
      throw new Error(`The context ${Context.displayName} is not provided`);
    }
    return value;
  }
  return {
    Context,
    useOptionalContext,
  };
};
