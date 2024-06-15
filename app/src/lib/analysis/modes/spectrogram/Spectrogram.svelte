<script lang="ts">
	import type { ModeComponentProps } from '..';
	import AudioControls from '$lib/components/audio-controls/AudioControls.svelte';
	import { used } from '$lib/utils';

	export let fileStates: ModeComponentProps<'spectrogram'>['fileStates'];
	export let modeState: ModeComponentProps<'spectrogram'>['modeState'];
	export let getComputedData: ModeComponentProps<'spectrogram'>['getComputedData'];

	used(modeState);
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileStates as fileState (fileState.id)}
		<AudioControls
			visualization="spectrogram"
			computedData={getComputedData(fileState)}
			{fileState}
		/>
	{/each}
</section>
