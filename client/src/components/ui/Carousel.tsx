import { useCallback, useEffect, useState } from "react";
import useEmblaCarousel, { EmblaOptionsType } from "embla-carousel-react";
import { cn } from "@/utils/cn";

interface CarouselProps {
  slides: {
    title: string;
    description: string;
    icon: React.ReactNode;
  }[];
  options?: EmblaOptionsType;
  className?: string;
  autoplayDelay?: number;
}

export function Carousel({
  slides,
  options = { loop: true },
  className,
  autoplayDelay = 4000,
}: CarouselProps) {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    ...options,
    watchDrag: false,
  });
  const [selectedIndex, setSelectedIndex] = useState(0);

  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setSelectedIndex(emblaApi.selectedScrollSnap());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on("select", onSelect);
    return () => {
      emblaApi.off("select", onSelect);
    };
  }, [emblaApi, onSelect]);

  useEffect(() => {
    if (!emblaApi) return;

    const autoplay = setInterval(() => {
      if (emblaApi.canScrollNext()) {
        emblaApi.scrollNext();
      } else {
        emblaApi.scrollTo(0);
      }
    }, autoplayDelay);

    return () => clearInterval(autoplay);
  }, [emblaApi, autoplayDelay]);

  return (
    <div className={cn("relative overflow-hidden", className)}>
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex touch-pan-y">
          {slides.map((slide, index) => (
            <div
              className="flex-[0_0_100%] min-w-0 relative pr-4 first:pl-0"
              key={index}
            >
              <div className="bg-white/5 dark:bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/10 dark:border-white/10">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-primary flex items-center justify-center">
                    {slide.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {slide.title}
                  </h3>
                </div>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  {slide.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="flex justify-center gap-2 mt-6">
        {slides.map((_, index) => (
          <button
            key={index}
            className={cn(
              "h-2 rounded-full transition-all duration-300",
              index === selectedIndex
                ? "w-8 bg-gradient-primary"
                : "w-2 bg-gray-300 dark:bg-white/20 hover:bg-gray-400 dark:hover:bg-white/30"
            )}
            onClick={() => emblaApi?.scrollTo(index)}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
