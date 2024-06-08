<script lang="ts">
	import type { mode } from '..';
	import * as Select from '$lib/components/ui/select';
	import type { Selected } from 'bits-ui';

	export let computedData: mode.ComputedData<'error-rate'>;
	export let fileState: mode.FileState<'error-rate'>;

	let selectedReference: Selected<unknown>;
	let selectedHypothesis: Selected<unknown>;

	fileState.reference = fileState.transcriptions[0].captions;
	fileState.hypothesis = fileState.transcriptions[1].captions;

	// $: if (selectedReference && selectedHypothesis) {
	// 	for (const transcription of fileState.transcriptions) {
	// 		if (transcription.id === selectedReference.value)  {
	// 			fileState.reference = transcription.captions;
	// 		}
	// 		else if (transcription.id === selectedHypothesis.value)  {
	// 			fileState.hypothesis = transcription.captions;
	// 		}
	// 	}
	//
	// 	console.log(fileState.hypothesis)
	// 	console.log(fileState.reference)
	// }
</script>

<div class="min-w-sm h-fit max-w-4xl flex-1 rounded bg-secondary p-4 text-secondary-foreground">
	<h2>name: {fileState.name}</h2>
	<h2>id: {fileState.id}</h2>
	<div class="flex w-full items-center gap-2">
		<span> Reference track </span>
		<Select.Root bind:selected={selectedReference}>
			<Select.Trigger class="w-[180px]">
				<Select.Value placeholder="Select a track" />
			</Select.Trigger>
			<Select.Content>
				{#each fileState.transcriptions as transcription}
					<Select.Item value={transcription.id}>{transcription.name}</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>
	</div>
	<div class="flex w-full items-center gap-2">
		<span> Hypothesis track </span>
		<Select.Root bind:selected={selectedHypothesis}>
			<Select.Trigger class="w-[180px]">
				<Select.Value placeholder="Select a track" />
			</Select.Trigger>
			<Select.Content>
				{#each fileState.transcriptions as transcription}
					<Select.Item value={transcription.id}>{transcription.name}</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>
	</div>
	{#if computedData !== null}
		blahhh
	{:else}
		<h2>This file has no ground truth</h2>
	{/if}
</div>
