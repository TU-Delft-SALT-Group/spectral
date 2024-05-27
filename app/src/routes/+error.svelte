<script lang="ts">
	import { page } from '$app/stores';
	import Json from '$lib/components/Json.svelte';
	import * as Accordion from '$lib/components/ui/accordion';

	// Workaround for https://github.com/sveltejs/eslint-plugin-svelte/issues/652
	page;
</script>

<main class="grid h-full w-full place-content-center">
	<h1 class="text-3xl">Something went wrong!</h1>
	<h2>Status code: {$page.status}</h2>

	<Accordion.Root class="text-muted-foreground">
		<Accordion.Item value="item-1">
			<Accordion.Trigger>Details</Accordion.Trigger>
			<Accordion.Content>
				<Json json={$page.error}></Json>
			</Accordion.Content>
		</Accordion.Item>
	</Accordion.Root>
</main>
