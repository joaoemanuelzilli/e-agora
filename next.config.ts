import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Modelo clássico: páginas estáticas geradas no build a partir dos JSON do estudo;
  // rotas /api/* rodam a cada requisição (cotações ao vivo da B3 e do BCB).
  cacheComponents: false,
  partialPrefetching: false,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
