<script lang="ts">
	import type { mode } from '..';

	export let computedData: mode.ComputedData<'simple-info'>;
	export let fileState: mode.FileState<'simple-info'>;

	$: displayData = [
		{ label: 'Duration', value: `${computedData.duration.toFixed(2)} seconds` },
		{ label: 'File size', value: `${computedData.fileSize} bytes` },
		{ label: 'Average pitch', value: `${computedData.averagePitch.toFixed(2)} Hz` },
		{ label: 'Date created', value: `${computedData.fileCreationDate.toLocaleString('en-US')}` }
	];

	$: frameData = computedData.frameData
		? [
				{ label: 'Frame Duration', value: `${computedData.frameData.duration.toFixed(2)} seconds` },
				{ label: 'Frame Pitch', value: `${computedData.frameData.pitch} pitch` },
				{ label: 'Frame F1 formant', value: `${computedData.frameData.f1} Hz` },
				{ label: 'Frame F2 formant', value: `${computedData.frameData.f2} Hz` }
			]
		: null;
</script>

<h1 class="text-xl font-bold">{fileState.fileId}</h1>

<div class="flex flex-col flex-wrap opacity-80">
	{#each displayData as { label, value }}
		<section class="flex items-baseline">
			<h2 class="mr-2 text-lg">{label}:</h2>
			<span class="h-full">
				{value}
			</span>
		</section>
	{/each}

	{#if frameData}
		{#each frameData as { label, value }}
			<section class="flex items-baseline opacity-80">
				<h2 class="mr-2 text-lg">{label}:</h2>
				<span class="h-full">
					{value}
				</span>
			</section>
		{/each}
	{:else}
		<div class="pt-4 opacity-50">Select a frame in the waveform mode to view its information</div>
	{/if}
</div>
