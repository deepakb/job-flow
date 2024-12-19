import * as RadixAspectRatio from "@radix-ui/react-aspect-ratio";

interface AspectRatioProps {
  ratio: number;
  children: React.ReactNode;
  className?: string;
}

export const AspectRatio = ({ ratio, children, className }: AspectRatioProps) => {
  return (
    <RadixAspectRatio.Root ratio={ratio} className={className}>
      {children}
    </RadixAspectRatio.Root>
  );
};
