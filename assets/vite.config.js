import path from "node:path";
import { defineConfig, loadEnv } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

import allowedKeys from "./env.json";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  const define = allowedKeys.reduce((m, key) => {
    m[`process.env.${key}`] = JSON.stringify(env[key]);
    return m;
  }, {});

  return {
    plugins: [svelte()],

    resolve: {
      alias: {
        "@": path.resolve("node_modules/documentcloud-frontend/src"),
      },
    },

    define,
  };
});
