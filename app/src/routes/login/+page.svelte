<script lang="ts">
	import type { PageData } from './$types.js';
	import LoginForm from './LoginForm.svelte';
	export let data: PageData;
</script>

<main class="mx-auto max-w-xl py-8">
	<h1 class="mb-4 text-2xl font-bold">Log in</h1>
	<LoginForm data={data.form} />
</main>
