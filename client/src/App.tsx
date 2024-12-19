import { ThemeProvider } from "./providers/ThemeProvider";
import { Navbar } from "./components/layout/Navbar";
import { HeroSection } from "./features/landing/HeroSection";
import { FeaturesSection } from "./features/landing/FeaturesSection";
import { HowItWorksSection } from "./features/landing/HowItWorksSection";
import { TestimonialsSection } from "./features/landing/TestimonialsSection";
import { PricingSection } from "./features/landing/PricingSection";
import { Footer } from "./components/layout/Footer";
import "@radix-ui/themes/styles.css";

function App() {
  return (
    <ThemeProvider>
      <main className="min-h-screen">
        <Navbar />
        <HeroSection />
        <FeaturesSection />
        <HowItWorksSection />
        <TestimonialsSection />
        <PricingSection />
        <Footer />
      </main>
    </ThemeProvider>
  );
}

export default App;
