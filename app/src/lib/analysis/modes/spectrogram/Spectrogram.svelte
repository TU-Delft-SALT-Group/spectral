<script lang="ts">
	import type { ModeComponentProps } from '..';
	import AudioControls from '$lib/components/audio-controls/AudioControls.svelte';

	export let fileData: ModeComponentProps<'spectrogram'>['fileData'];
	export let modeState: ModeComponentProps<'spectrogram'>['modeState'];
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileData as { computedData, fileState } (fileState.id)}
		<AudioControls visualization="spectrogram" {computedData} {fileState} width={modeState.width} />
	{/each}
</section>
