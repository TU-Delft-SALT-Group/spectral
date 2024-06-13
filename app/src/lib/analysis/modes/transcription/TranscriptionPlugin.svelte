<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { mode } from '..';
	import { onDestroy, onMount } from 'svelte';
	import { used } from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import * as Select from '$lib/components/ui/select';
	import { generateIdFromEntropySize } from 'lucia';
	import Track from './Track.svelte';
	import { logger } from '$lib/logger';
	import { doubleClick, focusOut, keyDown } from '.';

	export let computedData: mode.ComputedData<'transcription'>;
	export let fileState: mode.FileState<'transcription'>;
	used(computedData);

	let wavesurferContainer: HTMLElement;
	let wavesurfer: WaveSurfer;
	let width: number;
	let minZoom: number;
	let duration: number;
	let transcriptionType: { label?: string; value: string } = { value: 'empty' };
	const models: string[] = ['whisper', 'deepgram', 'allosaurus'];

	function transcriptionTypeChanger(newSelection: { label?: string; value: string } | undefined) {
		if (!newSelection) return;

		transcriptionType.value = newSelection.value;
	}

	const trackNameSpace = 100;

	onMount(() => {
		wavesurfer = WaveSurfer.create({
			container: wavesurferContainer,
			url: `/db/file/${fileState.id}`,
			height: 300,
			backend: 'WebAudio'
		});

		let wrapper = wavesurfer.getWrapper();

		wrapper.style.overflow = 'visible';
		wrapper.style.overflowX = 'visible';

		wavesurfer.once('decode', () => {
			duration = wavesurfer.getDuration();
			minZoom = (width - trackNameSpace) / duration;

			wavesurfer.setOptions({
				width: minZoom * duration
			});
		});

		wavesurfer.on('zoom', (px) => {
			wavesurfer.setOptions({
				width: duration * px
			});
		});
	});

	onDestroy(() => {
		wavesurfer.destroy();
	});

	async function exportTextGrid() {
		let text;
		try {
			const response = await fetch('/api/transcription/textgrid', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ transcriptions: fileState.transcriptions })
			});

			if (!response.ok) {
				throw new Error('Failed to fetch the TextGrid file');
			}

			text = JSON.parse(await response.text());
			if (text === null) {
				throw new Error('No tracks were given');
			}
		} catch (error) {
			logger.error(error);
			return;
		}

		const blob = new Blob([text], { type: 'text/plain' });
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement('a');

		a.style.display = 'none';
		a.href = url;
		a.download = 'transcription.TextGrid';

		document.body.appendChild(a);
		a.click();

		window.URL.revokeObjectURL(url);
		document.body.removeChild(a);
	}

	async function addTrack() {
		if (transcriptionType.value === 'empty') {
			fileState.transcriptions = [
				...fileState.transcriptions,
				{
					id: generateIdFromEntropySize(10),
					name: 'new track',
					captions: [
						{
							start: 0,
							end: duration,
							value: ''
						}
					]
				}
			];
		} else if (models.includes(transcriptionType.value)) {
			let response = await (
				await fetch(`/api/transcription/${transcriptionType.value}/${fileState.id}`)
			).json();
			logger.trace(response);
			fileState.transcriptions = [
				...fileState.transcriptions,
				{
					id: generateIdFromEntropySize(10),
					name: transcriptionType.value,
					captions: response
				}
			];
		} else {
			logger.error('no match for: ' + transcriptionType.value);
		}
	}
</script>

<section bind:clientWidth={width} class="w-full">
	<div
		class={`grid w-full overflow-x-scroll`}
		style={`grid-template-columns: ${trackNameSpace}px 1fr;`}
		onwheel={(event) => {
			event.preventDefault();
			event.stopImmediatePropagation();

			let px = wavesurfer.options.minPxPerSec - event.deltaY;
			if (px < minZoom) px = minZoom - 1;

			wavesurfer.zoom(px);
		}}
	>
		<div></div>
		<div bind:this={wavesurferContainer}></div>
		{#each fileState.transcriptions as transcription}
			<span
				role="button"
				tabindex="0"
				class="flex content-center justify-center bg-primary text-primary-foreground"
				ondblclick={doubleClick}
				onfocusout={(event: FocusEvent) => focusOut(event, transcription)}
				onkeydown={(event: KeyboardEvent) => keyDown(event, transcription)}
				>{transcription.name}</span
			>
			<Track captions={transcription.captions} {duration} />
		{/each}
	</div>
	<div class="flex w-full">
		<Select.Root selected={transcriptionType} onSelectedChange={transcriptionTypeChanger}>
			<Select.Trigger class="m-0 h-full w-1/6">
				{transcriptionType.value}
			</Select.Trigger>
			<Select.Content>
				<Select.Item value="empty">empty</Select.Item>
				{#each models as model}
					<Select.Item value={model}>{model}</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>
		<Button class="w-2/3 rounded-t-none" on:click={addTrack}>+</Button>
		<Button class="m-0 h-full w-1/6" on:click={exportTextGrid}>Get Textgrid</Button>
	</div>
</section>
