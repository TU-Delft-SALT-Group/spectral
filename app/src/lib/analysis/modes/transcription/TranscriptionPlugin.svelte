<script lang="ts">
	import WaveSurfer from 'wavesurfer.js';
	import type { mode } from '..';
	import { onDestroy, onMount } from 'svelte';
	import { used } from '$lib/utils';
	import { Button } from '$lib/components/ui/button';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import * as Select from '$lib/components/ui/select';
	import { generateIdFromEntropySize } from 'lucia';
	import Track from './Track.svelte';
	import { logger } from '$lib/logger';
	import { doubleClick, focusOut, keyDown } from '.';
	import { numberToTime } from '$lib/components/audio-controls';
	import { Separator } from '$lib/components/ui/separator';
	import { Download, PauseIcon, PlayIcon, TrashIcon } from 'lucide-svelte';
	import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js';
	import HoverPlugin from 'wavesurfer.js/dist/plugins/hover.esm.js';
	import type { Action } from 'svelte/action';
	import RegionsPlugin, { type Region } from 'wavesurfer.js/dist/plugins/regions.js';
	import type { Frame } from '$lib/analysis/kernel/framing';

	let {
		fileState = $bindable(),
		computedData
	}: {
		computedData: mode.ComputedData<'transcription'>;
		fileState: mode.FileState<'transcription'>;
	} = $props();

	used(computedData);

	let scrollElement: HTMLElement;
	let referenceElement: HTMLElement;
	let wavesurferContainer: HTMLElement;
	let wavesurfer: WaveSurfer;
	let timeline: TimelinePlugin;
	let hover: HoverPlugin;
	let regions: RegionsPlugin;

	let width: number = $state(100);
	let minZoom: number;
	let duration: number | null = $state(null);
	let current: number = $state(0);
	let playing: boolean = $state(false);

	let previousSelection: number[] | null = null;

	let transcriptionType: { label?: string; value: string } = $state({ value: 'no model' });
	const models: string[] = ['whisper', 'deepgram', 'allosaurus'];
	const trackNameSpace = 150;

	$effect(() => {
		if (duration === null) return;

		minZoom = (width - trackNameSpace) / duration;
		wavesurfer?.setOptions({
			width: minZoom * duration
		});
	});

	onMount(() => {
		wavesurfer = WaveSurfer.create({
			container: wavesurferContainer,
			url: `/db/file/${fileState.id}`,
			height: 300,
			backend: 'WebAudio'
		});

		timeline = wavesurfer.registerPlugin(
			TimelinePlugin.create({
				timeInterval: 0.1,
				primaryLabelInterval: 1,
				secondaryLabelInterval: 0.5
			})
		);

		regions = wavesurfer.registerPlugin(RegionsPlugin.create());

		hover = wavesurfer.registerPlugin(
			HoverPlugin.create({
				formatTimeCallback: () => ''
			})
		);
		hover.on('hover', (event) => {
			const shadowRoot = wavesurferContainer.children[0].shadowRoot;
			if (shadowRoot) {
				const hoverLabel = shadowRoot.querySelector('span[part="hover-label"]');
				if (hoverLabel) {
					hoverLabel.innerHTML =
						numberToTime(wavesurfer.getDuration() * event) +
						'<br>' +
						getHoverString(wavesurfer.getDuration() * event);
				}
			}
		});

		let wrapper = wavesurfer.getWrapper().parentElement!;

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
			if (duration === null) return;

			wavesurfer.setOptions({
				width: duration * px
			});
		});

		wavesurfer.on('timeupdate', () => {
			if (wavesurfer.getCurrentTime() > wavesurfer.getDuration())
				wavesurfer.setTime(wavesurfer.getDuration());
			if (regions.getRegions().length == 1) {
				if (wavesurfer.getCurrentTime() > regions.getRegions()[0].end) {
					wavesurfer.pause();
					wavesurfer.setTime(regions.getRegions()[0].end);
				}
			}
			current = wavesurfer.getCurrentTime();
		});
		wavesurfer.on('play', () => {
			if (regions.getRegions().length == 1) {
				wavesurfer.setTime(regions.getRegions()[0].start);
			}
			playing = true;
		});
		wavesurfer.on('pause', () => (playing = false));

		// regions.enableDragSelection(
		// 	{
		// 		color: 'rgba(255, 0, 0, 0.1)'
		// 	},
		// 	10
		// );

		regions.on('region-created', (region: Region) => {
			regions.getRegions().forEach((r) => {
				if (r.id === region.id) return;
				r.remove();
			});

			let frame: Frame = {
				startIndex: Math.floor(region.start * wavesurfer.options.sampleRate),
				endIndex: Math.ceil(region.end * wavesurfer.options.sampleRate)
			};

			fileState.frame = frame;
		});

		window.addEventListener('keydown', (e: KeyboardEvent) => {
			switch (e.key) {
				case 'Escape':
					regions.clearRegions();
					previousSelection = null;
					break;
			}
		});
	});

	onDestroy(() => {
		timeline.destroy();

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
		a.download = `${fileState.name}.TextGrid`;

		document.body.appendChild(a);
		a.click();

		window.URL.revokeObjectURL(url);
		document.body.removeChild(a);
	}

	function getHoverString(time: number) {
		let result = '';
		for (let transcription of fileState.transcriptions) {
			if (!transcription.selected) continue;
			result += transcription.name + ': ';
			for (let caption of transcription.captions) {
				if (time >= caption.start && time <= caption.end) {
					result += caption.value + '<br>';
					break;
				}
			}
		}
		return result;
	}

	async function addTrack() {
		if (duration === null) return;

		if (transcriptionType.value === 'no model') {
			fileState.transcriptions = [
				...fileState.transcriptions,
				{
					id: generateIdFromEntropySize(10),
					name: 'track name',
					selected: true,
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
			const model = transcriptionType.value;
			let response = await (
				await fetch(`/api/transcription/${transcriptionType.value}/${fileState.id}`)
			).json();
			logger.trace(response);
			fileState.transcriptions = [
				...fileState.transcriptions,
				{
					id: generateIdFromEntropySize(10),
					name: model + (response.language ? '-' + response.language : ''),
					selected: true,
					captions: response.transcription
				},
				{
					id: generateIdFromEntropySize(10),
					name: model + '-sentence' + (response.language ? '-' + response.language : ''),
					selected: true,
					captions: sentenceCaption(response.transcription)
				}
			];
		} else {
			logger.error('no match for: ' + transcriptionType.value);
		}
	}

	function sentenceCaption(captions: { start: number; end: number; value: string }[]) {
		let sentence = '';
		for (const caption of captions) {
			if (caption.value === '') continue;
			sentence += caption.value + ' ';
		}
		if (sentence.charAt(sentence.length - 1) === ' ') {
			sentence = sentence.substring(0, sentence.length - 1);
		}
		return [{ start: captions[0].start, end: captions[captions.length - 1].end, value: sentence }];
	}

	const nonPassiveWheel: Action<HTMLElement, (event: WheelEvent) => void> = (node, callback) => {
		node.addEventListener('wheel', callback, { passive: false });

		return {
			destroy() {
				node.removeEventListener('wheel', callback);
			}
		};
	};

	function createRegion(start: number, end: number, currentTime: number[] | null) {
		if (currentTime != null && previousSelection != null) {
			if (Math.abs(previousSelection[0] - currentTime[1]) < 0.00001) {
				start = end;
				end = previousSelection[1];
			}
			if (start > end) {
				start = end;
			}
		}
		previousSelection = [start, end];
		regions.addRegion({ start, end, drag: false, resize: false, color: 'rgba(255, 0, 0, 0.1)' });
	}

	function resetRegion() {
		regions.clearRegions();
		previousSelection = null;
	}
</script>

<section bind:this={referenceElement} bind:clientWidth={width} class="w-full bg-accent/50">
	<!-- This is the bar -->
	<div class="flex w-full flex-row items-center bg-secondary/75">
		<Button
			class="h-fit w-fit rounded-none"
			variant="ghost"
			on:click={() => wavesurfer?.playPause()}
		>
			{#if playing}
				<PauseIcon size="16" fill="currentColor" />
			{:else}
				<PlayIcon size="16" fill="currentColor" />
			{/if}
		</Button>
		<div class="font-mono">
			{numberToTime(current)}/{numberToTime(duration ?? 0)}
		</div>
		<Separator orientation="vertical" class="mx-2" />
		<span>{fileState.name}</span>
	</div>

	<div
		bind:this={scrollElement}
		class="grid w-full overflow-x-scroll transition"
		style:grid-template-columns="{trackNameSpace}px 1fr"
		use:nonPassiveWheel={(event: WheelEvent) => {
			if (duration === null) return;
			if (!event.ctrlKey) return;

			event.preventDefault();
			event.stopImmediatePropagation();

			let oldPx = wavesurfer.options.minPxPerSec;
			let px = wavesurfer.options.minPxPerSec - event.deltaY;
			if (px < minZoom) px = minZoom - 1;

			const x = event.clientX - referenceElement.getBoundingClientRect().left;
			const scrollX = scrollElement.scrollLeft;
			const pointerTime = (scrollX + x) / oldPx;
			const newLeftSec = x / px;

			if (px * duration < width) {
				wavesurfer.zoom(width / duration);
				scrollElement.scrollLeft = 0;
			} else {
				wavesurfer.zoom(px);
				scrollElement.scrollLeft = (pointerTime - newLeftSec) * px;
			}

			wavesurfer.zoom(px);
		}}
	>
		<div></div>
		<div bind:this={wavesurferContainer} class="bg-accent"></div>

		{#each fileState.transcriptions as transcription, i (transcription.id)}
			<div class="flex w-full items-center gap-1 border-y">
				<Tooltip.Root>
					<Tooltip.Trigger>
						<Checkbox class="flex h-4 w-4 p-1" bind:checked={transcription.selected} />
					</Tooltip.Trigger>
					<Tooltip.Content>
						<p>Show caption on hover</p>
					</Tooltip.Content>
				</Tooltip.Root>
				<Tooltip.Root>
					<Tooltip.Trigger>
						<Button
							class="flex h-6 p-1"
							variant="destructive"
							on:click={() => {
								fileState.transcriptions = [
									...fileState.transcriptions.slice(0, i),
									...fileState.transcriptions.slice(i + 1)
								];
							}}><TrashIcon class="w-4" /></Button
						>
					</Tooltip.Trigger>
					<Tooltip.Content>
						<p>Delete track</p>
					</Tooltip.Content>
				</Tooltip.Root>
				<Tooltip.Root>
					<Tooltip.Trigger class="h-full w-full">
						<span
							role="button"
							tabindex="0"
							class="flex h-full w-full items-center justify-center overflow-clip text-secondary-foreground opacity-80"
							ondblclick={doubleClick}
							onfocusout={(event: FocusEvent) => focusOut(event, transcription)}
							onkeydown={(event: KeyboardEvent) => keyDown(event, transcription)}
							>{transcription.name}</span
						>
					</Tooltip.Trigger>
					<Tooltip.Content>
						<p>Name of the track</p>
					</Tooltip.Content>
				</Tooltip.Root>
			</div>
			<Track
				bind:captions={transcription.captions}
				{duration}
				{createRegion}
				{resetRegion}
				isLast={i === fileState.transcriptions.length - 1}
			/>
		{/each}
	</div>
	<!-- Inserting/Exporting track stuff down here -->
	<div class="flex w-full justify-center gap-5 pt-2">
		<div class="flex items-center">
			<span class="mr-2 flex"> Select transcription model: </span>
			<Select.Root bind:selected={transcriptionType}>
				<Select.Trigger class="m-0 w-32">
					{transcriptionType.value}
				</Select.Trigger>
				<Select.Content>
					<Select.Item value="no model">no model</Select.Item>
					{#each models as model}
						<Select.Item value={model}>{model}</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
		</div>

		<Button class="w-fit" variant="secondary" on:click={addTrack}>Create New Track</Button>

		<Tooltip.Root>
			<Tooltip.Trigger>
				<Button class="m-0 w-fit" on:click={exportTextGrid} variant="outline"><Download /></Button>
			</Tooltip.Trigger>
			<Tooltip.Content>
				<p>Export the transcriptions to TextGrid</p>
			</Tooltip.Content>
		</Tooltip.Root>
	</div>
</section>
