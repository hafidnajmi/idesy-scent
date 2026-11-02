/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./js/**/*.js"
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "forest-green": "#0D2A1D",
        "deep-forest": "#0D2A1D",
        "forest": "#0D2A1D",
        "primary": "#0D2A1D",
        "antique-gold": "#C9A24B",
        "gold": "#C9A24B",
        "secondary": "#C9A24B",
        "warm-ivory": "#F7F3EC",
        "surface": "#F7F3EC",
        "background": "#F7F3EC",
        "soft-stone": "#EDE6D8",
        "charcoal": "#1F1F1D",
        "on-surface-variant": "#424844",
        "primary-container": "#0d2a1d",
        "on-primary": "#ffffff",
        "on-primary-container": "#749381",
        "secondary-container": "#f4dfcb",
        "on-secondary": "#ffffff",
        "on-secondary-container": "#775800",
        "tertiary": "#240600",
        "on-tertiary": "#ffffff",
        "tertiary-container": "#461501",
        "on-tertiary-container": "#c5785a",
        "surface-container": "#eeeeeb",
        "surface-container-high": "#e9e8e5",
        "surface-container-highest": "#e3e2e0",
        "surface-container-low": "#f4f4f1",
        "surface-container-lowest": "#ffffff",
        "surface-dim": "#dadad7",
        "surface-bright": "#faf9f6",
        "surface-variant": "#e3e2e0",
        "on-surface": "#1a1c1b",
        "outline": "#727973",
        "outline-variant": "#c2c8c2",
        "error": "#ba1a1a",
        "error-container": "#ffdad6",
        "on-error": "#ffffff",
        "on-error-container": "#93000a"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "section-gap": "100px",
        "section-gap-sm": "80px",
        "section-gap-lg": "160px",
        "margin-desktop": "64px",
        "margin-mobile": "24px",
        "gutter": "32px",
        "container-max": "1280px",
        "unit": "8px"
      },
      fontFamily: {
        "sans": ["'Nunito'", "'Inter'", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        "serif": ["'Libre Caslon Display'", "Georgia", "serif"],
        "display": ["'Libre Caslon Display'", "Georgia", "serif"],
        "body": ["'Nunito'", "'Inter'", "sans-serif"],
        "nav": ["'Nunito'", "sans-serif"],
        "body-md": ["'Nunito'", "sans-serif"],
        "display-lg-mobile": ["'Libre Caslon Display'", "serif"],
        "label-caps": ["'Nunito'", "sans-serif"],
        "display-lg": ["'Libre Caslon Display'", "serif"],
        "headline-sm": ["'Libre Caslon Display'", "serif"],
        "headline-md": ["'Libre Caslon Display'", "serif"],
        "body-lg": ["'Nunito'", "sans-serif"]
      },
      fontSize: {
        "body-md": ["16px", { lineHeight: "1.5", fontWeight: "400" }],
        "display-lg-mobile": ["40px", { lineHeight: "1.1", fontWeight: "400" }],
        "label-caps": ["12px", { lineHeight: "1.2", letterSpacing: "0.1em", fontWeight: "600" }],
        "display-lg": ["64px", { lineHeight: "1.1", letterSpacing: "-0.02em", fontWeight: "400" }],
        "headline-sm": ["24px", { lineHeight: "1.3", fontWeight: "400" }],
        "headline-md": ["32px", { lineHeight: "1.2", fontWeight: "400" }],
        "body-lg": ["18px", { lineHeight: "1.6", letterSpacing: "0.01em", fontWeight: "400" }]
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries')
  ]
};
