<script lang="ts">
	import type { SpecificModeData } from '..';

	// eslint-disable-next-line
	export let data: SpecificModeData<'simple-info'>;

	$: displayData = [
		{ label: 'Duration', value: `${data.duration.toFixed(2)} seconds` },
		{ label: 'File size', value: `${data.fileSize} bytes` },
		{ label: 'Average pitch', value: `${data.averagePitch.toFixed(2)} Hz` },
		{ label: 'Date created', value: `${data.fileCreationDate.toLocaleString('en-US')}` }
	];

	$: frameData = data.frame
		? [
				{ label: 'Frame Duration', value: `${data.frame.duration.toFixed(2)} seconds` },
				{ label: 'Frame Pitch', value: `${data.frame.pitch} pitch` },
				{ label: 'Frame F1 formant', value: `${data.frame.f1} Hz` },
				{ label: 'Frame F2 formant', value: `${data.frame.f2} Hz` }
			]
		: null;
</script>

<h1 class="text-xl font-bold">{data.fileId}</h1>

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
		{#each displayData as { label, value }}
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
