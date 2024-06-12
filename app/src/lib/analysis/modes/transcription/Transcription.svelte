<script lang="ts">
	import { used } from '$lib/utils';
	import type { ModeComponentProps } from '..';
	import TranscriptionPlugin from './TranscriptionPlugin.svelte';

	export let fileData: ModeComponentProps<'transcription'>['fileData'];
	export let modeState: ModeComponentProps<'transcription'>['modeState'];

	used(modeState);
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileData as { computedData, fileState } (fileState.id)}
		<TranscriptionPlugin {fileState} {computedData} />
	{/each}
</section>
