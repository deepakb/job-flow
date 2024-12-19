import { createElement } from 'react';
import { cn } from '../../utils/cn';

type TextElement = 'h1' | 'h2' | 'h3' | 'h4' | 'p' | 'span';

interface TextProps extends React.HTMLAttributes<HTMLElement> {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'body' | 'small' | 'caption';
  weight?: 'normal' | 'medium' | 'semibold' | 'bold' | 'black';
  color?: 'default' | 'muted' | 'primary' | 'white';
  align?: 'left' | 'center' | 'right';
  as?: TextElement;
}

export const Text = ({
  children,
  variant = 'body',
  weight = 'normal',
  color = 'default',
  align = 'left',
  as,
  className,
  ...props
}: TextProps) => {
  const variants = {
    h1: 'text-h1 leading-tight',
    h2: 'text-h2 leading-tight',
    h3: 'text-h3 leading-snug',
    h4: 'text-xl leading-snug',
    body: 'text-base leading-relaxed',
    small: 'text-sm leading-relaxed',
    caption: 'text-xs leading-relaxed',
  };

  const weights = {
    normal: 'font-normal',
    medium: 'font-medium',
    semibold: 'font-semibold',
    bold: 'font-bold',
    black: 'font-[900]',
  };

  const colors = {
    default: 'text-neutral-dark',
    muted: 'text-neutral-dark/60',
    primary: 'text-primary-main',
    white: 'text-white',
  };

  const alignments = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right',
  };

  // Determine the element type based on variant or override with 'as' prop
  const element: TextElement = as || (variant.startsWith('h') ? variant as TextElement : 'p');

  return createElement(
    element,
    {
      className: cn(
        variants[variant],
        weights[weight],
        colors[color],
        alignments[align],
        className
      ),
      ...props
    },
    children
  );
};
