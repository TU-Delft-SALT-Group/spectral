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
	import { syncPaneStateToDb as syncPaneStateToDb } from '$lib/database/sync';
	import type { PaneState } from './analysis-pane';
	import { getComputedFileData } from './kernel/communication';
	import ModeSelector from './modes/ModeSelector.svelte';

	export let state: PaneState;

	type RendererBundle<M extends mode.Name> = {
		component: ModeComponent<M>;
		props: ModeComponentProps<M> | null;
	};

	let data = Object.fromEntries(
		Object.entries(modeComponents).map(([mode, { component }]) => {
			return [
				mode,
				{
					component,
					props: null
				}
			];
		})
	) as {
		[M in mode.Name]: RendererBundle<M>;
	};

	async function getProps(state: PaneState) {
		if (data[state.mode].props === null) {
			const modeState = state.modeState;
			const fileData = state.files.map(
				async (fileState): Promise<FileData<mode.Name>> => ({
					fileState,
					computedData: await getComputedFileData({
						fileId: fileState.fileId,
						mode: state.mode,
						frame: fileState.frame ?? null
					})
				})
			);

			data[state.mode].props = {
				modeState,
				fileData: (await Promise.all(fileData)) as any // eslint-disable-line @typescript-eslint/no-explicit-any
			};
		}

		return data[state.mode].props as ModeComponentProps<mode.Name>;
	}

	$: browser && getProps(state);

	$: syncPaneStateToDb(state);
	$: console.log(data);
</script>

<section class="relative h-full">
	<ModeSelector bind:mode={state.mode} onModeHover={(mode) => getProps({ ...state, mode })}
	></ModeSelector>

	{#if data[state.mode].props !== null}
		<svelte:component
			this={(data[state.mode] as RendererBundle<mode.Name>).component}
			bind:modeState={(data[state.mode].props as ModeComponentProps<mode.Name>).modeState}
			bind:fileData={(data[state.mode].props as ModeComponentProps<mode.Name>).fileData}
		></svelte:component>
	{/if}
</section>
