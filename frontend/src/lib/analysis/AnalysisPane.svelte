<!--
	@component

	A pane of analysis. TODO: Expand docs

	The analysis pane is responsible for fetching the data that the mode components need.
-->

<script lang="ts">
	import { getComponent, type Mode, type ModeData } from '$lib/analysis/modes';
	import { getData } from '$lib/analysis/engine/communication';
	import type { PaneState } from './analysis-pane';
	import ModeSelector from './modes/ModeSelector.svelte';
	import type { AnalysisFile } from '$lib/files';

	export let state: PaneState;

	function populateDataPromisesForMode(state: PaneState) {
		if (state.mode in dataPromises) {
			return;
		}

		const promises = state.files.map((file: AnalysisFile) =>
			getData({ mode: state.mode, fileId: file.id, frame: file.frame })
		);

		dataPromises[state.mode] = Promise.all(promises);
	}

	function getModeDataPromise(state: PaneState) {
		populateDataPromisesForMode(state);
		return dataPromises[state.mode];
	}

	let dataPromises: Partial<Record<Mode, Promise<ModeData[]>>> = {};

	$: dataPromise = getModeDataPromise(state);

	$: component = getComponent(state.mode);
</script>

<section class="relative h-full">
	<ModeSelector bind:mode={state.mode} onModeHover={() => populateDataPromisesForMode(state)}
	></ModeSelector>

	{#await dataPromise then data}
		<svelte:component this={component} {data}></svelte:component>
	{:catch error}
		<p>Error: {error.message}</p>
	{/await}
</section>
