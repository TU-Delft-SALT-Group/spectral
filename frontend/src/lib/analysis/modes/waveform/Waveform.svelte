<script lang="ts">
	import type { SpecificModeData } from '..';
	import AudioControls from '../audio-controls/AudioControls.svelte';

	export let data: SpecificModeData<'waveform'>[];
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each data as item}
		<AudioControls visualization="waveform" {item} />
	{/each}
</section>
