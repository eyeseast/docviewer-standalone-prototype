import sveltePreprocess from "svelte-preprocess";
import autoprefixer from "autoprefixer";

function scssAliases(aliases) {
  return (url) => {
    for (const [alias, aliasPath] of Object.entries(aliases)) {
      if (url.indexOf(alias) === 0) {
        return {
          file: url.replace(alias, aliasPath),
        };
      }
    }
    return url;
  };
}

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: sveltePreprocess({
    scss: {
      includePaths: ["node_modules", "src"],
      importer: [
        scssAliases({
          "@": "node_modules/documentcloud-frontend/src",
        }),
      ],
      prependData: '@import "@/style/variables.scss";',
    },
    postcss: {
      plugins: [autoprefixer],
    },
    typescript: {
      compilerOptions: {
        target: "es2020",
      },
    },
  }),
};
