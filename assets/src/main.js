import "documentcloud-frontend/src/style/variables.css";
import "documentcloud-frontend/src/style/global.css";

import App from "./App.svelte";

const app = new App({
  target: document.getElementById("app"),
});

export default app;
