<script lang="ts">
	import { LOCALE } from '$lib/time';
	import XIcon from 'lucide-svelte/icons/x';
	import type { mode } from '..';
	import { Button } from '$lib/components/ui/button';
	import { formatHumanSensibleFileSize } from '$lib/files/size';

	export let computedData: mode.ComputedData<'simple-info'>;
	export let fileState: mode.FileState<'simple-info'>;

	export let onRemoveFile: () => void = () => {};

	const display = (value: number | null, unit: string, decimals = 2) =>
		value === null ? 'N/A' : `${value.toFixed(decimals)} ${unit}`;

	$: displayData = [
		{ label: 'Duration', value: display(computedData.duration, 'seconds') },
		{ label: 'File size', value: formatHumanSensibleFileSize(computedData.fileSize) },
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

<h1 class="overflow-hidden text-ellipsis text-xl font-bold">{fileState.name}</h1>
<p class="overflow-hidden text-ellipsis text-xs text-muted-foreground">{fileState.id}</p>

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

	<Button class="mx-auto mt-4 w-fit" variant="destructive" on:click={onRemoveFile}>
		<XIcon></XIcon>
	</Button>
</div>
