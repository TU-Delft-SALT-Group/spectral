<script lang="ts">
	import type { ModeComponentProps } from '..';
	import AudioControls from '$lib/components/audio-controls/AudioControls.svelte';
	import { used } from '$lib/utils';

	// Example for later on how to do this in Svelte 5
	let {
		fileStates = $bindable(),
		modeState = $bindable(),
		getComputedData
	}: ModeComponentProps<'waveform'> = $props();

	used(modeState);
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileStates as fileState, i (fileState.id)}
		<AudioControls
			visualization="waveform"
			bind:fileState={fileStates[i]}
			computedData={getComputedData(fileState)}
		/>
	{/each}
</section>
