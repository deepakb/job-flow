import { motion } from 'framer-motion';

interface HeroIllustrationProps {
  className?: string;
}

export const HeroIllustration = ({ className }: HeroIllustrationProps) => {
  return (
    <motion.svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 597.03 590.1"
      className={className}
      initial="hidden"
      animate="visible"
    >
      <defs>
        <linearGradient id="hero-gradient-1" x1="325.79" x2="38.1" y1="335.51" y2="787.23" gradientUnits="userSpaceOnUse">
          <motion.stop offset="0" stopOpacity="0" />
          <motion.stop offset=".99" />
        </linearGradient>
        <linearGradient id="hero-gradient-2" x1="572.52" x2="582.9" y1="59.32" y2="62.5" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="var(--color-primary-main)" />
          <stop offset=".42" stopColor="var(--color-primary-light)" />
          <stop offset="1" stopColor="var(--color-secondary-teal)" />
        </linearGradient>
      </defs>

      {/* Background Shape */}
      <motion.path
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 0.18 }}
        transition={{ duration: 1.5, ease: "easeInOut" }}
        fill="url(#hero-gradient-1)"
        d="M46.71 85.48C62.03 59.61 88.5 42.4 115.47 29.13c23.94-11.79 50.23-21.4 76.77-18.55 50.87 5.5 88.21 54.4 138.72 62.65 19.89 3.24 40.19-.16 60.15-3 34.53-5 69.91-8.31 104.14-1.56s67.57 24.86 85.76 54.63c20.2 33 19 75.2 9 112.63s-27.7 72.28-39.23 109.24c-4.38 14-7.86 29-4.31 43.2 3.22 12.88 11.82 23.6 18.62 35A137.87 137.87 0 0 1 584.31 498c-61.46 19.37-128.47 4.33-188.87-18.14-53.66-20-105-45.63-156.1-71.43-40.74-20.57-81.8-41.49-116.94-70.61-33.31-27.61-60.39-61.82-87.21-95.77-8.53-10.8-26.49-27.58-29.24-41.29-2.89-14.38 6.37-23.17 12.14-36.19 11.43-25.71 14.13-54.64 28.62-79.09Z"
      />

      {/* Main Elements */}
      <motion.g
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
      >
        {/* Career Path */}
        <motion.path
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, ease: "easeInOut" }}
          fill="var(--color-primary-main)"
          d="M585.06 492.46v97.64H0V185.38h97.64v63.43h97.62v63.42h97.64v63.43h97.62v53.38h96.9v63.42h97.64z"
        />

        {/* Character */}
        <motion.path
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, delay: 1 }}
          fill="var(--color-neutral-dark)"
          d="M427.76 213.08s-72.34 22.88-77.19 46 18.47 79.06 18.47 79.06l26.15-7.47s-13.23-40.58-2.68-51.76 87.34-19.14 102.54-61.08c0 .08-25.69-29.75-67.29-4.75Z"
        />
      </motion.g>

      {/* Floating Elements */}
      <motion.g
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 1.5 }}
      >
        {/* Add floating animation to specific elements */}
        <motion.path
          animate={{
            y: [0, -10, 0],
            x: [0, 5, 0]
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          fill="var(--color-secondary-teal)"
          d="M497.9 222.36l-51.15-7.9-19-1.35 4.17-16-6.49-67.23s-.07-8.51.36-18.71c.37-9 1.12-19.36 2.64-26.32 2.9-13.31 28.22-10.94 38.09-9.24a14.52 14.52 0 0 1 11.31 10.11c7.27 23.66 23.18 78.82 23.82 85.77 3.5 37.84-3.75 50.87-3.75 50.87Z"
        />
      </motion.g>

      {/* Interactive Elements */}
      <motion.g
        whileHover={{ scale: 1.05 }}
        transition={{ duration: 0.3 }}
      >
        {/* Add any interactive elements here */}
      </motion.g>
    </motion.svg>
  );
};
