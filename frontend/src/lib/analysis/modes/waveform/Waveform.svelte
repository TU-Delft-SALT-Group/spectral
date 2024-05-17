<script lang="ts" context="module">
	let selected: WaveSurfer | null = null;
</script>

<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { SpecificModeData } from '..';
	import type { WaveColor } from '.';
	import WaveformSingle from './WaveformSingle.svelte';

	export let data: SpecificModeData<'waveform'>[];

	const selectedColor: WaveColor = {
		wave: '#aaaaaa',
		progress: '#ffffff'
	};

	const deselectedColor: WaveColor = {
		wave: '#444444',
		progress: '#999999'
	};

	function interaction(wavesurfer: WaveSurfer) {
		selected?.setOptions({
			waveColor: deselectedColor.wave,
			progressColor: deselectedColor.progress
		});

		wavesurfer.setOptions({
			waveColor: selectedColor.wave,
			progressColor: selectedColor.progress
		});

		selected = wavesurfer;
	}

	function keybinds(e: KeyboardEvent) {
		switch (e.key) {
			case ' ':
				e.preventDefault();
				selected?.playPause();
				break;
			case 'Escape':
				selected?.setOptions({
					waveColor: deselectedColor.wave,
					progressColor: deselectedColor.progress
				});

				selected = null;
				break;
		}
	}
</script>

<section class="flex h-full w-full flex-col pr-20">
	{#each data as item}
		<WaveformSingle {item} onInteract={interaction} color={deselectedColor}></WaveformSingle>
	{/each}
</section>

<svelte:window on:keydown={keybinds} />
