<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import type { mode } from '..';
	import used from '$lib/utils';
	import type { Frame } from '$lib/analysis/kernel/framing';

	export let computedData: mode.ComputedData<'waveform'>;
	export let fileState: mode.FileState<'waveform'>;

	used(computedData);

	export const controls: ControlRequirements = {
		setSpeed(speed: number) {
			wavesurfer.setPlaybackRate(speed);
		},
		clearRegions() {
			if (regions.getRegions().length === 0) return false;

			regions.clearRegions();
			fileState.frame = null;
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
			container: `#${fileState.id}-waveform`,
			url: `/db/file/${fileState.id}`,
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

			let frame: Frame = {
				startIndex: Math.floor(region.start * wavesurfer.options.sampleRate),
				endIndex: Math.ceil(region.end * wavesurfer.options.sampleRate)
			};

			fileState.frame = frame;
			setAsSelected();
		});

		wavesurfer.on('decode', () => {
			duration = wavesurfer.getDuration();
			current = wavesurfer.getCurrentTime();

			if (fileState.frame !== null) {
				regions.clearRegions();

				regions.addRegion({
					start: fileState.frame.startIndex / wavesurfer.options.sampleRate,
					end: fileState.frame.endIndex / wavesurfer.options.sampleRate,
					color: 'rgba(255, 0, 0, 0.1)'
				});
			}
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
	id={`${fileState.id}-waveform`}
	class="waveform w-full flex-1 overflow-x-scroll rounded-tr bg-secondary"
	role="region"
></div>
