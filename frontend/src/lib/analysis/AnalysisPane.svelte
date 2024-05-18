<!--
	@component

	A pane of analysis. TODO: Expand docs

	The analysis pane is responsible for fetching the data that the mode components need.
-->

<script lang="ts">
	import { getComponent } from '$lib/analysis/modes';
	import { getData } from '$lib/analysis/engine/communication';
	import type { PaneState } from './analysis-pane';
	import ModeSelector from './modes/ModeSelector.svelte';

	export let state: PaneState;

	$: dataPromise = Promise.all(
		state.files.map((file) => getData({ mode: state.mode, fileId: file.id, frame: file.frame }))
	);

	$: component = getComponent(state.mode);
</script>

<section class="relative h-full">
	<ModeSelector bind:mode={state.mode}></ModeSelector>

	{#await dataPromise then data}
		<svelte:component this={component} {data}></svelte:component>
	{:catch error}
		<p>Error: {error.message}</p>
	{/await}
</section>
