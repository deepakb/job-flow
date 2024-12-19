import { forwardRef } from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import { cn } from '../../utils/cn';

interface ButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'gradient-border';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  rounded?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    children, 
    variant = 'primary', 
    size = 'md', 
    fullWidth = false,
    isLoading = false,
    leftIcon,
    rightIcon,
    rounded = false,
    className,
    ...props 
  }, ref) => {
    const baseStyles = cn(
      "inline-flex items-center justify-center font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed active:scale-[0.98]",
      rounded ? "rounded-full" : "rounded-lg"
    );
    
    const variants = {
      primary: "bg-gradient-primary text-white shadow-sm hover:shadow-md hover:opacity-90 focus:ring-primary-main",
      secondary: "bg-white text-primary-main border-2 border-primary-main hover:bg-primary-main hover:text-white focus:ring-primary-main",
      outline: "bg-transparent border-2 border-neutral-light hover:border-primary-main focus:ring-primary-main",
      ghost: "bg-transparent hover:bg-neutral-light/50 focus:ring-neutral-light",
      'gradient-border': "relative bg-gradient-to-r from-[#3366FF] to-[#00B3A6]",
    };

    const sizes = {
      sm: "px-4 py-2 text-sm gap-1.5",
      md: "px-6 py-3 text-base gap-2",
      lg: "px-8 py-4 text-lg gap-2.5",
    };

    if (variant === 'gradient-border') {
      const contentPadding = {
        sm: "px-4 py-[6px]",
        md: "px-6 py-[10px]",
        lg: "px-8 py-[14px]",
      };

      return (
        <motion.button
          ref={ref}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={cn(
            baseStyles,
            variants[variant],
            "p-[2px]",
            fullWidth && "w-full",
            className
          )}
          {...props}
        >
          <span className={cn(
            "inline-flex items-center justify-center w-full bg-white dark:bg-gray-950 text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-900",
            rounded ? "rounded-full" : "rounded-lg",
            contentPadding[size],
            size === 'sm' ? 'text-sm gap-1.5' : size === 'md' ? 'text-base gap-2' : 'text-lg gap-2.5'
          )}>
            {leftIcon && <span className="mr-2">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="ml-2">{rightIcon}</span>}
          </span>
        </motion.button>
      );
    }

    return (
      <motion.button
        ref={ref}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          fullWidth && "w-full",
          className
        )}
        disabled={isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <svg 
              className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <circle 
                className="opacity-25" 
                cx="12" 
                cy="12" 
                r="10" 
                stroke="currentColor" 
                strokeWidth="4"
              />
              <path 
                className="opacity-75" 
                fill="currentColor" 
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Loading...
          </>
        ) : (
          <>
            {leftIcon && <span className="mr-2">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="ml-2">{rightIcon}</span>}
          </>
        )}
      </motion.button>
    );
  }
);
