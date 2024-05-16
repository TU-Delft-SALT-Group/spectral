<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { SpecificModeData } from '..';
	import { onMount } from 'svelte';

	export let data: SpecificModeData<'waveform'>[];
	let lastSelected: WaveSurfer | null = null;

	type waveColour = {
		wave: string;
		progress: string;
	};

	const selected: waveColour = {
		wave: '#aaaaaa',
		progress: '#ffffff'
	};

	const other: waveColour = {
		wave: '#444444',
		progress: '#999999'
	};

	function keybinds(e: KeyboardEvent) {
		switch (e.key) {
			case ' ':
				if (lastSelected === null) return;
				lastSelected.playPause();
				break;
			case 'Escape':
				lastSelected?.setOptions({
					waveColor: other.wave,
					progressColor: other.progress
				});

				lastSelected = null;
				break;
		}
	}

	onMount(() =>
		data.forEach((item) => {
			let wavesurfer = new WaveSurfer({
				container: `#${item.fileId}-waveform`,
				url: `/db/${item.fileId}`,
				waveColor: other.wave,
				progressColor: other.progress
			});

			wavesurfer.on('interaction', () => {
				if (lastSelected) {
					lastSelected.setOptions({
						progressColor: other.progress,
						waveColor: other.wave
					});
				}

				lastSelected = wavesurfer;

				lastSelected.setOptions({
					progressColor: selected.progress,
					waveColor: selected.wave
				});
			});
		})
	);
</script>

<section class="w-full pr-20">
	{#each data as item}
		<div id={`${item.fileId}-waveform`}></div>
	{/each}
</section>

<svelte:window on:keydown={keybinds} />
