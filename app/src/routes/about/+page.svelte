<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<svelte:head>
	<title>About</title>
</svelte:head>

<main class="mx-auto max-w-xl px-4 py-8">
	<!-- eslint-disable svelte/no-at-html-tags Markdown data is trusted because it comes from our own server. -->
	{@html data.markDown}
</main>

<style lang="postcss">
	main :global(h2) {
		@apply pb-3 pt-6 text-3xl;
	}

	main :global(p) {
		@apply py-1;
	}

	main :global(ul) {
		@apply py-5;
	}

	main :global(a) {
		@apply text-blue-600 underline;
	}
</style>
