import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import {
  UploadIcon,
  MagicWandIcon,
  LightningBoltIcon,
  ChatBubbleIcon,
  RocketIcon,
} from "@radix-ui/react-icons";

const steps = [
  {
    title: "Upload Your Resume",
    description: "Simply upload your resume and let our AI analyze your skills, experience, and career goals.",
    icon: <UploadIcon className="w-6 h-6" />,
    color: "from-blue-500 to-purple-500",
  },
  {
    title: "AI-Powered Analysis",
    description: "Our advanced AI analyzes your profile and matches you with the most relevant job opportunities.",
    icon: <MagicWandIcon className="w-6 h-6" />,
    color: "from-purple-500 to-pink-500",
  },
  {
    title: "Instant Matching",
    description: "Get matched with jobs that align with your skills and preferences in real-time.",
    icon: <LightningBoltIcon className="w-6 h-6" />,
    color: "from-pink-500 to-red-500",
  },
  {
    title: "Apply with Confidence",
    description: "Apply to multiple jobs with a single click and track your applications in real-time.",
    icon: <RocketIcon className="w-6 h-6" />,
    color: "from-red-500 to-orange-500",
  },
];

const benefits = [
  "90% faster job application process",
  "75% better job matches",
  "60% higher response rate",
  "100% secure and confidential",
];

export const HowItWorksSection = () => {
  return (
    <section className="py-24 bg-white dark:bg-gray-950 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 left-0 w-1/3 h-1/3 bg-gradient-to-br from-primary-500/20 to-secondary-500/20 dark:from-primary-500/10 dark:to-secondary-500/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-1/4 right-0 w-1/3 h-1/3 bg-gradient-to-br from-secondary-500/20 to-primary-500/20 dark:from-secondary-500/10 dark:to-primary-500/10 blur-[120px] rounded-full" />
      </div>

      <Container className="relative">
        {/* Section Header */}
        <div className="text-center mb-20">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-sm font-medium bg-gradient-primary bg-clip-text text-transparent mb-4"
          >
            How It Works
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold text-gray-900 dark:text-white mb-4"
          >
            Your Dream Job in 4 Simple Steps
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto"
          >
            Our AI-powered platform simplifies your job search process, making it faster and more efficient than ever.
          </motion.p>
        </div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-20 relative">
          {/* Connecting Line - Single line across all steps */}
          <div className="hidden lg:block absolute top-24 left-0 w-full h-[2px] bg-gradient-primary opacity-80" />
          
          {steps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="relative h-full"
            >
              {/* Step Card */}
              <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800 hover:border-primary-500 dark:hover:border-primary-400 transition-all duration-300 group h-full flex flex-col relative z-10 hover:shadow-lg">
                {/* Icon */}
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${step.color} p-3 mb-4 text-white transform group-hover:scale-110 transition-transform duration-300`}>
                  {step.icon}
                </div>

                {/* Content */}
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {step.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm flex-grow">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="bg-gradient-to-r from-gray-50 via-white to-gray-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 rounded-2xl px-8 py-6 border border-gray-200 dark:border-gray-800"
        >
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {benefits.map((benefit, index) => {
              const [number, ...rest] = benefit.split(' ');
              const text = rest.join(' ');
              
              return (
                <motion.div
                  key={benefit}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className="relative group flex flex-col items-center justify-center min-h-[80px] text-center"
                >
                  <div className="flex flex-col items-center gap-2">
                    <span className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent leading-none">
                      {number}
                    </span>
                    <span className="text-sm text-gray-600 dark:text-gray-400 font-medium leading-tight max-w-[150px]">
                      {text}
                    </span>
                  </div>
                  
                  {/* Hover Effect Line */}
                  <motion.div 
                    className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-primary"
                    initial={{ scaleX: 0 }}
                    whileHover={{ scaleX: 1 }}
                    transition={{ duration: 0.3 }}
                  />
                </motion.div>
              );
            })}
          </div>
        </motion.div>

        {/* Support Banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
          className="mt-20 text-center"
        >
          <div className="inline-flex items-center gap-2 text-gray-600 dark:text-gray-400">
            <ChatBubbleIcon className="w-5 h-5" />
            <span>Need help? Our support team is available 24/7</span>
          </div>
        </motion.div>
      </Container>
    </section>
  );
};
