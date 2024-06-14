<script lang="ts">
	import { type ModeComponentProps } from '..';
	import ErrorRatePlugin from './ErrorRatePlugin.svelte';
	import { used } from '$lib/utils';
	import { flip } from 'svelte/animate';
	import { fly } from 'svelte/transition';

	export let fileStates: ModeComponentProps<'error-rate'>['fileStates'];
	export let modeState: ModeComponentProps<'error-rate'>['modeState'];
	export let getComputedData: ModeComponentProps<'error-rate'>['getComputedData'];

	used(modeState);
</script>

<section class="flex h-fit w-full flex-col gap-6 p-6">
	{#each fileStates as fileState (fileState.id)}
		<div class="h-full w-full" transition:fly={{ x: -50 }} animate:flip>
			<ErrorRatePlugin computedData={getComputedData(fileState)} bind:fileState />
		</div>
	{/each}
</section>
