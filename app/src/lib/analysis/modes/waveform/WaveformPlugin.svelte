<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js';
	import type { mode } from '..';
	import type { Frame } from '$lib/analysis/kernel/framing';
	import HoverPlugin from 'wavesurfer.js/dist/plugins/hover.js';
	import { numberToTime } from '$lib/components/audio-controls';

	export let computedData: mode.ComputedData<'waveform'>;
	export let fileState: mode.FileState<'waveform'>;
	let element: HTMLElement;

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
	export let width: number;

	let wavesurfer: WaveSurfer;
	let regions: RegionsPlugin;
	let timeline: TimelinePlugin;
	let hover: HoverPlugin;
	let minZoom: number;

	$: if (width) {
		minZoom = width / duration;
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
			width,
			backend: 'WebAudio'
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());

		timeline = wavesurfer.registerPlugin(
			TimelinePlugin.create({
				timeInterval: 0.1,
				primaryLabelInterval: 1,
				secondaryLabelInterval: 0.5
			})
		);

		hover = wavesurfer.registerPlugin(
			HoverPlugin.create({
				formatTimeCallback: () => ''
			})
		);

		hover.on('hover', (event) => {
			const shadowRoot = element.children[0].shadowRoot;
			if (shadowRoot) {
				const hoverLabel = shadowRoot.querySelector('span[part="hover-label"]');
				if (hoverLabel) {
					hoverLabel.innerHTML =
						numberToTime(wavesurfer.getDuration() * event) + '<br>' + hoverInfo(event);
				}
			}
		});

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

		wavesurfer.on('timeupdate', () => {
			if (wavesurfer.getCurrentTime() > wavesurfer.getDuration())
				wavesurfer.setTime(wavesurfer.getDuration());
			if (regions.getRegions().length == 1) {
				if (wavesurfer.getCurrentTime() > regions.getRegions()[0].end) {
					wavesurfer.pause();
					wavesurfer.setTime(regions.getRegions()[0].end);
				}
			}
			current = wavesurfer.getCurrentTime();
		});

		wavesurfer.on('interaction', () => {
			setAsSelected();
		});

		wavesurfer.on('play', () => {
			if (regions.getRegions().length == 1) {
				wavesurfer.setTime(regions.getRegions()[0].start);
			}
			playing = true;
		});

		wavesurfer.on('pause', () => {
			playing = false;
		});
	});

	onDestroy(() => {
		regions.destroy();
		timeline.destroy();

		wavesurfer.destroy();
	});

	function hoverInfo(time: number) {
		let res = '';
		if (!computedData) return res;
		let pitchPos = Math.min(
			computedData.pitch.length - 1,
			Math.max(0, Math.floor(computedData.pitch.length * time))
		);
		let formantsPos = Math.min(
			computedData.formants.length - 1,
			Math.max(0, Math.floor(computedData.formants.length * time))
		);
		if (pitchPos >= 0) {
			res += 'pitch: ' + computedData.pitch[pitchPos] + '<br>';
		}
		if (formantsPos >= 0) {
			res += 'f1: ' + computedData.formants[formantsPos][0] + '<br>';
			res += 'f2: ' + computedData.formants[formantsPos][1] + '<br>';
		}
		return res;
	}
</script>

<div
	bind:this={element}
	class="waveform w-full flex-1 rounded-tr bg-secondary"
	role="region"
	on:wheel|nonpassive={(event: WheelEvent) => {
		if (!event.ctrlKey) return;

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
