import { Theme } from "@radix-ui/themes";
import { ThemeProvider as NextThemeProvider } from "next-themes";
import { ReactNode } from "react";

interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  return (
    <NextThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <Theme appearance="light" accentColor="blue" grayColor="slate" radius="medium">
        {children}
      </Theme>
    </NextThemeProvider>
  );
}
