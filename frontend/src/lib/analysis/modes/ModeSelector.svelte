<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { getIcon, modes, type Mode } from '.';

	export let mode: Mode;

	$: selectedIndex = modes.indexOf(mode);
</script>

<div class="main absolute right-4 top-4 z-30 flex flex-col gap-2 transition-all">
	{#each modes as currentMode, i}
		<div
			class:z-40={mode === currentMode}
			style:--index={i - selectedIndex}
			class:opacity-0={mode !== currentMode}
			class="select relative transition duration-500"
		>
			<Button
				on:click={() => (mode = currentMode)}
				variant={mode === currentMode ? 'default' : 'ghost'}
				class="h-10 w-16 shadow"
			>
				<svelte:component this={getIcon(currentMode)} class="w-12"></svelte:component>
			</Button>

			<span
				class="label pointer-events-none absolute right-16 top-2 h-16 w-max pr-2 transition duration-500 ease-in-out"
			>
				{currentMode}
			</span>
		</div>
	{/each}
</div>

<style>
	.select {
		transform: translateY(calc(-100% * var(--index)));
		transition-timing-function: cubic-bezier(0.86, 0, 0.07, 1); /* exponential-ish in out */
		transition-delay: 0.3s;
	}

	.main:hover > .select {
		transform: translateY(0);
		transition-timing-function: cubic-bezier(0.3, 0.86, 0.07, 1); /* exponential-ish out */
		transition-delay: 0s;
	}

	.main:hover > div {
		opacity: 1;
	}

	.main:hover > div > .label {
		opacity: 0.7;
		transition-delay: 1s;
	}

	.main > div > .label {
		opacity: 0;
		transition-delay: 0s;
	}
</style>
