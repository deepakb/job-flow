import { useState } from "react";
import { GitHubLogoIcon, LinkedInLogoIcon } from "@radix-ui/react-icons";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";
import Logo from "@/components/ui/Logo";
import { Link } from "react-router-dom";
import { Carousel } from "@/components/ui/Carousel";
import { features } from "@/features/auth/features-data";

// Google icon component to match Radix Icons style
const GoogleIcon = () => (
  <svg
    width="15"
    height="15"
    viewBox="0 0 15 15"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className="w-5 h-5"
  >
    <path
      d="M14.5 7.5c0-.542-.046-1.075-.139-1.591H7.5v3.014h3.938a3.436 3.436 0 01-1.459 2.209v1.85h2.368C13.663 11.675 14.5 9.755 14.5 7.5z"
      fill="currentColor"
    />
    <path
      d="M7.5 15c1.982 0 3.637-.662 4.847-1.786l-2.368-1.85c-.657.444-1.5.706-2.479.706-1.904 0-3.513-1.288-4.087-3.02H.987v1.914A7.496 7.496 0 007.5 15z"
      fill="currentColor"
    />
    <path
      d="M3.413 9.05A4.478 4.478 0 013.103 7.5c0-.537.113-1.062.31-1.55V4.036H.987A7.496 7.496 0 000 7.5c0 1.213.288 2.363.987 3.464l2.426-1.914z"
      fill="currentColor"
    />
    <path
      d="M7.5 3.03c1.074 0 2.037.37 2.795 1.097l2.101-2.117C11.088.757 9.433.001 7.5.001 4.574.001 2.028 1.671.987 4.036l2.426 1.914C3.987 4.318 5.596 3.03 7.5 3.03z"
      fill="currentColor"
    />
  </svg>
);

const Login = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // TODO: Implement Firebase login
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Container className="flex min-h-screen">
        {/* Left Side - Form */}
        <div className="flex-1 flex flex-col justify-center max-w-md mx-auto w-full py-12 px-4">
          <div className="text-center mb-8">
            <a href="/" className="inline-flex items-center gap-2 mb-8">
              <Logo width={40} height={40} className="w-[40px] h-[40px]" />
              <span className="text-2xl font-black bg-gradient-primary bg-clip-text text-transparent">
                JobFlow
              </span>
            </a>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Welcome back
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Sign in to continue to JobFlow
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            {/* Email Input */}
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Email address
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-200 dark:border-gray-800 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 dark:focus:border-primary-500 transition-colors"
                placeholder="Enter your email"
              />
            </div>

            {/* Password Input */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-200 dark:border-gray-800 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 dark:focus:border-primary-500 transition-colors"
                placeholder="Enter your password"
              />
            </div>

            {/* Forgot Password Link */}
            <div className="flex items-center justify-end">
              <a
                href="#forgot-password"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-transparent hover:bg-gradient-primary hover:bg-clip-text dark:hover:text-transparent transition-colors"
              >
                Forgot password?
              </a>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full bg-gradient-primary text-white font-medium hover:shadow-lg transition-shadow rounded-lg"
              disabled={isLoading}
            >
              {isLoading ? "Signing in..." : "Sign in"}
            </Button>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200 dark:border-gray-800"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-950">
                  Or continue with
                </span>
              </div>
            </div>

            {/* Social Login Buttons */}
            <div className="grid grid-cols-3 gap-3">
              <Button
                type="button"
                className="w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 font-medium transition-colors rounded-lg flex items-center justify-center"
              >
                <GoogleIcon />
              </Button>
              <Button
                type="button"
                className="w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 font-medium transition-colors rounded-lg flex items-center justify-center"
              >
                <GitHubLogoIcon className="w-5 h-5" />
              </Button>
              <Button
                type="button"
                className="w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 font-medium transition-colors rounded-lg flex items-center justify-center"
              >
                <LinkedInLogoIcon className="w-5 h-5" />
              </Button>
            </div>

            {/* Sign Up Link */}
            <p className="text-center text-sm text-gray-600 dark:text-gray-400">
              Don't have an account?{" "}
              <Link
                to="/signup"
                className="font-medium hover:text-transparent hover:bg-gradient-primary hover:bg-clip-text dark:hover:text-transparent transition-colors"
              >
                Sign up
              </Link>
            </p>
          </form>
        </div>

        {/* Right Side - Features Carousel */}
        <div className="hidden lg:flex flex-1 items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950">
          <div className="w-full max-w-xl px-8">
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Welcome to JobFlow
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                Discover a smarter way to manage your job search with our AI-powered platform
              </p>
            </div>
            <Carousel 
              slides={features} 
              autoplayDelay={5000}
              className="w-full"
            />
          </div>
        </div>
      </Container>
    </div>
  );
};

export default Login;
