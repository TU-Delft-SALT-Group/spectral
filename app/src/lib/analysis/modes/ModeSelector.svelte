<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { flip } from 'svelte/animate';
	import { modeNames, modeComponents, type mode as modeType } from '.';

	export let mode: modeType.Name;
	export let onModeHover: (mode: modeType.Name) => void = () => {};
</script>

<div class="main absolute right-4 top-4 z-30 flex flex-col gap-2 transition-all">
	{#each modeNames as currentMode, i (currentMode)}
		<div
			class:z-40={mode === currentMode}
			style:--index={i}
			class:opacity-0={mode !== currentMode}
			class="select relative transition duration-500"
			animate:flip={{ delay: 1000 }}
		>
			<Button
				on:click={() => (mode = currentMode)}
				on:hover={() => onModeHover(currentMode)}
				variant={mode === currentMode ? 'default' : 'ghost'}
				class="h-10 w-16 shadow"
			>
				<svelte:component this={modeComponents[currentMode].icon} class="w-12"></svelte:component>
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
		pointer-events: all;
	}

	.main {
		pointer-events: none;
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
