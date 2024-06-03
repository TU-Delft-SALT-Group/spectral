<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { mode } from '..';
	import { onDestroy, onMount } from 'svelte';
	import used from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import { type Track } from '.';
	import Tracks from './Tracks.svelte';

	export let computedData: mode.ComputedData<'transcription'>;
	export let fileState: mode.FileState<'transcription'>;
	used(computedData);

	let wavesurferContainer: HTMLElement;
	let wavesurfer: WaveSurfer;
	let tracks: Track[] = [];
	let width: number = 300;

	let minZoom: number;
	let currentPxPerSecond: number = 100;
	let duration: number;

	onMount(() => {
		wavesurfer = WaveSurfer.create({
			container: wavesurferContainer,
			url: `/db/file/${fileState.id}`,
			height: 300
		});

		wavesurfer.once('decode', () => {
			duration = wavesurfer.getDuration();
			minZoom = width / duration;
			currentPxPerSecond = width / duration;
		});

		wavesurfer.on('zoom', (px) => {
			currentPxPerSecond = px;
			let duration = wavesurfer.getDuration();
			wavesurfer.setOptions({
				width: duration * px
			});
		});
	});

	$: minZoom = width / duration;

	onDestroy(() => {
		wavesurfer.destroy();
	});
</script>

<section bind:clientWidth={width} class="w-full">
	<div
		class="overflow-x-scroll"
		onwheel={(event) => {
			event.preventDefault();
			event.stopImmediatePropagation();

			let px = wavesurfer.options.minPxPerSec - event.deltaY;
			if (px < minZoom) px = minZoom - 1;

			wavesurfer.zoom(px);
		}}
	>
		<div style:width={`${width}px`} bind:this={wavesurferContainer}></div>
		<Tracks width={currentPxPerSecond * duration} {tracks} />
	</div>
	<Button
		class="w-full"
		on:click={() => {
			tracks = [
				...tracks,
				{
					id: 'broken',
					name: 'lmao',
					captions: []
				}
			];
		}}
	>
		+
	</Button>
</section>
