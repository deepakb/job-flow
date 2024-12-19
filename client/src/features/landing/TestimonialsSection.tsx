import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { StarFilledIcon, QuoteIcon } from "@radix-ui/react-icons";

const testimonials = [
  {
    name: "Sarah Johnson",
    role: "Software Engineer",
    company: "Tech Solutions Inc.",
    image: "/testimonials/sarah.jpg",
    content: "JobFlow's AI-powered matching system helped me land my dream job at a top tech company. The process was seamless and the recommendations were spot-on!",
    rating: 5,
  },
  {
    name: "Michael Chen",
    role: "Product Manager",
    company: "Innovation Labs",
    image: "/testimonials/michael.jpg",
    content: "The personalized job recommendations and instant application feature saved me countless hours. I secured multiple interviews within weeks!",
    rating: 5,
  },
  {
    name: "Emily Rodriguez",
    role: "Marketing Director",
    company: "Creative Minds",
    image: "/testimonials/emily.jpg",
    content: "What sets JobFlow apart is their attention to detail in matching candidates with the right opportunities. Their platform is truly revolutionary.",
    rating: 5,
  },
];

export const TestimonialsSection = () => {
  return (
    <section className="py-24 bg-white dark:bg-gray-950 relative overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-gradient-to-bl from-primary-500/[0.07] to-transparent dark:from-primary-500/[0.03] blur-[120px] rounded-full" />
        <div className="absolute bottom-0 left-0 w-1/2 h-1/2 bg-gradient-to-tr from-secondary-500/[0.07] to-transparent dark:from-secondary-500/[0.03] blur-[120px] rounded-full" />
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
            Success Stories
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold text-gray-900 dark:text-white mb-4"
          >
            Hear from our successful job seekers
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto"
          >
            Join thousands of professionals who have found their perfect career match through JobFlow
          </motion.p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group relative"
            >
              {/* Testimonial Card */}
              <div className="bg-white dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 hover:border-primary-500 dark:hover:border-primary-400 transition-all duration-300 h-full flex flex-col relative z-10">
                {/* Quote Icon */}
                <div className="absolute -top-3 -left-3 w-12 h-12 rounded-xl bg-gradient-primary p-3 text-white transform rotate-12 group-hover:rotate-0 transition-transform duration-300">
                  <QuoteIcon className="w-6 h-6" />
                </div>

                {/* Content */}
                <div className="mb-6 pt-4">
                  <p className="text-gray-600 dark:text-gray-400 italic">
                    "{testimonial.content}"
                  </p>
                </div>

                {/* Rating */}
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <StarFilledIcon
                      key={i}
                      className="w-4 h-4 text-yellow-400"
                    />
                  ))}
                </div>

                {/* Author */}
                <div className="flex items-center mt-auto">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 p-[2px] mr-4">
                    <div className="w-full h-full rounded-full overflow-hidden">
                      <img
                        src={testimonial.image}
                        alt={testimonial.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white">
                      {testimonial.name}
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {testimonial.role} at {testimonial.company}
                    </p>
                  </div>
                </div>

                {/* Hover Gradient Border */}
                <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 opacity-0 group-hover:opacity-10 dark:group-hover:opacity-20 transition-opacity duration-300" />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <div className="bg-white dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 text-center">
            <h3 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
              95%
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Success Rate
            </p>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 text-center">
            <h3 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
              10k+
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Happy Users
            </p>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl p-8 border border-gray-200 dark:border-gray-800 text-center">
            <h3 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
              30+
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Partner Companies
            </p>
          </div>
        </motion.div>
      </Container>
    </section>
  );
};
