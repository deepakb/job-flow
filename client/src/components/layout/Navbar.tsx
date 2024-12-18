import { Button } from "../ui/Button";
import { ThemeToggle } from "../ui/ThemeToggle";
import { Container } from "../ui/Container";
import { Link, useNavigate } from "react-router-dom";
import Logo from "../ui/Logo";

export const Navbar = () => {
  const navigate = useNavigate();
  
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-800">
      <Container>
        <nav className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2">
              <Logo 
                width={30} 
                height={30} 
                className="w-[30px] h-[30px]" 
              />
              <span className="text-xl font-black bg-gradient-primary bg-clip-text text-transparent">
                JobFlow
              </span>
            </Link>
            <div className="hidden md:flex items-center gap-6">
              <Link
                to="/#features"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-transparent hover:bg-gradient-primary hover:bg-clip-text dark:hover:text-transparent transition-colors relative group"
              >
                Features
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-primary transition-all group-hover:w-full"></span>
              </Link>
              <Link
                to="/#pricing"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-transparent hover:bg-gradient-primary hover:bg-clip-text dark:hover:text-transparent transition-colors relative group"
              >
                Pricing
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-primary transition-all group-hover:w-full"></span>
              </Link>
              <Link
                to="/#about"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-transparent hover:bg-gradient-primary hover:bg-clip-text dark:hover:text-transparent transition-colors relative group"
              >
                About
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-primary transition-all group-hover:w-full"></span>
              </Link>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <div className="hidden md:flex items-center gap-6">
              <Link
                to="/login"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-transparent hover:bg-gradient-primary hover:bg-clip-text dark:hover:text-transparent transition-colors relative group"
              >
                Login
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-primary transition-all group-hover:w-full"></span>
              </Link>
              <Button
                size="sm"
                rounded
                className="bg-gradient-primary text-white font-medium hover:shadow-lg transition-shadow"
                onClick={() => navigate('/signup')}
              >
                Get Started
              </Button>
            </div>
          </div>
        </nav>
      </Container>
    </header>
  );
};
