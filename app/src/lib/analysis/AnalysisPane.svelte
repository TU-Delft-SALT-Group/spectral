<!--
	@component

	A pane of analysis.

	The analysis pane is responsible for fetching the data that the mode components need.

	This component represents a single "tab".

	@see Workspace
-->

<script lang="ts">
	import { modeComponents, modeNames, type ModeComponent, type mode } from '$lib/analysis/modes';
	import { memoize, deepEqual, JsonSafeParse } from '$lib/utils';
	import { snapshotState } from '$lib/utils.svelte';
	import type { PaneState } from './analysis-pane';
	import { getComputedFileData } from './kernel/communication';
	import ModeSelector from './modes/ModeSelector.svelte';
	import { fileState } from './modes/file-state';

	let { paneState }: { paneState: PaneState } = $props();

	// Computed data is memoized for each mode and fileState
	const memoizedGetComputedData = memoize(getComputedFileData, {
		maxSize: modeNames.length * paneState.files.length * 5,
		hashKey: ({ mode, fileState }) => structuredClone({ mode, fileState: snapshotState(fileState) })
	});

	// This function returns a closure when all the computed data is loaded, so that the consumers
	// don't need to handle asynchronicity
	const getComputedDataFunction = async (mode: mode.Name, paneState: PaneState) => {
		const computedFileData = await Promise.all(
			paneState.files.map(async (fileState) => await memoizedGetComputedData({ mode, fileState }))
		);

		return (fileState: mode.FileState<mode.Name>) => {
			const index = paneState.files.findIndex((file) => deepEqual(file, fileState));
			return computedFileData[index];
		};
	};

	let getComputedDataProp: null | mode.GetComputedData = $state(null);

	// We delay changing mode until we have the data properly loaded
	let activeMode = $state(paneState.mode);

	// Whenever we have data ready, update mode and the `getComputedData` function
	$effect(() => {
		getComputedDataFunction(paneState.mode, paneState).then((fn) => {
			getComputedDataProp = fn;
			activeMode = paneState.mode;
		});
	});

	export function removeFile(fileId: string) {
		paneState.files = paneState.files.filter((file) => file.id !== fileId);
	}
</script>

<section
	class="relative h-full overflow-scroll"
	ondragover={(event) => {
		event.preventDefault();
		if (event.dataTransfer) {
			event.dataTransfer.dropEffect = 'move';
		}
	}}
	ondrop={async (event) => {
		event.preventDefault();
		if (event.dataTransfer) {
			const transferredData = event.dataTransfer.getData('application/json');
			const { value: json, ok } = JsonSafeParse(transferredData);
			if (!ok) {
				// From Dockview
				return;
			}

			const file = fileState.parse(json);

			// Don't add files already present
			if (paneState.files.some((f) => f.id === file.id)) {
				// TODO: Show message (in a Sonner)
				return;
			}

			// When adding a file, wait until we compute the data to add it in
			const newFiles = [...paneState.files, file];
			getComputedDataProp = await getComputedDataFunction(paneState.mode, {
				...paneState,
				files: newFiles
			});
			paneState.files = newFiles;
		}
	}}
	role="group"
>
	<ModeSelector
		bind:mode={paneState.mode}
		onModeHover={(mode) => getComputedDataFunction(mode, paneState)}
	></ModeSelector>

	{#if getComputedDataProp === null}
		Loading...
	{:else}
		<!--
			The type of the component is a union of mode components. However, this means that
			the resulting type only accepts the *intersection* of all modeState and fileData.

			We can use (or abuse?) contravariance, setting the component as a component that accepts
			the modeState and fileData of *any* mode. This is technically incorrect, but I've found
			no way to make the types realize that we're passing *one* mode in two places.

			This is particularly tricky because of the computed data :/

			(prepend every word of this with an "I think")
		-->
		<svelte:component
			this={modeComponents[activeMode].component as ModeComponent<mode.Name>}
			bind:modeState={paneState.modeState[activeMode]}
			bind:fileStates={paneState.files}
			getComputedData={getComputedDataProp}
			onRemoveFile={removeFile}
		></svelte:component>
	{/if}
</section>
