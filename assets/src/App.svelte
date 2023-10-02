<script>
  import { onMount } from "svelte";
  import { isLoading } from "svelte-i18n";

  import NotFound from "documentcloud-frontend/src/pages/NotFound.svelte";
  import Empty from "documentcloud-frontend/src/pages/home/Empty.svelte";

  import Index from "./Index.svelte";
  import Viewer from "documentcloud-frontend/src/pages/viewer/Viewer.svelte";

  import { router } from "documentcloud-frontend/src/router/router.js";
  import { lazyComponent } from "documentcloud-frontend/src/util/lazyComponent.js";

  import "documentcloud-frontend/src/langs/i18n.js";

  lazyComponent.default = Index;
  lazyComponent.viewer = Viewer;

  // inline everything we can to avoid accidental imports
  function loadDefault() {
    if (lazyComponent.default !== null) return;
    return import("./Index.svelte").then((module) => {
      lazyComponent.default = module.default;
    });
  }

  function loadViewer() {
    if (lazyComponent.viewer !== null) return;
    return import("documentcloud-frontend/src/pages/viewer/Viewer.svelte").then(
      (module) => {
        lazyComponent.viewer = module.default;
      }
    );
  }

  router.notFound = NotFound;
  router.routeFunc = function route(lazyComponent) {
    return {
      default: {
        path: "/",
        component: lazyComponent.default,
        get: loadDefault,
      },

      viewer: {
        path: "/documents/:id",
        component: lazyComponent.viewer,
        get: loadViewer,
      },
    };
  };

  $: routeComponent =
    ($router.resolvedRoute || { component: Empty }).component || Empty;
  $: routeProps = ($router.resolvedRoute || { props: [] }).props || {};

  onMount(() => {
    window.router = router;
    router.currentUrl = window.location.pathname;

    if (!window.history.state) {
      window.history.replaceState(
        { path: window.location.pathname },
        "",
        window.location.href
      );
    }
  });
</script>

{#if $isLoading}
  Please wait...
{:else if $router.resolvedRoute}
  <svelte:component this={routeComponent} {...routeProps} />
{/if}
