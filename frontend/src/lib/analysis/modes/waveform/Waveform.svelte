<script lang="ts">
	import type { SpecificModeData } from '..';
	import WaveformSingle from './WaveformSingle.svelte';

	export let data: SpecificModeData<'waveform'>[];
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each data as item}
		<WaveformSingle {item}></WaveformSingle>
	{/each}
</section>
