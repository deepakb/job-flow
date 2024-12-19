import { Container } from "../ui/Container";
import Logo from "../ui/Logo";
import {
  TwitterLogoIcon,
  LinkedInLogoIcon,
  GitHubLogoIcon,
  DiscordLogoIcon,
  HeartFilledIcon,
  RocketIcon,
  PersonIcon,
  ReaderIcon,
  LockClosedIcon,
  ChatBubbleIcon,
} from "@radix-ui/react-icons";

const footerLinks = {
  product: {
    title: "Product",
    icon: <RocketIcon className="w-4 h-4" />,
    links: [
      { label: "Features", href: "#features" },
      { label: "Pricing", href: "#pricing" },
      { label: "Resources", href: "#resources" },
    ],
  },
  company: {
    title: "Company",
    icon: <PersonIcon className="w-4 h-4" />,
    links: [
      { label: "About", href: "#about" },
      { label: "Blog", href: "#blog" },
      { label: "Contact", href: "#contact" },
    ],
  },
  legal: {
    title: "Legal",
    icon: <LockClosedIcon className="w-4 h-4" />,
    links: [
      { label: "Privacy", href: "#privacy" },
      { label: "Terms", href: "#terms" },
      { label: "Security", href: "#security" },
    ],
  },
};

const socialLinks = [
  { icon: <TwitterLogoIcon className="w-5 h-5" />, href: "https://twitter.com", label: "Twitter" },
  { icon: <LinkedInLogoIcon className="w-5 h-5" />, href: "https://linkedin.com", label: "LinkedIn" },
  { icon: <GitHubLogoIcon className="w-5 h-5" />, href: "https://github.com", label: "GitHub" },
  { icon: <DiscordLogoIcon className="w-5 h-5" />, href: "https://discord.com", label: "Discord" },
];

export const Footer = () => {
  return (
    <footer className="bg-white dark:bg-gray-950 border-t border-gray-200 dark:border-gray-800 py-12 relative overflow-hidden">
      {/* Background Decoration */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -right-24 -bottom-24 w-96 h-96 bg-gradient-primary opacity-[0.03] blur-3xl rounded-full" />
        <div className="absolute -left-24 -top-24 w-96 h-96 bg-gradient-primary opacity-[0.03] blur-3xl rounded-full" />
      </div>

      <Container className="relative">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          {/* Company Info */}
          <div className="col-span-2 md:col-span-1">
            <a href="/" className="inline-flex items-center gap-2 mb-4">
              <Logo className="w-6 h-6" />
              <span className="text-xl font-black bg-gradient-primary bg-clip-text text-transparent">
                JobFlow
              </span>
            </a>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
              Your next career move is just a click away.
            </p>
            <div className="flex items-center gap-4">
              {socialLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  aria-label={link.label}
                >
                  {link.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Footer Links */}
          {Object.values(footerLinks).map((section) => (
            <div key={section.title}>
              <div className="flex items-center gap-2 mb-4">
                <span className="text-gray-400 dark:text-gray-500">
                  {section.icon}
                </span>
                <h3 className="font-semibold text-sm text-gray-900 dark:text-white">
                  {section.title}
                </h3>
              </div>
              <ul className="space-y-3">
                {section.links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="text-sm text-gray-600 dark:text-gray-400 group transition-colors"
                    >
                      <span className="group-hover:text-transparent group-hover:bg-gradient-primary group-hover:bg-clip-text transition-colors">
                        {link.label}
                      </span>
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-200 dark:border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-1">
              &copy; {new Date().getFullYear()} JobFlow. Made with{" "}
              <HeartFilledIcon className="w-4 h-4 text-red-500" /> in India
            </p>
            <div className="flex items-center gap-6">
              <a
                href="#help"
                className="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-1.5 group transition-colors"
              >
                <ChatBubbleIcon className="w-4 h-4 group-hover:text-transparent group-hover:bg-gradient-primary group-hover:bg-clip-text transition-colors" />
                <span className="group-hover:text-transparent group-hover:bg-gradient-primary group-hover:bg-clip-text transition-colors">
                  Help Center
                </span>
              </a>
              <a
                href="#docs"
                className="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-1.5 group transition-colors"
              >
                <ReaderIcon className="w-4 h-4 group-hover:text-transparent group-hover:bg-gradient-primary group-hover:bg-clip-text transition-colors" />
                <span className="group-hover:text-transparent group-hover:bg-gradient-primary group-hover:bg-clip-text transition-colors">
                  Documentation
                </span>
              </a>
            </div>
          </div>
        </div>
      </Container>
    </footer>
  );
};
