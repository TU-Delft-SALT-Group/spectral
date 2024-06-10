<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import { onDestroy, onMount } from 'svelte';
	import { type ControlRequirements } from '$lib/components/audio-controls';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import Spectrogram from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
	import SpectrogramPlugin from 'wavesurfer.js/dist/plugins/spectrogram.esm.js';
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
	let spectrogram: SpectrogramPlugin;

	onMount(async () => {
		wavesurfer = new WaveSurfer({
			container: element,
			url: `/db/file/${fileState.id}`,
			height: 0,
			width,
			backend: 'WebAudio'
		});

		element.id = 'spectrogram' + fileState.id; // set id to later use for drawing formants

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
			let canvas = document.getElementById('spectrogram' + fileState.id)?.children[0].shadowRoot
				?.children[1].children[0].children[4].children[1] as HTMLCanvasElement; // get to the correct canvas to draw on
			const ctx = canvas.getContext('2d');
			if (ctx !== null && computedData !== null && computedData.formants !== null) {
				for (let i = 0; i < computedData.formants.length; i++) {
					// loop over all formant groups
					for (let formant of computedData.formants[i]) {
						// loop over all formants
						if (formant === null) continue;
						ctx.beginPath();
						ctx.arc(
							(i / computedData.formants.length) * canvas.width, // x position based on group index
							(formant / 4000) * canvas.height, // y position based on height, divided by 4k, but maybe this is not always 4k
							5,
							0,
							2 * Math.PI
						);
						ctx.strokeStyle = 'red';
						ctx.stroke();
					}
				}
			}

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
	bind:this={element}
	class="waveform w-full flex-1 overflow-x-scroll rounded-tr bg-secondary"
	role="region"
></div>
