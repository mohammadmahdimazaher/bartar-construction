"use client";

import { useEffect } from "react";

export default function ScrollAnimations() {
  useEffect(() => {
    const elements = document.querySelectorAll<HTMLElement>(
      "section, article, [class*='card'], [class*='Card']"
    );

    elements.forEach((element, index) => {
      element.classList.add("scroll-reveal");

      // تأخیر کوتاه برای کارت‌ها
      if (
        element.matches("[class*='card'], [class*='Card']")
      ) {
        element.style.transitionDelay = `${(index % 4) * 100}ms`;
      }
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("scroll-reveal-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.12,
      }
    );

    elements.forEach((element) => observer.observe(element));

    return () => observer.disconnect();
  }, []);

  return null;
}