<script lang="ts">
	import { onMount } from 'svelte';
	import type { SpecificModeData } from '..';
	import WaveSurfer from 'wavesurfer.js';
	import type { WaveColor } from '.';

	export let onInteract: (w: WaveSurfer) => void;
	export let item: SpecificModeData<'waveform'>;
	export let color: WaveColor;

	onMount(() => {
		let wavesurfer = new WaveSurfer({
			container: `#${item.fileId}-waveform`,
			url: `/db/${item.fileId}`,
			waveColor: color.wave,
			progressColor: color.progress
		});

		wavesurfer.on('interaction', () => {
			onInteract(wavesurfer);
		});
	});
</script>

<div id={`${item.fileId}-waveform`}></div>
