import { cn } from '../../utils/cn';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error';
  size?: 'sm' | 'md';
}

export const Badge = ({
  children,
  variant = 'default',
  size = 'md',
  className,
  ...props
}: BadgeProps) => {
  const baseStyles = "inline-flex items-center font-medium rounded-full";
  
  const variants = {
    default: "bg-neutral-light text-neutral-dark",
    primary: "bg-primary-main text-white",
    success: "bg-secondary-teal text-white",
    warning: "bg-secondary-yellow text-neutral-dark",
    error: "bg-red-500 text-white",
  };

  const sizes = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-3 py-1 text-sm",
  };

  return (
    <span
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
