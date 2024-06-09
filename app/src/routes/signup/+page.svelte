<script lang="ts">
	import type { PageData } from './$types.js';
	import SignupForm from './SignupForm.svelte';
	export let data: PageData;
</script>

<svelte:head>
	<title>Sign up Spectral</title>
</svelte:head>

<main class="mx-auto max-w-xl py-8">
	<h1 class="mb-4 text-2xl font-bold">Sign up</h1>

	<SignupForm data={data.form} />
</main>
