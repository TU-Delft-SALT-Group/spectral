<script lang="ts">
	import type { ModeComponentProps } from '..';
	import AudioControls from '$lib/components/audio-controls/AudioControls.svelte';

	export let fileData: ModeComponentProps<'waveform'>['fileData'];
	export let modeState: ModeComponentProps<'waveform'>['modeState'];
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileData as { fileState, computedData } (fileState.id)}
		<AudioControls visualization="waveform" {fileState} {computedData} width={modeState.width} />
	{/each}
</section>
