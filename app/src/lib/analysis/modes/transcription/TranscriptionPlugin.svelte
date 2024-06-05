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
	let width: number;
	let minZoom: number;
	let duration: number;

	const trackNameSpace = 100;

	onMount(() => {
		wavesurfer = WaveSurfer.create({
			container: wavesurferContainer,
			url: `/db/file/${fileState.id}`,
			height: 300
		});

		let wrapper = wavesurfer.getWrapper();

		wrapper.style.overflow = 'visible';
		wrapper.style.overflowX = 'visible';

		wavesurfer.once('decode', () => {
			duration = wavesurfer.getDuration();
			minZoom = (width - trackNameSpace) / duration;

			wavesurfer.setOptions({
				width: minZoom * duration
			});
		});

		wavesurfer.on('zoom', (px) => {
			wavesurfer.setOptions({
				width: duration * px
			});
		});
	});

	onDestroy(() => {
		wavesurfer.destroy();
	});
</script>

<section bind:clientWidth={width} class="w-full">
	<div
		class={`grid w-full overflow-x-scroll grid-cols-[${trackNameSpace}px_1fr]`}
		onwheel={(event) => {
			event.preventDefault();
			event.stopImmediatePropagation();

			let px = wavesurfer.options.minPxPerSec - event.deltaY;
			if (px < minZoom) px = minZoom - 1;

			wavesurfer.zoom(px);
		}}
	>
		<div></div>
		<div bind:this={wavesurferContainer}></div>
		{#each fileState.transcriptions as transcription (transcription)}
			<span
				role="button"
				tabindex="0"
				class="flex content-center justify-center bg-primary text-primary-foreground"
				ondblclick={(event: MouseEvent) => {
					const element = event.target! as HTMLElement;
					element.contentEditable = 'true';
			}}
				onfocusout={(event: FocusEvent) => {
					const element = event.target! as HTMLElement;
					element.contentEditable = 'false';
					transcription.name = element.textContent ?? '';
				}}
				onkeydown={(event: KeyboardEvent) => {
					const element = event.target! as HTMLElement;

					if (!element.isContentEditable) {
						return;
					}

					if (event.key === 'Escape') {
						element.contentEditable = 'false';
						element.textContent = transcription.name;
					} else if (event.key === 'Enter') {
						element.contentEditable = 'false';
						transcription.name = element.textContent ?? '';
					}
				}}
				>{transcription.name}</span
			>
			<Track {transcription} {duration} />
		{/each}
	</div>
	<Button
		class="w-full rounded-t-none"
		on:click={() => {
			fileState.transcriptions = [
				...fileState.transcriptions,
				{
					id: generateIdFromEntropySize(10),
					name: 'new track',
					captions: [
						{
							start: 0,
							end: duration,
							value: ''
						}
					]
				}
			];
		}}
	>
		+
	</Button>
</section>
