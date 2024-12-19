import { ThemeProvider } from "./providers/ThemeProvider";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/layout/Navbar";
import { HeroSection } from "./features/landing/HeroSection";
import { FeaturesSection } from "./features/landing/FeaturesSection";
import { HowItWorksSection } from "./features/landing/HowItWorksSection";
import { TestimonialsSection } from "./features/landing/TestimonialsSection";
import { PricingSection } from "./features/landing/PricingSection";
import { Footer } from "./components/layout/Footer";
import Login from "./pages/login";
import SignUp from "./pages/signup";
import "@radix-ui/themes/styles.css";

const LandingPage = () => (
  <>
    <Navbar />
    <HeroSection />
    <FeaturesSection />
    <HowItWorksSection />
    <TestimonialsSection />
    <PricingSection />
    <Footer />
  </>
);

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
