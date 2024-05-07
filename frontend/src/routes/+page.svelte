<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<main class="grid h-screen place-content-center">
	<div class="my-4">
		<h1 class="text-[12vw] font-bold">Spectral</h1>
		<p class="text-lg opacity-70">Toolkit for atypical speech</p>
	</div>

	<div class="flex w-full gap-2 px-16">
		<Button class="flex-1" href="/analyze">Start analyzing</Button>
		<Button class="flex-1" href="/about" variant="secondary">About</Button>
	</div>
</main>
