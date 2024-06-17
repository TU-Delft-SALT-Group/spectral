<script lang="ts">
	import type { mode } from '..';
	import * as Select from '$lib/components/ui/select';
	import type { Selected } from 'bits-ui';
	import ErrorDiff from './ErrorDiff.svelte';
	import { Separator } from '$lib/components/ui/separator';

	export let computedData: mode.ComputedData<'error-rate'>;
	export let fileState: mode.FileState<'error-rate'>;

	let selectedReference: Selected<mode.FileState<'error-rate'>['reference'] | null> = {
		value: fileState.reference,
		label: fileState.reference?.name
	};

	let selectedHypothesis: Selected<mode.FileState<'error-rate'>['hypothesis'] | null> = {
		value: fileState.hypothesis,
		label: fileState.hypothesis?.name
	};

	$: if (selectedReference && selectedHypothesis) {
		fileState.reference = selectedReference.value;
		fileState.hypothesis = selectedHypothesis.value;
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
					<Select.Item value={transcription}>{transcription.name}</Select.Item>
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
					<Select.Item value={transcription}>{transcription.name}</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>
	</div>

	{#if computedData !== null}
		<Separator />

		<h3 class="pt-4 text-xl">Word Error Rate</h3>

		<div class="flex flex-wrap gap-3 font-mono">
			<span>WER: {(computedData.wordLevel.wer * 100).toFixed(2) + '%'}</span>
			<span>MER: {(computedData.wordLevel.mer * 100).toFixed(2) + '%'}</span>
			<span>WIL: {(computedData.wordLevel.wil * 100).toFixed(2) + '%'}</span>
			<span>WIP: {(computedData.wordLevel.wip * 100).toFixed(2) + '%'}</span>
		</div>
		<div class="flex flex-wrap gap-3 font-mono">
			<span>BERT: {computedData.wordLevel.bert.toFixed(2)}</span>
			<span>Jaro Winkler: {computedData.wordLevel.jaroWinkler.toFixed(2)}</span>
		</div>
		<ErrorDiff common={computedData.wordLevel} joinString=" " />

		<Separator />

		<h3 class="pt-4 text-xl">Character Error Rate</h3>

		<span class="font-mono">CER: {(computedData.characterLevel.cer * 100).toFixed(2) + '%'}</span>
		<ErrorDiff common={computedData.characterLevel} joinString="" />
	{:else}
		<h2 class="text-muted-foreground">This file has no ground truth.</h2>
	{/if}
</div>
