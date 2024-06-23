<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { modeNames, modeComponents, modeDisplayNames, type mode as modeType } from '.';

	export let mode: modeType.Name;
	export let onModeHover: (mode: modeType.Name) => void = () => {};
</script>

<div class="main absolute right-4 top-4 z-30 flex flex-col transition-all">
	<div
		class="dim-screen fixed inset-0 z-10 bg-background opacity-0 backdrop-blur transition duration-500 ease-out"
	></div>
	{#each modeNames as currentMode, i (currentMode)}
		<div
			class:z-40={mode === currentMode}
			style:--index={i}
			class:opacity-0={mode !== currentMode}
			class="select mode relative z-20 pb-2 transition duration-300"
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
				class="label absolute right-16 top-0 h-10 w-max rounded p-2 text-secondary-foreground/80 transition duration-300 ease-in-out hover:text-primary/100"
				on:click={() => (mode = currentMode)}
			>
				<span class="drop-shadow">
					{modeDisplayNames[currentMode]}
				</span>
			</button>
		</div>
	{/each}
</div>

<style lang="postcss">
	.select {
		/* --percentage-plus-padding: calc(-100%); */
		--move-offset: calc(-100% * var(--index));
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

	.main:hover > .mode {
		opacity: 1;
		transition-delay: 0s;
	}

	.main:hover > .dim-screen {
		opacity: 0.6;
	}

	.main:hover > .mode > .label {
		opacity: 1;
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
		/* @apply bg-secondary; */
	}
</style>
