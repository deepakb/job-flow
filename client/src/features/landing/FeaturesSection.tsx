import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import {
  RocketIcon,
  MagicWandIcon,
  LightningBoltIcon,
  MagnifyingGlassIcon,
  LayersIcon,
  TargetIcon,
  LockClosedIcon,
  BellIcon,
} from "@radix-ui/react-icons";

const features = [
  {
    title: "AI Resume Analysis",
    description: "Get detailed skill assessments, ATS optimization, and career insights powered by advanced AI.",
    icon: <MagicWandIcon className="w-5 h-5" />,
    gradient: "from-blue-500 to-purple-500",
  },
  {
    title: "Smart Job Matching",
    description: "Find perfect job matches with real-time scraping and intelligent skill-based recommendations.",
    icon: <LightningBoltIcon className="w-5 h-5" />,
    gradient: "from-purple-500 to-pink-500",
  },
  {
    title: "Career Growth Tools",
    description: "Track your professional development with skill gap analysis and career path guidance.",
    icon: <TargetIcon className="w-5 h-5" />,
    gradient: "from-pink-500 to-red-500",
  },
  {
    title: "Real-time Updates",
    description: "Stay informed with instant notifications about job matches and application status.",
    icon: <BellIcon className="w-5 h-5" />,
    gradient: "from-red-500 to-orange-500",
  },
  {
    title: "Resume Enhancement",
    description: "Get AI-powered suggestions to improve content, quantify achievements, and optimize for ATS.",
    icon: <LayersIcon className="w-5 h-5" />,
    gradient: "from-orange-500 to-yellow-500",
  },
  {
    title: "Advanced Search",
    description: "Search jobs across multiple sources with smart filters and personalized rankings.",
    icon: <MagnifyingGlassIcon className="w-5 h-5" />,
    gradient: "from-yellow-500 to-green-500",
  },
  {
    title: "Secure Platform",
    description: "Enterprise-grade security with Firebase authentication and API protection.",
    icon: <LockClosedIcon className="w-5 h-5" />,
    gradient: "from-green-500 to-teal-500",
  },
  {
    title: "Career Insights",
    description: "Get industry-specific recommendations and professional development tracking.",
    icon: <RocketIcon className="w-5 h-5" />,
    gradient: "from-teal-500 to-cyan-500",
  },
];

export const FeaturesSection = () => {
  return (
    <section className="py-24 bg-white dark:bg-gray-950 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-1/2 h-1/2 bg-gradient-to-br from-primary-500/[0.07] to-transparent dark:from-primary-500/[0.03] blur-[120px] rounded-full" />
        <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-gradient-to-br from-secondary-500/[0.07] to-transparent dark:from-secondary-500/[0.03] blur-[120px] rounded-full" />
      </div>

      <Container className="relative">
        {/* Section Header */}
        <div className="text-center mb-16">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-sm font-medium bg-gradient-primary bg-clip-text text-transparent mb-4"
          >
            Powered by Advanced AI
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold text-gray-900 dark:text-white mb-4"
          >
            Comprehensive Job Search Platform
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto"
          >
            Our AI-powered platform combines cutting-edge technology with user-friendly features to streamline your job search and career growth.
          </motion.p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group relative"
            >
              <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800 hover:border-primary-500 dark:hover:border-primary-400 transition-all duration-300 h-full flex flex-col relative z-10">
                {/* Icon */}
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} p-3.5 text-white mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  {feature.icon}
                </div>

                {/* Content */}
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm flex-grow">
                  {feature.description}
                </p>

                {/* Hover Gradient Border */}
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 opacity-0 group-hover:opacity-10 dark:group-hover:opacity-20 transition-opacity duration-300" />
              </div>
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  );
};
