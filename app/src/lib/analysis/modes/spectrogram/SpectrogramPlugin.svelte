<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
	import SpectrogramPlugin from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
	import type { Frame } from '$lib/analysis/kernel/framing';
	import type { mode } from '..';
	import { used } from '$lib/utils';

	export let computedData: mode.ComputedData<'spectrogram'>;
	export let fileState: mode.FileState<'spectrogram'>;
	let element: HTMLElement;

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
	export let width: number = 100;

	let minZoom: number;
	let wavesurfer: WaveSurfer;
	let regions: RegionsPlugin;
	let spectrogram: SpectrogramPlugin;
	let timeline: TimelinePlugin;
	let spectrogramCanvas: HTMLCanvasElement;

	$: if (width) {
		minZoom = width / duration;
		wavesurfer?.setOptions({
			width
		});
	}

	onMount(async () => {
		wavesurfer = new WaveSurfer({
			container: element,
			url: `/db/file/${fileState.id}`,
			height: 0,
			width,
			backend: 'WebAudio',
			autoScroll: true,
			autoCenter: true
		});

		element.id = 'spectrogram' + fileState.id; // set id to later use for drawing formants

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());
		spectrogram = wavesurfer.registerPlugin(
			Spectrogram.create({
				labels: true,
				labelsColor: 'black'
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

		spectrogram.once('ready', () => {
			spectrogramCanvas = element.children[0].shadowRoot?.children[1].children[0].children[4]
				.children[1] as HTMLCanvasElement; // get to the correct canvas to draw on

			spectrogramCanvas.style.zIndex = '-20';
		});

		wavesurfer.on('interaction', () => {
			setAsSelected();
		});

		wavesurfer.on('decode', () => {
			duration = wavesurfer.getDuration();
			current = wavesurfer.getCurrentTime();
			minZoom = width / duration;

			if (fileState.frame !== null) {
				regions.clearRegions();

				regions.addRegion({
					start: fileState.frame.startIndex / wavesurfer.options.sampleRate,
					end: fileState.frame.endIndex / wavesurfer.options.sampleRate,
					color: 'rgba(255, 0, 0, 0.1)'
				});
			}
		});

		wavesurfer.on('play', () => {
			let ctx = spectrogramCanvas.getContext('2d');

			// we do this because the property exists in spectrogram but isnt' available to us
			const maxFrequency = (spectrogram as unknown as { frequencyMax: number }).frequencyMax;
			const colours = ['red', 'orange', 'yellow', 'green', 'blue'];

			if (ctx === null || computedData === null || computedData.formants === null) {
				return;
			}

			for (let i = 0; i < computedData.formants.length; i++) {
				// loop over all formant groups
				computedData.formants[i].forEach((formant, j) => {
					// loop over all formants
					if (formant === null || computedData.formants === null) {
						return;
					}

					ctx.beginPath();
					ctx.arc(
						(i / computedData.formants.length) * spectrogramCanvas.width, // x position based on group index
						(1 - formant / maxFrequency) * spectrogramCanvas.height,
						2,
						0,
						2 * Math.PI
					);
					ctx.strokeStyle = colours[j];
					ctx.stroke();
				});
			}
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
		timeline.destroy();
		wavesurfer.destroy();
	});
</script>

<div
	bind:this={element}
	class="waveform w-full flex-1 overflow-x-scroll rounded-tr bg-secondary"
	role="region"
	on:wheel|nonpassive={(event) => {
		event.preventDefault();
		event.stopImmediatePropagation();

		let oldPx = wavesurfer.options.minPxPerSec;
		let px = wavesurfer.options.minPxPerSec - event.deltaY;
		if (px < minZoom) px = minZoom - 1;

		// most of this was copied from
		// https://github.com/katspaugh/wavesurfer.js/blob/main/src/plugins/zoom.ts
		const container = wavesurfer.getWrapper().parentElement!;
		const x = event.clientX - element.getBoundingClientRect().left;
		const scrollX = wavesurfer.getScroll();
		const pointerTime = (scrollX + x) / oldPx;
		const newLeftSec = (width / px) * (x / width);

		if (px * duration < width) {
			wavesurfer.zoom(width / duration);
			container.scrollLeft = 0;
		} else {
			wavesurfer.zoom(px);
			container.scrollLeft = (pointerTime - newLeftSec) * px;
		}
	}}
></div>
