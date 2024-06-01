<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { mode } from '..';
	import { onDestroy, onMount } from 'svelte';
	import used from '$lib/utils';
	import ZoomPlugin from 'wavesurfer.js/dist/plugins/zoom.js';
	import { Button } from '$lib/components/ui/button';
	import { TracksPlugin, type Track } from '.';

	export let computedData: mode.ComputedData<'transcription'>;
	export let fileState: mode.FileState<'transcription'>;
	used(computedData);

	let element: HTMLElement;

	let wavesurfer: WaveSurfer;
	let zoom: ZoomPlugin;
	let tracksPlugin: TracksPlugin;
	let tracks: Track[] = [];

	onMount(() => {
		wavesurfer = WaveSurfer.create({
			container: element,
			url: `/db/file/${fileState.id}`,
			height: 300
		});

		zoom = wavesurfer.registerPlugin(ZoomPlugin.create());
		tracksPlugin = wavesurfer.registerPlugin(
			TracksPlugin.create({
				tracks
			})
		);
	});

	onDestroy(() => {
		zoom.destroy();
		tracksPlugin.destroy();

		wavesurfer.destroy();
	});
</script>

<section class="w-full">
	<div bind:this={element}></div>
	<Button
		class="w-full"
		on:click={() => {
			tracks = [...tracks, {}];
			tracksPlugin.update({ tracks: [...tracks, {}] });
		}}
	>
		+
	</Button>
</section>
