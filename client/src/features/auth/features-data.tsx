import {
  RocketIcon,
  MagnifyingGlassIcon,
  LightningBoltIcon,
  UpdateIcon,
  FileTextIcon,
  LockClosedIcon,
  BarChartIcon,
  StarIcon,
} from "@radix-ui/react-icons";

export const features = [
  {
    title: "AI Resume Analysis",
    description:
      "Get instant feedback on your resume with our advanced AI analysis. Optimize your CV for better job matches and higher response rates.",
    icon: <FileTextIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Smart Job Matching",
    description:
      "Our AI-powered system matches your skills and preferences with the perfect job opportunities, saving you time and increasing your success rate.",
    icon: <MagnifyingGlassIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Career Growth Tools",
    description:
      "Access powerful tools and insights to plan your career path, identify skill gaps, and take strategic steps towards your professional goals.",
    icon: <RocketIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Real-time Updates",
    description:
      "Stay informed with instant notifications about new job postings, application status changes, and important deadlines.",
    icon: <UpdateIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Resume Enhancement",
    description:
      "Get AI-powered suggestions to enhance your resume, highlighting your strengths and making your profile stand out to employers.",
    icon: <StarIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Advanced Search",
    description:
      "Use our powerful search filters to find exactly what you're looking for, from salary ranges to remote work options and company culture.",
    icon: <LightningBoltIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Secure Platform",
    description:
      "Your data is protected with enterprise-grade security. Apply with confidence knowing your information is safe and private.",
    icon: <LockClosedIcon className="w-6 h-6 text-white" />,
  },
  {
    title: "Career Insights",
    description:
      "Access detailed analytics about your job search performance, application success rates, and personalized recommendations.",
    icon: <BarChartIcon className="w-6 h-6 text-white" />,
  },
];
