import { motion, HTMLMotionProps } from 'framer-motion';
import { cn } from '../../utils/cn';

interface CardProps extends HTMLMotionProps<"div"> {
  variant?: 'default' | 'elevated' | 'bordered';
  isHoverable?: boolean;
  isInteractive?: boolean;
}

export const Card = ({
  children,
  variant = 'default',
  isHoverable = false,
  isInteractive = false,
  className,
  ...props
}: CardProps) => {
  const baseStyles = "rounded-xl overflow-hidden";
  
  const variants = {
    default: "bg-white",
    elevated: "bg-white shadow-lg",
    bordered: "bg-white border border-neutral-light",
  };

  const hoverStyles = isHoverable ? "transition-all duration-300 hover:shadow-lg" : "";
  const interactiveStyles = isInteractive ? "cursor-pointer transform transition-transform hover:scale-[1.02]" : "";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className={cn(
        baseStyles,
        variants[variant],
        hoverStyles,
        interactiveStyles,
        className
      )}
      {...props}
    >
      {children}
    </motion.div>
  );
};
