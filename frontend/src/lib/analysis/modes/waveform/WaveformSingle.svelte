<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import type { SpecificModeData } from '..';
	import WaveSurfer from 'wavesurfer.js';
	import type { WaveColor } from '.';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.esm.js';

	export let onInteract: (w: WaveSurfer) => void;
	export let item: SpecificModeData<'waveform'>;
	export let color: WaveColor;
	let wavesurfer: WaveSurfer;
	let regions: RegionsPlugin;

	onMount(() => {
		wavesurfer = new WaveSurfer({
			container: `#${item.fileId}-waveform`,
			url: `/db/${item.fileId}`,
			waveColor: color.wave,
			progressColor: color.progress,
			height: 'auto'
		});

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());

		regions.enableDragSelection({
			color: 'rgba(255, 0, 0, 0.1)'
		});

		regions.on('region-created', (region: Region) => {
			regions.getRegions().forEach((r) => {
				if (r.id === region.id) return;
				r.remove();
			});
		});

		wavesurfer.on('interaction', () => {
			onInteract(wavesurfer);
		});
	});

	onDestroy(() => {
		regions.destroy();

		wavesurfer.destroy();
	});
</script>

<div id={`${item.fileId}-waveform`} class="flex-1 overflow-x-scroll" role="region"></div>
