<!--
	@component

	A pane of analysis. TODO: Expand docs

	The analysis pane is responsible for fetching the data that the mode components need.
-->

<script lang="ts">
	import { browser } from '$app/environment';
	import {
		modeComponents,
		type FileData,
		type mode,
		type ModeComponent,
		type ModeComponentProps
	} from '$lib/analysis/modes';
	import Json from '$lib/components/Json.svelte';
	import type { PaneState } from './analysis-pane';
	import { getComputedFileData } from './kernel/communication';
	import ModeSelector from './modes/ModeSelector.svelte';
	import { fileState } from './modes/file-state';

	export let state: PaneState;

	type RendererBundle<M extends mode.Name> = {
		component: ModeComponent<M>;
		props: ModeComponentProps<M> | { error: unknown } | null;
		stale: boolean;
	};

	let data = Object.fromEntries(
		Object.entries(modeComponents).map(([mode, { component }]) => {
			return [
				mode,
				{
					component,
					props: null,
					stale: false
				}
			];
		})
	) as {
		[M in mode.Name]: RendererBundle<M>;
	};

	async function getProps(state: PaneState) {
		if (data[state.mode].props === null || data[state.mode].stale) {
			try {
				const modeState = state.modeState;
				const fileData = state.files.map(
					async (fileState): Promise<FileData<mode.Name>> => ({
						fileState,
						computedData: await getComputedFileData({
							fileId: fileState.id,
							mode: state.mode,
							frame: fileState.frame ?? null
						})
					})
				);

				data[state.mode].props = {
					modeState,
					fileData: (await Promise.all(fileData)) as any // eslint-disable-line @typescript-eslint/no-explicit-any
				};
				data[state.mode].stale = false;
			} catch (error) {
				data[state.mode].props = { error };
			}
		}

		return data[state.mode].props as ModeComponentProps<mode.Name>;
	}

	$: browser && getProps(state);

	function makeStale() {
		for (const bundle of Object.values(data)) {
			bundle.stale = true;
		}
	}

	export function removeFile(fileId: string) {
		state.files = state.files.filter((file) => file.id !== fileId);
		makeStale();
	}

	$: if (browser) {
		getProps(state);
	}
</script>

<section
	class="relative h-full"
	on:dragover={(event) => {
		event.preventDefault();
		if (event.dataTransfer) {
			event.dataTransfer.dropEffect = 'copy';
		}
	}}
	on:drop={async (event) => {
		event.preventDefault();
		if (event.dataTransfer) {
			const transferredData = event.dataTransfer.getData('application/json');
			const json = JSON.parse(transferredData);
			const file = fileState.parse(json);

			// Don't add files already present
			if (state.files.some((f) => f.id === file.id)) {
				return;
			}

			state.files = [...state.files, file];
			makeStale();
		}
	}}
	role="group"
>
	<ModeSelector bind:mode={state.mode} onModeHover={(mode) => getProps({ ...state, mode })}
	></ModeSelector>

	{#if data[state.mode].props === null}
		Loading
	{:else if 'error' in data[state.mode].props!}
		<div class="h-full w-full p-8 text-2xl">
			Error: <Json json={(data[state.mode].props as { error: unknown }).error}></Json>

			<!-- TODO:Add an option to reset session state  -->
		</div>
	{:else}
		<svelte:component
			this={(data[state.mode] as RendererBundle<mode.Name>).component}
			bind:modeState={(data[state.mode].props as ModeComponentProps<mode.Name>).modeState}
			bind:fileData={(data[state.mode].props as ModeComponentProps<mode.Name>).fileData}
			onRemoveFile={removeFile}
		></svelte:component>
	{/if}
</section>
