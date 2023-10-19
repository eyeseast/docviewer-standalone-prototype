<script>
  import { onMount } from "svelte";

  let results = Promise.resolve([]);

  async function get_documents() {
    const endpoint = new URL("/api/documents.json", window.location);
    const r = await fetch(endpoint).then((r) => r.json());

    return r.results;
  }

  onMount(() => {
    results = get_documents();
  });
</script>

<h1>Standalone viewer prototype</h1>

{#await results}
  <p>Loading ...</p>
{:then documents}
  <ul>
    {#each documents as document}
      <li>
        <a href="/documents/{document.id}-{document.slug}">{document.title}</a>
      </li>
    {/each}
  </ul>
{:catch err}
  <p>Something went wrong.</p>
{/await}
<ul />
