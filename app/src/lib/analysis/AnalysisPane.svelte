<!--
	@component

	A pane of analysis. TODO: Expand docs

	The analysis pane is responsible for fetching the data that the mode components need.
-->

<script lang="ts">
	import { browser } from '$app/environment';
	import { modeComponents, modeNames, type FileData, type mode } from '$lib/analysis/modes';
	import Json from '$lib/components/Json.svelte';
	import { memoize } from '$lib/utils';
	import type { PaneState } from './analysis-pane';
	import { getComputedFileData } from './kernel/communication';
	import ModeSelector from './modes/ModeSelector.svelte';
	import { fileState, type FileState } from './modes/file-state';

	let {
		paneState
	}: {
		paneState: PaneState;
	} = $props();

	const getFileData = memoize(
		async (state: PaneState) => {
			const fileData = state.files.map(
				async (fileState): Promise<FileData> => ({
					fileState,
					computedData: await getComputedFileData({
						mode: state.mode,
						fileState
					})
				})
			);

			return await Promise.all(fileData);
		},
		{
			maxSize: modeNames.length * 5,
			hashKey: (state) => structuredClone($state.snapshot(state))
		}
	);

	/**
	 * This variables holds the file data for the current mode.
	 *
	 *
	 * It would be nice to bind `paneState.fileState` directly. However,
	 * we need to bundle the file state with the computed data because we want it
	 * to be one object in the consumer side. This variable is a dummy variable
	 * so that the component has something to bind to.
	 *
	 * Then, whenever `fileData.value.state` changes, we update the `paneState.fileState`.

	 */
	let fileData: { value: FileData[]; for: mode.Name } | { error: unknown } | null = $state(null);

	// Update the computed file data (i.e., `fileData`) whenever the pane state changes
	$effect(() => {
		if (browser) {
			getFileData(paneState)
				.then((awaitedFileData) => (fileData = { value: awaitedFileData, for: paneState.mode }))
				.catch((error) => (fileData = { error }));
		}
	});

	// Whenever a child updates the file data, sync the pane state to reflect the changes and
	// compute the new computed file data from the kernel.
	$effect(() => {
		// Prevent infinite loops
		if ($effect.active() || fileData === null || 'error' in fileData) {
			return;
		}

		// Sync paneState <- fileData
		for (let i = 0; i < paneState?.files.length ?? 0; i++) {
			paneState.files[i]! = fileData.value[i].fileState as FileState;
		}
	});

	export function removeFile(fileId: string) {
		paneState.files = paneState.files.filter((file) => file.id !== fileId);
	}

	$effect(() => {
		console.log(paneState.mode);
	});
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
			let json;
			try {
				json = JSON.parse(transferredData);
			} catch (e) {
				// TODO: find a better fix
				return; // this might be from the dockview
			}
			const file = fileState.parse(json);

			// Don't add files already present
			if (paneState.files.some((f) => f.id === file.id)) {
				return;
			}

			paneState.files = [...paneState.files, file];
		}
	}}
	role="group"
>
	<ModeSelector
		bind:mode={paneState.mode}
		onModeHover={(mode) => getFileData({ ...paneState, mode })}
	></ModeSelector>

	{#if fileData === null || ('for' in fileData && fileData.for !== paneState.mode)}
		Loading
	{:else if 'error' in fileData}
		Error: <Json json={fileData.error}></Json>

		<!-- TODO:Add an option to reset session state  -->
	{:else}
		<svelte:component
			this={modeComponents[paneState.mode].component}
			bind:modeState={/* eslint-disable-line @typescript-eslint/no-explicit-any */ paneState.modeState as any}
			bind:fileData={/* eslint-disable-line @typescript-eslint/no-explicit-any */ fileData.value as any}
			onRemoveFile={removeFile}
		></svelte:component>
	{/if}
</section>
