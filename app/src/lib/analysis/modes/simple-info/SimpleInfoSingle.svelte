<script lang="ts">
	import { LOCALE } from '$lib/time';
	import type { mode } from '..';

	export let computedData: mode.ComputedData<'simple-info'>;
	export let fileState: mode.FileState<'simple-info'>;

	const display = (value: number | null, unit: string, decimals = 2) =>
		value === null ? 'N/A' : `${value.toFixed(decimals)} ${unit}`;

	$: displayData = [
		{ label: 'Duration', value: display(computedData.duration, 'seconds') },
		{ label: 'File size', value: display(computedData.fileSize, 'bytes', 0) }, // TODO: Display a logical unit of size
		{ label: 'Average pitch', value: display(computedData.averagePitch, 'Hz') },
		{ label: 'Date created', value: `${computedData.fileCreationDate.toLocaleString(LOCALE)}` }
	];

	function getFrameData(frame: typeof computedData.frame) {
		if (frame === null) {
			return null;
		}

		const { duration, pitch, f1, f2 } = frame;

		return [
			{ label: 'Frame Duration', value: display(duration, 'seconds') },
			{ label: 'Frame Pitch', value: display(pitch, 'pitch') },
			{ label: 'Frame F1 formant', value: display(f1, 'Hz') },
			{ label: 'Frame F2 formant', value: display(f2, 'Hz') }
		];
	}

	$: frameData = getFrameData(computedData.frame);
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
