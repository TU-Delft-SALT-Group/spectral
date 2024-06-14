<script lang="ts">
	import { used } from '$lib/utils';
	import { flip } from 'svelte/animate';
	import type { ModeComponentProps } from '..';
	import SimpleInfoSingle from './SimpleInfoSingle.svelte';
	import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let fileStates: ModeComponentProps<'simple-info'>['fileStates'];
	export let modeState: ModeComponentProps<'simple-info'>['modeState'];
	export let getComputedData: ModeComponentProps<'simple-info'>['getComputedData'];
	export let onRemoveFile: (fileId: string) => void = () => {};

	used(modeState);
</script>

<div class="flex h-full flex-wrap items-center justify-center gap-4 p-4">
	{#each fileStates as fileState (fileState.id)}
		<div
			class="min-w-sm h-fit max-w-2xl flex-1 rounded bg-secondary p-4 text-secondary-foreground"
			animate:flip={{ duration: 500, easing: quintOut }}
			transition:fly={{ x: 50 }}
		>
			<SimpleInfoSingle
				computedData={getComputedData(fileState)}
				bind:fileState
				onRemoveFile={() => onRemoveFile(fileState.id)}
			></SimpleInfoSingle>
		</div>
	{/each}
</div>
