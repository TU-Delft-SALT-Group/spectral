<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<div class="grid h-full place-content-center">
	<div class="mb-4">
		<h1 class="text-[12vw] font-bold">Spectral</h1>
		<p class="text-lg text-muted-foreground">Toolkit for atypical speech</p>
	</div>

	<div class="flex w-full gap-2">
		<Button class="h-fit flex-1 text-lg" href="/session">Start analyzing</Button>
		<Button class="h-fit flex-1 text-lg" href="/recorder">Start Recording</Button>
		<Button class="h-fit flex-1 text-lg" href="/about" variant="secondary">About</Button>
	</div>
</div>
