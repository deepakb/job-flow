import { motion } from 'framer-motion';
import { RocketIcon } from '@radix-ui/react-icons';
import { Button } from '../../components/ui/Button';
import { Container } from '../../components/ui/Container';

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
            className="relative inline-flex items-center gap-2 rounded-full mb-8 p-[2px] bg-gradient-to-r from-[#3366FF] to-[#00B3A6]"
          >
            <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-white dark:bg-gray-950">
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
              rounded
              className="bg-gradient-primary text-white font-medium hover:shadow-lg transition-shadow min-w-[160px]"
              onClick={() => console.log('Get Started clicked')}
            >
              Get Started
            </Button>
            <Button
              size="lg"
              variant="gradient-border"
              rounded
              className="min-w-[160px]"
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
            ].map((stat) => (
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
