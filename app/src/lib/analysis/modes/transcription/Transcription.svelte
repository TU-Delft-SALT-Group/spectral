<script lang="ts">
	import { used } from '$lib/utils';
	import type { ModeComponentProps } from '..';
	import TranscriptionPlugin from './TranscriptionPlugin.svelte';

	let {
		fileStates = $bindable(),
		modeState = $bindable(),
		getComputedData
	}: ModeComponentProps<'transcription'> = $props();

	used(modeState);
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileStates as fileState, i (fileState.id)}
		<TranscriptionPlugin bind:fileState={fileStates[i]} computedData={getComputedData(fileState)} />
	{/each}
</section>
