import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */

  pageExtensions: ["tsx", "ts", "jsx", "js"],
  eslint: {
    dirs: ["src"],
  },
  // Optional but helpful:
  // webpack: (config) => {
  //   config.watchOptions = {
  //     ignored: ["**/core/**", "**/ecommerce/**"],
  //     // poll: 1000,
  //     // aggregateTimeout: 300,
  //   };
  //   return config;
  // },

  webpack: (config, { dev }) => {
    if (dev) {
      config.cache = false; // 🛑 disables filesystem cache in dev
    }
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
      ignored: ["**/core/**", "**/ecommerce/**", "**/*.py"],
    };
    return config;
  },


};

export default nextConfig;
