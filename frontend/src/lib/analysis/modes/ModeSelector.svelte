<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { getIcon, modes, type Mode } from '.';

	export let mode: Mode;
</script>

<div class="absolute right-4 top-4 flex flex-col">
	{#each modes as currentMode}
		<Button
			on:click={() => (mode = currentMode)}
			variant={mode === currentMode ? 'default' : 'ghost'}
		>
			<svelte:component this={getIcon(currentMode)}></svelte:component>
		</Button>
	{/each}
</div>
