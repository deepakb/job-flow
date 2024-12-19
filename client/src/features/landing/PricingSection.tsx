import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";
import {
  CheckIcon,
  StarIcon,
  LightningBoltIcon,
  RocketIcon,
} from "@radix-ui/react-icons";

const pricingPlans = [
  {
    name: "Free",
    price: "0",
    description: "Perfect for getting started",
    features: [
      "Up to 10 job applications",
      "Basic resume analysis",
      "Job matching algorithm",
      "Email notifications",
    ],
    icon: <StarIcon className="w-5 h-5" />,
    popular: false,
  },
  {
    name: "Pro",
    price: "15",
    description: "Best for active job seekers",
    features: [
      "Unlimited job applications",
      "Advanced AI resume analysis",
      "Priority job matching",
      "Real-time notifications",
      "1-on-1 career coaching",
      "Interview preparation",
    ],
    icon: <LightningBoltIcon className="w-5 h-5" />,
    popular: true,
  },
  {
    name: "Enterprise",
    price: "49",
    description: "For teams and businesses",
    features: [
      "Everything in Pro",
      "Custom branding",
      "Team collaboration",
      "Analytics dashboard",
      "API access",
      "Dedicated support",
    ],
    icon: <RocketIcon className="w-5 h-5" />,
    popular: false,
  },
];

export const PricingSection = () => {
  return (
    <section className="py-24 bg-gray-50/50 dark:bg-gray-950 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -left-40 -bottom-40 w-80 h-80 bg-gradient-primary opacity-[0.15] dark:opacity-[0.02] blur-[100px] rounded-full" />
        <div className="absolute -right-40 -top-40 w-80 h-80 bg-gradient-primary opacity-[0.15] dark:opacity-[0.02] blur-[100px] rounded-full" />
      </div>

      <Container className="relative">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-sm font-medium bg-gradient-primary bg-clip-text text-transparent mb-4"
          >
            Pricing Plans
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold text-gray-900 dark:text-white mb-4"
          >
            Choose the perfect plan for your needs
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto"
          >
            Simple, transparent pricing that grows with you. Try any plan free for 30 days.
          </motion.p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {pricingPlans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className={`relative bg-white dark:bg-gray-900 rounded-xl overflow-hidden ${
                plan.popular
                  ? "ring-2 ring-primary-500 dark:ring-primary-400"
                  : "border border-gray-200 dark:border-gray-800"
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 right-0 bg-gradient-primary text-white text-xs font-medium px-3 py-1 rounded-bl-lg">
                  Most Popular
                </div>
              )}
              <div className="p-8">
                {/* Plan Header */}
                <div className="flex items-center gap-3 mb-6">
                  <div className={`p-2 rounded-lg ${
                    plan.popular 
                      ? "bg-gradient-primary text-white"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
                  }`}>
                    {plan.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {plan.name}
                  </h3>
                </div>

                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-bold text-gray-900 dark:text-white">
                      ${plan.price}
                    </span>
                    <span className="text-gray-600 dark:text-gray-400">/mo</span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                    {plan.description}
                  </p>
                </div>

                {/* Features */}
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-3">
                      <CheckIcon className="w-5 h-5 text-green-500" />
                      <span className="text-gray-600 dark:text-gray-400 text-sm">
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* CTA Button */}
                <Button
                  className={`w-full ${
                    plan.popular
                      ? "bg-gradient-primary text-white hover:shadow-lg"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700"
                  } transition-all`}
                >
                  {plan.popular ? "Get Started" : "Try Free"}
                </Button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Enterprise Contact */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="mt-16 text-center"
        >
          <p className="text-gray-600 dark:text-gray-400">
            Need a custom plan?{" "}
            <a
              href="#contact"
              className="text-transparent bg-gradient-primary bg-clip-text font-medium hover:underline"
            >
              Contact us
            </a>
          </p>
        </motion.div>
      </Container>
    </section>
  );
};
