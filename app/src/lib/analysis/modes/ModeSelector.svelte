<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { modeNames, modeComponents, modeDisplayNames, type mode as modeType } from '.';

	export let mode: modeType.Name;
	export let onModeHover: (mode: modeType.Name) => void = () => {};
</script>

<div class="main absolute right-4 top-4 z-30 flex flex-col gap-2 transition-all">
	{#each modeNames as currentMode, i (currentMode)}
		<div
			class:z-40={mode === currentMode}
			style:--index={i}
			class:opacity-0={mode !== currentMode}
			class="select relative transition duration-300"
		>
			<Button
				variant={mode === currentMode ? 'default' : 'outline'}
				class="h-10 w-16 shadow-xl"
				on:click={() => (mode = currentMode)}
				on:hover={() => onModeHover(currentMode)}
			>
				<svelte:component this={modeComponents[currentMode].icon} class="w-12"></svelte:component>
			</Button>

			<button
				class="label absolute right-16 top-0 h-12 w-max pb-2 pr-2 transition duration-300 ease-in-out"
				on:click={() => (mode = currentMode)}
			>
				{modeDisplayNames[currentMode]}
			</button>
		</div>
	{/each}
</div>

<style>
	.select {
		--percentage-plus-padding: calc(-100% - 0.5rem);
		--move-offset: calc(var(--percentage-plus-padding) * var(--index));
		transform: translateY(var(--move-offset));
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
		transition-delay: 0s;
	}

	.main:hover > div > .label {
		opacity: 0.7;
		pointer-events: all;
		cursor: pointer;
		transition-delay: 0s;
	}

	.label {
		opacity: 0;
		pointer-events: none;
		transition-delay: 0.3s;
	}

	.main > div:hover > .label {
		opacity: 1;
	}
</style>
