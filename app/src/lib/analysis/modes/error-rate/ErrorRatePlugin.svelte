<script lang="ts">
	import type { mode } from '..';
	import * as Select from '$lib/components/ui/select';
	import type { Selected } from 'bits-ui';
	import ErrorDiff from './ErrorDiff.svelte';
	import { Separator } from '$lib/components/ui/separator';

	export let computedData: mode.ComputedData<'error-rate'>;
	export let fileState: mode.FileState<'error-rate'>;

	let selectedReference: Selected<unknown> = {
		value: fileState.reference?.id,
		label: fileState.reference?.name
	};
	let selectedHypothesis: Selected<unknown> = {
		value: fileState.hypothesis?.id,
		label: fileState.hypothesis?.name
	};

	$: console.log(selectedReference, selectedHypothesis);

	$: if (selectedReference && selectedHypothesis) {
		for (const transcription of fileState.transcriptions) {
			if (transcription.id === selectedReference.value) {
				fileState.reference = {
					...transcription
				};
			}
			if (transcription.id === selectedHypothesis.value) {
				fileState.hypothesis = {
					...transcription
				};
			}
		}
	}
</script>

<div
	class="min-w-sm flex h-fit max-w-4xl flex-1 flex-col gap-3 overflow-x-hidden rounded bg-secondary/50 p-4 text-secondary-foreground"
>
	<div>
		<h2 class="text-2xl font-bold">{fileState.name}</h2>
		<div class="text-sm text-muted-foreground">{fileState.id}</div>
	</div>
	<div class="grid w-full grid-cols-[auto,1fr] items-center gap-1">
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
		<Separator />
		<h3 class="pt-4 text-xl">Word level</h3>
		<div class="flex flex-wrap gap-3 font-mono">
			<span>wer: {(computedData.wordLevel.wer * 100).toFixed(2) + '%'}</span>
			<span>mer: {(computedData.wordLevel.mer * 100).toFixed(2) + '%'}</span>
			<span>wil: {(computedData.wordLevel.wil * 100).toFixed(2) + '%'}</span>
			<span>wip: {(computedData.wordLevel.wip * 100).toFixed(2) + '%'}</span>
		</div>
		<ErrorDiff common={computedData.wordLevel} joinString=" " />

		<Separator />
		<h3 class="pt-4 text-xl">Character level</h3>

		<span class="font-mono">cer: {(computedData.characterLevel.cer * 100).toFixed(2) + '%'}</span>
		<ErrorDiff common={computedData.characterLevel} joinString="" />
	{:else}
		<h2 class="text-muted-foreground">This file has no ground truth.</h2>
	{/if}
</div>
