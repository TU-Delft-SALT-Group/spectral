<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { SpecificModeData } from '..';
	import { onMount } from 'svelte';

	export let data: SpecificModeData<'waveform'>[];

	let lastSelected: WaveSurfer | null = null;

	function keybinds(e: KeyboardEvent) {
		switch (e.key) {
			case ' ':
				if (lastSelected === null) return;
				lastSelected.playPause();
				break;
		}
	}

	onMount(() =>
		data.forEach((item) => {
			let wavesurfer = new WaveSurfer({
				container: `#${item.fileId}-waveform`,
				url: `/db/${item.fileId}`
			});

			wavesurfer.on('interaction', () => {
				lastSelected = wavesurfer;
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
