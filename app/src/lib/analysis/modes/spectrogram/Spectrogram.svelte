<script lang="ts">
	import AudioControls from '$lib/components/audio-controls/AudioControls.svelte';
	import type { SpecificModeData } from '..';

	export let data: SpecificModeData<'spectrogram'>[];
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each data as item}
		<AudioControls visualization="spectrogram" {item} />
	{/each}
</section>
