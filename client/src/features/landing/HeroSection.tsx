import { motion } from 'framer-motion';
import { RocketIcon } from '@radix-ui/react-icons';
import { Button } from '../../components/ui/Button';
import { Container } from '../../components/ui/Container';
import { Text } from '../../components/ui/Text';

const HeroIllustration = () => (
  <motion.svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 597.03 590.1"
    className="w-full h-full"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.5 }}
  >
    {/* Background shape */}
    <path fill="#68e1fd" d="M46.71 85.48C62.03 59.61 88.5 42.4 115.47 29.13c23.94-11.79 50.23-21.4 76.77-18.55 50.87 5.5 88.21 54.4 138.72 62.65 19.89 3.24 40.19-.16 60.15-3 34.53-5 69.91-8.31 104.14-1.56s67.57 24.86 85.76 54.63c20.2 33 19 75.2 9 112.63s-27.7 72.28-39.23 109.24c-4.38 14-7.86 29-4.31 43.2 3.22 12.88 11.82 23.6 18.62 35A137.87 137.87 0 0 1 584.31 498c-61.46 19.37-128.47 4.33-188.87-18.14-53.66-20-105-45.63-156.1-71.43-40.74-20.57-81.8-41.49-116.94-70.61-33.31-27.61-60.39-61.82-87.21-95.77-8.53-10.8-26.49-27.58-29.24-41.29-2.89-14.38 6.37-23.17 12.14-36.19 11.43-25.71 14.13-54.64 28.62-79.09Z" opacity=".18" />
    
    {/* Body parts with adjusted colors */}
    <path fill="#25233a" d="M504.16 205.36v7.68l4.59-.41v-4.64a4.92 4.92 0 0 1 4.56-4.91l25.89-2.07a4.91 4.91 0 0 1 5.22 4l.79 4.31 3.61-.32v-5.42a6.64 6.64 0 0 0-7-6.64l-31.38 1.75a6.64 6.64 0 0 0-6.28 6.67Z" />
    <path fill="#68e1fd" d="m499.53 213.46 4.68-.42 74.87-6.75 4.23 64.02-92.73 8.45-5.25-61.54 14.2-3.76z" />
    <path fill="#68e1fd" d="M585.06 492.46v97.64H0V185.38h97.64v63.43h97.62v63.42h97.64v63.43h97.62v53.38h96.9v63.42h97.64z" />
    <path fill="#25233a" d="M427.76 213.08s-72.34 22.88-77.19 46 18.47 79.06 18.47 79.06l26.15-7.47s-13.23-40.58-2.68-51.76 87.34-19.14 102.54-61.08c0 .08-25.69-29.75-67.29-4.75Z" />
    <path fill="#68e1fd" d="m497.9 222.36-51.15-7.9-19-1.35 4.17-16-6.49-67.23s-.07-8.51.36-18.71c.37-9 1.12-19.36 2.64-26.32 2.9-13.31 28.22-10.94 38.09-9.24a14.52 14.52 0 0 1 11.31 10.11c7.27 23.66 23.18 78.82 23.82 85.77 3.5 37.84-3.75 50.87-3.75 50.87Z" />
    <path fill="#68e1fd" d="M462.23 76.1v-6.93l-32.5 4.84-1.28 10.85 33.78-8.76zM537.13 179.64h-20.9l-4.2-43.78-21.19-8.23-13-27.8-11.3-24.18c1 .6 64.87 38.69 67.74 40.91s2.85 63.08 2.85 63.08Z" />
    <path fill="#3f3d56" d="M559.19 319.08s-52.84 19.72-79.69 8.88-52.01-80.88-51.74-114.88c0 0 26-16.46 51.33-6.35.54.21 1.07.42 1.59.65l.41.2c.32.14.64.28.94.44s.73.35 1.08.54c1 .52 2 1.09 3 1.72.33.21.64.42 1 .61l1.7 1.16c.27.21.54.4.8.59.52.39 1 .77 1.46 1.14l.66.54c1.19 1 2.36 2.08 3.53 3.24l.13.14s-11.81 42.3.79 69.19c10.43 22.22 54.26 9.08 57.91 8l.24-.08Z" />
    <path fill="#25233a" d="m375.6 366.08 18-6.18a10.43 10.43 0 0 0 6.3-13.82l-.42-1-4.29-14.32-19.59 5.59s3.42 8.18-1.18 11.65-22.5 15.75-22.76 23.16 23.94-5.08 23.94-5.08ZM554.31 295.25s21.75-5.56 24.12-5 7.79 6.43 12.19 21.61 6.44 22.48 4.07 23.94-13.21 2.63-16.93-6.43-5.42-14.49-8.81-15.87-10.92 0-10.92 0Z" />
    <path fill="#3f3d56" d="M404.42 8.68s-8.35 3.47-9.2 10.46 6.3 11.42 6.3 11.42 5.63-3.24 10.23-2S430.16 26 430.16 26l6 13.29s3.07-10 6.14-7.67 1 10.23 0 11.94.68 3.7.68 3.7l3.06 6.18 4.1 2.39 5.62-1s-2.55-37.85-7.5-44.84-12.44-8.52-13.29-7.5-20.66-9.41-30.55 6.19Z" />
    <path fill="#68e1fd" d="m451.99 112.4-24.53 53.21s-1 5.26-16.82 7.54-68.71-5-68.71-5l.41-13.59.3-10.27s61.54 3.71 61.51.94c0-2.29 14-37 18.77-48.91a16.18 16.18 0 0 1 9.84-9.41 14.27 14.27 0 0 1 12.07 1.5 18.76 18.76 0 0 1 7.16 23.99Z" />
    <path fill="#68e1fd" d="M0 185.38 585.06 590.1H0V185.38z" />
  </motion.svg>
);

export const HeroSection = () => {
  return (
    <section className="relative pt-20 pb-32 bg-white dark:bg-gray-950 overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-3/4 h-3/4 bg-gradient-to-br from-primary-500/[0.07] to-transparent dark:from-primary-500/[0.03] blur-[120px] rounded-full" />
        <div className="absolute bottom-0 right-1/4 w-3/4 h-3/4 bg-gradient-to-tl from-secondary-500/[0.07] to-transparent dark:from-secondary-500/[0.03] blur-[120px] rounded-full" />
      </div>

      <Container className="relative">
        <div className="max-w-4xl mx-auto text-center">
          {/* Eyebrow Text */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 rounded-full mb-8 bg-gradient-to-r from-primary-500/20 to-secondary-500/20 dark:from-primary-500/30 dark:to-secondary-500/30 p-3 backdrop-blur-sm border border-primary-500/20 dark:border-primary-500/30"
          >
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center">
                <RocketIcon className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-semibold text-gray-900 dark:text-white px-2">
                AI-Powered Job Search Platform
              </span>
            </div>
          </motion.div>

          {/* Main Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6 bg-clip-text"
          >
            Find Your Dream Job with{' '}
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              AI-Powered
            </span>{' '}
            Precision
          </motion.h1>

          {/* Subheading */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto"
          >
            Let our AI analyze your skills and experience to match you with the perfect job opportunities. Fast, accurate, and tailored to your career goals.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Button
              size="lg"
              className="bg-gradient-primary text-white font-medium hover:shadow-lg transition-shadow min-w-[160px]"
              onClick={() => console.log('Get Started clicked')}
            >
              Get Started
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-900 min-w-[160px]"
              onClick={() => console.log('Learn More clicked')}
            >
              Learn More
            </Button>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 px-4"
          >
            {[
              { number: '95%', label: 'Success Rate' },
              { number: '24h', label: 'Average Match Time' },
              { number: '10k+', label: 'Active Users' },
              { number: '500+', label: 'Partner Companies' },
            ].map((stat, index) => (
              <div key={stat.label} className="text-center group">
                <div className="relative inline-block">
                  <div className="absolute inset-0 bg-gradient-primary blur-lg opacity-20 group-hover:opacity-30 transition-opacity" />
                  <h3 className="relative text-3xl md:text-4xl font-bold mb-2 bg-gradient-primary bg-clip-text text-transparent transform transition-transform duration-300 group-hover:scale-110">
                    {stat.number}
                  </h3>
                </div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {stat.label}
                </p>
              </div>
            ))}
          </motion.div>
        </div>
      </Container>
    </section>
  );
};
