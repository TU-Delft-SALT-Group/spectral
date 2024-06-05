<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import ZoomPlugin from 'wavesurfer.js/dist/plugins/zoom.esm.js';
	import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js';
	import type { mode } from '..';
	import used from '$lib/utils';
	import type { Frame } from '$lib/analysis/kernel/framing';

	export let computedData: mode.ComputedData<'waveform'>;
	export let fileState: mode.FileState<'waveform'>;
	let element: HTMLElement;

	used(computedData);

	export const controls: ControlRequirements = {
		setSpeed(speed: number) {
			wavesurfer.setPlaybackRate(speed);
		},
		clearRegions() {
			if (regions.getRegions().length === 0) return false;

			// regions.clearRegions();
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
	export let width: number = 100;

	let wavesurfer: WaveSurfer;
	let regions: RegionsPlugin;
	let zoom: ZoomPlugin;
	let timeline: TimelinePlugin;

	$: if (width) {
		wavesurfer?.setOptions({
			width
		});
	}

	onMount(() => {
		if (element === undefined) return;

		wavesurfer = new WaveSurfer({
			container: element,
			url: `/db/file/${fileState.id}`,
			height: 300,
			barHeight: 0.9,
			width
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());
		zoom = wavesurfer.registerPlugin(
			ZoomPlugin.create({
				scale: 0.5
			})
		);

		timeline = wavesurfer.registerPlugin(
			TimelinePlugin.create({
				timeInterval: 0.1,
				primaryLabelInterval: 1,
				secondaryLabelInterval: 0.5
			})
		);

		regions.enableDragSelection(
			{
				color: 'rgba(255, 0, 0, 0.1)'
			},
			10
		);

		regions.on('region-created', (region: Region) => {
			// regions.getRegions().forEach((r) => {
			// 	if (r.id === region.id) return;
			// 	r.remove();
			// });

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
				// regions.clearRegions();

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
		zoom.destroy();
		timeline.destroy();

		wavesurfer.destroy();
	});
</script>

<div bind:this={element} class="waveform w-full flex-1 rounded-tr bg-secondary" role="region"></div>
