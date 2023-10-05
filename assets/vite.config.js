import path from "node:path";
import url from "node:url";
import { defineConfig, loadEnv } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

import allowedKeys from "./env.json";

const __filename = url.fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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
        "@": path.resolve(__dirname, "documentcloud-frontend/src"),
        "documentcloud-frontend": path.resolve(
          __dirname,
          "documentcloud-frontend"
        ),
      },
    },

    define,
  };
});
