<script>
  import { onMount } from "svelte";
  import { isLoading } from "svelte-i18n";

  import NotFound from "documentcloud-frontend/src/pages/NotFound.svelte";
  import Empty from "documentcloud-frontend/src/pages/home/Empty.svelte";
  import Viewer from "documentcloud-frontend/src/pages/viewer/Viewer.svelte";

  import { router } from "documentcloud-frontend/src/router/router.js";
  import { viewer } from "documentcloud-frontend/src/viewer/viewer.js";
  import { layout } from "documentcloud-frontend/src/viewer/layout.js";

  import "documentcloud-frontend/src/langs/i18n.js";

  import Index from "./Index.svelte";

  let component;

  // inline everything we can to avoid accidental imports
  router.notFound = NotFound;
  router.routeFunc = function route() {
    return {
      app: {
        path: "/",
        component: Index,
      },

      viewer: {
        path: "/documents/:id",
        component: Viewer,
      },
    };
  };

  viewer.router = router;
  layout.router = router;

  function handleBackNav(e) {
    console.log(e);
    if (e.state == null) return;
    router.currentUrl = e.state.path;
  }

  $: routeComponent =
    ($router.resolvedRoute || { component: Empty }).component || Empty;
  $: routeProps = ($router.resolvedRoute || { props: [] }).props || {};

  $: console.log($router.resolvedRoute);
  $: console.log(component);

  onMount(() => {
    window.router = router;
    window.viewer = viewer;
    window.layout = layout;
    window.component = component;

    router.currentUrl = window.location.pathname + window.location.search;

    if (!window.history.state) {
      window.history.replaceState(
        { path: window.location.pathname },
        "",
        window.location.href
      );
    }
  });
</script>

<svelte:window on:popstate={handleBackNav} />

{#if $isLoading}
  Please wait...
{:else if $router.resolvedRoute}
  <svelte:component
    this={routeComponent}
    bind:this={component}
    {...routeProps}
  />
{/if}
