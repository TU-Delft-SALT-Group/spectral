<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { mode } from '..';
	import { onDestroy, onMount } from 'svelte';
	import used from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import { generateIdFromEntropySize } from 'lucia';
	import Track from './Track.svelte';

	export let computedData: mode.ComputedData<'transcription'>;
	export let fileState: mode.FileState<'transcription'>;
	used(computedData);

	let wavesurferContainer: HTMLElement;
	let wavesurfer: WaveSurfer;
	let width: number = 300;

	let minZoom: number;
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
		});

		wavesurfer.on('zoom', (px) => {
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
		<div style:width={`${width}px` ?? '100%'}>
			{#each fileState.transcriptions as transcription (transcription)}
				<Track {transcription} {duration} />
			{/each}
		</div>
	</div>
	<Button
		class="w-full"
		on:click={() => {
			fileState.transcriptions = [
				...fileState.transcriptions,
				{
					id: generateIdFromEntropySize(10),
					name: 'default',
					captions: [
						{
							start: 0,
							end: duration,
							value: 'test'
						}
					]
				}
			];
		}}
	>
		+
	</Button>
</section>
