<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { SpecificModeData } from '..';
	import type { ControlRequirements } from '../audio-controls';
	import { onDestroy, onMount } from 'svelte';
	import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.js';

	export let item: SpecificModeData<'waveform'>;
	// eslint-disable-next-line
	export let controls: ControlRequirements = {
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
			container: `#${item.fileId}-waveform`,
			url: `/db/${item.fileId}`,
			height: 'auto'
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());

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
		wavesurfer.destroy();
	});
</script>

<div
	id={`${item.fileId}-waveform`}
	class="waveform w-full flex-1 overflow-x-scroll rounded-tr bg-secondary"
	role="region"
></div>
