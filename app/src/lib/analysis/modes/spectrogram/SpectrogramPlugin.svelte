<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
	import SpectrogramPlugin from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
	import type { mode } from '..';
	import used from '$lib/utils';

	export let computedData: mode.ComputedData<'spectrogram'>;
	export let fileState: mode.FileState<'spectrogram'>;

	used(computedData);

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
	let spectrogram: SpectrogramPlugin;

	onMount(() => {
		wavesurfer = new WaveSurfer({
			container: `#${fileState.fileId}-spectrogram`,
			url: `/db/file/${fileState.fileId}`,
			height: 0
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());
		spectrogram = wavesurfer.registerPlugin(
			Spectrogram.create({
				labels: true,
				labelsColor: 'black',
				height: 232
			})
		);

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

		wavesurfer.on('interaction', () => {
			setAsSelected();
		});

		wavesurfer.on('decode', () => {
			duration = wavesurfer.getDuration();
			current = wavesurfer.getCurrentTime();
		});

		wavesurfer.on('timeupdate', () => {
			current = wavesurfer.getCurrentTime();
		});

		wavesurfer.on('play', () => {
			playing = true;
		});

		wavesurfer.on('pause', () => {
			playing = false;
		});
	});

	onDestroy(() => {
		spectrogram.destroy();
		regions.destroy();
	});
</script>

<div
	id={`${fileState.fileId}-spectrogram`}
	class="waveform w-full flex-1 overflow-x-scroll rounded-tr bg-secondary"
	role="region"
></div>
