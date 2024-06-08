<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<div class="grid h-full place-content-center">
	<div class="mb-4">
		<h1 class="text-[12vw] font-bold">Spectral</h1>
		<p class="text-lg text-muted-foreground">Toolkit for atypical speech</p>
	</div>

	<div class="flex w-full gap-2">
		<Button class="h-fit flex-1 text-lg" href="/session">Analyze</Button>
		<Button class="h-fit flex-1 text-lg" href="/recorder">Record</Button>
		<Button class="h-fit flex-1 text-lg" href="/about" variant="secondary">About</Button>
	</div>
</div>
