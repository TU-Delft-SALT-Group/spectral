<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import type { mode } from '..';
	import used from '$lib/utils';

	export let computedData: mode.ComputedData<'waveform'>;
	export let fileState: mode.FileState<'waveform'>;

	used(computedData);

	// This is disabled because for some reason it complains that it is not being used
	// when in reality it is bound in the AudioControls.svelte
	// eslint-disable-next-line
	export const controls: ControlRequirements = {
		setSpeed(speed: number) {
			wavesurfer.setPlaybackRate(speed);
		},
		clearRegions() {
			if (regions.getRegions().length === 0) return false;

			regions.clearRegions();
			return true;
		},
		play() {
			wavesurfer.play();
		},
		pause() {
			wavesurfer.pause();
		},
		togglePlay() {
			wavesurfer.playPause();
		},
		seek(amount: number) {
			wavesurfer.skip(amount);
		}
	};
	export let duration: number;
	export let current: number;
	export let setAsSelected: () => void;
	export let playing = false;

	let wavesurfer: WaveSurfer;
	let regions: RegionsPlugin;

	onMount(() => {
		wavesurfer = new WaveSurfer({
			container: `#${fileState.fileId}-waveform`,
			url: `/db/file/${fileState.fileId}`,
			height: 'auto'
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());

		regions.enableDragSelection(
			{
				color: 'rgba(255, 0, 0, 0.1)'
			},
			10
		);

		regions.on('region-created', (region: Region) => {
			regions.getRegions().forEach((r) => {
				if (r.id === region.id) return;
				r.remove();
			});

			setAsSelected();
		});

		wavesurfer.on('decode', () => {
			duration = wavesurfer.getDuration();
			current = wavesurfer.getCurrentTime();
		});

		wavesurfer.on('timeupdate', () => {
			current = wavesurfer.getCurrentTime();
		});

		wavesurfer.on('interaction', () => {
			setAsSelected();
		});

		wavesurfer.on('play', () => {
			playing = true;
		});

		wavesurfer.on('pause', () => {
			playing = false;
		});
	});

	onDestroy(() => {
		regions.destroy();

		wavesurfer.destroy();
	});
</script>

<div
	id={`${fileState.fileId}-waveform`}
	class="waveform w-full flex-1 overflow-x-scroll rounded-tr bg-secondary"
	role="region"
></div>
